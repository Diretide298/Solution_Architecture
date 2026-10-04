# WS161 — Resource Management Configuration board 7

**10 screens · 16 operations · 25 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `AI_USE, APPROVAL_REQUEST, EVENT_CONFIGURE, RESOURCE_BOOK, RESOURCE_CONFIGURE, RESOURCE_VIEW, WORKFORCE_MANAGE`. A control nobody can use must say so,
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

### Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue)

Venue operations is everything that happens after a sale and inside the gates. A guest's ticket is one virtual ticket with interchangeable media (QR, dynamic QR, RFID wristband, NFC, Face Pass or Face Tag); at an access point a scanner (P07, or the scan function inside the Staff App P06) validates the media against the admission profile and the guest admission policy, offline if it must, and every deny carries a reason and a next action. The back office (Venue Management P08) configures that estate: the venue topology (venue, park, zone, attraction, access point, gate and lane, device placement), admission profiles and rules (entry, exit, re-entry, anti-passback, validity, crossover, companions), credential security (dynamic QR, device binding, beacons), biometrics, gate modes, and the live operations, fraud and monitoring views. Accreditation (P08 setup and review, P11 web portal for applicants, web first) takes an applicant from a configurable form through document checks, OCR, duplicate blocking and multi-level approval to a credential with zone rights. Resources and capacity manage bookable resources (rooms, vehicles, equipment, cabanas, instructors) that are booked as a consequence of selling a product, never sold directly. Workforce covers shift templates, rosters, attendance, swaps and breaks, mirrored on the Staff App. Maintenance and safety cover the asset register, preventive calendars, work orders with scored priority, inspections and incidents, with technicians working from the Staff App. Games and rides configure readers, credit types and consumption priority, play entitlements, game pricing, retry pricing, redemption and the card lifecycle. The virtual queue (Q1) gives a guest a live wait time and a return window for a ride; it is not the on-sale waiting room (Q2). Every calendar has day, week and month views. Configuration resolves tenant, region, venue (outlet only for F&B and retail), and a user's permissions, never the device, decide what they may do. The guest apps (P01, P02) show the guest's side of this: My Tickets, the scan code, Face Pass, wait times, the virtual queue, map booking of cabanas and the visit planner.
*(source: F06 step 1 / F112 step 1 / F111 step 1 / ADR-0002 / ADR-0012 / ADR-0018 / ADR-0041 / ADR-0066 / ADR-0067 / ADR-0068 / DI-652 / DI-627 / DI-640 / DI-654 / DI-666 / DI-482 / DI-483 / DI-907 / DI-919 / DI-923 / DI-865 / DI-678 / TRACKER Actions row 160 / MoM 2026-09-02 AccessControl / MoM 2026-09-07 …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Ticket | The one virtual record a guest owns (ticket number, product, validity, entries). Its number never changes, whatever media carries it or whoever it is transferred or resold to. | Pass (unless the product is a pass), Booking, Order line | DI-652 / DI-620 / contracts/spine/access.yaml#/components/schemas/TicketStatus |
| Media | What the ticket is presented by at a gate (QR code, dynamic QR, wristband/RFID card, NFC, Face Pass, Face Tag). One ticket can carry several media as fallbacks; a media code can also cover several tickets scanned as one group. Show one … | Credential (for guest media; keep Credential for accreditation badges and staff), Ticket code | DI-180 / DI-608 / DI-652 |
| Access point | A place where a scan is judged, with a fixed direction (entry, exit, re-entry, crossover). Hierarchy shown to users is Venue > Park > Zone > Attraction > Access point > Gate/lane > Device. | Scanner (that is the device), Door | screens/P08-venue-back-office.yaml#BO-144 / … |
| Admission profile | The named set of rules an access point enforces (opening window, entries, exit scan, re-entry, validity, crossover). Products point at a profile; tiers such as Bronze/Silver/Gold are profiles with gate allow and deny lists. | Admission rules (as a screen title), Access rule set | DI-185 / contracts/spine/access.yaml#/components/schemas/AdmissionRules |
| Admitted / Denied / Overridden | The three scan outcomes. A denial is always shown with its reason in plain words and a next action; an override is a supervisor admitting despite a denial, and is always attributed and reasoned. | Valid/Invalid, Success/Fail, Error | contracts/spine/access.yaml#/components/schemas/ScanOutcome / … |
| Used | A ticket entry is used the moment a scan succeeds, whether or not the guest physically passed. Mistakes are resolved from the scan history, not by un-scanning. | Redeemed (for admission), Checked in (that is group check-in, a different step) | DI-627 / TRACKER Actions row 221 / TRACKER Actions row 189 |
| Gate mode | What a lane is doing now, set live by the podium or supervisor - Normal, Free flow (counts, does not validate), Drop arm (everybody through, evacuation), Closed (nobody through), Podium (staff validating by eye), Maintenance. Direction is … | Turnstile mode (as a label for direction), Open/Locked | contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / R221 |
| Offline package | What a scanner holds to validate with no network - entitlements, blacklist, admission profiles and the active guest admission policy version - with its age always visible. | Cache, Local DB | F06 step 3 / ADR-0068 |
| Sync and reconciliation | Sending the offline scan journal to the server, and the duty manager's review of scans the server rejected after the device had already admitted the guest. | Upload, Retry | F06 step 6 / DI-065 |
| Face Pass / Face Tag | Face Pass is the long-lived face credential for members and season-pass holders (renewable); Face Tag is short-lived, for one day or event. Retention is set per tier by the venue. | Face ID, Biometric login | DI-640 / ADR-0063 |
| Accreditation / Credential (accreditation) | Accreditation is the application and approval of a person (media, contractor, corporate, staff of a partner) for an event or season; the credential is what is issued after approval (photo badge, QR or RFID) with zone access rights. | Registration (for the whole process), Ticket | DI-654 / DI-662 |
| Resource | A bookable thing or person a product needs (room, vehicle, cabana, equipment set, instructor). Guests buy products; resources are assigned to the booking, pre-assigned or dynamically. | Asset (that is maintenance), Inventory (that is stock) | DI-475 / DI-482 / TRACKER Actions row 160 |
| Asset | A physical item maintained by the venue (ride, turnstile, printer, pump) with a register record, documents, warranty and maintenance history. | Resource, Device (unless it is an IT device in the device register) | DI-910 / ADR-0067 |
| Work order | A unit of maintenance work, lifecycle Created > Assigned > In progress > Review > Closed, with a resolution timer. | Ticket (reserved for guest tickets), Job card | DI-231 |
| Game / attraction (games module) | In the games and rides module an attraction is an individual game or ride (roller coaster, racing game, bumper cars), not a venue. | Venue, Park | DI-863 |
| Virtual queue / Return window | A guest's place in a ride's queue held without standing in line, with a return window (for example 4:50 to 5:00 PM) that recalculates live. Distinct from the walk-in line and the VIP/express lane, and from the on-sale waiting room. | Waiting room, Fast pass (that is the express product), Booking | DI-675 / DI-678 / DI-679 / ADR-0066 |
| Wait time source | Where a ride's wait time comes from - Sensor, Throughput, Manual, or Unavailable - always shown beside the number. | Live (when the source is manual) | contracts/satellite/queue.yaml#/components/schemas/WaitTimeSource / DI-315 |

### AI & Intelligence

AI in TICVAI is one governed engine behind many screens. The guest meets it as Sahli, the concierge (WEB-044, GST-031, GST-033), as the planner agent that refines a rules-built day plan by chat (GST-054), and as upsell and cross-sell offers on a separate Extras step (WEB-008, GST-048). Staff meet it as the Staff App's AI tab (EMP-019/020, knowledge EMP-040/041), the kiosk assistant (KSK-015) and the support copilot (SUP-006, SUP-018). Venue managers meet it in Venue Management (BO-091 policy and spend, BO-919/BO-925..932 resource and staffing forecasts, BO-597/598 configuration drafts, BO-772/782 marketing optimisation, BO-793 translations, BO-970/975 seat-map generation, BO-1048 seat upsell, BO-1160 fraud cases) and in Analytics (ANL-010 suggestions, ANL-019 management insights, ANL-055 anomalies, ANL-057 forecasting studio, ANL-059 insight history, ANL-060 governance, ANL-071 AI maturity). The governance, configuration-assistant, forecasting, oversight, audit and monitoring boards sit on the TICVAI Console (P09: ADM-037 providers, ADM-469..498 configuration assistant, ADM-499..518 forecasting, ADM-519..558 governance, ADM-633/637 fraud, ADM-680..697 recommendation governance). Five rules hold on every one of these screens. (1) Baseline first, then it learns per tenant: every data-driven answer (forecast, suggestion, risk score, recommendation) exists from day one, from the venue AI profile, a starting pattern for the venue type, the UAE calendar and the weather, and shifts to the venue's own data as it trades; nothing says "comes later" or refuses for lack of history - a refusal only names a missing setting. (2) Every answer shows its basis and maturity: a "Based on" line, a stage badge (Starting, Learning, Established, Trained on your data), "Limited historical data" while the starting pattern carries more than half the weight, ranges or bands rather than a bare percentage, a confidence only where the producer really has one, a plain-words explanation always. (3) A trained model replaces the baseline only when it beats it in a shadow run of at least six weeks and an admin promotes it; the platform raises "Ready to promote" and never switches by itself. (4) The LLM never reads raw data: numbers come only from query results the platform runs (the answer shows the query), only the masked prompt and retrieved context leave the platform, and AI only drafts - the owning screen applies. (5) One autonomy scale, L0 Disabled to L4 Controlled auto, with first-release ceilings, separate from user permission and from the approval tier; impactful actions route to a person, who sees current against proposed, impact, risk and what is affected, and can approve within a limit, challenge, override or roll back; every decision is traceable (data, model, approver, time) and searchable by customer, venue and capability. In Block A (5 October to 20 November 2026) the guest concierge with retrieval, Help me choose, translations, the planner agent, the gateway and …
*(source: ADR-0051; ADR-0050; ADR-0020; ADR-0052; ADR-0053; ADR-0054; ADR-0059; ADR-0051 (AI-D01..AI-D20); ADR-0051 (AI functions review 30 Sep §2 §4 §9); MoM 18 Sep 4.1-4.10; MoM 21 Sep 4.1-4.14; MoM 30 Sep 4.1 4.7; ADR-0059 (Block A slice: tasks.csv))*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sahli | The guest concierge's name; the entry reads "Ask Sahli" and shows as mascot art when the venue's Concierge mascot setting is on (default), otherwise a plain button. | Chatbot, Bot, AI Concierge (as a visible label), Virtual agent | DI-1069 / screens/P01-guest-web-storefront.yaml#WEB-044 |
| Based on | The line on every AI answer that says what it was computed from, e.g. "Based on: your venue profile, UAE calendar, weather, 23 days of your sales". Always present. | Data sources, Model inputs, Powered by AI | ADR-0051 Maturity / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Starting / Learning / Established / Trained on your data | The four maturity stages (enum starting, learning, established, learned), shown as one badge. Moves by itself from Starting to Established as own data arrives; Trained on your data only after an admin promotion. | Beta, Experimental, Low confidence, Cold start (in UI), Not enough data | ADR-0051 / ADR-0051 (AI functions review 30 Sep §2) |
| Limited historical data | Shown while own data carries less than half the weight (AiMaturity.limitedHistory, ownDataShare < 0.5). An honest qualifier, never a refusal. | Insufficient data, Not available until, Comes later | ADR-0051 / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Range | The 10th-90th percentile band a forecast or estimate is shown with (e.g. "1,850-3,400 guests, most likely 2,600"). Never a bare accuracy percentage on an answer; measured accuracy (WAPE, bias, coverage) appears only on accuracy screens … | Accuracy 92%, Confidence 0.87 (on a heuristic), Exact | ADR-0051 / contracts/satellite/ai.yaml#getForecast / … |
| Running in the background | A trained model in shadow next to the live answer (AiRelease.stage shadow); it changes nothing a person sees. | Live, Active model, Testing in production | ADR-0051 Promotion / ADR-0051 (AI functions review 30 Sep §2) |
| Ready to promote / Promote | A shadow model passed its gate (governance alert promotionReady); an admin promotes it one stage at a time (canary, then production). The only way a model replaces the baseline. | Deploy, Go live, Auto-switch, Activate model, Upgrade AI | ADR-0051 (AI-D16) / contracts/satellite/ai.yaml#promoteAiRelease |
| L0 Disabled / L1 Advisory / L2 Prepare / L3 Execute with … | The one autonomy scale for every AI capability, shown as "L2 Prepare" etc. with the capability's ceiling beside it. Lower scopes tighten, never raise. | Autopilot, Copilot mode, Level 0-3 (CFG book), Approval level (for autonomy), Manual/Semi/Auto | ADR-0050 / ADR-0050 (AI-D04) / … |
| Approval tier | How many people must approve a proposed action (ProposedAction.approvalLevel, 1 or 2). Not an autonomy level. | Autonomy level, Approval level (ambiguous) | ADR-0050 |
| Suggestion / Draft | What AI produces. A suggestion advises; a draft is a ready-to-review change that a person applies in the owning screen. Copy says "Nothing is applied until you approve it." | AI changed, Auto-applied, AI updated your prices | ADR-0020 / ADR-0051 (AI functions review 30 Sep §4 Configuration assistant) / … |
| Why this? | The link or expander that opens an answer's explanation (Suggestion.explanation, recommendation template reason, decision trace). Plain words; for guests a template reason. | Explainability, SHAP, Feature importance (in operator copy) | ADR-0052 (AI-D09) / contracts/satellite/ai.yaml#/components/schemas/Suggestion |
| No thanks | The explicit decline on an offer. Only this counts as a decline and it is remembered across channels; scrolling past or closing the step is not a decline. | Dismiss (as a decline), Skip (as a decline), X (as a decline) | ADR-0052 (AI-D07) / DI-962 / … |
| Hold for review | What a high fraud or risk score does to a payment or order. The transaction goes through; it is held for a person. | Decline, Block, Reject (for a risk score), Fraud detected | ADR-0053 / ADR-0053 (AI-D06) |
| Hand over to a person | The concierge passes the whole conversation and its own summary to a live agent; the guest does not repeat themselves. | Escalate, Transfer, Contact bot | contracts/satellite/marketing-crm.yaml#handoverToAgent |
| Not available yet | The analytics assistant's answer to a question outside the semantic model; it records a knowledge gap and never improvises a number. | I cannot answer, Error, Unknown | ADR-0054 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-913` | Event Resource Planning Command Center | B | 2 | 24 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-914` | Event Resource Requirement Builder | B | 0 | 40 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-915` | Venue & Space Allocation | B | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-916` | Equipment & Asset Allocation | D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-917` | Event Staff & Personnel Allocation | D | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-918` | Event Resource Template Library | D | 37 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-919` | AI Event Resource Forecasting | A | 10 | 19 | 6 | 49 | 0 | 0 | — | notStarted (—) |
| `BO-920` | Event Resource Cost Estimator | B | 2 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-921` | Multi-Event Allocation & Conflict Optimizer | D | 4 | 15 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-922` | Event Resource Approval & Readiness Gate | B | 0 | 0 | 6 | 5 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-914, BO-915, BO-916, BO-922 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-913` Event Resource Planning Command Center

**Provide event and operations managers with a single workspace for understanding the resource readiness of upcoming events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-913 |
| Who uses it | venue staff holding `EVENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/rentals/event-resource-planning-command-center-bo-913` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Resource readiness of upcoming events in one workspace for event and operations managers.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search event resource planning | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by event, date, venue, event type, resource status, readiness and 4 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every event resource planning** (data table)

| Shows | Format | Notes |
|---|---|---|
| Upcoming events | text | not in the schema: `Upcoming events` |
| Events fully resourced | text | not in the schema: `Events fully resourced` |
| Events partially resourced | text | not in the schema: `Events partially resourced` |
| Events with critical gaps | text | not in the schema: `Events with critical gaps` |
| Pending resource requests | text | not in the schema: `Pending resource requests` |
| Pending approvals | text | not in the schema: `Pending approvals` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Staff shortages | text | not in the schema: `Staff shortages` |
| Equipment shortages | text | not in the schema: `Equipment shortages` |
| Venue/space conflicts | text | not in the schema: `Venue/space conflicts` |
| Forecast resource cost | text | not in the schema: `Forecast resource cost` |
| Event readiness | text | not in the schema: `Event Readiness` |

**The selected event resource planning** (detail panel): The pack groups this record's detail under its own headings: “Corporate Gala”, “Concert A”.

| Shows | Format | Notes |
|---|---|---|
| Upcoming events | text | not in the schema: `Upcoming events` |
| Events fully resourced | text | not in the schema: `Events fully resourced` |
| Events partially resourced | text | not in the schema: `Events partially resourced` |
| Events with critical gaps | text | not in the schema: `Events with critical gaps` |
| Pending resource requests | text | not in the schema: `Pending resource requests` |
| Pending approvals | text | not in the schema: `Pending approvals` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Staff shortages | text | not in the schema: `Staff shortages` |
| Equipment shortages | text | not in the schema: `Equipment shortages` |
| Venue/space conflicts | text | not in the schema: `Venue/space conflicts` |
| Forecast resource cost | text | not in the schema: `Forecast resource cost` |
| Event readiness | text | not in the schema: `Event Readiness` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **readiness**: Same readiness badge and unsecured count as BO-710. *(source: contracts/spine/catalogue.yaml#getEventResourcePlan)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-914` Event Resource Requirement Builder: *Event Resource Requirement Builder*; carries `eventId`
- → `BO-915` Venue & Space Allocation: *Venue & Space Allocation*
- → `BO-916` Equipment & Asset Allocation: *Equipment & Asset Allocation*
- → `BO-917` Event Staff & Personnel Allocation: *Event Staff & Personnel Allocation*
- → `BO-918` Event Resource Template Library: *Event Resource Template Library*
- → `BO-919` AI Event Resource Forecasting: *AI Event Resource Forecasting*
- → `BO-920` Event Resource Cost Estimator: *Event Resource Cost Estimator*; carries `eventId`
- → `BO-921` Multi-Event Allocation & Conflict Optimizer: *Multi-Event Allocation & Conflict Optimizer*
- → `BO-922` Event Resource Approval & Readiness Gate: *Event Resource Approval & Readiness Gate*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource planning list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource planning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event resource planning yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event resource planning are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-710`: The same view on two boards; draw one component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
events:
- event: Desert Symphony
  readiness: ready
```

#### Permissions

- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-913` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-913`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 1: Opens Event Resource Planning Command Center → Provide event and operations managers with a single workspace for understanding the resource readiness of upcoming events.
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F270 branch at step 1 (expected): when Nothing has been set up on Event Resource Planning Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F270 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-913?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-914`, `BO-915`, `BO-916`, `BO-917`, `BO-918`, `BO-919`, `BO-920`, `BO-921`, `BO-922`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-914` Event Resource Requirement Builder

**Define every resource required to deliver a specific event.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-914 |
| Who uses it | venue staff holding `EVENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/rentals/event-resource-requirement-builder-bo-914` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Event Resource Requirement Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Define every resource a specific event needs, by kind and quantity, as BO-711.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setEventResourcePlan and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every event resource requirement** (data table)

| Shows | Format | Notes |
|---|---|---|
| Event | text | not in the schema: `Event` |
| Event type | text | not in the schema: `Event type` |
| Venue | text | not in the schema: `Venue` |
| Event date | text | not in the schema: `Event date` |
| Start/end | text | not in the schema: `Start/end` |
| Expected attendance | text | not in the schema: `Expected attendance` |
| Capacity | text | not in the schema: `Capacity` |
| Event manager | text | not in the schema: `Event manager` |
| Resource requirement sections | text | not in the schema: `Resource Requirement Sections` |
| Spaces | text | not in the schema: `Spaces` |

**Everything an event needs, and whether it has been secured** (detail panel, from `getEventResourcePlan`)

| Shows | Format | Notes |
|---|---|---|
| Event | the name it points at, never the id | — |
| Requirements | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Kind | chip: Space, Equipment, Staff, Contractor, Vehicle, Service | — |
| Resource type | the name it points at, never the id | — |
| Role code | text | — |
| Quantity | 1,234 | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Location scope path | text | — |
| Secured count | 1,234 | — |
| Status | chip: Required, Partially secured, Secured, At risk | — |
| Bookings | list or chips (count when long) | — |
| Contractors | list or chips (count when long) | — |
| Organisation | the name it points at, never the id | — |
| Role | text | — |
| Headcount | 1,234 | — |
| Accreditation programme | the name it points at, never the id | — |
| Insurance verified | yes / no (icon or chip) | — |
| Readiness | chip: Not planned, Planning, At risk, Ready | — |

**The selected event resource requirement** (detail panel): The pack groups this record's detail under its own headings: “Event Selection”, “For each requirement”, “Requirements may change according to”.

| Shows | Format | Notes |
|---|---|---|
| Event | text | not in the schema: `Event` |
| Event type | text | not in the schema: `Event type` |
| Venue | text | not in the schema: `Venue` |
| Event date | text | not in the schema: `Event date` |
| Start/end | text | not in the schema: `Start/end` |
| Expected attendance | text | not in the schema: `Expected attendance` |
| Capacity | text | not in the schema: `Capacity` |
| Event manager | text | not in the schema: `Event manager` |
| Resource requirement sections | text | not in the schema: `Resource Requirement Sections` |
| Spaces | text | not in the schema: `Spaces` |

**Data it reads**: `getEventResourcePlan` (onLoad, Everything an event needs, and whether it has been secured)

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource requirement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource requirement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event resource requirement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event resource requirement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-711`: Same editor and record (setEventResourcePlan); keep one design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
requirements:
- kind: equipment
  item: LED wall 6x3 m
  quantity: 1
```

#### Permissions

- `setEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-914` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-914`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 2: Works in Event Resource Requirement Builder → Define every resource required to deliver a specific event.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-914?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-915` Venue & Space Allocation

**Assign suitable physical spaces to an event and its operational components.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-915 |
| Who uses it | venue staff holding `EVENT_CONFIGURE`, `RESOURCE_BOOK` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/venue-space-allocation-bo-915` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Assign spaces to an event and its parts, and book them so the space's calendar shows the event including set-up and tear-down.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listSpaces return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every venue space allocation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Capacity | text | not in the schema: `Capacity` |
| Layout | text | not in the schema: `Layout` |
| Location | text | not in the schema: `Location` |
| Availability | text | not in the schema: `Availability` |
| Existing bookings | text | not in the schema: `Existing bookings` |
| Setup time | text | not in the schema: `Setup time` |
| Teardown time | text | not in the schema: `Teardown time` |
| Accessibility | text | not in the schema: `Accessibility` |
| Associated resources | text | not in the schema: `Associated resources` |
| Operational restrictions | text | not in the schema: `Operational restrictions` |

**The selected venue space allocation** (detail panel): The pack groups this record's detail under its own headings: “The interface shall display available”, “Users shall see”, “Event”, “Teardown”, “Conflict Detection”.

| Shows | Format | Notes |
|---|---|---|
| Capacity | text | not in the schema: `Capacity` |
| Layout | text | not in the schema: `Layout` |
| Location | text | not in the schema: `Location` |
| Availability | text | not in the schema: `Availability` |
| Existing bookings | text | not in the schema: `Existing bookings` |
| Setup time | text | not in the schema: `Setup time` |
| Teardown time | text | not in the schema: `Teardown time` |
| Accessibility | text | not in the schema: `Accessibility` |
| Associated resources | text | not in the schema: `Associated resources` |
| Operational restrictions | text | not in the schema: `Operational restrictions` |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Book space**: Refused on conflict including set-up and tear-down, naming the clashing booking. *(source: contracts/satellite/resources.yaml#bookResource)*

**Data it reads**: `listSpaces` (onLoad, Venue and space allocation)

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue space allocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue space allocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue space allocation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue space allocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Conflicts, and the response names them with times. *"Not available"* on a resource a guest can see in front of them is not an answer. (ResourceConflictProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
allocation:
  event: Gulf Attractions Summit
  space: Hall B
  from: 13 Nov 08:00
  to: 15 Nov 20:00
```

#### Permissions

- `listSpaces` → `EVENT_CONFIGURE` (configure) · staff
- `bookResource` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-915` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-915`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 4: Works in Venue & Space Allocation → Assign suitable physical spaces to an event and its operational components.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-915?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`, `RESOURCE_BOOK`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-916` Equipment & Asset Allocation

**Allocate physical equipment and operational assets required for events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-916 |
| Who uses it | venue staff holding `RESOURCE_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/equipment-asset-allocation-bo-916` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Turns an event's equipment needs into real allocated items: per line (projectors, wireless microphones, LED screens, lighting rigs, furniture, barriers) required, allocated, available and gap, with each item checked for availability, maintenance, inspection, location, existing reservations, setup and dependencies before it is allocated. The one thing to get right: the gap column and the reason an item was not allocated ("P-17 under maintenance") are visible per line.

**Known correction pending (do not draw the wrong version)**

- **The screen has an unlabelled primary button and Cancel, and the gap note says nothing is drawable** Why: The pack gives the Required / Allocated / Available / Gap table, validation checks and specific vs dynamic assignment. *(source: screens/P08-venue-back-office.yaml#BO-916; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read of the event's equipment requirements or its current allocations, and no event id on an allocation** Why: allocateResources takes requirements, a window, a subject and an order; it cannot say which event an item serves, so the table cannot be reloaded. *(source: contracts/satellite/resources.yaml#allocateResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Event**: The event opened from the event command centre (its id carried in), with its date, time and venue shown in the header. *(source: screens/P08-venue-back-office.yaml#BO-916)*
- **Requirement line**: Either a specific asset (Projector P-01) or a type and quantity (2 x 4K projector) - a radio per line; quantity whole number; category tabs All, Audio, Lighting, Video, Furniture, Other. *(source: screens/P08-venue-back-office.yaml#BO-916)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Allocation table**: Resource, Required, Allocated, Available, Gap, Status (tick, amber partial, red shortage); sorted by gap descending; allocated items listed under each line with their codes. *(source: screens/P08-venue-back-office.yaml#BO-916)*
- **Summary tiles**: Total required, Allocated (with %), Shortage - metric tiles above the table. *(source: screens/P08-venue-back-office.yaml#BO-916)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Allocate**: Fills each line from the pool (rotation by default) for the event's whole occupancy window including setup and teardown; a line that cannot be fully met is refused by name with the available count, not half-filled. *(source: contracts/satellite/resources.yaml#allocateResources / contracts/satellite/resources.yaml#/components/schemas/ResourceAllocationProblem)*
- **Swap item**: Replace an allocated item with another eligible one (keeps the event booking). *(source: contracts/satellite/resources.yaml#updateResourceBooking)*

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The equipment asset allocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the equipment asset allocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No equipment asset allocation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the equipment asset allocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Nothing available, or a dependency is missing. Both are named — "no instructor free" and "the stage has no sound system" need different actions from the person … (ResourceAllocationProblem) |

#### Edge cases to draw

- **An item fails inspection after allocation**: Line turns red "LED Screen S-04 failed inspection - replace"; recovery offered. *(source: screens/P08-venue-back-office.yaml#BO-916 / contracts/satellite/maintenance.yaml#submitInspection)*
- **Required dependency missing (stage without sound system)**: Allocation refused naming the missing dependency. *(source: contracts/satellite/resources.yaml#allocateResources)*

#### Consistency with other screens

- Match `BO-921`: Shortages here roll up into the multi-event optimiser.
- Match `BO-861`: A line may request a package (Event Stage Package).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event: Corporate Gala - Fri 16 Oct 2026 18:00-23:00 (setup from 14:00) - Summit Peaks Grand Hall
lines:
- resource: Projectors
  required: 4
  allocated: 4
  available: 6
  gap: 0
- resource: Wireless microphones
  required: 12
  allocated: 10
  available: 10
  gap: 2
- resource: LED screens
  required: 3
  allocated: 3
  available: 3
  gap: 0
- resource: Lighting rigs
  required: 4
  allocated: 3
  available: 3
  gap: 1
  reason: Rig 4 under maintenance until 18 Oct
```

#### Permissions

- `allocateResources` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.57 | AI shall optimize schedules automatically. | Ticketing Catalogue | CONTRACTED_PARTIAL | `allocateResources` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-916` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-916`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 6: Works in Equipment & Asset Allocation → Allocate physical equipment and operational assets required for events.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-916?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-917` Event Staff & Personnel Allocation

**Assign qualified staff resources to event roles.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-917 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each candidate may display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/event-staff-personnel-allocation-bo-917` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Event staff and personnel allocation: for an event, the roles it needs (event manager, supervisor, ushers, security, technical crew, AV operators, hosts, performers, mascots, registration, customer service, custom), how many of each with what skill, certification, shift and venue, and the qualified candidates to fill them. The one thing to get right: each role row shows required versus allocated and its gap, and candidates are ranked with explained, rule-based matches - nobody failing a mandatory requirement is offered.

**Known correction pending (do not draw the wrong version)**

- **"Event manager", "Supervisor", "Security", "Customer service" are drawn as action buttons** Why: They are event role values (rows of the role table). *(source: screens/P08-venue-back-office.yaml#BO-917; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only createRotaAssignment is bound and a rota assignment cannot record the event or role requirement it fills** Why: Write with no read (no role requirements, no candidates) and no event link on RotaAssignment. *(source: contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Candidate "AI match" percentages** Why: Staff matching was agreed as attribute matching; label it "Match" and show its reasons. *(source: contracts/satellite/resources.yaml#suggestResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where are event role requirements stored (quantity, skill, certification, shift per role)?** → Drawn default accepted: Draw the role table editable; mark storage as pending under the event resource plan. *(decided by Chinmay, 2026-10-02; DEC-514 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Role requirement**: Per role - required quantity, minimum skill level, certification, shift, start-end, break requirement, venue, priority (High, Medium, Low). *(source: screens/P08-venue-back-office.yaml#BO-917)*
- **Allocate**: Pick a candidate for a role slot; creates a rota assignment for the shift. Refusals (overlap, missing role) shown on the slot. *(source: contracts/satellite/workforce.yaml#createRotaAssignment)*

#### Outputs: what the screen shows and produces

**Shown**

**Every event staff personnel** (data table)

| Shows | Format | Notes |
|---|---|---|
| Name | text | not in the schema: `Name` |
| Role | text | not in the schema: `Role` |
| Skill | text | not in the schema: `Skill` |
| Certification | text | not in the schema: `Certification` |
| Availability | text | not in the schema: `Availability` |
| Existing workload | text | not in the schema: `Existing workload` |
| Venue | text | not in the schema: `Venue` |
| Overtime impact | text | not in the schema: `Overtime impact` |
| AI match | text | not in the schema: `AI match` |

**The selected event staff personnel** (detail panel): The pack groups this record's detail under its own headings: “For each role”, “AV Technician Required”.

| Shows | Format | Notes |
|---|---|---|
| Name | text | not in the schema: `Name` |
| Role | text | not in the schema: `Role` |
| Skill | text | not in the schema: `Skill` |
| Certification | text | not in the schema: `Certification` |
| Availability | text | not in the schema: `Availability` |
| Existing workload | text | not in the schema: `Existing workload` |
| Venue | text | not in the schema: `Venue` |
| Overtime impact | text | not in the schema: `Overtime impact` |
| AI match | text | not in the schema: `AI match` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event manager (primary button) | navigation or local | — | — | — | — |
| Supervisor (secondary button) | navigation or local | — | — | — | — |
| Security (secondary button) | navigation or local | — | — | — | — |
| Customer service (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Role table**: Role, required, allocated, gap, shift; roles as rows (the event roles are values, not buttons). *(source: screens/P08-venue-back-office.yaml#BO-917)*
- **Candidates**: Name, role, skill, certification, availability, existing workload ("3 assignments this week"), venue, overtime impact, match with reasons ("Sanjay Pillai - 97% - AV Level 3, available, same venue, no overtime"). *(source: screens/P08-venue-back-office.yaml#BO-917 / screens/P08-venue-back-office.yaml#BO-918 / contracts/satellite/resources.yaml#suggestResources)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Smart assign**: Proposes the best candidate per open slot with reasons; applied by the event manager. *(source: screens/P08-venue-back-office.yaml#BO-918)*

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event staff personnel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event staff personnel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event staff personnel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event staff personnel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlaps an existing assignment, or the person lacks the required role |

#### Edge cases to draw

- **Best candidate is at another venue**: Shown lower with "Different venue - 30-minute transfer"; never hidden. *(source: screens/P08-venue-back-office.yaml#BO-882)*
- **Role needs a certification nobody available holds**: Gap stays with "No qualified person available"; offer "Request external resource" where configured. *(source: screens/P08-venue-back-office.yaml#BO-887)*

#### Consistency with other screens

- Match `BO-714`: Event shifts and this allocation are one roster; draw this as the role and candidate panel of BO-714 (per VO-R14).
- Match `BO-884`: Same candidate card.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event: Corporate Gala - Summit Peaks Grand Hall - 1,200 guests - Fri 20 Nov 2026
roles:
- role: Security
  required: 18
  allocated: 12
  gap: 6
- role: Ushers
  required: 24
  allocated: 24
  gap: 0
- role: AV operators
  required: 4
  allocated: 3
  gap: 1
candidates:
- name: Sanjay Pillai
  match: 97%
  why: AV Level 3, available, same venue, no overtime
- name: Hessa Al Marzooqi
  match: 86%
  why: AV Level 3, available, different venue
```

#### Permissions

- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-917` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-917`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 8: Works in Event Staff & Personnel Allocation → Assign qualified staff resources to event roles.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-917?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event manager, Supervisor, Security, Customer service.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-918` Event Resource Template Library

**Allow frequently used event-resource configurations to be saved as reusable templates.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-918 |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `packageId` (navigation) |
| Route | `/rentals/event-resource-template-library-bo-918` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Reusable resource plans for common events (Corporate Conference 500 guests - main hall, 3 breakout rooms, stage, 2 LED screens, 8 wireless mics, sound, lighting, event manager, 8 ushers, 6 security, 4 technical crew), applied when a new event is created and then adjusted. The one thing to get right: templates are versioned - changing one never silently changes an event plan already approved.

**Known correction pending (do not draw the wrong version)**

- **Every template setting, and "Template Application", is a selectField** Why: Text, ranges, durations and a line table need their own controls; application is an action from an event. *(source: screens/P08-venue-back-office.yaml#BO-918; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Event type, attendance range, setup and teardown duration, versioning and an apply operation have no field or operation** Why: The library is bound to resource packages, which have none of these; nothing applies a template to an event. *(source: screens/P08-venue-back-office.yaml#BO-919 / contracts/satellite/resources.yaml#/components/schemas/ResourcePackage; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): No update operation bound (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Template code | select field | — | — | — | — | — | — |
| Template name | select field | — | — | — | — | — | — |
| Event type | select field | — | — | — | — | — | — |
| Attendance range | select field | — | — | — | — | — | — |
| Applicable venues | select field | — | — | — | — | — | — |
| Required resources | select field | — | — | — | — | — | — |
| Quantities | select field | — | — | — | — | — | — |
| Staff roles | select field | — | — | — | — | — | — |
| Setup duration | select field | — | — | — | — | — | — |
| Teardown duration | select field | — | — | — | — | — | — |
| Dependencies | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Template Application | select field | — | — | — | — | — | — |

**Form: Save template** (modal, opened by *Save template*; *Save template* calls `updateResourcePackage`, *Cancel* sends nothing)

**Collects what `updateResourcePackage` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Code `code` | text field | required | — | — | — | — | `updateResourcePackage` body |
| Name `name` | text field | required | — | — | — | — | `updateResourcePackage` body |
| Description `description` | text area | optional | — | — | — | — | `updateResourcePackage` body |
| Applicable venues `applicableVenueIds` | multi-picker: choose applicable venues | optional | — | — | — | — | `updateResourcePackage` body |
| Components `components` | repeatable rows | optional | — | — | — | — | `updateResourcePackage` body |
| ID `components[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Resource type `components[].resourceTypeId` | picker: choose a resource type | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Category `components[].categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateResourcePackage` body |
| Resource `components[].resourceId` | picker: choose a resource | optional | — | — | shows names, sends the id | A fixed component, and the exception rather than the rule. Meeting Room A really is Meeting Room A; the technician is not. | `updateResourcePackage` body |
| Quantity `components[].quantity` | number field | required | 1 | — | — | — | `updateResourcePackage` body |
| Mandatory `components[].mandatory` | toggle | optional | on | — | — | — | `updateResourcePackage` body |
| Required qualifications `components[].requiredQualifications` | list of values (chips) | optional | — | — | — | — | `updateResourcePackage` body |
| Required attributes `components[].requiredAttributes` | key and value settings | optional | — | — | — | — | `updateResourcePackage` body |
| Substitute resources `components[].substituteResourceIds` | multi-picker: choose substitute resources | optional | — | — | — | — | `updateResourcePackage` body |
| Scope path `components[].scopePath` | text field | optional | — | — | — | — | `updateResourcePackage` body |
| Allocation priority `allocationPriority` | number field | optional | 0 | — | — | — | `updateResourcePackage` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateResourcePackage` body |
| Effective to `effectiveTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateResourcePackage` body |
| Minimum minutes `minimumMinutes` | number field (minutes) | optional | — | — | — | — | `updateResourcePackage` body |
| Maximum minutes `maximumMinutes` | number field (minutes) | optional | — | — | — | — | `updateResourcePackage` body |
| Requires approval `requiresApproval` | toggle | optional | off | — | — | — | `updateResourcePackage` body |
| Internal cost `internalCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateResourcePackage` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `updateResourcePackage` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Template header**: Template code, name, event type (Conference, Concert, Gala, Wedding, Product launch, VIP dinner), attendance range (from-to guests), applicable venues, effective dates. *(source: screens/P08-venue-back-office.yaml#BO-919)*
- **Resource lines**: Grouped Spaces / Equipment / Staff - each line a resource, type or package with quantity; staff by role; setup and teardown durations for the template; dependencies picked from rules. *(source: screens/P08-venue-back-office.yaml#BO-918 / screens/P08-venue-back-office.yaml#BO-919)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save template (secondary button) | `updateResourcePackage` PUT `/resource-packages/{packageId}` | ResourcePackage | ResourcePackage | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Template cards**: Name, attendance range, counts (Spaces 5, Equipment 14, Staff 8), version and Active badge; filter by event type; search. *(source: screens/P08-venue-back-office.yaml#BO-918)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Create template / Save as new version**: Saves a new version; events planned from an earlier version keep theirs and show "Template v3 available". *(source: screens/P08-venue-back-office.yaml#BO-919 / contracts/satellite/resources.yaml#createResourcePackage)*
- **Apply to event**: From an event, populates its resource plan from the template; the user then edits the event's own plan. *(source: screens/P08-venue-back-office.yaml#BO-919)*

**Data it reads**: `listResourcePackages` (onLoad, Template library)

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource template configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event resource template configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Template applied to a venue it is not valid for**: Lines naming resources of another venue shown as "Not at this venue - choose a substitute". *(source: screens/P08-venue-back-office.yaml#BO-919)*

#### Consistency with other screens

- Match `BO-861`: Templates and packages are the same object family; draw this as the event view of the package library (VO-R14) with event-only fields.
- Match `BO-916`: Applying a template fills that screen's lines.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
templates:
- code: TPL-CONF-500
  name: Corporate Conference - 500
  type: Conference
  attendance: 300-600
  lines: 1 Main hall, 3 Breakout rooms, 1 Stage, 2 LED screens, 8 Wireless mics, 1 Sound system, 1 Lighting package,
    1 Event manager, 8 Ushers, 6 Security, 4 Technical crew
  setup: 4 h
  teardown: 2 h
  version: v2
- code: TPL-CONCERT-M
  name: Concert - Medium
  type: Concert
  lines: Main stage, Backstage, Lighting package, Sound package, 12 Security, 15 Ushers, 8 Technical crew
```

#### Permissions

- `listResourcePackages` → `RESOURCE_VIEW` (read) · staff
- `createResourcePackage` → `RESOURCE_CONFIGURE` (configure) · staff
- `updateResourcePackage` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-918` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-918`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 10: Works in Event Resource Template Library → Allow frequently used event-resource configurations to be saved as reusable templates.

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-918?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save template.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-919` AI Event Resource Forecasting

**Predict the resources required for an event before final allocation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 1 · needs the `resources` module |
| Block | Block A · task APP-SETUP-BO-919 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/ai-event-resource-forecasting-bo-919` |

**What the spec says about it.** **The forecast definition and the event's dates are picked on the screen 4 October 2026: getForecast reads definitionKey with from and to set to the event's days, and listOperationalRequirements the same window (Event carries no dates, so the window is the event's days as the planner enters them)** (CHG-FXS-004)

**From the AI & Intelligence process.** Event resource forecast: before resources are finally allocated for an event or a busy day, the manager sees, per resource type, what is configured against what the forecast says will be needed, with the busy-case figure, and can test a what-if (a bigger crowd, an extra show, rain). The forecast exists from day one on the venue's starting pattern and says so. The one thing to get right: "AI recommended" is a range from a published forecast version, shown next to the configured figure - never a silent overwrite of the allocation.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The dataTable and detail panel bind no operation (columns "Configured", "AI Recommended" with op None), and in Block A only createForecastScenario is in the slice. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): DI-280 (14 August) says data-dependent forecasting cannot be delivered in phase one for lack of history. (CHG-CLN-012).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which resource types does the event forecast cover in release 1 (staff, gates, F&B tills, rentable equipment)?** → The event forecast covers every requirement kind (staff, pos, kiosk, gates, fnb, retail, stock, resource, equipment, facility), filtered to what the venue configured. Action: a curated model per AI/ML task with 3-4 alternatives (done as research; see the curated-range decision). *(decided by Chinmay, 2026-10-02; DEC-009 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Requirement kinds | select | optional | — | Staff · POS · Kiosk · Gates · Fnb · Retail · Stock · Resource · Equipment · Facility | — | **Every requirement kind (decided 2 October 2026 by Chinmay, DEC-009; CHG-CSA-005)**: staff, POS, kiosk, gates, F&B, retail, stock, resource, equipment, facility, filtered to what the venue … | `AiOperationalRequirement.kind` |
| Forecast | text field | optional | — | — | — | Query subject attendance; the first active definition by default. | `AiForecastDefinition.definitionKey` |
| Event from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | The event's first day; getForecast `from` and listOperationalRequirements `from`. | `AiForecastPoint.targetStart` |
| Event to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | The event's last day; `to` on both reads. | `AiForecastPoint.targetEnd` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Kind | select | — | Staff · POS · Kiosk · Gates · Fnb · Retail · Stock · Resource · Equipment · Facility | `listOperationalRequirements` ?kind |
| Status | select | — | Issued · Accepted · Modified · Rejected · Handed over · Expired | `listOperationalRequirements` ?status |
| From | date and time picker | — | — | `listOperationalRequirements` ?from |
| To | date and time picker | — | — | `listOperationalRequirements` ?to |
| Version | picker: choose a version | — | — | `listOperationalRequirements` ?versionId |
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |

**Form: Run a what-if** (modal, opened by *Run a what-if*; *Run a what-if* calls `createForecastScenario`, *Cancel* sends nothing)

**Collects what `createForecastScenario` sends before it is called.** Required: `baseVersionId`, `changes`. Optional: `name`. A scenario starts from a published `baseVersionId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | — | — | — | `createForecastScenario` body |
| Base version `baseVersionId` | picker: choose a base version | required | — | — | shows names, sends the id | — | `createForecastScenario` body |
| Changes `changes` | repeatable rows | required | — | at least 1 | — | — | `createForecastScenario` body |
| Lever `changes[].lever` | select | required | — | Price · Capacity · Opening hours · Weather · Event · Marketing · Staffing · Closure | — | — | `createForecastScenario` body |
| Target `changes[].target` | text field | optional | — | — | — | — | `createForecastScenario` body |
| Value `changes[].value` | key and value settings | optional | — | — | — | — | `createForecastScenario` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **what-if changes (createForecastScenario)**: A scenario is built on a published forecast version (baseVersionId, chosen from the event's date) with typed changes: expected attendance, opening hours, an added performance, weather, a closure, staffing. Name optional; default "What-if: <event> <date>". It never changes production. *(source: contracts/satellite/ai.yaml#createForecastScenario / MoM 18 Sep 4.10)*

#### Outputs: what the screen shows and produces

**Shown**

**Recommended requirements** (data table, from `listOperationalRequirements`): "Configured" against "AI recommended" from the board is the requirement against what the venue has set up; the board labels were not fields.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Staff, POS, Kiosk, Gates, Fnb, Retail… | — |
| Subject ref | text | A role, outlet, gate, item or resource type. |
| Period start | 1 Oct 2026, 14:30 | — |
| Period end | 1 Oct 2026, 14:30 | — |
| Quantity | 1,234.5 | — |
| Quantity P90 | 1,234.5 | The requirement at the forecast's 90th percentile, for planning to the busy case. |
| Unit | text | — |
| Status | chip: Issued, Accepted, Modified, Rejected, Handed over, Expired | — |

**Forecast basis** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Target end | 1 Oct 2026, 14:30 | — |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Unit | text | — |
| Drivers | grouped details | Component decomposition or SHAP contributions, largest first (ADM-506). |

**The selected requirement** (detail panel, from `listOperationalRequirements`)

| Shows | Format | Notes |
|---|---|---|
| Target contract | text | The owning module that applies it: `workforce`, `fnb`, `inventory`, `resources`, `access`. |
| Productivity standard | grouped details | The standard used, e.g. covers per staff hour, scans per gate per hour. |
| Decision note | text | — |
| Handover ref | text | The owning module's record once handed over. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run a what-if (primary button) | `createForecastScenario` POST `/forecast-scenarios` | AiForecastScenario | AiForecastScenario | — | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Configured vs AI recommended**: Two columns per resource (lifeguards, cashiers, gate lanes, golf carts, cabanas): configured quantity, and the recommended quantity at the most-likely forecast with the busy case (P90) beside it, e.g. "14 (busy case 17)". A difference is highlighted, not corrected. *(source: contracts/satellite/ai.yaml#/components/schemas/AiOperationalRequirement (quantity, quantityP90) / screens/P08-venue-back-office.yaml#BO-919)*
- **basis and maturity**: The forecast's "Based on" line and stage badge above the table, e.g. "Starting - Based on: your venue profile, water-park pattern, UAE calendar, weather. Limited historical data." The forecast range is shown, not a single number. *(source: ADR-0051 / contracts/satellite/ai.yaml#/components/schemas/AiForecastVersion (maturity))*
- **scenario result**: The scenario's figures beside the base version's, clearly labelled "What-if", with the changes listed. *(source: contracts/satellite/ai.yaml#createForecastScenario)*
- **Requirement kinds covered**: Every requirement kind (staff, pos, kiosk, gates, fnb, retail, stock, resource, equipment, facility), filtered to what the venue has configured. The model behind each task comes from TICVAI's curated range (the best-suited model plus 3-4 alternatives). *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-001))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Run what-if**: Creates the scenario and shows its requirements next to the base; nothing is allocated. *(source: contracts/satellite/ai.yaml#createForecastScenario)*
- **Open in staffing requirements**: Opens BO-927 for the staff rows, where a requirement is accepted, modified or rejected. *(source: screens/P08-venue-back-office.yaml#BO-927)*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listOperationalRequirements` (onLoad, Requirements derived from the forecast); `listForecastDefinitions` (onLoad, The attendance forecast definitions; the picked one's …)

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource forecasting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No published forecast for this event yet: the baseline forecast fills the requirements as soon as one is published (ADR-0051). Offers Run a what-if once a base version exists. |
| Empty, no results (`?state=emptyNoResults`) | Nothing of the chosen kinds: names the kinds filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No published forecast for the date yet**: Says so and offers to run one (or that the nightly run will publish it); never shows a blank recommended column. The day-one forecast exists from the starting pattern, so this happens only before the first run. *(source: ADR-0051 / contracts/satellite/ai.yaml#getForecast)*
- **Forecast stale (more than 36 hours since the last publication)**: A "Forecast is out of date" marker on the recommended column with the publication time. *(source: contracts/satellite/ai.yaml#getForecast (stale))*
- **Venue profile missing a setting the requirement needs (e.g. no productivity standard for a role)**: The row says which setting is missing and links to the AI venue profile; other rows still show. *(source: ADR-0051 (Contract change) / contracts/satellite/ai.yaml#/components/schemas/AiVenueSettings (staffProductivity))*

#### Consistency with other screens

- Match `BO-927`: Same requirement rows for staff; the decision is taken there.
- Match `ADM-507`: Same what-if model as the console simulator; same labels for changes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event: Ladies' Night, Coastal Aqua, Thu 15 Oct 2026, 18:00-23:00
forecast:
  mostLikely: 2600
  range: 1,850-3,400 guests
  stage: Starting
  basedOn: your venue profile, water-park pattern, UAE calendar, weather (31°C, clear)
rows:
- resource: Lifeguards
  configured: 12
  recommended: 14 (busy case 17)
- resource: F&B cashiers
  configured: 6
  recommended: 6 (busy case 8)
- resource: Gate lanes
  configured: 4
  recommended: 3 (busy case 4)
whatIf: +600 guests (DJ announced)
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `createForecastScenario` → `AI_USE` (operate) · staff
- `listOperationalRequirements` → `AI_USE` (operate) · staff
- `listForecastDefinitions` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.55 | AI shall forecast future resource demand. | Ticketing Catalogue | CONTRACTED | `getForecast` |
| 4.1.17 | Forecast demand based on historical and operational data. | Bundles and Promotions | CONTRACTED | `getForecast` |
| 5.6.26 | Predict queue lengths, wait times, peak demand, and capacity shortages. | F&B & Guest Management | CONTRACTED | `getForecast` |
| 8.2.1 | System shall forecast attendance based on historical attendance patterns. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.2 | System shall forecast attendance by venue. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.3 | System shall forecast attendance by attraction. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.4 | System shall forecast attendance by event. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.5 | System shall forecast attendance by session. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.6 | System shall forecast attendance by date range. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.7 | System shall forecast attendance by day of week. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.8 | System shall forecast attendance by month. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.9 | System shall forecast attendance by season. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-919` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-919`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 12: Works in AI Event Resource Forecasting → Predict the resources required for an event before final allocation.
- ADR-0051 *Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence* (`docs/adr/0051-ai-ships-on-a-baseline-and-learns-per-tenant.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-919?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run a what-if.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-920` Event Resource Cost Estimator

**Calculate the expected resource cost of delivering an event.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-920 |
| Who uses it | venue staff holding `EVENT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/rentals/event-resource-cost-estimator-bo-920` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What an event's resource plan will cost, by kind, with the requirements that have no price yet listed so the total is not mistaken for complete.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search event resource cost | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by resource type, department, venue, event phase, internal/external, staff/equipment and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include contractors | toggle | on | — | `estimateEventResourceCost` ?includeContractors |

#### Outputs: what the screen shows and produces

**Shown**

**Every event resource cost** (data table)

| Shows | Format | Notes |
|---|---|---|
| Budget | text | not in the schema: `Budget` |
| Estimated | text | not in the schema: `Estimated` |
| Committed | text | not in the schema: `Committed` |
| Actual | text | not in the schema: `Actual` |
| Variance | text | not in the schema: `Variance` |

**The selected event resource cost** (detail panel): The pack groups this record's detail under its own headings: “Budget Variance”, “Estimated saving”.

| Shows | Format | Notes |
|---|---|---|
| Budget | text | not in the schema: `Budget` |
| Estimated | text | not in the schema: `Estimated` |
| Committed | text | not in the schema: `Committed` |
| Actual | text | not in the schema: `Actual` |
| Variance | text | not in the schema: `Variance` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue cost (primary button) | navigation or local | — | — | — | — |
| Equipment cost (secondary button) | navigation or local | — | — | — | — |
| External resource cost (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **estimate**: Lines per requirement, totals by kind, grand total, and "unpriced: 3 requirements" as a warning. *(source: contracts/spine/catalogue.yaml#estimateEventResourceCost)*

**Data it reads**: `estimateEventResourceCost` (onLoad, What the event's resource plan costs, by kind)

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource cost list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource cost untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event resource cost yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event resource cost are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
estimate:
  total: AED 184,500.00
  byKind:
    staff: AED 62,000.00
    equipment: AED 96,500.00
    contractors: AED 26,000.00
  unpriced: 2
```

#### Permissions

- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `estimateEventResourceCost` → `EVENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-920` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-920`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 14: Works in Event Resource Cost Estimator → Calculate the expected resource cost of delivering an event.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-920?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue cost, Equipment cost, External resource cost.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-921` Multi-Event Allocation & Conflict Optimizer

**Manage scarce resources across simultaneous or overlapping events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-921 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/multi-event-allocation-conflict-optimizer-bo-921` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Scarce resources across overlapping events on one view: a shared timeline of the week's events, a resource summary (Security Level 2+ required 50, available 43, gap 7; LED screens 9 vs 7), priority rules, and AI-proposed redistributions compared against the current allocation before anyone applies them. The one thing to get right: a proposal shows its effect (gaps, conflicts, cost, transfers) next to the current plan, and a person applies it.

**Known correction pending (do not draw the wrong version)**

- **Total required and Gap tiles and the event, priority and proposed resolution fields have no source** Why: getResourceCalendar returns resource states; nothing returns demand per event, event priority or optimisation proposals. *(source: contracts/satellite/resources.yaml#getResourceCalendar / screens/P08-venue-back-office.yaml#BO-921; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The View filter is a selectField and the shared timeline a data table of segments** Why: The timeline is the calendar component with Day/Week views (VO-R01). *(source: DI-907 / DI-919; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do optimisation proposals come through the AI proposed-actions queue (listProposedActions / decideProposedAction) like BO-928 and BO-929?** → Drawn default accepted: Draw proposals as AI proposed actions with Accept / Reject and an audit line. *(decided by Chinmay, 2026-10-02; DEC-515 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Resource type | select field | — | — | — | — | Sends `?resourceTypeId=` (e.g. Security Level 2+, LED screens). | — |
| View | select field | — | — | — | — | Sends `?granularity=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceCalendar` ?from |
| To | date and time picker | — | — | `getResourceCalendar` ?to |
| Resource type | picker: choose a resource type | — | — | `getResourceCalendar` ?resourceTypeId |
| Category | picker: choose a category | — | — | `getResourceCalendar` ?categoryId |
| Granularity | radio group | — | Day · Week · Month · Agenda | `getResourceCalendar` ?granularity |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Window and scope**: Week or day window with the calendar navigator (VO-R01), venue scope, resource type filter. *(source: contracts/satellite/resources.yaml#getResourceCalendar)*
- **Priority rules**: Ordered list - event priority, SLA, customer tier, revenue, contractual commitment, resource suitability, operational risk - used to break shortages. *(source: screens/P08-venue-back-office.yaml#BO-921)*

#### Outputs: what the screen shows and produces

**Shown**

**Total required** (metric tile): The pack asks for total required; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Total required | text | not in the schema: `Total required` |

**Available** (metric tile, from `getResourceCalendar`): Count of resources of the chosen type.

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | — |

**Gap** (metric tile): The pack asks for gap; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Gap | text | not in the schema: `Gap` |

**Shared timeline** (data table, from `getResourceCalendar`): Segments in conflict are highlighted; the pack draws events, not resources, across the timeline.

| Shows | Format | Notes |
|---|---|---|
| Resource name | text | — |
| Resource type | the name it points at, never the id | — |
| Utilisation percent | 1,234.5 | — |
| Segments | list or chips (count when long) | — |

**The selected conflict** (detail panel, from `getResourceCalendar`): Event, priority and the proposed resolution are pack labels.

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| State | chip: Available, Reserved, Assigned, Partially utilised, Fully utilised, Unavailable… | — |
| Booking | the name it points at, never the id | — |
| Conflicts with | list or chips (count when long) | — |
| Event | text | not in the schema: `Event` |
| Event priority | text | not in the schema: `Event priority` |
| Proposed resolution | text | not in the schema: `Proposed resolution` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resource summary**: Resource, total required, total available, gap, severity chip (Critical, High, Medium, OK); gap red when negative. *(source: screens/P08-venue-back-office.yaml#BO-921)*
- **Event timeline**: Events as bars across the days (Corporate Gala, Concert A, Conference B, VIP Dinner) coloured Confirmed, Needs attention, Conflict, Optimised. *(source: screens/P08-venue-back-office.yaml#BO-921)*
- **Proposals and comparison**: Each proposal as a sentence with its saving or gap closed ("Move 4 security staff from Conference B after 18:00 to Concert A - closes 4 of 7"); Current vs Optimised table for gaps, conflicts, cost (AED), transfers and utilisation. *(source: screens/P08-venue-back-office.yaml#BO-921 / screens/P08-venue-back-office.yaml#BO-922)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Apply selected / Apply all**: Shows the list of changes and their effect, then applies on confirm; each change re-runs conflict detection and is recorded as an AI recommendation approved by the user. *(source: screens/P08-venue-back-office.yaml#BO-932 / contracts/satellite/resources.yaml#updateResourceBooking)*
- **Click a conflict**: Detail with the event, its priority and the proposed resolution. *(source: screens/P08-venue-back-office.yaml#BO-921)*

**Data it reads**: `getResourceCalendar` (onLoad, Conflicts across events)

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-event allocation conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-event allocation conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-event allocation conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-event allocation conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A proposal would break a mandatory rule (unqualified security staff)**: Not shown as available (VO-R11); listed under "Rejected by rules" with the rule. *(source: screens/P08-venue-back-office.yaml#BO-932)*

#### Consistency with other screens

- Match `BO-871`: Same planner component (VO-R14); this entry adds cost and scenario comparison for events.
- Match `BO-928`: AI conflict resolution proposals use the same proposal card.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
window: Sun 18 - Sat 24 Oct 2026
summary:
- resource: Security Level 2+
  required: 50
  available: 43
  gap: -7
  severity: Critical
- resource: LED screens
  required: 9
  available: 7
  gap: -2
  severity: High
- resource: Wireless mics
  required: 26
  available: 24
  gap: -2
  severity: Medium
- resource: Technical crew
  required: 28
  available: 28
  gap: 0
  severity: OK
proposal: Move 4 security staff from Conference B after 18:00 to Concert A; use projector package at VIP Dinner
  instead of 2 LED screens
```

#### Permissions

- `getResourceCalendar` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The system must prevent the same resource being double-booked or assigned to overlapping bookings (conflict detection and resolution). Multi-event planning and drag-and-drop allocation assign resources visually, alongside rule-based automatic assignment. *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-484)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-921` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-921`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 16: Works in Multi-Event Allocation & Conflict Optimizer → Manage scarce resources across simultaneous or overlapping events.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-921?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-922` Event Resource Approval & Readiness Gate

**Provide the final governance checkpoint before an event resource plan becomes operational.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-922 |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `EVENT_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `eventId` (navigation) |
| Route | `/rentals/event-resource-approval-readiness-gate-bo-922` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The last check before an event's resource plan becomes operational: readiness, unsecured items and the approval request that signs it off.

**Fixed on main** (the package already carries these; draw what it says): The purpose also describes an AI resource intelligence engine. (CHG-WIR-026).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create approval request (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Submit for approval**: Raises an approval request of kind configuration change for the plan; the gate shows pending until decided. *(source: contracts/spine/approvals.yaml#createApprovalRequest)*

**Where the user goes next**

- → `BO-913` Event Resource Planning Command Center: *Back to Event Resource Planning Command Center*; carries `eventId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event resource approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event resource approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event resource approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event resource approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gate:
  event: Gulf Attractions Summit
  readiness: ready
  approval: pending, Operations director
```

#### Permissions

- `getEventResourcePlan` → `EVENT_CONFIGURE` (configure) · staff
- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-922` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-922`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 7
- Flow F270 *Resource Management Configuration board 7: Event Resource Planning Command …*, step 18: Works in Event Resource Approval & Readiness Gate → Provide the final governance checkpoint before an event resource plan becomes operational.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-922?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create approval request, Cancel.
- [ ] Every transition is wired: `BO-913`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `EVENT_CONFIGURE`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"allocateResources": {"method":"POST","path":"/resource-allocations","contract":"resources","summary":"Fill a requirement from the pool, rotating rather than repeating","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"bookResource": {"method":"POST","path":"/resource-bookings","contract":"resources","summary":"Reserve a specific resource for a window — staff only","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createForecastScenario": {"method":"POST","path":"/forecast-scenarios","contract":"ai","summary":"Run a what-if","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiForecastScenario","responds":null},
"createResourcePackage": {"method":"POST","path":"/resource-packages","contract":"resources","summary":"Define a reusable combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"},
"createRotaAssignment": {"method":"POST","path":"/rota-assignments","contract":"workforce","summary":"Put someone on the rota","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RotaAssignment","responds":"RotaAssignment"},
"estimateEventResourceCost": {"method":"GET","path":"/events/{eventId}/resource-cost","contract":"catalogue","summary":"What an event's resource plan costs, by kind","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"includeContractors","in":"query","required":false}],"requestBody":null,"responds":"EventResourceCostEstimate"},
"getEventResourcePlan": {"method":"GET","path":"/events/{eventId}/resource-plan","contract":"catalogue","summary":"Everything an event needs, and whether it has been secured","permission":"EVENT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"EventResourcePlan"},
"getForecast": {"method":"GET","path":"/forecasts","contract":"ai","summary":"Forecast values","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":true},{"name":"versionId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"dimensionKey","in":"query","required":null},{"name":"scenarioId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getResourceCalendar": {"method":"GET","path":"/resource-calendar","contract":"resources","summary":"Every resource against time, with conflicts already marked","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"resourceTypeId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"granularity","in":"query","required":null}],"requestBody":null,"responds":"ResourceCalendarRow"},
"listForecastDefinitions": {"method":"GET","path":"/forecast-definitions","contract":"ai","summary":"What is forecast","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subject","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOperationalRequirements": {"method":"GET","path":"/operational-requirements","contract":"ai","summary":"Requirements derived from the forecast","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"versionId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResourcePackages": {"method":"GET","path":"/resource-packages","contract":"resources","summary":"Predefined combinations assigned as one","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourcePackage"},
"listSpaces": {"method":"GET","path":"/spaces","contract":"catalogue","summary":"Halls, rooms and areas an event can occupy","permission":"EVENT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Space"},
"setEventResourcePlan": {"method":"PUT","path":"/events/{eventId}/resource-plan","contract":"catalogue","summary":"State what the event needs, by role and by kind","permission":"EVENT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EventResourcePlan","responds":"EventResourcePlan"},
"updateResourcePackage": {"method":"PUT","path":"/resource-packages/{packageId}","contract":"resources","summary":"Change a combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiForecastDefinition": {"type":"object","x-ticvai-persistence":"ai.forecast_definition","description":"**What is forecast, at what grain, for what horizon, how often and by which producer** (design 3.1 Forecast, 5.2; ADM-500). One forecasting service for the platform: BI's extra subjects are definitions here, not a second forecaster (AIP-036, AIP-037).","required":["definitionKey","subject","grain","horizonDays","producer"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionKey":{"type":"string"},"name":{"type":"string"},"subject":{"type":"string","enum":["attendance","arrivalPattern","productDemand","timeslotDemand","channelPace","revenue","occupancy","attractionUtilisation","queue","entryFlow","staffing","posDemand","fnbDemand","retailDemand","stockDemand","resourceDemand","refunds","cashCollection","membershipRenewals","churn"]},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"description":"**Whose AI this forecast is, and so who publishes it** (Chinmay, 2 October, workbook Q3: \"the permission holder for that module's AI\"; CHG-FUP-004). `publishForecastVersion` requires the permission `contracts/shared/permissions.yaml` `x-ticvai-module-ai-publish` names for this module. Absent on a write, the server takes it from `subject`: ticketing for `attendance`, `arrivalPattern`, `productDemand`, `timeslotDemand`, `channelPace`, `occupancy` and `refunds`; access for `entryFlow` and `attractionUtilisation`; queue for `queue`; fnb for `fnbDemand`; retail for `retailDemand`; inventory for `stockDemand`; resources for `resourceDemand`; membership for `membershipRenewals` and `churn`; core for `revenue`, `staffing`, `posDemand` and `cashCollection`. Proposed, client to correct; a venue may name the module itself. Always present on a read."},"grain":{"type":"string","enum":["hour","day","week","month"]},"dimensions":{"type":"array","items":{"type":"string"},"description":"Breakdowns forecast directly or reconciled to. **Documented keys (29 September, build; 8.2.12, 8.2.14, 8.2.27):** `product`, `channel`, `timeslot`, `gate`, `outlet`, `customerSegment` and `originCountry`. `customerSegment` is the marketing-crm segment (of those in `segmentIds`, else the membership tier) the guest belonged to on the day of the booking; `originCountry` is the guest profile's country, else the order's billing country, else the channel's market, recorded as `unknown` rather than guessed. **The nightly snapshot (design 2.2 C step 1) carries both for every booking and admission**, so a definition that names them is forecast and reconciled by them. Any other key is accepted and forecast only where the snapshot carries it."},"segmentIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"The marketing-crm segments `customerSegment` breaks down by, in priority order where a guest is in several. Empty means membership tiers."},"horizonDays":{"type":"integer","minimum":1,"maximum":730},"refreshCadence":{"type":"string","enum":["hourly","daily","weekly"]},"producer":{"type":"string","enum":["rule","statistical","model","ensemble"],"description":"Which producer is live (design 3.10). A model is promoted only through `promoteAiRelease`. **`ensemble`** (18 September minutes, M18-16): a weighted blend of the rule and statistical producers, and of a promoted model where one exists; the weights are recorded on each version. Setting `ensemble` never brings in an unpromoted model."},"historyWindowMonths":{"type":"integer","minimum":1,"maximum":60,"default":36,"description":"How much of the venue's own history the statistical producer reads (18 September minutes, M18-16: \"36 months of history\"). Imported history (`importVenueHistory`) counts. Less than the window is not an error: the cold-start setting fills the gap."},"coldStart":{"type":"object","description":"**What the forecast stands on before the venue has history** (29 September, AI functions review; forecasting book p.27 \"New Venue / New Product Problem\"). Day one is never empty: the prior is the venue AI settings (typical weekday and weekend attendance, capacity, opening hours) x the starting pattern for the venue type x the UAE calendar x weather, with bookings on hand as a floor. The statistical producer blends own data in as `(k x prior + n x own) / (k + n)`, with `k` = `priorWeightObservations`. The version's `maturity` says which stage it reached.","properties":{"strategy":{"type":"string","enum":["venueSettings","startingPattern","sisterVenue","categoryBaseline","importedHistory"],"default":"venueSettings","description":"`venueSettings` uses the onboarding figures with the venue-type pattern; `sisterVenue` a venue of the same tenant; `categoryBaseline` a product category's own history; `importedHistory` means an import covers the window and the prior only fills unseen holidays."},"sisterVenueId":{"type":"string","format":"uuid","nullable":true,"description":"For `sisterVenue`. Same tenant only (no data is pooled across tenants, AIP-149)."},"priorWeightObservations":{"type":"integer","minimum":1,"maximum":52,"default":4,"description":"`k`: how many own observations the prior is worth (4 same weekdays by default)."},"startingBandPercent":{"type":"integer","minimum":5,"maximum":80,"default":40,"description":"The width of the range while the prior carries most of the weight (about +/-40%)."}}},"producerRef":{"type":"string","readOnly":true},"shadowProducerRef":{"type":"string","nullable":true,"readOnly":true,"description":"Runs alongside and is recorded, never shown (design 3.5)."},"autoPublish":{"type":"boolean","default":false,"description":"Publish without approval when the quality gates pass (autonomy L4, design 3.8). Otherwise an `AI_APPROVE` holder publishes."},"qualityGates":{"type":"object","additionalProperties":true,"nullable":true,"description":"Completeness, blocking signals and accuracy-regression thresholds a version must pass to publish."},"signalKeys":{"type":"array","items":{"type":"string"},"description":"Signal sources this definition may use (ADM-501)."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastPoint": {"type":"object","x-ticvai-persistence":"ai.forecast_point","description":"One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["versionId","targetStart","p50"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"scenarioId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_scenario","description":"Set where the point belongs to a what-if scenario rather than the version itself."},"targetStart":{"type":"string","format":"date-time"},"targetEnd":{"type":"string","format":"date-time"},"dimensionKey":{"type":"string","nullable":true,"description":"Canonical key of the breakdown, e.g. `product=…;channel=web`."},"p10":{"type":"number","nullable":true},"p50":{"type":"number"},"p90":{"type":"number","nullable":true},"unit":{"type":"string"},"drivers":{"type":"object","additionalProperties":true,"nullable":true,"description":"Component decomposition or SHAP contributions, largest first (ADM-506)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastScenario": {"type":"object","x-ticvai-persistence":"ai.forecast_scenario","description":"**A what-if against a published version** (ADM-507, ADM-517, BO-931). Changes nothing in production; its points are written with `scenarioId`.","required":["baseVersionId","changes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"baseVersionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"changes":{"type":"array","items":{"type":"object","required":["lever"],"properties":{"lever":{"type":"string","enum":["price","capacity","openingHours","weather","event","marketing","staffing","closure"]},"target":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true}}},"minItems":1},"status":{"type":"string","enum":["computing","ready","failed"],"readOnly":true},"result":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Deltas against the base version by subject and period."},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastVersion": {"type":"object","x-ticvai-persistence":"ai.forecast_version","description":"**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.","required":["definitionId","versionNumber","status","basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionNumber":{"type":"integer","minimum":1},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"readOnly":true,"description":"The module of the version's definition (`AiForecastDefinition.module`), copied when the version is produced; the module whose AI publish permission `publishForecastVersion` requires (CHG-FUP-004)."},"status":{"type":"string","enum":["running","draft","awaitingApproval","published","superseded","rejected","failed"],"readOnly":true},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string"},"modelVersion":{"type":"string","nullable":true},"dataCutoffAt":{"type":"string","format":"date-time","description":"The analytical replica watermark the snapshot was taken at."},"horizonStart":{"type":"string","format":"date-time"},"horizonEnd":{"type":"string","format":"date-time"},"qualityChecks":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Each gate and whether it passed."},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal","description":"Null where the definition auto-published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiOperationalRequirement": {"type":"object","x-ticvai-persistence":"ai.operational_requirement","description":"**A requirement derived from a forecast version** (design 2.2 C step 6, AIP-067): staff, POS, gates, F&B, stock or resources, computed with the tenant's productivity standards. **Autonomy L2 (prepare)**: it is sent to the owning module as a recommendation bound to that version, and a person applies it there.\n**Every kind, from release 1** (Chinmay, 2 October, workbook Q9: \"all kinds\"; CHG-CSA-005). The event forecast derives requirements of every `kind` below, filtered to what the venue has configured (a venue with no kiosks gets no `kiosk` rows); the models in place improve with the venue's data.","required":["versionId","kind","periodStart","quantity"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"kind":{"type":"string","enum":["staff","pos","kiosk","gates","fnb","retail","stock","resource","equipment","facility"]},"targetContract":{"type":"string","description":"The owning module that applies it: `workforce`, `fnb`, `inventory`, `resources`, `access`."},"subjectRef":{"type":"string","nullable":true,"description":"A role, outlet, gate, item or resource type."},"periodStart":{"type":"string","format":"date-time"},"periodEnd":{"type":"string","format":"date-time"},"quantity":{"type":"number"},"quantityP90":{"type":"number","nullable":true,"description":"The requirement at the forecast's 90th percentile, for planning to the busy case."},"unit":{"type":"string"},"productivityStandard":{"type":"object","additionalProperties":true,"nullable":true,"description":"The standard used, e.g. covers per staff hour, scans per gate per hour."},"status":{"type":"string","enum":["issued","accepted","modified","rejected","handedOver","expired"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionNote":{"type":"string","nullable":true},"handoverRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning module's record once handed over."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n\n**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request\nwith no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the\nShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"EventResourceCostEstimate": {"type":"object","x-ticvai-persistence":"none — projection over the event resource plan and the rates in resources and workforce, computed at read time","description":"What `estimateEventResourceCost` returns (decided 29 September, readiness close-out): the event's resource plan priced, one line per requirement or contractor, with the total by kind.","required":["eventId","lines","total"],"properties":{"eventId":{"type":"string","format":"uuid"},"lines":{"type":"array","items":{"type":"object","required":["kind","quantity","total"],"properties":{"kind":{"type":"string","enum":["venue","equipment","staff","external","transport"],"description":"The cost heading on BO-920. Mapped from the requirement kind: space -> venue, equipment and service -> equipment, staff -> staff, contractor -> external, vehicle -> transport."},"requirementId":{"type":"string","format":"uuid","nullable":true,"description":"The `EventResourcePlan.requirements[].id` priced; null on a contractor line."},"organisationId":{"type":"string","format":"uuid","nullable":true,"description":"The contractor organisation, on an `external` line."},"label":{"type":"string"},"quantity":{"type":"integer","minimum":0},"hours":{"type":"number","nullable":true,"description":"Booked hours the unit cost applies to, where the rate is per hour."},"unitCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"costSource":{"type":"string","enum":["resourceRate","workforceRate","contractorQuote","manual"]}}}},"totalsByKind":{"type":"object","description":"The sum of `lines[].total` for each kind, keyed by `kind`.","additionalProperties":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"unpricedRequirementIds":{"type":"array","description":"Requirements with no rate to price them; left out of `total` rather than guessed.","items":{"type":"string","format":"uuid"}}}},
"EventResourcePlan": {"type":"object","x-ticvai-persistence":"catalogue.event_resource_plan","description":"Event board 6. **Secured against required is the only number an event manager wants.**\n","properties":{"eventId":{"type":"string","format":"uuid"},"requirements":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["space","equipment","staff","contractor","vehicle","service"]},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"roleCode":{"type":"string","nullable":true},"quantity":{"type":"integer"},"from":{"type":"string","format":"date-time","nullable":true},"to":{"type":"string","format":"date-time","nullable":true},"locationScopePath":{"type":"string","nullable":true},"securedCount":{"type":"integer","readOnly":true},"status":{"type":"string","enum":["required","partiallySecured","secured","atRisk"]},"bookingIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"contractors":{"type":"array","items":{"type":"object","properties":{"organisationId":{"type":"string","format":"uuid"},"role":{"type":"string"},"headcount":{"type":"integer"},"accreditationProgrammeId":{"type":"string","format":"uuid","nullable":true},"insuranceVerified":{"type":"boolean","default":false}}}},"readiness":{"type":"string","readOnly":true,"enum":["notPlanned","planning","atRisk","ready"]},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ResourceBooking": {"type":"object","x-ticvai-persistence":"resources.booking","required":["id","resourceId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/ResourceBookingStatus"},"holdId":{"type":"string","format":"uuid","nullable":true,"description":"The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"},"recurrenceGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"conditionOut":{"type":"string","nullable":true},"conditionIn":{"type":"string","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"}}},
"ResourceBookingStatus": {"type":"string","enum":["reserved","checkedOut","returned","overdue","cancelled","noShow"]},
"ResourceCalendarRow": {"type":"object","description":"Board 2.01. **One resource across the window, with its states already computed** — including conflict, which a client cannot derive from a booking list.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"resourceName":{"type":"string"},"resourceTypeId":{"type":"string","format":"uuid"},"utilisationPercent":{"type":"number"},"segments":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["available","reserved","assigned","partiallyUtilised","fullyUtilised","unavailable","onBreak","onLeave","underMaintenance","operationallyBlocked","pendingApproval","conflict"]},"bookingId":{"type":"string","format":"uuid","nullable":true},"conflictsWith":{"type":"array","items":{"type":"string","format":"uuid"}}}}}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourcePackage": {"type":"object","x-ticvai-persistence":"resources.resource_package","description":"Board 1.08. **A package may hold placeholders.** \"One technician\" is a slot, and naming a person would make the package unbookable whenever they are off.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"applicableVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"components":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRequirement"}},"allocationPriority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"minimumMinutes":{"type":"integer","nullable":true},"maximumMinutes":{"type":"integer","nullable":true},"requiresApproval":{"type":"boolean","default":false},"internalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"ResourceRequirement": {"type":"object","x-ticvai-persistence":"resources.resource_requirement","description":"**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n","required":["quantity"],"properties":{"id":{"type":"string","format":"uuid"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"},"quantity":{"type":"integer","default":1},"mandatory":{"type":"boolean","default":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"requiredAttributes":{"type":"object","additionalProperties":true},"substituteResourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"},"packageId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The package this requirement is a component of** (4 October 2026, CHG-FXC-003). Written by `updateResourcePackage`, which replaces the package's `components` as these rows; `listResourcePackages` reads them back by it. Null for an experience's own requirement (`productId`)."},"productId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The experience product this requirement belongs to (`setExperienceResourceRequirements`). Exactly one of `packageId` and `productId` is set."}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"Space": {"type":"object","x-ticvai-persistence":"catalogue.space","description":"Event board 3.2. **Bookable, as distinct from navigable** — `venue-map` owns the geometry.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"venueMapZoneId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**Where the space is also a bookable `resources` resource**, so its calendar and conflict detection come from there rather than a second scheduler.\n"},"parentSpaceId":{"type":"string","format":"uuid","nullable":true},"maximumCapacity":{"type":"integer","nullable":true},"safeCapacity":{"type":"integer","nullable":true},"setupMinutes":{"type":"integer","default":0},"teardownMinutes":{"type":"integer","default":0},"accessRules":{"type":"object","nullable":true,"additionalProperties":true},"bookable":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]}
}
```
