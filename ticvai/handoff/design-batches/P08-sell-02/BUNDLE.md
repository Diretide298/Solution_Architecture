# P08-sell-02 — P08 · Sell (2 of 4)

**10 screens · 56 operations · 67 schemas · 14 permissions**

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

- **Every control that can be refused must be gated.** 14 permissions apply here:
  `AI_USE, CAPACITY_CONFIGURE, EVENT_CONFIGURE, ORDER_CREATE, ORDER_VIEW, PERFORMANCE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_VIEW`…. A control nobody can use must say so,
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
| `BO-017` | Capacity Management | B | 24 | 20 | 6 | 14 | 7 | 0 | — | notStarted (generated) |
| `BO-018` | Allocation & Holds | B | 4 | 14 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-019` | Closures & Blackouts | B | 44 | 31 | 6 | 38 | 1 | 0 | — | notStarted (generated) |
| `BO-037` | Offline Package Status | B | 52 | 32 | 6 | 3 | 0 | 0 | — | notStarted (generated) |
| `BO-063` | Opening Hours & Calendar | B | 16 | 9 | 6 | 17 | 2 | 0 | — | notStarted (generated) |
| `BO-102` | Sell | A | 2 | 37 | 6 | 57 | 0 | 0 | — | notStarted (generated) |
| `BO-109` | Menu Builder & POS Layout Designer | A | 49 | 7 | 6 | 8 | 2 | 2 | — | notStarted (generated) |
| `BO-110` | Recipe & BOM Management | B–D | 0 | 0 | 6 | 0 | 2 | 2 | — | notStarted (generated) |
| `BO-111` | Ingredient Substitution, Allergen & Nutrition | A | 21 | 39 | 5 | 6 | 1 | 0 | — | notStarted (generated) |
| `BO-112` | Production Planning & Production Sheets | A | 35 | 20 | 5 | 17 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-063, BO-110 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-017` Capacity Management

**Change how many people a performance can take (renamed from session, decided 28 September, audit R165).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block B · ticket #29669 (VM-BO-017) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `channelCapacityId` (deepLink), `entryId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/capacity-management` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How many people a performance can take and how that is split: sales capacity per channel envelope, and the waitlist for sold-out performances. Sales capacity (tickets) and admission capacity (people inside, counted by scans) are two different numbers and must be shown apart.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listWaitlistEntries return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Performance id | picker: choose a performance (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?performanceId=` to `listChannelCapacities`. | `listChannelCapacities` ?performanceId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listWaitlistEntries` ?performanceId |

**Form: Create channel capacity** (modal, opened by *Create channel capacity*; *Create channel capacity* calls `createChannelCapacity`, *Cancel* sends nothing)

**Collects what `createChannelCapacity` sends before it is called.** Required: `performanceId`, `name`, `capacity`. Optional: `seatCategoryId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Performance `performanceId` | picker: choose a performance | required | — | — | shows names, sends the id | — | `createChannelCapacity` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createChannelCapacity` body |
| Seat category `seatCategoryId` | picker: choose a seat category | optional | — | — | shows names, sends the id | — | `createChannelCapacity` body |
| Capacity `capacity` | number field | required | — | min 0 | — | — | `createChannelCapacity` body |

**Form: Release channel allocation** (modal, opened by *Release channel allocation*; *Release channel allocation* calls `relinquishChannelAllocation`, *Cancel* sends nothing)

**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | multi-select chips | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre; at least 1 | — | — | `relinquishChannelAllocation` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `relinquishChannelAllocation` body |

**Form: Save channel allocations** (modal, opened by *Save channel allocations*; *Save channel allocations* calls `setChannelAllocations`, *Cancel* sends nothing)

**Collects what `setChannelAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Allocations `allocations` | repeatable rows | required | — | at least 1 | — | — | `setChannelAllocations` body |
| Channel `allocations[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `setChannelAllocations` body |
| Allocated units `allocations[].allocatedUnits` | number field | required | — | min 0 | — | — | `setChannelAllocations` body |
| Release at `allocations[].releaseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it. | `setChannelAllocations` body |
| Sales channel `allocations[].salesChannelId` | picker: choose a sales channel | optional | — | — | shows names, sends the id | The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3). | `setChannelAllocations` body |
| Allocation type `allocations[].allocationType` | radio group | optional | Dedicated | Shared pool · Dedicated · Percentage · Dynamic | — | How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row. | `setChannelAllocations` body |
| Minimum units `allocations[].minimumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Maximum units `allocations[].maximumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Replenishment rule `allocations[].replenishmentRule` | key and value settings | optional | — | — | — | `{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`. | `setChannelAllocations` body |
| Waitlist behavior `allocations[].waitlistBehavior` | segmented control | optional | None | None · Join waitlist · Notify on release | — | — | `setChannelAllocations` body |
| Release threshold units `allocations[].releaseThresholdUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Release hours before event `allocations[].releaseHoursBeforeEvent` | number field | optional | — | min 0 | — | Alternative to `releaseAt`, relative to the performance start. | `setChannelAllocations` body |
| Contractual units `allocations[].contractualUnits` | number field | optional | — | min 0 | — | Units a partner agreement guarantees; rebalancing never goes below it. | `setChannelAllocations` body |
| Minimum guaranteed units `allocations[].minimumGuaranteedUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Is frozen `allocations[].isFrozen` | toggle | optional | off | — | — | Excluded from rebalancing. | `setChannelAllocations` body |

Errors to draw in the form: 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101)

**Form: Save channel capacity** (modal, opened by *Save channel capacity*; *Save channel capacity* calls `updateChannelCapacity`, *Cancel* sends nothing)

**Collects what `updateChannelCapacity` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateChannelCapacity` body |
| Capacity `capacity` | number field | optional | — | min 0 | — | — | `updateChannelCapacity` body |

Errors to draw in the form: 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101)

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **capacity change**: Bulk edit across selected performances is allowed; reducing below sold is refused. *(source: DI-168 / contracts/spine/catalogue.yaml#updateChannelCapacity)*

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
| Create channel capacity (primary button) | `createChannelCapacity` POST `/channel-capacities` | CreateEnvelopeRequest | ChannelCapacity | — | opens modal first |
| Release channel allocation (secondary button) | `relinquishChannelAllocation` POST `/channel-capacities/{channelCapacityId}/channel-allocations/release` | inline | ChannelAllocationSet | — | opens modal first |
| Save channel allocations (secondary button) | `setChannelAllocations` PUT `/channel-capacities/{channelCapacityId}/channel-allocations` | inline | ChannelAllocationSet | 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101) | opens modal first |
| Save channel capacity (secondary button) | `updateChannelCapacity` PATCH `/channel-capacities/{channelCapacityId}` | inline | ChannelCapacity | 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **two capacities**: Sales capacity per performance and live admission count against venue admission capacity, side by side with different labels. *(source: DI-455 / DI-456)*
- **waitlist**: Who is waiting, in order, and how many places each asked for; "Offer freed capacity" invites them in order. *(source: contracts/spine/catalogue.yaml#listWaitlistEntries / contracts/spine/catalogue.yaml#offerWaitlistCapacity)*

**Data it reads**: `listChannelCapacities` (onLoad, List capacity envelopes); `listWaitlistEntries` (onLoad, Guests waiting for capacity)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity yet. Offers Create channel capacity (`createChannelCapacity`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on performanceId and the capacity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `createChannelCapacity`, `relinquishChannelAllocation`, `setChannelAllocations`, `updateChannelCapacity` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101); 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101) |

#### Consistency with other screens

- Match `BO-013`: Same envelope bar.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
performance:
  name: Dune Nights Fri 14 Nov 20:00
  salesCapacity: 1000
  sold: 912
  admissionCapacity: 6500
  inside: 4120
waitlist:
- guest: Hessa Al Mazrouei
  places: 4
  since: 12 Nov 18:20
```

#### Permissions

- `listChannelCapacities` → `PRODUCT_VIEW` (read) · staff, partner
- `getChannelAllocations` → `PRODUCT_VIEW` (read) · staff, partner
- `createChannelCapacity` → `CAPACITY_CONFIGURE` (configure) · staff
- `relinquishChannelAllocation` → `CAPACITY_CONFIGURE` (configure) · staff, partner
- `setChannelAllocations` → `CAPACITY_CONFIGURE` (configure) · staff
- `updateChannelCapacity` → `CAPACITY_CONFIGURE` (configure) · staff
- `listWaitlistEntries` → `PRODUCT_VIEW` (read) · staff
- `offerWaitlistCapacity` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `createChannelCapacity`, `relinquishChannelAllocation`, `setChannelAllocations`, `updateChannelCapacity` …

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.40 | Capacity Management Visibility | Ticketing Sales | CONTRACTED | `listChannelCapacities` |
| 8.9.2 | System shall display current attendance, occupancy levels, capacity utilization, and crowd distribution across parks, venues, facilities, and attractions. | Unified Operations Dashboard | CONTRACTED | `listChannelCapacities` |
| 1.1.3 | The system should be able to sell time-slot based tickets for attractions. The system should support: - Creation of timeslots for a whole day or for a period - Configuration of capacity for each … | Ticketing Catalogue | CONTRACTED | `createChannelCapacity` |
| 7.3.2 | Allow configure inventory and capacity for parks | F&B POS | CONTRACTED | `createChannelCapacity` |
| 1.1.10 | The system should allow the capacity for all type of ticket to be configurable. Capacity of a ticket can be configurable at multiple levels: 1) Sales Capacity: Allow only a fixed number of tickets to … | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 1.1.127 | Maximum sellable quantity controls | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 2.1.1 | The system should have the ability to create as many sales channels as necessary by the system admin. Sales Channels creation should involve capture of all required data such as account assignment … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.2 | The system should support the configuration of products, prices, quotas, sales limits and sales schedule for each sales channels. Some sales channels can be configured to be accessible to only … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.3 | The system should store and manage all rules for product compatibility, eligibility and pricing that will be applicable to for each sales channel. These rules will be part of the system and not … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.5 | For BtoB online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.11 | - Only BtoB PLUs | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.15 | - Quotas can be applied for one Customer or a category of Customers | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*
- Decision: venue-level admission capacity supersedes event-level capacity; a system prompt/validation prevents configuring or selling an event beyond the remaining venue capacity. Overriding is an authorisation-gated (RBAC) action for authorised users only. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 5. Key Decisions · DI-456)*
- Two capacity types shown distinctly: sales capacity (tickets sellable per performance) and admission capacity (a real-time, scan-based count of guests inside via entry/exit turnstiles), capping on-site attendance independent of tickets sold. *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-455)*
- AI suggestions from sales forecasts: add/remove time slots, merge under-sold adjacent slots (with guest notification of the time change), and dynamic pricing (raise when a slot is >~80% sold, lower when <~20–30%). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-454)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- "Envelopes" split a performance's capacity by channel (e.g. of 100: 30 B2C, 40 B2B, 30 on-site); each channel shows only its own share as available. Configured once and applied to all linked performances. *(agreed · MoM 7 Aug 2026, 15. Capacity Splitting via Envelopes · DI-170)*
- Performance capacity is edited individually or by multi-select bulk edit; a performance can be suspended, resumed (any time before start) or cancelled — a state change, never a delete. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-168)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-017` · status **notStarted** · provenance generated
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create channel capacity, Release channel allocation, Save channel allocations, Save channel capacity.
- [ ] Every transition is wired: `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 7 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-018` Allocation & Holds

**See who is holding capacity, and release it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | Block B · ticket #29673 (VM-BO-018) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listInventoryHolds` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `inventoryHoldId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/allocation-holds` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): Acquire, renew and relinquish a lease are terminal and order-service calls (workstation scope; guests never call them); the supervisor's act on the holds screen … Removed 2 October 2026 (CHG-WIR-025): Acquire, renew and relinquish a lease are terminal and order-service calls (workstation scope; guests never call them); the supervisor's act on the holds screen … Removed 2 October 2026 (CHG-WIR-025): Acquire, renew and relinquish a lease are terminal and order-service calls (workstation scope; guests never call them); the supervisor's act on the holds screen …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Who is holding capacity right now (tills, kiosks, guest baskets) and for how long, with the supervisor's ability to reclaim a hold stranded by a dead terminal. Holds are not reservations; they expire.

**Fixed on main** (the package already carries these; draw what it says): The screen offers Acquire, Renew and Release hold forms. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel capacity id | picker: choose a channel capacity (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?channelCapacityId=` to `listInventoryHolds`. | `listInventoryHolds` ?channelCapacityId |
| Holder workstation id | picker: choose a holder workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?holderWorkstationId=` to `listInventoryHolds`. | `listInventoryHolds` ?holderWorkstationId |
| Status | radio group | optional | — | Active · Expired · Released · Force released · Converted | — | Sends `?status=` to `listInventoryHolds`. | `listInventoryHolds` ?status |

**Sent by *Force release inventory hold*** (`forceReleaseInventoryHold`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `forceReleaseInventoryHold` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every inventory hold** (data table, from `listInventoryHolds`)

| Shows | Format | Notes |
|---|---|---|
| Requested units | 1,234 | — |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Allocation this lease draws from. |
| Status | chip: Active, Expired, Released, Force released, Converted | `states/lease.yaml`. `expired` is set by that model's timer transition when `expiresAt` passes without a renewal, not by any operation in … |
| Acquired at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Released at | 1 Oct 2026, 14:30 | — |

**The selected inventory hold** (detail panel, from `listInventoryHolds`)

| Shows | Format | Notes |
|---|---|---|
| Requested units | 1,234 | — |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Allocation this lease draws from. |
| Granted units | 1,234 | May be less than requested — a partial grant is not an error. Constrained by the channel's remaining allocation plus the general pool … |
| Consumed units | 1,234 | — |
| Status | chip: Active, Expired, Released, Force released, Converted | `states/lease.yaml`. `expired` is set by that model's timer transition when `expiresAt` passes without a renewal, not by any operation in … |
| Acquired at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Released at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Force release inventory hold (destructive button) | `forceReleaseInventoryHold` POST `/inventory-holds/{inventoryHoldId}/force-release` | inline | InventoryHold | 403 Authenticated but not permitted at the requested scope | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **hold list**: Holder (workstation name or "Guest basket"), envelope, units granted and consumed, expires in (countdown), status (Active, Expired, Released, Force released, Converted). *(source: contracts/spine/catalogue.yaml#acquireInventoryHold)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Force release**: Reason required; reported consumption is honoured and the remainder returns immediately; the dialog names the holder. *(source: contracts/spine/catalogue.yaml#forceReleaseInventoryHold)*

**Data it reads**: `listInventoryHolds` (onLoad, List leases)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

**What opens over it**

- confirmDialog *Force release inventory hold*: **Names what `forceReleaseInventoryHold` changes and what it leaves alone**, in the consequence rather than the verb. A allocation holds this affects should be identified in the dialog, not just counted. **Collects what `forceReleaseInventoryHold` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The allocation holds list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the allocation holds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No allocation holds yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on channelCapacityId, holderWorkstationId, status and the allocation holds are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryHolds` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `forceReleaseInventoryHold`. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
holds:
- holder: Till 07, Main Gate
  envelope: Day Pass 15 Nov
  granted: 20
  consumed: 14
  expiresIn: 6 min
- holder: Guest basket
  granted: 4
  consumed: 0
  expiresIn: 13 min
```

#### Permissions

- `listInventoryHolds` → `PRODUCT_VIEW` (read) · staff
- `forceReleaseInventoryHold` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryHolds` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `forceReleaseInventoryHold`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*
- "Envelopes" split a performance's capacity by channel (e.g. of 100: 30 B2C, 40 B2B, 30 on-site); each channel shows only its own share as available. Configured once and applied to all linked performances. *(agreed · MoM 7 Aug 2026, 15. Capacity Splitting via Envelopes · DI-170)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-018` · status **notStarted** · provenance generated
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Force release inventory hold.
- [ ] Every transition is wired: `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-019` Closures & Blackouts

**Stop selling something, for a reason.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | Block B · ticket #29676 (VM-BO-019) |
| Who uses it | venue staff holding `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `VENUE_MAP_MANAGE` (3 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPerformances` reads the population and `getEvent` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `eventId` (deepLink), `performanceId` (deepLink), `mapId` (navigation), `pathId` (navigation) · cold entry: **A link to a performance that has happened.** Offers the next performance of the same event. |
| Route | `/venue-operations/closures-blackouts` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2d`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for product blackout dates and venue closure days from the closures screen (blackoutDates sit on entitlement templates, edited on BO-012).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Stop selling something for a reason: cancel or suspend performances, close the venue or an attraction on dates, close a path on the map. Blackout dates for products such as memberships on public holidays are part of this.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No operation sets product blackout dates or a venue closure day; the screen only cancels performances and closes paths. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listPerformances`. | `listPerformances` ?from |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `listPerformances`. | `listPerformances` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

**Form: Create event** (modal, opened by *Create event*; *Create event* calls `createEvent`, *Cancel* sends nothing)

**Collects what `createEvent` sends before it is called.** Required: `code`, `name`, `venueId`. Optional: `parentEventId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; A code already used by any event in the tenant is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`. | `createEvent` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createEvent` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `createEvent` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Create performances** (modal, opened by *Create performances*; *Create performances* calls `createPerformances`, *Cancel* sends nothing)

**Collects what `createPerformances` sends before it is called.** Required: `startsAt`, `endsAt`. Optional: `admissionRulesId`, `seatMapId`, `recurrence`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Seat map `seatMapId` | picker: choose a seat map | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Recurrence `recurrence` | group | optional | — | — | — | Generate a series rather than a single performance. Read in the region's time zone: the Region owns the zone and every venue inherits it without override (tenancy), so … | `createPerformances` body |
| Interval minutes `recurrence.intervalMinutes` | number field (minutes) | optional | — | min 1 | — | — | `createPerformances` body |
| Until `recurrence.until` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Days of week `recurrence.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createPerformances` body |

**Form: Recommend seats** (modal, opened by *Recommend seats*; *Recommend seats* calls `recommendSeats`, *Cancel* sends nothing)

**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party size `partySize` | stepper or slider | required | — | min 1; max 50 | — | — | `recommendSeats` body |
| Strategy `strategy` | radio group | required | — | Best available · Best value · Closest to stage · Accessible · Contiguous | — | — | `recommendSeats` body |
| Categorys `categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `recommendSeats` body |
| Max price `maxPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `recommendSeats` body |
| Accessible count `accessibleCount` | number field | optional | 0 | — | — | Wheelchair spaces in the party. Companions are added automatically. | `recommendSeats` body |
| Max options `maxOptions` | number field | optional | 3 | max 10 | — | — | `recommendSeats` body |

Errors to draw in the form: 404 No selection satisfies the constraints

**Form: Save event** (modal, opened by *Save event*; *Save event* calls `updateEvent`, *Cancel* sends nothing)

**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `updateEvent` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateEvent` body |

**Form: Save performance** (modal, opened by *Save performance*; *Save performance* calls `updatePerformance`, *Cancel* sends nothing)

**Collects what `updatePerformance` sends before it is called.** Nothing in the body is required. Optional: `startsAt`, `endsAt`, `status`, `admissionRulesId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Status `status` | segmented control | optional | — | Scheduled · On sale · Suspended | — | — | `updatePerformance` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `updatePerformance` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |

Errors to draw in the form: 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.

**Form: Save path closure** (modal, opened by *Save path closure*; *Save path closure* calls `setPathClosure`, *Cancel* sends nothing)

**Collects what `setPathClosure` sends before it is called.** Required: `isClosed`. Optional: `reason` (maintenance, incident, event, weather, crowding, other), `note`, `force`, `expectedReopenAt`. **Choosing Other makes the note required** — the form will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is closed `isClosed` | toggle | required | — | — | — | — | `setPathClosure` body |
| Reason `reason` | select | optional | — | Maintenance · Incident · Event · Weather · Crowding · Other | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222); refused `400` without one, and the notes are reviewed quarterly so the common … | `setPathClosure` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setPathClosure` body |
| Force `force` | toggle | optional | off | — | — | Close it even though something becomes unreachable. | `setPathClosure` body |
| Expected reopen at `expectedReopenAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPathClosure` body |

Errors to draw in the form: 400 Validation failed; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on a park with two hundred paths is not actionable. (PathClosureProblem)

**Sent by *Cancel performance*** (`cancelPerformance`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `cancelPerformance` body |
| Guest message `guestMessage` | key and value settings | optional | — | — | — | — | `cancelPerformance` body |
| Refund percentage `refundPercentage` | stepper or slider | optional | 100 | min 0; max 100 | — | — | `cancelPerformance` body |
| Offer alternative performance `offerAlternativePerformanceId` | picker: choose an offer alternative performance | optional | — | — | shows names, sends the id | — | `cancelPerformance` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `cancelPerformance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | Required unless `dryRun` (audit R144, proposed by the coordinator). | `cancelPerformance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `cancelPerformance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `cancelPerformance` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **closure**: What (performance, product, path), when, reason and the guest message; for sold performances the cancellation path (dry run, refund percentage, alternative) applies. *(source: contracts/spine/catalogue.yaml#cancelPerformance / contracts/satellite/venue-map.yaml#setPathClosure / DI-452)*

#### Outputs: what the screen shows and produces

**Shown**

**Every performance** (data table, from `listPerformances`)

| Shows | Format | Notes |
|---|---|---|
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |

**Every event** (data table, from `listEvents`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**The selected performance** (detail panel, from `getPerformance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |

**The seat availability** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| By category | list or chips (count when long) | — |
| Seats | list or chips (count when long) | — |

**The event** (detail panel, from `getEvent`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Parent event | the name it points at, never the id | For grouped events. |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Cancel performance (destructive button) | `cancelPerformance` POST `/performances/{performanceId}/cancel` | inline | PerformanceCancellationResult | 403 The supervisor step-up is missing or failed (audit R144). The PIN did not verify, or the principal does not hold `PERFORMANCE_CONFIGURE` at this venue.; 409 The performance is `cancelled`, `completed` or `soldOut`. … | step-up: pin (Cancels a performance and queues refunds to every holder; a supervisor signs it in place (proposed by the coordinator …) |
| Create event (secondary button) | `createEvent` POST `/events` | CreateEventRequest | Event | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Create performances (secondary button) | `createPerformances` POST `/events/{eventId}/performances` | CreatePerformancesRequest | inline | — | opens modal first |
| Recommend seats (secondary button) | `recommendSeats` POST `/performances/{performanceId}/seat-recommendations` | SeatRecommendationRequest | inline | 404 No selection satisfies the constraints | opens modal first |
| Save event (secondary button) | `updateEvent` PATCH `/events/{eventId}` | inline | Event | — | opens modal first |
| Save performance (secondary button) | `updatePerformance` PATCH `/performances/{performanceId}` | inline | Performance | 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow. | opens modal first |
| Save path closure (secondary button) | `setPathClosure` POST `/venue-maps/{mapId}/paths/{pathId}/closure` | inline | PathClosureResult | 400 Validation failed; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on a park with two hundred paths is not actionable. (PathClosureProblem) | opens modal first |

**Data it reads**: `getPerformance` (onLoad, Read a performance); `getSeatAvailability` (onLoad, Seat status for a performance); `listEvents` (onLoad, List events)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

**What opens over it**

- confirmDialog *Cancel performance*: **Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A closures blackouts this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The closures blackouts list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the closures blackouts untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No closures blackouts yet. Offers Create event (`createEvent`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to and the closures blackouts are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getPerformance` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `EVENT_CONFIGURE` for `createEvent`, `updateEvent`; `PERFORMANCE_CONFIGURE` for `cancelPerformance`, `createPerformances`, `updatePerformance` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.; 409 Closing this strands a point, and the response names which in `strandedPoints`. *"Cannot close"* on … |

#### Edge cases to draw

- **Closing a performance that has sales**: Dry run first showing affected orders and refund exposure; supervisor PIN for the real run. *(source: R144)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
closures:
- what: Sandstorm Coaster
  when: 2026-11-20 all day
  reason: maintenance
- what: Annual Pass Gold
  blackout:
  - '2026-12-02'
  - '2026-12-31'
```

#### Permissions

- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `cancelPerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff · step-up pin
- `createEvent` → `EVENT_CONFIGURE` (configure) · staff
- `createPerformances` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `getEvent` → `PRODUCT_VIEW` (read) · staff
- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `listEvents` → `PRODUCT_VIEW` (read) · staff
- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `updateEvent` → `EVENT_CONFIGURE` (configure) · staff
- `updatePerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `setPathClosure` → `VENUE_MAP_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getPerformance` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `EVENT_CONFIGURE` for `createEvent`, `updateEvent`; `PERFORMANCE_CONFIGURE` for `cancelPerformance`, `createPerformances`, `updatePerformance` …

#### Requirements it meets

38 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.3.20 | System shall support event cancellation workflows including refunds, exchanges, notifications and audit tracking. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.21 | System shall support changing event dates, times and venues while automatically updating tickets, reservations and guest communications. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.4 | The system should propagate any changes made to the properties of a product to the already sold tickets as well. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.16 | System shall identify affected tickets, reservations, memberships, events and integrations before applying product changes. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.1 | The system should allow creation of events such as performances, workshops, activities or guided-tours. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.3.14 | Ability to create events with metadata (name, type, venue, date, time, organizer). The events could be free marketing, paid marketing events or show-tech events. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.3.29 | System shall support events spanning multiple venues, halls, spaces or locations under a single event. | Ticketing Catalogue | CONTRACTED | `createEvent` |
| 1.1.2 | The system should be able to sell dated tickets for attractions that allow access only for selected dates by guest. Special day tickets should also be supported. These are dated tickets that skip … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.4 | The system should provide an easy-to-use interface for creation and configuration of timeslots. A calendar view should be available for the user to define the timeslot and recurrence rules. The user … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| … 26 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-019` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 2.dc.html`
- Client design-board frames: `Seat Board 2.dc.html#seat-2d`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (44), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Cancel performance, Create event, Create performances, Recommend seats, Save event, Save performance, Save path closure.
- [ ] Every transition is wired: `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`, `VENUE_MAP_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-037` Offline Package Status

**Know what each device is enforcing right now.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block B · ticket #29666 (VM-BO-037) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE` (1 operate, 3 read, 2 configure); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCatalogueBundles` reads the population and `getLatestBundle` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/venue-operations/offline-package-status` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): Offline Operations Dashboard; Offline Product & Data Cache Management. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Owns POS board frame(s) POS-5A, POS-5C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): getOfflinePackage is workstation-scoped (the session's access point); a back-office screen cannot read another device's package with it. F89 step 3 keeps … Contract gap recorded 2 October 2026 (CHG-WIR-027): A venue-scoped read of the offline package version each device holds (getOfflinePackage answers only for the calling workstation).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What each device is enforcing right now: the catalogue release it applied, the offline access package it holds and the offline sales it has not yet synced or that were refused. Not what was configured, what is in force on the device (F89 step 3).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCatalogueBundles return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): getOfflinePackage is workstation-scoped (the session's access point); a back-office screen cannot read another device's package with it. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since | text field | — | — | `getLatestBundle` ?since |
| Workstation | picker: choose a workstation | — | — | `listSyncRejections` ?workstationId |
| Kind | radio group | — | Order · Payment · Refund · Void · Scan | `listSyncRejections` ?kind |
| Resolved | toggle | — | — | `listSyncRejections` ?resolved |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |

**Form: Publish bundle** (modal, opened by *Publish bundle*; *Publish bundle* calls `publishBundle`, *Cancel* sends nothing)

**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `publishBundle` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `publishBundle` body |
| Stale after hours `staleAfterHours` | number field (hours) | optional | — | min 1 | — | How long a terminal may trade on this bundle before refusing. Defaults to the venue's configured bound. | `publishBundle` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue

**Form: Report bundle applied** (modal, opened by *Report bundle applied*; *Report bundle applied* calls `reportBundleApplied`, *Cancel* sends nothing)

**Collects what `reportBundleApplied` sends before it is called.** Required: `appliedAt`, `outcome`. Optional: `error`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Applied at `appliedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportBundleApplied` body |
| Outcome `outcome` | segmented control | required | — | Applied · Rolled back · Signature invalid | — | — | `reportBundleApplied` body |
| Error `error` | text field | optional | — | — | — | — | `reportBundleApplied` body |

**Form: Save offline policy** (modal, opened by *Save offline policy*; *Save offline policy* calls `setOfflinePolicy`, *Cancel* sends nothing)

**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope path `scopePath` | text field | required | — | pattern `^[a-z0-9_]+(\.[a-z0-9_]+)*$` | — | The node this policy is for, and the key `setOfflinePolicy` upserts on. The body names its target here, because the path does not. | `setOfflinePolicy` body |
| Max offline hours `maxOfflineHours` | stepper or slider (hours) | optional | 24 | min 1; max 72 | — | After which the workstation refuses to sell rather than keep journalling. A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody … | `setOfflinePolicy` body |
| Allowed offline `allowedOffline` | multi-select chips | optional | — | Sale · Refund · Exchange · Entitlement issue · Entitlement validate · Loyalty accrual · Loyalty redemption · Wallet spend · Price override · Discount · Void line · No sale; Selling from a cached catalogue is safe; issuing a refund is not, because the original … | — | What may happen with no network, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified. | `setOfflinePolicy` body |
| Offline value ceiling `offlineValueCeiling` | money field | optional | — | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | `setOfflinePolicy` body |
| Offline transaction ceiling `offlineTransactionCeiling` | number field | optional | — | min 1; max 5000 | — | A ceiling on count as well as value. Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. | `setOfflinePolicy` body |
| On ceiling breach `onCeilingBreach` | segmented control | optional | Block new sales | Warn · Block new sales · Block all | — | — | `setOfflinePolicy` body |
| Requires manager to extend `requiresManagerToExtend` | toggle | optional | on | — | — | — | `setOfflinePolicy` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

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

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle** (data table, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**Every sync rejection** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolution | chip: Posted, Voided, Refunded | What `resolveSyncRejection` recorded. Null while the rejection waits. |

**Every workstation** (data table, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |

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
|  (publish gate) | navigation or local | — | — | — | — |
| Publish bundle (primary button) | `publishBundle` POST `/catalogue/bundles` | inline | BundleSummary | 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue | opens modal first |
| Report bundle applied (secondary button) | `reportBundleApplied` POST `/catalogue/bundles/{version}/applied` | inline | — | — | opens modal first |
| Save offline policy (secondary button) | `setOfflinePolicy` PUT `/offline-policy` | OfflinePolicy | OfflinePolicy | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Sync orders (secondary button) | `syncOrders` POST `/sync/orders` | inline | OrderSyncResult | — | emits `order.paid`, `sync.rejectionRaised`; opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **device table**: Device, last seen, release version applied (with "behind by 2" when old), offline package valid until, unsynced count, rejected count; rows past the staleness bound in red. *(source: F89 step 3 / contracts/spine/catalogue.yaml#listCatalogueBundles / contracts/spine/access.yaml#getOfflinePackage)*

**Data it reads**: `listCatalogueBundles` (onLoad, List published bundles); `getLatestBundle` (onLoad, Pull the current bundle for this workstation's venue); `listSyncRejections` (onLoad, Entries the server refused); `listWorkstations` (onLoad, List workstations)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `BO-128` Live Workstation Health Monitor: *The fleet is monitored*; carries `workstationId`; calls `listCatalogueBundles`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline package status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline package status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline package status yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `syncOrders` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A publish is already in progress for this venue |

#### Edge cases to draw

- **Device stopped reporting**: Flagged "about to refuse to trade" when its release passes staleAfter. *(source: contracts/spine/catalogue.yaml#reportBundleApplied)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
devices:
- device: Till 07
  release: 2026.11.14-3
  offlinePackageUntil: 15 Nov 06:00
  unsynced: 0
- device: Kiosk K-03
  release: 2026.11.12-1
  behind: 2
  unsynced: 18
  rejected: 4
```

#### Permissions

- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `getLatestBundle` → `PRODUCT_VIEW` (read) · staff
- `publishBundle` → `PRODUCT_CONFIGURE` (configure) · staff
- `reportBundleApplied` → `PRODUCT_VIEW` (read) · staff
- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff
- `setOfflinePolicy` → `TENANT_CONFIGURE` (configure) · staff
- `syncOrders` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `syncOrders` …

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.7 | System shall allow publishing products to selected sales channels including Website, Mobile App, POS, API and Reseller channels. | Ticketing Catalogue | CONTRACTED | `publishBundle` |
| 2.3.1 | The system should support offline mode for POS and Kiosk: - Ability to switch automatically to offline mode in case of server outage / network loss - Definition of which functionality will be lost in … | Ticketing Sales | CONTRACTED | `syncOrders` |
| 2.14.2 | For all sales at POS, it is possible to have an offline mode. | Ticketing Sales | CONTRACTED | `syncOrders` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-037` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 5.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 5.dc.html#pos-5a`, `POS Board 5.dc.html#pos-5c`, `Retail Board 3.dc.html#ret-3j`
- Flow F89 *Offline policy is set, cached, monitored and reconciled*, step 3: Each device's cached package is checked. → **What each device is enforcing right now**, not what was configured.
- Flow F89 *Offline policy is set, cached, monitored and reconciled*, step 5: What the tills did offline is reconciled. → **Every rejected offline sale is seen by a person.** A rejection nobody reads is money nobody collects.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (52), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish bundle, Report bundle applied, Save offline policy, Sync orders, What publishing changes.
- [ ] Every transition is wired: `BO-007`, `BO-009`, `BO-128`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-063` Opening Hours & Calendar

**Say when the venue is open, including the exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block B · ticket #29107 (VM-BO-063) |
| Who uses it | venue staff holding `REGION_CONFIGURE`, `TENANT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPerformances` reads the population and `getPerformance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `outletId` (session) · cold entry: An outlet opened from the directory. |
| Route | `/venue-operations/opening-hours-calendar` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): Operating Hours & Service Periods; Operating Hours & Sales Periods. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Drawn 26 August** — `Seat Board 1.dc.html` frame `seat-1c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): Opening hours are venue and outlet settings; the full performance, event and seat-recommendation set (createPerformances, recommendSeats and the rest) belongs to … Removed 2 October 2026 (CHG-WIR-025): Opening hours are venue and outlet settings; the full performance, event and seat-recommendation set (createPerformances, recommendSeats and the rest) belongs to … Removed 2 October 2026 (CHG-WIR-025): Opening hours are venue and outlet settings; the full performance, event and seat-recommendation set (createPerformances, recommendSeats and the rest) belongs to …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When the venue and its outlets are open, including exceptions (public holidays, Ramadan hours, private hire), and the business day boundary (midnight to midnight, or 06:00 to 06:00).

**Fixed on main** (the package already carries these; draw what it says): The screen carries the full performance and seat-recommendation set (createPerformances, recommendSeats). (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Form: Save outlet** (modal, opened by *Save outlet*; *Save outlet* calls `updateOutlet`, *Cancel* sends nothing)

**Collects what `updateOutlet` sends before it is called.** Nothing in the body is required. Optional: `name`, `stockLocationId`, `costCenterId`, `openingHours`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateOutlet` body |
| Name translations `nameTranslations` | key and value settings | optional | — | localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. | — | The outlet's name in other languages, keyed by ISO 639-1 code (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: "Yes, where a country needs it: the local language plus … | `updateOutlet` body |
| Stock location `stockLocationId` | picker: choose a stock location | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Outlet type `outletType` | select | optional | — | Fine dining · Casual dining · Quick service · Coffee shop · Bar lounge · Food court · Buffet · Commissary · Retail | — | How an F&B or retail outlet trades, which switches features on or off (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: "Add both fields: outlet type and department … | `updateOutlet` body |
| Payment timing `paymentTiming` | segmented control | optional | Send first | Send first · Pay first | — | When an F&B order is paid, set per outlet (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). | `updateOutlet` body |
| Admission context `admissionContext` | segmented control | optional | — | Inside venue · Standalone | — | Whether an outlet sits behind the admission gate (decided 2 October 2026, Chinmay, batch 1, WEB-036: "Inside the venue, a ticket is needed. | `updateOutlet` body |
| Produces for outlets `producesForOutletIds` | multi-picker: choose produces for outlets | optional | — | — | — | Replaces the whole list of outlets this one produces for (CHG-CSP-005). | `updateOutlet` body |
| Sale board `saleBoardId` | picker: choose a sale board | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | Replaces the whole weekly pattern. An empty array clears it. | `updateOutlet` body |
| Day `openingHours[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `updateOutlet` body |
| From `openingHours[].from` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet opens. | `updateOutlet` body |
| To `openingHours[].to` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet closes. | `updateOutlet` body |
| Ends next day `openingHours[].endsNextDay` | toggle | optional | off | With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours. | — | A late-night window is one window past midnight (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). | `updateOutlet` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateOutlet` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 As `createOutlet`: a missing required local-language name (`local-name-required`), a window that ends before it starts (`window-ends-before-start`), or a …

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **business day**: Day start hour shown with an example ("a sale at 01:30 counts on the previous day"). *(source: DI-149)*
- **outlet hours**: Weekly hours per outlet plus dated exceptions; an exception overrides the week. *(source: contracts/spine/tenancy.yaml#updateOutlet)*

#### Outputs: what the screen shows and produces

**Shown**

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Save outlet (secondary button) | `updateOutlet` PATCH `/outlets/{outletId}` | inline | Outlet | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `getVenueSettings` (onLoad, Operational settings for this venue)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The opening hours calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the opening hours calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No opening hours calendar yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to and the opening hours calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_VIEW`, which `getVenueSettings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REGION_CONFIGURE` for `updateOutlet`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 As `createOutlet`: a missing required local-language name (`local-name-required`), a window that ends before it starts (`window-ends-before-start`), or a … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
hours:
  venue: Dune Park
  week: Sun-Thu 10:00-22:00, Fri-Sat 10:00-24:00
  exceptions:
  - date: '2026-12-02'
    hours: 10:00-02:00
    label: National Day
  dayStart: 06:00
```

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `updateOutlet` → `REGION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_VIEW`, which `getVenueSettings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REGION_CONFIGURE` for `updateOutlet`.

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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- The operating calendar is configurable: a midnight-to-midnight transaction day or an alternative such as 6am to 6am. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-149)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-063` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 1.dc.html`
- Client design-board frames: `Seat Board 1.dc.html#seat-1c`

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-063?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Save outlet.
- [ ] Every transition is wired: `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `REGION_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-102` Sell

**Everything in sell, and what in it needs attention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #28085 (VM-BO-102) |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_VIEW`, `TENANT_VIEW` (1 operate, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listUpsellRules` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/sell` |

**What the spec says about it.** Section landing. **14 screens reach the entry point through here** — before 20 August they reached it through nothing.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-012): Staff previewing a recommendation slot must not write impressions or declines into the guest decline store; recordRecommendationEvents on a back-office landing … Contract gap recorded 2 October 2026 (CHG-WIR-014): No staff preview of a recommendation slot that records nothing.

**From the AI & Intelligence process.** The Sell section landing of Venue Management: the way into the selling screens, and the home of the upsell and cross-sell rules - the Promotions relationship map that Block A upsell on WEB-008, GST-048 and the till answers from. From the AI angle the one thing to get right: these rules are the "business rules always win" layer - each rule shows where it appears, what it suggests and how many suggestions it allows, with a live preview of what a guest would see for a sample cart.

**Fixed on main** (the package already carries these; draw what it says): decideRecommendations is called onLoad and recordRecommendationEvents on actions from a back-office landing. (CHG-WIR-012); The upsell suggestion panel binds getUpsellSuggestions, which the screen does not declare. (CHG-SBO-019).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Placement | select | optional | — | Product detail · Cart · Checkout · Post purchase · At gate · In venue | — | Sends `?placement=` to `listUpsellRules`. | `listUpsellRules` ?placement |
| Search sell | search field | — | — | — | — | — | — |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **upsell rule (placement, triggers, suggested variants or bundle, channels, priority, max suggestions, active)**: Placement in guest words (Extras step, cart, checkout, till basket, kiosk basket); max suggestions defaults to 3 at checkout; channels exclude OTA and reseller in release 1. *(source: contracts/satellite/promotions.yaml#listUpsellRules / DI-959 / ADR-0052 (AI-D08 no OTA or reseller recommendations))*

#### Outputs: what the screen shows and produces

**Shown**

**Every upsell rule** (data table, from `listUpsellRules`): **Read-only at the venue** (decided 28 September, audit R183) — upsell rules are created and deleted at region level; the venue sees the rules of its region in force, with no create, edit or delete here.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Priority | 1,234 | — |
| Max suggestions | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**Card list** (card list): 14 screens, each with what needs attention.

**The selected upsell rule** (detail panel, from `listUpsellRules`): **Read-only at the venue** (decided 28 September, audit R183) — upsell rules are created and deleted at region level; the venue sees the rules of its region in force, with no create, edit or delete here.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Placement | chip: Product detail, Cart, Checkout, Post purchase, At gate, In venue | — |
| Channels | list or chips (count when long) | Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience … |
| Priority | 1,234 | — |
| Max suggestions | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**The upsell suggestion** (detail panel, from `decideRecommendations`): The slot preview, as on WEB-008: `decideRecommendations` with `previewOnly` (ADR-0052).

| Shows | Format | Notes |
|---|---|---|
| Decision | the name it points at, never the id | — |
| Placement | chip: Product page, Cart, Checkout, Post purchase, Pre visit, In venue… | — |
| Mode | chip: Personalised, Contextual, Rules only, Fallback | — |
| Items | list or chips (count when long) | — |
| Tracking | the name it points at, never the id | Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses. |
| Product | the name it points at, never the id | The product recommended. Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind` (29 … |
| Promotion | the name it points at, never the id | For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine. |
| Coupon ref | text | For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`). |
| Reward | the name it points at, never the id | For `reward`, a marketing-crm loyalty reward the guest can redeem. |
| Challenge | the name it points at, never the id | For `challenge`, a marketing-crm challenge the guest can join. |
| Kind | chip: Upsell, Cross sell, Upgrade, Bundle, Add on, Membership… | — |
| Rank | 1,234 | — |
| Price ref | text | The Pricing reference the channel resolves to a price. AI never computes a price. |
| Reason template key | text | The template reason (decided 29 September, decision 9): no model writes guest-visible reasons. |
| Reason text | text | The rendered template in the session locale, where the channel shows reasons. |
| Confidence band | chip: High, Medium, Low | Design 5.6: a band, never a bare percentage. |
| Score | 1,234.5 | Normalised score. Returned to staff callers only; a guest response omits it. |
| Expires at | 1 Oct 2026, 14:30 | — |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **rules list**: Name, placement, trigger → suggestion in words ("2 adults + 2 children in cart → Family Day Pass"), channels, priority, active. *(source: contracts/satellite/promotions.yaml#listUpsellRules)*
- **preview**: "Preview for a sample cart" shows the offers the slot would return now, with each removal reason (owned already, contradicts the cart, sold out). *(source: contracts/satellite/ai.yaml#decideRecommendations / DI-960)*
- **needs attention**: Rules pointing at inactive or sold-out products, and offers declined most often, at the top of the landing. *(source: screens/P08-venue-back-office.yaml#BO-102 (purpose) / contracts/satellite/ai.yaml#recordRecommendationEvents)*

**Data it reads**: `getVenueSettings` (onLoad, What is enabled here); `listUpsellRules` (onLoad, Upsell rules in force, read-only — owned at region (decided …); `decideRecommendations` (onLoad, Fill a recommendation slot)

**Where the user goes next**

- → `BO-485` Self-Service Kiosk Profile & Channel Configuration: *Kiosk groups*
- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `BO-010` Promotions & Coupons: *Promotions & Coupons*
- → `BO-011` Packages & Bundles: *Packages & Bundles*
- → `BO-012` Membership Products: *Membership Products*
- → `BO-013` Channel & Distribution: *Channel & Distribution*
- → `BO-014` Catalogue Publishing: *Catalogue Publishing*
- → `BO-015` Performance Calendar: *Performance Calendar*
- → `BO-016` Performance Template: *Performance Template*
- → `BO-017` Capacity Management: *Capacity Management*
- → `BO-018` Allocation & Holds: *Allocation & Holds*
- → `BO-019` Closures & Blackouts: *Closures & Blackouts*
- → `BO-037` Offline Package Status: *Offline Package Status*
- → `BO-063` Opening Hours & Calendar: *Opening Hours & Calendar*
- → `BO-109` Menu Builder & POS Layout Designer: *Menu Builder & POS Layout Designer*
- → `BO-110` Recipe & BOM Management: *Recipe & BOM Management*
- → `BO-111` Ingredient Substitution, Allergen & Nutrition: *Ingredient Substitution, Allergen & Nutrition*
- → `BO-112` Production Planning & Production Sheets: *Production Planning & Production Sheets*
- → `BO-113` Central Kitchen & Commissary Management: *Central Kitchen & Commissary Management*
- → `BO-114` Variants, Attributes, Barcode & RFID Management: *Variants, Attributes, Barcode & RFID Management*
- → `BO-115` Category, Brand & Merchandise Hierarchy: *Category, Brand & Merchandise Hierarchy*
- → `BO-116` Merchandising & Product Presentation: *Merchandising & Product Presentation*
- → `BO-117` Product Import, Governance & AI Configuration Assistant: *Product Import, Governance & AI Configuration Assistant*
- → `BO-118` Campaign & Audience Management: *Campaign & Audience Management*
- → `BO-119` Cross-Sell, Upsell & Recommendation Rules: *Cross-Sell, Upsell & Recommendation Rules*; carries `ruleId`
- → `BO-120` Omnichannel Commerce & Journey Configuration: *Omnichannel Commerce & Journey Configuration*
- → `BO-121` Personalized Offers & Guest Engagement: *Personalized Offers & Guest Engagement*
- → `BO-122` POS Experience Dashboard: *POS Experience Dashboard*
- → `BO-123` POS Profile Management: *POS Profile Management*
- → `BO-124` Layout & Journey Builder: *Layout & Journey Builder*
- → `BO-125` Product & Category Button Configuration: *Product & Category Button Configuration*
- → `BO-126` Deployment, Preview & Audit: *Deployment, Preview & Audit*
- → `BO-142` Store Rules, Controls & Permissions: *Store Rules, Controls & Permissions*
- → `BO-143` Retail Global Settings & Controls: *Retail Global Settings & Controls*
- → `BO-1190` Donation Campaigns: *Donation Campaigns*
- → `ADM-164` Code Distribution & Assignment Manager: *Opens Code Distribution & Assignment Manager*
- → `ADM-570` Gateway, PSP & Acquirer Directory: *Opens Gateway, PSP & Acquirer Directory*
- → `ADM-603` B2B Invoice, On-Account & Payment Terms Configuration: *Opens B2B Invoice, On-Account & Payment Terms Configuration*
- → `BO-696` Event Duplication & Clone Configuration: *Opens Event Duplication & Clone Configuration*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in sell yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for sell. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `WEB-008`: The guest Extras step these rules fill.
- Match `GST-048`: Same.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- name: Family upgrade
  placement: Extras step
  trigger: 2 Adult + 2 Child Day Pass
  suggests: Family Day Pass (2+2)
  channels:
  - Website
  - App
  - Kiosk
  - POS
  maxSuggestions: 3
  priority: 1
- name: Fast pass on weekends
  placement: Checkout
  trigger: Day Pass, Sat-Sun
  suggests: Wave Rider Fast Pass
  priority: 2
```

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listUpsellRules` → `PRODUCT_VIEW` (read) · staff
- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous

**A refused user sees:** You do not have permission for sell. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

57 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 45 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-102` · status **notStarted** · provenance generated
- ADR-0052 *One recommendation engine; runtime in AI, configuration in Promotions* (`docs/adr/0052-one-recommendation-engine.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-102?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-485`, `BO-007`, `BO-009`, `BO-010`, `BO-011`, `BO-012`, `BO-013`, `BO-014`, `BO-015`, `BO-016`, `BO-017`, `BO-018`, `BO-019`, `BO-037`, `BO-063`, `BO-109`, `BO-110`, `BO-111`, `BO-112`, `BO-113`, `BO-114`, `BO-115`, `BO-116`, `BO-117`, `BO-118`, `BO-119`, `BO-120`, `BO-121`, `BO-122`, `BO-123`, `BO-124`, `BO-125`, `BO-126`, `BO-142`, `BO-143`, `BO-1190`, `ADM-164`, `ADM-570`, `ADM-603`, `BO-696`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_VIEW`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-109` Menu Builder & POS Layout Designer

**Arrange one outlet's menu and till grid for the next publish.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #27940 (APP-SETUP-BO-109) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE` (2 configure, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMenus` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `menuId` (BO-045), `saleBoardId` (navigation) · cold entry: Opened from BO-045 with a menu picked there. Opened cold, it says which menu to pick and links back to BO-045. |
| Route | `/sell/menu-builder-pos-layout-designer` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Drawn 31 August** — `FnB Board 2.dc.html` frame `fnb-2b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Menu Builder &amp; POS Layout Designer* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly. **The arranging canvas, opened from BO-045 (2 October 2026, CHG-SBO-008; DI-671, DI-987):** no menu list of its own, one hub entry; the till grid shares one designer with BO-124 and BO-125.

**Known gaps.** The menu list lives on BO-045; this canvas opens on the menu picked there (design-note correction fnb-retail BO-045/BO-109, CHG-SBO-008).

**From the Food, Beverage & Retail process.** The arranging canvas for one outlet's menu draft: sections on the left, the till grid in the middle, button properties on the right - what is arranged here is exactly what the cashier taps on the counter till (FNB-2B). The client agreed the Menu Builder defines the front-end POS layout per outlet, with categories, item tiles (image, name, price) and configurable button sizes for fast sellers. The one thing to get right is a faithful till preview and the rule that nothing reaches a till until the menu is published.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Two sources of the till order. setMenuSections says its sequence is the sequence on the sale board, while updateSaleBoard stores its own pages and tiles (by catalogue variant, not menu item). (CHG-SBO-005)
- The sale-board tile has no size or span, and a sale board is per venue, not per outlet. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Plumbing - "Outlet id" text field, "Active at" date picker, "Every menu" table with raw columns, and a "Save sale board" modal collecting … (CHG-SBO-008); emptyFirstRun says the screen offers no create action, yet createSaleBoard exists (on BO-124). (CHG-WIR-008); Overlap with BO-045 (shared frame fnb-2b, both set sections) and with BO-124/BO-125 (the same sale-board update on seven screens). (CHG-SBO-008); Purpose is a placeholder ("from the client design board, 20 August"). (CHG-WIR-010).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the till layout per outlet (DI-326) or per workstation (Workstation.saleBoard binds a board to a till, MATRIX 2.1.9)? Can two tills in one outlet differ?** → Till layout per outlet, with a till override (Workstation.saleBoard). *(decided by Chinmay, 2026-10-02; DEC-183 / CHG-NOTE-004)*
- **Which system functions may be placed on an F&B till grid (DI-157 lists ticket list, reservation list, transaction list, media lookup)?** → Drawn default stands (answer: "F&B functions only"): Recall held sale, Table map, Order list as action tiles; no ticketing functions on an F&B grid. *(decided by Chinmay, 2026-10-02; DEC-184 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listSaleBoards` ?kind |

**Form: Save menu sections** (modal, opened by *Save menu sections*; *Save menu sections* calls `setMenuSections`, *Cancel* sends nothing)

**Collects what `setMenuSections` sends before it is called.** Required: `sections`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sections `sections` | repeatable rows | required | — | — | — | — | `setMenuSections` body |
| Code `sections[].code` | text field | required | — | — | — | — | `setMenuSections` body |
| Name `sections[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Sort order `sections[].sortOrder` | number field | required | — | — | — | — | `setMenuSections` body |
| Items `sections[].items` | repeatable rows | optional | — | — | — | The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`. | `setMenuSections` body |
| ID `sections[].items[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setMenuSections` body |
| Product variant `sections[].items[].productVariantId` | picker: choose a product variant | required | — | — | shows names, sends the id | The catalogue variant this item links to, for reporting, stock and tax class only. | `setMenuSections` body |
| Name `sections[].items[].name` | text field | required | — | — | — | — | `setMenuSections` body |
| Description `sections[].items[].description` | text area | optional | — | — | — | — | `setMenuSections` body |
| Price `sections[].items[].price` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setMenuSections` body |
| Sort order `sections[].items[].sortOrder` | number field | optional | — | — | — | — | `setMenuSections` body |
| Modifier groups `sections[].items[].modifierGroupIds` | multi-picker: choose modifier groups | optional | — | — | — | — | `setMenuSections` body |
| Station `sections[].items[].stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `setMenuSections` body |
| Is stock tracked `sections[].items[].isStockTracked` | toggle | optional | — | Stock-tracked items cannot be sold offline. | — | True where a recipe exists. Stock-tracked items cannot be sold offline. | `setMenuSections` body |
| Is available `sections[].items[].isAvailable` | toggle | required | — | — | — | — | `setMenuSections` body |
| Unavailable reason `sections[].items[].unavailableReason` | text field | optional | — | — | — | — | `setMenuSections` body |
| Restore at `sections[].items[].restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand. | `setMenuSections` body |
| Preparation minutes `sections[].items[].preparationMinutes` | number field (minutes) | optional | — | — | — | — | `setMenuSections` body |
| Allergens `sections[].items[].allergens` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setMenuSections` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save sale board** (modal, opened by *Save sale board*; *Save sale board* calls `updateSaleBoard`, *Cancel* sends nothing)

**Collects what `updateSaleBoard` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. **The canvas is the input:** `pages` and their tiles come from the arranged grid, `venueId` from the session, `code` and `kind` from the outlet; only the name is typed. Dismissing sends nothing; the screen behind is unchanged.

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

**Form: New sale board** (modal, opened by *New sale board*; *New sale board* calls `createSaleBoard`, *Cancel* sends nothing)

**Collects what `createSaleBoard` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. **The canvas is the input:** `pages` and their tiles come from the arranged grid, `venueId` from the session, `code` and `kind` from the outlet; only the name is typed. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createSaleBoard` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createSaleBoard` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createSaleBoard` body |
| Kind `kind` | radio group | required | — | Ticketing · Fnb · Retail · Mixed | — | — | `createSaleBoard` body |
| Pages `pages` | repeatable rows | required | — | at least 1 | — | — | `createSaleBoard` body |
| Name `pages[].name` | text field | required | — | — | — | — | `createSaleBoard` body |
| Sort order `pages[].sortOrder` | number field | required | — | — | — | — | `createSaleBoard` body |
| Tiles `pages[].tiles` | repeatable rows | required | — | — | — | — | `createSaleBoard` body |
| Position `pages[].tiles[].position` | number field | required | — | — | — | — | `createSaleBoard` body |
| Kind `pages[].tiles[].kind` | radio group | required | — | Product · Category · Action · Spacer | — | — | `createSaleBoard` body |
| Variant `pages[].tiles[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `createSaleBoard` body |
| Label `pages[].tiles[].label` | text field | optional | — | — | — | — | `createSaleBoard` body |
| Colour `pages[].tiles[].colour` | text field | optional | — | — | — | — | `createSaleBoard` body |
| Image `pages[].tiles[].imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createSaleBoard` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createSaleBoard` body |

Errors to draw in the form: 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Menu**: Arrives with the menu chosen on BO-045 (menu and outlet in the header: "Dinner Menu - Oasis Bistro - draft v8"); no outlet id field, no date picker. *(source: screens/P08-venue-back-office.yaml#BO-109 / DI-326)*
- **Sections and item order**: Drag to reorder sections and items; an item sits in exactly one section; an "Unassigned items" tray holds items not yet placed. Hidden sections stay in the list with a Hidden tag. *(source: contracts/satellite/fnb.yaml#setMenuSections / contracts/satellite/fnb.yaml#/components/schemas/MenuItem)*
- **Grid**: Columns by rows (4 x 4 default) per page with pages; drag from the tray onto a cell; snap on. *(source: screens/P08-venue-back-office.yaml#BO-109 / DI-157)*
- **Button properties**: Display name (defaults to the item name), colour, show image on or off, size (1x1, 2x1, 2x2) for fast sellers, and "prompt modifiers" for items with required choices. Tile kinds are an item, a category jump, an action (system function) or a spacer. *(source: DI-326 / DI-157 / contracts/spine/tenancy.yaml#/components/schemas/SaleBoard)*
- **Layout scope**: One layout per outlet; a till may override it (Workstation.saleBoard), and the editor says which tills use an override. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Outputs: what the screen shows and produces

**Shown**

**Menu sections** (detail panel, from `getMenu`): The canvas: sections and items dragged into order. The order saved by Save menu sections is the till's order.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Sections | list or chips (count when long) | — |
| Availability | grouped details | When this menu is in force. Absent means always. |

**Till grid** (detail panel, from `listSaleBoards`): **Per outlet, with a till override (decided 2 October 2026 by Chinmay, DEC-183; CHG-CSP-006):** the outlet's `saleBoardId` is the layout every till of the outlet loads unless a till overrides it (`Workstation.saleBoardSource`). Only F&B functions can be placed (DEC-184 default).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save menu sections (primary button) | `setMenuSections` PUT `/menus/{menuId}/sections` | inline | Menu | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save sale board (secondary button) | `updateSaleBoard` PUT `/sale-boards/{saleBoardId}` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| New sale board (secondary button) | `createSaleBoard` POST `/sale-boards` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Till preview**: Renders the tiles as POS-021 does - name, price in the venue currency, image when on, an "86" overlay on unavailable items - so the manager sees the till, not a form. *(source: DI-326 / screens/P08-venue-back-office.yaml#BO-109)*
- **Draft changes**: A running list ("added Wagyu Slider to Burgers; moved Kids Menu to hidden") with a count, so the manager knows what Publish will carry. *(source: screens/P08-venue-back-office.yaml#BO-109 / F31 step 1)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save draft**: Saves sections and item order (and the grid). The live menu keeps selling. A 412 conflict says who changed the menu and offers reload while keeping the user's arrangement visible. *(source: contracts/satellite/fnb.yaml#setMenuSections / F31 step 1)*
- **Save layout**: The layout save replaces the whole board - every page and tile; anything not on the canvas is removed. Changes reach tills with the next catalogue bundle, not immediately, and the success message says so. *(source: contracts/spine/tenancy.yaml#updateSaleBoard)*
- **Publish**: Hands over to the publish gate of BO-045 (what goes live, where, from when); the builder has no publish path of its own. *(source: contracts/satellite/fnb.yaml#publishMenu / F31 step 5)*

**Data it reads**: `getMenu` (onLoad, The menu opened from BO-045, its sections and items); `listSaleBoards` (onLoad, The outlet's till layout and any till overrides)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The menu pos layout list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the menu pos layout untouched. |
| Empty, first run (`?state=emptyFirstRun`) | The picked menu has no sections yet: the canvas opens empty and Save menu sections (`setMenuSections`) saves the first arrangement; a new outlet layout starts with New sale board. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: the canvas does not filter. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getMenu` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setMenuSections`; `WORKSTATION_CONFIGURE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tile references an unknown or unsellable variant |

#### Edge cases to draw

- **The user may edit menus but not workstation layouts**: The layout save needs a different permission from the section save; the grid shows read-only with "You can arrange sections; ask a POS administrator to change the till layout". *(source: contracts/spine/tenancy.yaml#updateSaleBoard / contracts/satellite/fnb.yaml#setMenuSections)*
- **A page left empty**: A board needs at least one page; deleting the last page is not offered. *(source: contracts/spine/tenancy.yaml#/components/schemas/SaleBoard)*
- **An item is 86'd while arranging**: Its tile shows the 86 overlay in the preview; arranging is not blocked. *(source: R110 / screens/P08-venue-back-office.yaml#BO-109)*

#### Consistency with other screens

- Match `BO-045`: Same menu and same draft; BO-109 is opened from it and returns to it.
- Match `POS-021`: Tile anatomy, sizes and section tabs must match the till exactly.
- Match `BO-124`: The ticketing sale-board designer (BO-124, BO-125) and this builder should share one designer component (DI-157 scopes all three).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
menu: Dinner Menu - Oasis Bistro - draft v8
sections:
- Starters 12
- Grill & Mains 16
- Burgers 18
- Sides 14
- Desserts 11
- Beverages 28
- Kids Menu (hidden)
tiles:
- label: Classic Beef Burger
  price: AED 46.00
  size: 2x1
  colour: '#0D6EFD'
- label: Chicken Machboos
  price: AED 58.00
  size: 1x1
- label: Karak Chai
  price: AED 12.00
  size: 1x1
- label: Wagyu Slider
  price: AED 88.00
  overlay: '86'
unassigned:
- Truffle Fries
- Luqaimat
- Mango Lassi
```

#### Permissions

- `setMenuSections` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff
- `createSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff
- `getMenu` → `PRODUCT_VIEW` (read) · staff
- `listSaleBoards` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getMenu` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setMenuSections`; `WORKSTATION_CONFIGURE` for …

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.22 | The system should provide the option to split menu items by sections for specific locations of the outlet. For example: one menu section going to kitchen and the other going to the drink bar. The … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.3 | The system should provide the option to remotely configure visibility and placement of available menu items available for sale on POS screen. The function should be limited to only users accounts … | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 4.9.4 | The system should be able to design a menu button layout page can be copied and re-used in multiple locations if the need arises | Bundles and Promotions | CONTRACTED | `setMenuSections` |
| 2.1.9 | The system should allow the interface of POS solution to be configurable: - Configurable hot keys on touch screen to link to a specific action. - Configuration of various sales screens (buttons … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.12.19 | Order Sales 1) The POS home page displays available products by category, for the current POS. 2) Staff can click a specific product to add it to the cart; quantity can be adjusted 3) The system … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.1.32 | System shall allow guests to purchase food and beverage items through self-service kiosks. The kiosk shall support menu browsing, product customization, combo meals, upsell recommendations … | Ticketing Sales | CONTRACTED | data `Menu` |
| 2.1.33 | System shall allow guests to purchase retail merchandise through self-service kiosks. The kiosk shall support product browsing, inventory validation, variant selection (size, color, style) … | Ticketing Sales | CONTRACTED | data `Menu` |
| 4.6.13 | The system should have a interface for kiosks where the guest should be able to place order via the self service option all the way till completing payments. | Bundles and Promotions | CONTRACTED | data `Menu` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Menu Builder defines the front-end POS layout per outlet — categories, item tiles (image, name, price) and configurable button sizes for fast-selling items. Agreed the current (reference) layout is a reference only and the UI/UX can be improved. *(agreed · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-326)*
- Drag-and-drop POS "sales board" designer placing products and system functions (ticket list, reservation list, transaction list, media lookup) as buttons with custom fonts and colours. Allam: the old interface is NOT a design reference — functional concept only. *(agreed · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-157)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-109` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 2.dc.html`
- Client design-board frames: `FnB Board 2.dc.html#fnb-2b`
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (49), with its required mark, default, format and its error state (400, 403, 404, 412).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-109?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save menu sections, Save sale board, New sale board.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-110` Recipe & BOM Management

**Recipe & BOM Management — from the client design board, 20 August (merged into BO-111 Ingredient Substitution, Allergen & Nutrition).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRecipes` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/recipe-bom-management` |

**What the spec says about it.** **Merged into BO-111** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). A dish's recipe, substitutions and allergens are one editing job (design-note correction fnb-retail BO-110). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-111, and nothing on it is built separately. **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Food, Beverage & Retail process.** One dish's recipe and bill of materials: the ingredient lines (inventory item, quantity, unit, optional), the yield, and the computed plate cost, with the selling price and food-cost percentage beside it. The recipe is what depletes stock when the dish sells and what makes it unavailable when an ingredient runs out. The one thing to get right is that cost is computed, never typed, and saving re-checks the dish's allergens.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Recipe yield allows 0 (minimum 0) although cost is divided by yield; waste % per line and recipe versions (both on FNB-2F) have no field or read; there is no way to remove a recipe. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The "Save recipe" modal collects costPerPortion. (CHG-SBO-008); Plumbing - "Menu item id" text field and a table "Every recipe" with menuItemId and the ingredients array as columns; two search fields. (CHG-SBO-008); The client frame for this screen (fnb-2f, "Recipe & BOM Costing") is mapped to BO-137; BO-110 has no board frame. (CHG-SBO-008); BO-110 and BO-111 both save the recipe (setRecipe) as separate screens under Sell. (CHG-SBO-021).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is a sub-recipe (Burger Sauce SUB-0071) modelled - as an inventory item produced by a production run and used as an ingredient line?** → Drawn default stands (answer: "Default / recommended accepted"): Draw sub-recipes as ingredient lines with a "sub-recipe" tag that links to their own recipe. *(decided by Chinmay, 2026-10-02; DEC-044 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Dish**: A search by menu item name (with outlet), not a "Menu item id" text field; items without a recipe can be filtered ("No recipe"). *(source: contracts/satellite/fnb.yaml#listRecipes / DI-325)*
- **Ingredient line**: Inventory item by name and code (Beef Patty 150g, ITM-1042), quantity, unit from the item's units of measure and pack conversions, and an "optional" tick for garnish the guest can decline. At least one line. *(source: contracts/satellite/fnb.yaml#/components/schemas/Recipe / DI-343)*
- **Yield**: Portions produced by one execution of the recipe (1 for a plated dish, 40 for a batch of soup); must be above zero. *(source: contracts/satellite/fnb.yaml#/components/schemas/Recipe)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Plate cost**: Read-only, computed from each line at its current inventory cost (weighted average or FIFO per the venue) divided by the yield; each line shows its unit cost and line cost. Labelled "Computed". *(source: R125 / contracts/satellite/fnb.yaml#setRecipe / DI-344)*
- **Price, food cost and margin**: The dish's selling price, food cost % (plate cost over price before VAT) and margin in AED, as DI-329 asks; derived for display, not stored. *(source: DI-329 / screens/P08-venue-back-office.yaml#BO-110)*
- **Allergen verdict after save**: The verdict panel refreshes with trigger "after a recipe change"; an undeclared allergen is shown first. *(source: R241 / contracts/satellite/fnb.yaml#getAllergenVerification)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save recipe**: Saves the lines, recomputes plate cost, re-runs the allergen check and marks the dish stock-tracked. A 412 says someone else changed this recipe and offers reload. *(source: contracts/satellite/fnb.yaml#setRecipe / R241 / R125)*

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-111 while it opens. |
| Error (`?state=error`) | Could not open BO-111; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-111, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-111. |
| Permission denied (`?state=emptyNoAccess`) | As BO-111: shown when the caller lacks the access BO-111 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **First recipe for a dish**: Warn before saving that the dish becomes stock-tracked and can no longer be sold on a till while it is offline. *(source: contracts/satellite/fnb.yaml#setRecipe)*
- **An ingredient has no cost yet (never received)**: The line cost reads "No cost yet" and the plate cost is marked incomplete rather than understated. *(source: designer default)*
- **An ingredient's purchase cost changes**: Plate cost updates on its own (recomputed when an ingredient cost changes); no re-save needed. *(source: contracts/satellite/fnb.yaml#/components/schemas/Recipe)*

#### Consistency with other screens

- Match `BO-111`: Same dish header and the same verdict panel; propose the two as tabs of one dish editor (see corrections).
- Match `BO-137`: Theoretical consumption comes from these lines; units must be the same.
- Match `BO-045`: The "No recipe" flag on a menu item links here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
dish: Classic Beef Burger (Oasis Bistro) - price AED 46.00
yield: 1 portion
lines:
- item: Beef Patty 150g (ITM-1042)
  qty: 1
  unit: pc
  unitCost: AED 6.40
- item: Brioche Bun (ITM-2201)
  qty: 1
  unit: pc
  unitCost: AED 2.10
- item: Cheddar Slice (ITM-1188)
  qty: 1
  unit: pc
  unitCost: AED 1.35
- item: Burger Sauce (SUB-0071)
  qty: 25
  unit: g
  unitCost: AED 0.028
- item: Pickles (ITM-3110)
  qty: 15
  unit: g
  unitCost: AED 0.014
  optional: true
plateCost: AED 13.06
foodCost: 29.8% of AED 43.81 before VAT
```

#### Permissions

**A refused user sees:** As BO-111: shown when the caller lacks the access BO-111 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*
- Menu & Product Command Center tracks menus, active recipes and products, and flags products without mapped recipes or with unavailable ingredients. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-325)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-110` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-110?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-102`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-111` Ingredient Substitution, Allergen & Nutrition

**Ingredient Substitution, Allergen & Nutrition — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28755 (APP-SETUP-BO-111-REST) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setRecipe`, `updateMenu`, `setSubstitutionRules`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `menuId` (deepLink), `menuItemId` (deepLink), `recipeId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. An item opened from the menu. **Allergen verification … |
| Route | `/sell/ingredient-substitution-allergen-nutrition` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **One recipe screen per dish, two tabs: Recipe / Substitutions & allergens** (decided 2 October 2026, merge as proposed; CHG-SBO-021; DI-987, DI-474). BO-110 Recipe & BOM Management is merged in; this id is kept as the home because flows F31 and F93 run on it. **The recipeId listIngredientSubstitutes and setIngredientSubstitutes need is Recipe.id (readOnly, agreed with contracts in the ledger 4 October 2026); the selected recipe row carries it** (CHG-FXS-003)

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): "Save menu" (updateMenu: name, service period, active) has nothing to do with allergens and was attached by name (R254); re-verification is automatic after a …

**From the Food, Beverage & Retail process.** For one dish, what is actually in it against what its label claims: allergens derived from the recipe lines, the approved substitutions for that recipe and the modifier groups, plus nutrition. The server re-checks the claim automatically after every recipe, substitution or modifier change; the manager can re-check by hand. The one thing to get right is the dangerous direction - an allergen present in the dish and missing from the label - shown first and impossible to miss.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Two substitution models on one screen - setSubstitutionRules (SubstitutionRule, per recipe, allergens as lists, R125 (10)) and setIngredientSubstitutes (FnbIngredientSubstitute, from the 20 September workbook, allergens … (CHG-SBO-005)
- "Needs approval" default contradicts itself - setSubstitutionRules says it defaults true wherever the swap changes an allergen; SubstitutionRule.requiresApproval defaults false. (CHG-SBO-005)
- "Nutrition" is in the name but no operation writes nutrition; the Nutrition and Allergen (contains / may contain) schemas are referenced by nothing; MenuItem.allergens is a flat list, so "may contain" from a shared … (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Recipe fields as raw text fields (menuItemId, yield, ingredients, costPerPortion) and a "Save menu" (updateMenu - name, service period … (CHG-WIR-008); The "Last allergen verdict" note says no read exists; getAllergenVerification exists and names BO-111. (CHG-WIR-008); Pattern configEditor (form) and the transition to BO-045 labelled "The draft is scheduled for Monday rather than published now"; F31 step 3 … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who approves an allergen-changing substitution, and where? No approval operation is wired for it.** → Drawn default stands (answer: "Default / recommended accepted"): Draw "Needs approval - head chef" as a state on the rule with no approve button until decided. *(decided by Chinmay, 2026-10-02; DEC-045 / CHG-NOTE-004)*
- **Is nutrition (per-serving energy, fat, sugar, salt) in the first release?** → Drawn default stands (answer: "Default / recommended accepted"): Leave a Nutrition section drawn but marked "coming later". *(decided by Chinmay, 2026-10-02; DEC-046 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search ingredient substitution, allergen | search field | — | — | — | — | — | — |
| Search | text field | optional | — | — | — | Sends `?search=` to `listRecipes`. | `listRecipes` ?search |
| Dish | select field | — | — | — | — | Find a dish by name; never a typed menu item id. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Menu item | picker: choose a menu item | — | — | `listRecipes` ?menuItemId |

**Form: Save substitution rules** (modal, opened by *Save substitution rules*; *Save substitution rules* calls `setSubstitutionRules`, *Cancel* sends nothing)

**Collects what `setSubstitutionRules` sends before it is called.** Required: `rules`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rules `rules` | repeatable rows | required | — | — | — | — | `setSubstitutionRules` body |
| ID `rules[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setSubstitutionRules` body |
| Recipe `rules[].recipeId` | picker: choose a recipe | required | — | — | shows names, sends the id | The recipe the rule applies to (decided 28 September, audit R125 (10)). Not a menu item and not the whole venue: a swap that is safe in one dish is not safe in another. | `setSubstitutionRules` body |
| From ingredient `rules[].fromIngredientId` | picker: choose a from ingredient | required | — | — | shows names, sends the id | — | `setSubstitutionRules` body |
| To ingredient `rules[].toIngredientId` | picker: choose a to ingredient | required | — | — | shows names, sends the id | — | `setSubstitutionRules` body |
| Ratio `rules[].ratio` | number field | optional | 1 | — | — | Not always one to one. Fresh herbs to dried is roughly three to one, and a rule that assumes parity produces a dish nobody would serve. | `setSubstitutionRules` body |
| Allergens added `rules[].allergensAdded` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setSubstitutionRules` body |
| Allergens removed `rules[].allergensRemoved` | multi-select chips | optional | — | Gluten · Crustaceans · Eggs · Fish · Peanuts · Soybeans · Milk · Nuts · Celery · Mustard · Sesame · Sulphites … | — | — | `setSubstitutionRules` body |
| Conditions `rules[].conditions` | multi-select chips | optional | — | Out of stock · Seasonal · Guest request · Cost saving · Always | — | — | `setSubstitutionRules` body |
| Requires approval `rules[].requiresApproval` | toggle | optional | off | — | — | True where the swap changes an allergen. A chef may substitute freely within a claim; changing the claim is somebody else's decision. | `setSubstitutionRules` body |
| Is active `rules[].isActive` | toggle | optional | on | — | — | — | `setSubstitutionRules` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save recipe** (modal, opened by *Save recipe*; *Save recipe* calls `setRecipe`, *Cancel* sends nothing)

**Collects what `setRecipe` sends before it is called.** Required: `menuItemId`, `ingredients`. Optional: `yield`. **Cost per portion is computed and read-only** (R125 (9)); the dish is picked by name; ingredients are lines (item, quantity, unit). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Menu item `menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `setRecipe` body |
| Yield `yield` | number field | optional | — | min 0 | — | Portions produced by one execution. | `setRecipe` body |
| Ingredients `ingredients` | repeatable rows | required | — | at least 1 | — | — | `setRecipe` body |
| Inventory item `ingredients[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `setRecipe` body |
| Quantity `ingredients[].quantity` | number field | required | — | min 0 | — | — | `setRecipe` body |
| Unit `ingredients[].unit` | text field | required | — | — | — | — | `setRecipe` body |
| Is optional `ingredients[].isOptional` | toggle | optional | off | — | — | — | `setRecipe` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Dish**: Arrives from the menu (BO-045) or the recipe with the dish chosen; otherwise a dish search by name. No id fields. *(source: screens/P08-venue-back-office.yaml#BO-111 / F31 step 3)*
- **Substitution rule**: From ingredient, to ingredient, ratio (default 1; fresh to dried herbs is about 3 to 1), when it applies (Out of stock, Seasonal, Guest request, Cost saving, Always), active. A rule belongs to one recipe. *(source: contracts/satellite/fnb.yaml#/components/schemas/SubstitutionRule / R125)*
- **Needs approval**: Switched on and locked whenever the swap adds or removes an allergen ("a chef may substitute freely within a claim; changing the claim is somebody else's decision"). *(source: contracts/satellite/fnb.yaml#setSubstitutionRules)*
- **Declared allergens**: The 14 declarable allergens as chips (gluten, crustaceans, eggs, fish, peanuts, soybeans, milk, nuts, celery, mustard, sesame, sulphites, lupin, molluscs) in English and Arabic. *(source: contracts/satellite/fnb.yaml#/components/schemas/AllergenCode / R096)*

#### Outputs: what the screen shows and produces

**Shown**

**Show the substitution rules before they are replaced** (card list, from `listSubstitutionRules`)

| Shows | Format | Notes |
|---|---|---|
| Ratio | 1,234.5 | Not always one to one. Fresh herbs to dried is roughly three to one, and a rule that assumes parity produces a dish nobody would serve. |
| Requires approval | yes / no (icon or chip) | True where the swap changes an allergen. A chef may substitute freely within a claim; changing the claim is somebody else's decision. |
| Is active | yes / no (icon or chip) | — |

**Show the recipe's approved substitutions** (card list, from `listIngredientSubstitutes`)

| Shows | Format | Notes |
|---|---|---|
| Substitution ratio | 1,234.5 | — |
| Conditions json | text | — |
| Allergens added json | text | — |
| Allergens removed json | text | — |
| Requires approval | yes / no (icon or chip) | — |
| Is active | yes / no (icon or chip) | — |

**Last allergen verdict** (detail panel, from `getAllergenVerification`)

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Matches | yes / no (icon or chip) | — |
| Declared | list or chips (count when long) | — |
| Actual | list or chips (count when long) | — |
| Undeclared | list or chips (count when long) | Present in the dish and absent from the label. The dangerous direction, and the response leads with it. |
| Allergen | text | — |
| Via | chip: Ingredient, Substitution, Modifier, Shared equipment | — |
| Source ref | text | — |
| Over declared | list or chips (count when long) | Labelled and no longer present. Safe, and still worth fixing — a menu that over-declares teaches guests the labels are guesses. |
| Checked at | 1 Oct 2026, 14:30 | — |
| Trigger | chip: Manual, Recipe changed, Substitution changed, Modifier changed | What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241). |

**Recipes** (data table, from `listRecipes`): Selecting a row sets the recipeId (Recipe.id, agreed field) for the substitutes and substitution rules.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The recipe's own id (4 October 2026, CHG-FXC-003; the Sprint 1-2 judging found no operation returned one, so `listIngredientSubstitutes` … |
| Menu item | the name it points at, never the id | — |
| Yield | 1,234.5 | Portions produced by one execution. |
| Cost per portion | AED 1,234.50 | Computed, never entered (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided … |

**The selected recipe** (detail panel, from `listRecipes`): Ingredients are drawn as lines (item, quantity, unit, cost), not one column.

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Yield | 1,234.5 | Portions produced by one execution. |
| Ingredients | list or chips (count when long) | — |
| Cost per portion | AED 1,234.50 | Computed, never entered (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided … |

**Last allergen verdict** (detail panel, from `verifyAllergens`): **Shows the last automatic verdict** — `matches`, `undeclared` (with `via` and `sourceRef`, shown first), `overDeclared` — from the check the server runs after every recipe, substitution or modifier change, with when it ran (decided 28 September, audit R241). **The contract records the verdict but exposes no read of it yet**, so until one exists this panel shows the result of the latest manual …

| Shows | Format | Notes |
|---|---|---|
| Menu item | the name it points at, never the id | — |
| Matches | yes / no (icon or chip) | — |
| Declared | list or chips (count when long) | — |
| Actual | list or chips (count when long) | — |
| Undeclared | list or chips (count when long) | Present in the dish and absent from the label. The dangerous direction, and the response leads with it. |
| Allergen | text | — |
| Via | chip: Ingredient, Substitution, Modifier, Shared equipment | — |
| Source ref | text | — |
| Over declared | list or chips (count when long) | Labelled and no longer present. Safe, and still worth fixing — a menu that over-declares teaches guests the labels are guesses. |
| Checked at | 1 Oct 2026, 14:30 | — |
| Trigger | chip: Manual, Recipe changed, Substitution changed, Modifier changed | What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save recipe (primary button) | `setRecipe` PUT `/recipes` | Recipe | Recipe | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save substitution rules (secondary button) | `setSubstitutionRules` PUT `/substitution-rules` | inline | SubstitutionRule[] | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Re-check allergens (manual) (secondary button) | `verifyAllergens` POST `/menu-items/{menuItemId}/verify-allergens` | — | AllergenVerdict | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Allergen verdict**: Undeclared first (danger), each with its route - ingredient, substitution, modifier or shared equipment - and the line it came from; over-declared second (amber); "Matches the label" in neutral when clean; when it ran and why ("after a substitution change", "manual re-check"). *(source: R241 / contracts/satellite/fnb.yaml#/components/schemas/AllergenVerdict)*
- **Allergens by ingredient line**: A table of recipe lines with the allergens each brings and a "Changed" tag on a line whose allergens changed since the last check (FNB-2L). *(source: screens/P08-venue-back-office.yaml#BO-111)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save substitutions**: Saves the recipe's whole substitution list and re-runs the check for every dish whose recipe the rules touch; the verdict panel refreshes. A rule pointing at a recipe that no longer exists is refused. *(source: contracts/satellite/fnb.yaml#setSubstitutionRules / R241)*
- **Re-check allergens**: Manual re-check; same panel, trigger "manual". *(source: R241 / contracts/satellite/fnb.yaml#verifyAllergens)*
- **Fix the label**: Takes the user to the dish on the menu to update its declared allergens (the claim is part of the menu item); then the next publish carries it. *(source: contracts/satellite/fnb.yaml#/components/schemas/MenuItem / contracts/satellite/fnb.yaml#setMenuSections)*

**Data it reads**: `getAllergenVerification` (onLoad, The last automatic allergen verdict for the dish); `listRecipes` (onLoad, List recipes); `listIngredientSubstitutes` (onLoad, Show the recipe's approved substitutions); `listSubstitutionRules` (onLoad, Show the substitution rules before they are replaced)

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-045` Menu Management: *The draft is scheduled for Monday rather than published now*; carries `menuId`, `menuItemId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved ingredient substitution allergen. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ingredient substitution allergen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ingredient substitution allergen configured. The form opens empty and `setRecipe` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getAllergenVerification` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setRecipe`, `setSubstitutionRules`, `setIngredientSubstitutes`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **No check has run yet for this dish**: "Not checked yet" with a Re-check button, never an empty or green panel. *(source: contracts/satellite/fnb.yaml#getAllergenVerification)*
- **A supplier change introduces an allergen into a sub-recipe**: Every dish using it shows Undeclared, and the screen says how many dishes and menus are affected so the menus can be republished (FNB-2L "Dishes affected 18, menus to republish 6"). *(source: screens/P08-venue-back-office.yaml#BO-111)*
- **An allergen-changing substitution is used at the till for a guest request**: It is offered only if approved; otherwise it does not appear as a till option. *(source: contracts/satellite/fnb.yaml#/components/schemas/SubstitutionRule)*

#### Consistency with other screens

- Match `BO-045`: Same verdict panel and wording.
- Match `BO-110`: Same dish header; propose one dish editor with tabs.
- Match `POS-021`: Allergen chips and words match what the cashier and the guest see on the item.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
dish: Classic Beef Burger (PLU 100241)
verdict: Undeclared - soybeans, via substitution (Burger Sauce SUB-0071, new mayonnaise supplier 22 Oct 2026). Over-declared
  - none. Checked 14:02 GST after a substitution change.
rules:
- from: Brioche Bun
  to: Gluten-free Bun
  ratio: 1
  when: Guest request
  needsApproval: true
- from: Fresh Coriander
  to: Dried Coriander
  ratio: 0.33
  when: Out of stock
  needsApproval: false
declared:
- gluten
- eggs
- milk
- mustard
- sulphites
```

#### Permissions

- `setRecipe` → `PRODUCT_CONFIGURE` (configure) · staff
- `setSubstitutionRules` → `PRODUCT_CONFIGURE` (configure) · staff
- `verifyAllergens` → `PRODUCT_VIEW` (read) · staff
- `setIngredientSubstitutes` → `PRODUCT_CONFIGURE` (configure) · staff
- `getAllergenVerification` → `PRODUCT_VIEW` (read) · staff
- `listRecipes` → `PRODUCT_VIEW` (read) · staff
- `listIngredientSubstitutes` → `PRODUCT_VIEW` (read) · staff
- `listSubstitutionRules` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getAllergenVerification` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `setRecipe`, `setSubstitutionRules`, `setIngredientSubstitutes`.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.7.6 | The system should have the ability to add or remove ingredients from a recipe product in a user friendly top-down approach. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.1 | The system should have the ability to add and remove multiple ingredients on one type of recipe order, while there are other recipe products on the same order without any modifications. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.4 | Create and manage recipes linked to menu items including ingredients, quantities, portions and preparation instructions. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 4.8.6 | Automatically calculate recipe costs based on ingredient costs and quantities. | Bundles and Promotions | CONTRACTED | `setRecipe` |
| 10.1.2 | The system should be able to sync all the recipes from the inventory management on real-time or timed intervals, to be able to display products and menu buttons. | Games & F&B Integration | CONTRACTED | `setRecipe` |
| 10.1.3 | The system should be able to sync all the recipe orders to manage and reflect on inventory and order management reports and further use this data for re-order levels. | Games & F&B Integration | CONTRACTED | `setRecipe` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-111` · status **notStarted** · provenance generated · **Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/FnB Board 2.dc.html`
- Drawn by: Claude Design F&B pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2f`, `FnB Board 2.dc.html#fnb-2l`
- Flow F31 *A menu is drafted, scheduled and rolled back*, step 3: An item's recipe changed, so its allergens are re-verified. → **A substituted ingredient changes the allergen claim.** BL-127 built allergens without linking substitution, and `verifyAllergens` is the one remaining gap this step names.
- Flow F93 *A recipe changes and its allergen claim is re-verified*, step 1: Ingredient Substitution, Allergen & Nutrition. → **Drawn by the client as FNB-2L.**
- Flow F93 branch at step 1 (medium): when A step is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` decides — the journey is shorter, not broken.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 404, 412).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-111?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save recipe, Save substitution rules, Re-check allergens (manual).
- [ ] Every transition is wired: `BO-102`, `BO-045`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-112` Production Planning & Production Sheets

**Production Planning & Production Sheets — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #28765 (APP-SETUP-BO-112) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`planProductionRun`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `planId` (navigation), `runId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/production-planning-production-sheets` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **One Production screen, three tabs: Plan / Commissary / Batches** (decided 2 October 2026, merge as proposed; CHG-SBO-021; DI-987, DI-671). BO-113 Central Kitchen & Commissary and BO-138 Production Execution & Batch are merged in; consumption stays with stock (BO-137). **The commissary is an outlet that produces for others** (DEC-186, DEC-188): a producing outlet's runs are sent to the outlets they serve with Send to outlets. **Plans are listed with listProductionPlans (agreed, ledger) 4 October 2026; a draft is built only by the Build plan action** (CHG-FXS-003)

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-011): No read of production plans (list or get).

**From the Food, Beverage & Retail process.** Tomorrow's prep list: a plan built from the demand forecast through the recipes into quantities per item and per station, edited by the chef, then released into production runs grouped by station - one printable prep sheet per station (FNB-2M). The client asked that production planning aggregate recipe requirements to forecast prepared quantities. The one thing to get right is that a plan is a draft until released, and the suggested quantity stays visible beside the planned one.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read of plans exists (no list or get of production plans). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Board frame mapped to Retail Board 2 ret-2e ("Catalog Builder & Store Assortment"); the client's frame for this screen is FnB Board 2 … (CHG-SBO-008); buildProductionPlan and releaseProductionPlan are declared on BO-136, not here; F85 step 1 lands planning on BO-136. (CHG-WIR-008); The form exposes id, recipeId, producingOutletId, forOutletIds, status, actualQuantity and varianceReason as text fields. (CHG-SBO-008); The transition to BO-009 (Pricing Rules) cites flow F78 step 3 to 4, but F78 has no BO-112 step. (CHG-WIR-009); Production is split over BO-112, BO-113, BO-136, BO-137 and BO-138 with the same operations repeated (planProductionRun on three … (CHG-SBO-021).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the printed prep sheet a browser print of the station view, or does it need a print operation and template?** → Prep sheets print from a print template, to kitchen printers and the browser. *(decided by Chinmay, 2026-10-02; DEC-185 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Planned · In progress · Completed · Cancelled | `listProductionRuns` ?status |
| Location kind | segmented control | — | Outlet · Commissary | `listProductionRuns` ?locationKind |
| From | date picker | — | — | `listProductionRuns` ?from |
| For date | date picker | — | — | `listProductionPlans` ?forDate |
| Status | text field | — | — | `listProductionPlans` ?status |

**Form: Build plan** (modal, opened by *Build plan*; *Build plan* calls `buildProductionPlan`, *Cancel* sends nothing)

**Collects what `buildProductionPlan` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `buildProductionPlan` body |
| Outlet `outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | — | `buildProductionPlan` body |
| For date `forDate` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | The trading day this prep list is for, in the Region's time zone. | `buildProductionPlan` body |
| Status `status` | radio group | required | — | Draft · Released · Superseded · Cancelled | — | — | `buildProductionPlan` body |
| Based on suggestion `basedOnSuggestionId` | picker: choose a based on suggestion | optional | — | — | shows names, sends the id | The forecast it started from. Kept so plan-against-forecast can be compared later — which is the label `recordSuggestionOutcome` needs. | `buildProductionPlan` body |
| Lines `lines` | repeatable rows | required | — | — | — | — | `buildProductionPlan` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `buildProductionPlan` body |
| Suggested quantity `lines[].suggestedQuantity` | number field | optional | — | — | — | — | `buildProductionPlan` body |
| Planned quantity `lines[].plannedQuantity` | number field | required | — | — | — | — | `buildProductionPlan` body |
| UOM `lines[].uom` | text field | optional | — | — | — | — | `buildProductionPlan` body |
| Station `lines[].stationId` | picker: choose a station | optional | — | — | shows names, sends the id | — | `buildProductionPlan` body |

**Form: Plan production run** (modal, opened by *Plan production run*; *Plan production run* calls `planProductionRun`, *Cancel* sends nothing)

**Collects what `planProductionRun` sends before it is called.** Required: `recipeId`, `plannedQuantity`. Optional: `stationId`, `producingOutletId`, `forOutletIds`, `scheduledFor`. `id` is a client UUIDv7 generated silently, never asked. The recipe, producing outlet and the outlets it serves are pickers by name; `status` is the server's (planned); actual quantity and variance belong to completing the run (BO-138), not to planning. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Recipe `recipeId` | picker: choose a recipe | required | — | — | shows names, sends the id | — | `planProductionRun` body |
| Station `stationId` | picker: choose a station | optional | — | — | shows names, sends the id | The station whose prep list this run is on. Copied from the plan line on release, where runs are grouped by station (audit R125 (7)). | `planProductionRun` body |
| Producing outlet `producingOutletId` | picker: choose a producing outlet | optional | — | — | shows names, sends the id | — | `planProductionRun` body |
| For outlets `forOutletIds` | multi-picker: choose for outlets | optional | — | — | — | Where it goes. A central kitchen produces for outlets that did not make it. | `planProductionRun` body |
| Planned quantity `plannedQuantity` | number field | required | — | — | — | — | `planProductionRun` body |
| Actual quantity `actualQuantity` | number field | optional | — | — | — | BL-126. Theoretical against actual is the whole point of recording this. | `planProductionRun` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `planProductionRun` body |
| Status `status` | radio group | required | — | Planned · In progress · Completed · Cancelled | — | — | `planProductionRun` body |
| Variance reason `varianceReason` | text field | optional | — | — | — | — | `planProductionRun` body |

**Form: Print prep sheet** (modal, opened by *Print prep sheet*; *Print prep sheet* calls `printPrepSheet`, *Cancel* sends nothing)

**Collects what `printPrepSheet` sends before it is called.** Required: `target`. Optional: `stationIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target `target` | segmented control | required | — | Browser · Station printers | — | — | `printPrepSheet` body |
| Stations `stationIds` | multi-picker: choose stations | optional | — | — | — | Only these stations' parts. Empty means every station in the plan. | `printPrepSheet` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not released yet (`plan-not-released`); a draft plan prints only to the browser.

**Form: Complete production run** (modal, opened by *Complete production run*; *Complete production run* calls `completeProductionRun`, *Cancel* sends nothing)

**Collects what `completeProductionRun` sends before it is called.** Required: `actualQuantity`, `recordedAt`. Optional: `varianceReason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Actual quantity `actualQuantity` | number field | required | — | — | — | — | `completeProductionRun` body |
| Variance reason `varianceReason` | text field | optional | — | — | — | — | `completeProductionRun` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `completeProductionRun` body |

Errors to draw in the form: 409 The run is not `inProgress` (states/production-run.yaml). Names its current status.

**Form: Send to outlets** (modal, opened by *Send to outlets*; *Send to outlets* calls `createStockTransfer`, *Cancel* sends nothing)

**Collects what `createStockTransfer` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| From location `fromLocationId` | picker: choose a from location | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| To location `toLocationId` | picker: choose a to location | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createStockTransfer` body |
| Item `lines[].itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockTransfer` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `createStockTransfer` body |
| Unit `lines[].unit` | text field | optional | — | — | — | — | `createStockTransfer` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `createStockTransfer` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockTransfer` body |

Errors to draw in the form: 409 Insufficient stock at the source

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Kitchen and day**: Outlet (kitchen) picker and the trading day (default tomorrow), a date in the Region's time zone. *(source: contracts/satellite/fnb.yaml#/components/schemas/ProductionPlan)*
- **Plan line**: Item, suggested quantity (read-only, from the forecast), planned quantity (editable), unit, station. Editing planned does not overwrite suggested. *(source: contracts/satellite/fnb.yaml#buildProductionPlan)*
- **Direct run (outside a plan)**: Recipe by name, planned quantity with its unit, where it is made, which outlets it is for, when. No id, status, actual quantity or variance fields at planning time. *(source: contracts/satellite/fnb.yaml#planProductionRun)*

#### Outputs: what the screen shows and produces

**Shown**

**Production runs** (data table, from `listProductionRuns`)

| Shows | Format | Notes |
|---|---|---|
| Recipe | the name it points at, never the id | — |
| Producing outlet | the name it points at, never the id | — |
| For outlets | list or chips (count when long) | Where it goes. A central kitchen produces for outlets that did not make it. |
| Planned quantity | 1,234.5 | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, In progress, Completed, Cancelled | — |
| Actual quantity | 1,234.5 | BL-126. Theoretical against actual is the whole point of recording this. |

**The batch** (detail panel, from `getProductionRun`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Recipe | the name it points at, never the id | — |
| Production plan | the name it points at, never the id | The plan whose release created this run. Null for a run planned directly. |
| Station | the name it points at, never the id | The station whose prep list this run is on. Copied from the plan line on release, where runs are grouped by station (audit R125 (7)). |
| Producing outlet | the name it points at, never the id | — |
| For outlets | list or chips (count when long) | Where it goes. A central kitchen produces for outlets that did not make it. |
| Planned quantity | 1,234.5 | — |
| Actual quantity | 1,234.5 | BL-126. Theoretical against actual is the whole point of recording this. |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, In progress, Completed, Cancelled | — |
| Variance reason | text | — |

**Production plans** (data table, from `listProductionPlans`): Opening the screen lists plans; Build plan makes a new draft only when pressed, never on load.

| Shows | Format | Notes |
|---|---|---|
| For date | 1 Oct 2026 | The trading day this prep list is for, in the Region's time zone. |
| Status | chip: Draft, Released, Superseded, Cancelled | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | `releaseProductionPlan` POST `/production-plans/{planId}/release` | — | ProductionPlan | — | — |
| Plan production run (primary button) | `planProductionRun` POST `/production-runs` | ProductionRun | ProductionRun | — | opens modal first |
| Build plan (secondary button) | `buildProductionPlan` POST `/production-plans` | ProductionPlan | ProductionPlan | — | opens modal first |
| Release plan (secondary button) | `releaseProductionPlan` POST `/production-plans/{planId}/release` | — | ProductionPlan | — | — |
| Print prep sheet (secondary button) | `printPrepSheet` POST `/production-plans/{planId}/prep-sheet` | inline | PrepSheet | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not released yet (`plan-not-released`); a draft plan prints only to the browser. | opens modal first; produces a document or message: Print a production plan's prep sheet |
| Complete production run (secondary button) | `completeProductionRun` POST `/production-runs/{runId}/complete` | inline | ProductionRun | 409 The run is not `inProgress` (states/production-run.yaml). Names its current status. | opens modal first |
| Send to outlets (secondary button) | `createStockTransfer` POST `/stock-transfers` | CreateStockTransferRequest | StockTransfer | 409 Insufficient stock at the source | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Plan grid**: Grouped by station (Grill, Cold, Pastry) with forecast covers in the header, on-hand beside to-make, and start times; total prep hours when known. *(source: screens/P08-venue-back-office.yaml#BO-112 / R125)*
- **Forecast badge**: The suggestion's maturity stage and basis in plain words ("Baseline from last 4 weeks - starting") and its explanation; never a confidence number for a rule-based answer. *(source: contracts/satellite/ai.yaml#requestSuggestion)*
- **Prep sheet**: One printable sheet per station for the day, listing items, quantities and start times (what releasing produces). Printed from a print template, to the kitchen printer or the browser. *(source: R125 / screens/P08-venue-back-office.yaml#BO-112 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Build plan**: Creates a draft plan from the forecast for the chosen day and kitchen; nothing is produced or issued. *(source: contracts/satellite/fnb.yaml#buildProductionPlan)*
- **Release plan**: Confirmation states "11 runs on 3 stations for Mon 2 Nov"; on success the plan reads Released and shows its runs. Ingredients leave stock only when each run starts. *(source: contracts/satellite/fnb.yaml#releaseProductionPlan / R125)*
- **Plan a run**: Creates a single planned run outside a plan (a central kitchen batch for several outlets). *(source: contracts/satellite/fnb.yaml#planProductionRun)*

**Data it reads**: `listProductionRuns` (onLoad, What is being made); `listProductionPlans` (onLoad, The production plans by date and status, to reopen one …)

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-137` Recipe Consumption & Theoretical Inventory: *Recipe Consumption & Theoretical Inventory*; carries `runId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved production planning production. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the production planning production untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No production planning production configured. The form opens empty and `planProductionRun` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProductionRuns` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `planProductionRun`, `buildProductionPlan`, `releaseProductionPlan`, `completeProductionRun` and 1 more. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient stock at the source; 409 The plan is not released yet (`plan-not-released`); a draft plan prints only to the browser.; 409 The run is not `inProgress` (states/production-run.yaml). Names its current status. |

#### Edge cases to draw

- **A setting the forecast needs is missing**: The forecast is refused and the message names the setting and the screen that sets it; the plan can still be built by hand. *(source: contracts/satellite/ai.yaml#requestSuggestion)*
- **Little or no sales history**: The forecast still answers from the baseline with stage "starting"; do not show an error. *(source: contracts/satellite/ai.yaml#requestSuggestion)*
- **Yesterday's draft never released**: It does not appear in today's prep list; it reads Draft for its own day and can be superseded or cancelled. *(source: contracts/satellite/fnb.yaml#releaseProductionPlan)*

#### Consistency with other screens

- Match `BO-113`: Commissary runs are the same runs viewed across outlets; same run card.
- Match `BO-138`: Released runs appear on the batch screen for execution; same item names and units.
- Match `BO-136`: Plan building and release currently sit on BO-136; see corrections.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kitchen: Oasis Bistro kitchen
day: Mon 2 Nov 2026 - forecast 418 covers (baseline, starting)
lines:
- item: Burger Sauce (SUB-0071)
  station: Cold
  suggested: 6.0 kg
  planned: 6.0 kg
  start: 06:30
- item: Marinated Chicken (SUB-0102)
  station: Grill
  suggested: 10.0 kg
  planned: 12.0 kg
  start: 07:30
- item: Luqaimat dough
  station: Pastry
  suggested: 8.0 kg
  planned: 8.0 kg
  start: 09:00
```

#### Permissions

- `planProductionRun` → `PRODUCT_CONFIGURE` (configure) · staff
- `buildProductionPlan` → `PRODUCT_CONFIGURE` (configure) · staff
- `releaseProductionPlan` → `PRODUCT_CONFIGURE` (configure) · staff
- `listProductionRuns` → `PRODUCT_VIEW` (read) · staff
- `printPrepSheet` → `PRODUCT_VIEW` (read) · staff
- `completeProductionRun` → `PRODUCT_CONFIGURE` (configure) · staff
- `createStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff
- `getProductionRun` → `PRODUCT_VIEW` (read) · staff
- `listProductionPlans` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProductionRuns` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `planProductionRun`, `buildProductionPlan`, `releaseProductionPlan`, `completeProductionRun` and 1 more.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.8.14 | AI forecasts production quantities using historical demand and attendance. | Bundles and Promotions | CONTRACTED | `buildProductionPlan` |
| 4.4.15 | Support stock transfers between stores and warehouses including approval workflows, shipment tracking, receiving confirmation, and audit logs. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.5 | The system should provide ability to transfer stocks to another store with a approval level | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.14 | Transfer inventory between locations with approval workflows. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 15.1.15 | In-Transit Inventory Tracking - System shall track inventory in transit. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.16 | Internal Transfers - System shall support internal transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.17 | Replenishment Management - System shall support warehouse replenishment. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.5.3 | Inter-Venue Transfers - System shall support inter-venue transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 4.6.36 | Compare theoretical recipe cost versus actual inventory consumption and wastage, highlighting variances and operational inefficiencies. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.7 | Manage recipe yields, shrinkage, wastage and final portions. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.12 | Plan kitchen production quantities based on expected demand. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| 4.8.13 | Manage batch preparation and production runs. | Bundles and Promotions | CONTRACTED | data `ProductionRun` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Recipe & BOM captures ingredient quantity, unit, cost (from purchase data), preparation time, yield, selling price and margin. Ingredient substitution uses an alternate ingredient automatically when the primary is out of stock; production planning aggregates recipe requirements to forecast prepared-item quantities. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-329)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-112` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2m`
- Flow F85 *Production is planned, costed and released*, step 1: F&B Global Settings & Controls. → **Drawn by the client as FNB-2M.** 3 operations on this step.
- Flow F85 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-112?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Plan production run, Build plan, Release plan, Print prep sheet, Complete production run, Send to outlets.
- [ ] Every transition is wired: `BO-102`, `BO-137`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
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

**18 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"buildProductionPlan": {"method":"POST","path":"/production-plans","contract":"fnb","summary":"Turn a forecast into a prep list","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductionPlan","responds":"ProductionPlan"},
"cancelPerformance": {"method":"POST","path":"/performances/{performanceId}/cancel","contract":"catalogue","summary":"Cancel a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceCancellationResult"},
"completeProductionRun": {"method":"POST","path":"/production-runs/{runId}/complete","contract":"fnb","summary":"Record what was actually made","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionRun"},
"createChannelCapacity": {"method":"POST","path":"/channel-capacities","contract":"catalogue","summary":"Create a channel capacity","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateEnvelopeRequest","responds":"ChannelCapacity"},
"createEvent": {"method":"POST","path":"/events","contract":"catalogue","summary":"Create an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateEventRequest","responds":"Event"},
"createPerformances": {"method":"POST","path":"/events/{eventId}/performances","contract":"catalogue","summary":"Create performances, singly or by schedule","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreatePerformancesRequest","responds":null},
"createSaleBoard": {"method":"POST","path":"/sale-boards","contract":"tenancy","summary":"Create a sale board","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SaleBoard","responds":"SaleBoard"},
"createStockTransfer": {"method":"POST","path":"/stock-transfers","contract":"inventory","summary":"Send stock to another location","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStockTransferRequest","responds":"StockTransfer"},
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"forceReleaseInventoryHold": {"method":"POST","path":"/inventory-holds/{inventoryHoldId}/force-release","contract":"catalogue","summary":"Reclaim a stranded inventory hold","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryHold"},
"getAllergenVerification": {"method":"GET","path":"/menu-items/{menuItemId}/allergen-verification","contract":"fnb","summary":"The last allergen verdict recorded for a dish","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AllergenVerdict"},
"getChannelAllocations": {"method":"GET","path":"/channel-capacities/{channelCapacityId}/channel-allocations","contract":"catalogue","summary":"Capacity allocated to each channel","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ChannelAllocationSet"},
"getEvent": {"method":"GET","path":"/events/{eventId}","contract":"catalogue","summary":"Read an event","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Event"},
"getLatestBundle": {"method":"GET","path":"/catalogue/bundles/latest","contract":"catalogue","summary":"Pull the current bundle for this workstation's venue","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"since","in":"query","required":null},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"CatalogueBundle"},
"getMenu": {"method":"GET","path":"/menus/{menuId}","contract":"fnb","summary":"Read a menu with sections and items","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Menu"},
"getPerformance": {"method":"GET","path":"/performances/{performanceId}","contract":"catalogue","summary":"Read a performance","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Performance"},
"getProductionRun": {"method":"GET","path":"/production-runs/{runId}","contract":"fnb","summary":"One run — its plan, its output, and the gap","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductionRun"},
"getSeatAvailability": {"method":"GET","path":"/performances/{performanceId}/seat-availability","contract":"seating","summary":"Seat status for a performance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"availableOnly","in":"query","required":null},{"name":"mode","in":"query","required":null}],"requestBody":null,"responds":"SeatAvailability"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listChannelCapacities": {"method":"GET","path":"/channel-capacities","contract":"catalogue","summary":"List channel capacities","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEvents": {"method":"GET","path":"/events","contract":"catalogue","summary":"List events","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIngredientSubstitutes": {"method":"GET","path":"/recipes/{recipeId}/substitutes","contract":"fnb","summary":"Approved substitutions for a recipe's ingredients","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"recipeId","in":"path","required":true},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInventoryHolds": {"method":"GET","path":"/inventory-holds","contract":"catalogue","summary":"List inventory holds","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channelCapacityId","in":"query","required":null},{"name":"holderWorkstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPerformances": {"method":"GET","path":"/events/{eventId}/performances","contract":"catalogue","summary":"List performances of an event","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"language","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductionPlans": {"method":"GET","path":"/production-plans","contract":"fnb","summary":"The production plans","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"forDate","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductionRuns": {"method":"GET","path":"/production-runs","contract":"fnb","summary":"What is being made, and what was","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationKind","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRecipes": {"method":"GET","path":"/recipes","contract":"fnb","summary":"List recipes","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":"menuItemId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSaleBoards": {"method":"GET","path":"/sale-boards","contract":"tenancy","summary":"List sale boards","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"SaleBoard"},
"listSubstitutionRules": {"method":"GET","path":"/substitution-rules","contract":"fnb","summary":"What may replace what, as saved","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listUpsellRules": {"method":"GET","path":"/upsell-rules","contract":"promotions","summary":"List upsell and cross-sell rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"placement","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaitlistEntries": {"method":"GET","path":"/waitlist-entries","contract":"catalogue","summary":"Who is waiting for capacity","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null}],"requestBody":null,"responds":"WaitlistEntry"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"offerWaitlistCapacity": {"method":"POST","path":"/waitlist-entries/{entryId}/offer","contract":"catalogue","summary":"Tell a waiting guest that capacity appeared","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WaitlistEntry"},
"planProductionRun": {"method":"POST","path":"/production-runs","contract":"fnb","summary":"Plan a batch, for one outlet or several","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductionRun","responds":"ProductionRun"},
"printPrepSheet": {"method":"POST","path":"/production-plans/{planId}/prep-sheet","contract":"fnb","summary":"Print a production plan's prep sheet","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PrepSheet"},
"publishBundle": {"method":"POST","path":"/catalogue/bundles","contract":"catalogue","summary":"Compute, sign and publish a catalogue bundle","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BundleSummary"},
"recommendSeats": {"method":"POST","path":"/performances/{performanceId}/seat-recommendations","contract":"seating","summary":"Recommend seats for a party","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRequest","responds":null},
"releaseProductionPlan": {"method":"POST","path":"/production-plans/{planId}/release","contract":"fnb","summary":"Make the plan real","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductionPlan"},
"relinquishChannelAllocation": {"method":"POST","path":"/channel-capacities/{channelCapacityId}/channel-allocations/release","contract":"catalogue","summary":"Return unsold channel allocation to the general pool","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelAllocationSet"},
"reportBundleApplied": {"method":"POST","path":"/catalogue/bundles/{version}/applied","contract":"catalogue","summary":"Report that a workstation applied a bundle","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setChannelAllocations": {"method":"PUT","path":"/channel-capacities/{channelCapacityId}/channel-allocations","contract":"catalogue","summary":"Allocate a channel capacity across sales channels","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelAllocationSet"},
"setIngredientSubstitutes": {"method":"PUT","path":"/recipes/{recipeId}/substitutes","contract":"fnb","summary":"Define approved substitutions","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"recipeId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"FnbIngredientSubstitute","responds":"FnbIngredientSubstitute"},
"setMenuSections": {"method":"PUT","path":"/menus/{menuId}/sections","contract":"fnb","summary":"Set menu sections and their item ordering","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Menu"},
"setOfflinePolicy": {"method":"PUT","path":"/offline-policy","contract":"tenancy","summary":"What a workstation may do with no network, and for how long","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OfflinePolicy","responds":"OfflinePolicy"},
"setPathClosure": {"method":"POST","path":"/venue-maps/{mapId}/paths/{pathId}/closure","contract":"venue-map","summary":"Close a route during works or an incident","permission":"VENUE_MAP_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PathClosureResult"},
"setRecipe": {"method":"PUT","path":"/recipes","contract":"fnb","summary":"Define a recipe for a menu item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"Recipe","responds":"Recipe"},
"setSubstitutionRules": {"method":"PUT","path":"/substitution-rules","contract":"fnb","summary":"What may replace what","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SubstitutionRule"},
"syncOrders": {"method":"POST","path":"/sync/orders","contract":"orders","summary":"Replay orders recorded offline","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderSyncResult"},
"updateChannelCapacity": {"method":"PATCH","path":"/channel-capacities/{channelCapacityId}","contract":"catalogue","summary":"Amend a channel capacity","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelCapacity"},
"updateEvent": {"method":"PATCH","path":"/events/{eventId}","contract":"catalogue","summary":"Amend an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Event"},
"updateOutlet": {"method":"PATCH","path":"/outlets/{outletId}","contract":"tenancy","summary":"Amend an outlet","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Outlet"},
"updatePerformance": {"method":"PATCH","path":"/performances/{performanceId}","contract":"catalogue","summary":"Amend a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Performance"},
"updateSaleBoard": {"method":"PUT","path":"/sale-boards/{saleBoardId}","contract":"tenancy","summary":"Update a sale board","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SaleBoard","responds":"SaleBoard"},
"verifyAllergens": {"method":"POST","path":"/menu-items/{menuItemId}/verify-allergens","contract":"fnb","summary":"Does this dish still match its claim?","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AllergenVerdict"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiRecommendationItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList","description":"One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).","required":["trackingId","rank"],"properties":{"trackingId":{"type":"string","format":"uuid","description":"Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."},"couponRef":{"type":"string","nullable":true,"description":"For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."},"rewardId":{"type":"string","format":"uuid","nullable":true,"description":"For `reward`, a marketing-crm loyalty reward the guest can redeem."},"challengeId":{"type":"string","format":"uuid","nullable":true,"description":"For `challenge`, a marketing-crm challenge the guest can join."},"kind":{"type":"string","enum":["upsell","crossSell","upgrade","bundle","addOn","membership","nextBestOffer","offer","reward","challenge"]},"rank":{"type":"integer","minimum":1},"priceRef":{"type":"string","nullable":true,"description":"The Pricing reference the channel resolves to a price. AI never computes a price."},"reasonTemplateKey":{"type":"string","nullable":true,"description":"The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."},"reasonText":{"type":"string","nullable":true,"description":"The rendered template in the session locale, where the channel shows reasons."},"confidenceBand":{"type":"string","enum":["high","medium","low"],"description":"Design 5.6: a band, never a bare percentage."},"score":{"type":"number","nullable":true,"description":"Normalised score. **Returned to staff callers only**; a guest response omits it."}}},
"AiRecommendationResult": {"type":"object","x-ticvai-persistence":"none — written as ai.rec_decision after the response","description":"The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.","required":["decisionId","mode","items","expiresAt"],"properties":{"decisionId":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"]},"items":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationItem"}},"expiresAt":{"type":"string","format":"date-time"}}},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AllergenVerdict": {"x-ticvai-persistence":"fnb.allergen_verdict","type":"object","description":"One allergen check of one dish (decided 28 September, audit R241). Written by the server on every automatic run and by `verifyAllergens` on a manual re-check; `getAllergenVerification` reads the latest.\n","required":["menuItemId","matches","checkedAt","trigger"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"matches":{"type":"boolean"},"declared":{"type":"array","items":{"type":"string"}},"actual":{"type":"array","items":{"type":"string"}},"undeclared":{"type":"array","x-ticvai-persistence-column":"jsonb","description":"**Present in the dish and absent from the label.** The dangerous direction, and the response leads with it.\n","items":{"type":"object","properties":{"allergen":{"type":"string"},"via":{"type":"string","enum":["ingredient","substitution","modifier","sharedEquipment"]},"sourceRef":{"type":"string"}}}},"overDeclared":{"type":"array","description":"Labelled and no longer present. **Safe, and still worth fixing** — a menu that over-declares teaches guests the labels are guesses.\n","items":{"type":"string"}},"checkedAt":{"type":"string","format":"date-time","readOnly":true},"trigger":{"type":"string","readOnly":true,"description":"What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241).","enum":["manual","recipeChanged","substitutionChanged","modifierChanged"]}}},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"CatalogueBundle": {"x-ticvai-persistence":"catalogue.published_bundle","type":"object","required":["version","venueId","isDelta","signature","signatureKeyId","contentHash","staleAfter","payload"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"isDelta":{"type":"boolean"},"baseVersion":{"type":"string","nullable":true,"description":"Present when `isDelta`. The version this delta applies to."},"signature":{"type":"string","description":"Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never traded against.\n"},"signatureKeyId":{"type":"string"},"contentHash":{"type":"string"},"staleAfter":{"type":"string","format":"date-time"},"payload":{"type":"object","description":"Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's sale boards. Shape is versioned with the bundle format, not with this API.\n","additionalProperties":true,"properties":{"saleBoards":{"type":"array","description":"**The venue's sale boards as `tenancy.listSaleBoards` returns them**, read from `platform.sale_board` when the bundle is snapshotted (decided 28 September, audit R129 (4)). A board changed by `updateSaleBoard` reaches terminals here, with the next bundle, and never mid-transaction.\n","items":{"type":"object","additionalProperties":true}}}}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelAllocation": {"x-ticvai-persistence":"catalogue.channel_allocation","type":"object","required":["channel","allocatedUnits"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"channel":{"$ref":"#/components/schemas/Channel"},"allocatedUnits":{"type":"integer","minimum":0},"soldUnits":{"type":"integer","readOnly":true},"leasedUnits":{"type":"integer","readOnly":true,"description":"Held by terminals on this channel but not yet sold."},"remainingUnits":{"type":"integer","readOnly":true},"releaseAt":{"type":"string","format":"date-time","nullable":true,"description":"Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it.\n"},"salesChannelId":{"type":"string","format":"uuid","nullable":true,"description":"The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3)."},"allocationType":{"type":"string","enum":["sharedPool","dedicated","percentage","dynamic"],"default":"dedicated","description":"How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row."},"minimumUnits":{"type":"integer","nullable":true,"minimum":0},"maximumUnits":{"type":"integer","nullable":true,"minimum":0},"replenishmentRule":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`."},"waitlistBehavior":{"type":"string","enum":["none","joinWaitlist","notifyOnRelease"],"default":"none"},"releaseThresholdUnits":{"type":"integer","nullable":true,"minimum":0},"releaseHoursBeforeEvent":{"type":"integer","nullable":true,"minimum":0,"description":"Alternative to `releaseAt`, relative to the performance start."},"contractualUnits":{"type":"integer","nullable":true,"minimum":0,"description":"Units a partner agreement guarantees; rebalancing never goes below it."},"minimumGuaranteedUnits":{"type":"integer","nullable":true,"minimum":0},"isFrozen":{"type":"boolean","default":false,"description":"Excluded from rebalancing."}}},
"ChannelAllocationSet": {"x-ticvai-persistence":"none — projection","type":"object","required":["channelCapacityId","capacity","allocations","generalPoolUnits"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"capacity":{"type":"integer"},"allocations":{"type":"array","items":{"$ref":"#/components/schemas/ChannelAllocation"}},"generalPoolUnits":{"type":"integer","description":"Unallocated remainder. Any channel may draw from it once its own allocation is exhausted.\n"},"totalSold":{"type":"integer"},"totalRemaining":{"type":"integer"}}},
"ChannelCapacity": {"x-ticvai-persistence":"catalogue.channel_capacity","type":"object","required":["id","performanceId","capacity","sold","leased","remaining","isSeated"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string"},"seatCategoryId":{"type":"string","format":"uuid","nullable":true},"oversellAllowance":{"type":"integer","default":0,"description":"BL-046, 1.3.13. **The guard existed in one direction** — an envelope could be raised freely and refused reduction below what had sold.\n**Free events oversell deliberately because no-show rates are known.** An allowance on the envelope rather than an admission policy, because **the gate must still refuse when actual capacity is reached** — overselling is a sales decision and admission is a safety one, and they must not share a number.\n"},"oversellBasis":{"type":"string","nullable":true,"enum":["fixedCount","historicNoShowRate","percentage"]},"capacity":{"type":"integer","minimum":0},"sold":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units sold. **Maintained on write** (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by consumption a workstation reports on `renewInventoryHold` or `relinquishInventoryHold`, lowered when a refund or cancellation returns the units. Always `capacity + oversellAllowance = sold + leased + remaining`.\n"},"leased":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023)."},"remaining":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"What can still be held. **Decremented at the hold with a guarded statement** (`remaining >= n`) under the row lock, never at the sale, so two buyers cannot both take the last unit (SD-023, 29 September).\n"},"hasChannelAllocations":{"type":"boolean","description":"True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity.\n"},"isSeated":{"type":"boolean","description":"Seated envelopes cannot be leased and are blocked offline. A seat map is not a count.\n"}}},
"CreateEnvelopeRequest": {"type":"object","description":"The body of `createChannelCapacity`. **Named before the 26 August rename** (envelope to `ChannelCapacity`); the name stays because generated code is keyed on it.","required":["performanceId","name","capacity"],"properties":{"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"seatCategoryId":{"type":"string","format":"uuid"},"capacity":{"type":"integer","minimum":0}}},
"CreateEventRequest": {"type":"object","required":["code","name","venueId"],"properties":{"code":{"type":"string","maxLength":64,"x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"parentEventId":{"type":"string","format":"uuid"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency. For a guest-channel card or wallet payment on an order with a `chargeCurrency`, the server sets it from the order (CHG-FIN-001)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePerformancesRequest": {"type":"object","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17)."},"format":{"type":"string","nullable":true,"maxLength":40,"description":"As `Performance.format` (decided 29 September, rev 3 REV3-17)."},"recurrence":{"type":"object","description":"Generate a series rather than a single performance. **Read in the region's time zone**: the Region owns the zone and every venue inherits it without override (tenancy), so `daysOfWeek` are the region's calendar days and `until` is compared on the region's clock.\n","properties":{"intervalMinutes":{"type":"integer","minimum":1},"until":{"type":"string","format":"date-time"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}}}}}},
"CreateStockTransferRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","fromLocationId","toLocationId","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"}}}},"note":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"Event": {"x-ticvai-persistence":"catalogue.event","type":"object","required":["id","code","name","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentEventId":{"type":"string","format":"uuid","nullable":true,"description":"For grouped events."},"performanceCount":{"type":"integer","readOnly":true,"description":"How many performances the event has. Counted by the server; never sent by a client."},"isActive":{"type":"boolean"},"lifecycleState":{"type":"string","readOnly":true,"enum":["draft","planned","onSale","live","closed","cancelled","archived"],"description":"**Where the event is in its lifecycle** (4 October 2026, CHG-FXC-003; catalogue.event had nowhere to keep it). Written only by `setEventLifecycleState`, which checks the transition; `createEvent` and `cloneEvent` create an event in `draft`. `isActive` stays the switch that hides an event from sale without changing its state."},"lifecycleStateChangedAt":{"type":"string","format":"date-time","readOnly":true,"nullable":true}}},
"FnbIngredientSubstitute": {"type":"object","x-ticvai-persistence":"fnb.ingredient_substitute","description":"**Taken from the backend workbook, 20 September.** Defines approved ingredient substitutions for F&B preparation.","required":["fromInventoryItemId","toInventoryItemId","substitutionRatio","requiresApproval","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"fromInventoryItemId":{"type":"string","format":"uuid"},"toInventoryItemId":{"type":"string","format":"uuid"},"substitutionRatio":{"type":"number"},"conditionsJson":{"type":"string","nullable":true},"allergensAddedJson":{"type":"string","nullable":true},"allergensRemovedJson":{"type":"string","nullable":true},"requiresApproval":{"type":"boolean"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"recipeId":{"type":"string","format":"uuid","readOnly":true,"description":"**The recipe this substitute belongs to** (4 October 2026, CHG-FXC-003): the `{recipeId}` of `listIngredientSubstitutes` and `setIngredientSubstitutes`, stored on every row so the list filters by it and the set replaces exactly that recipe's rows. Taken from the path, never from the body."}}},
"InventoryHold": {"x-ticvai-persistence":"catalogue.inventory_hold","type":"object","required":["id","channelCapacityId","holderKind","grantedUnits","consumedUnits","status","acquiredAt","expiresAt"],"properties":{"id":{"type":"string"},"channelCapacityId":{"type":"string","format":"uuid"},"holderKind":{"$ref":"#/components/schemas/InventoryHoldHolderKind"},"holderWorkstationId":{"type":"string","format":"uuid","nullable":true,"description":"The holding workstation when `holderKind` is `workstation`; null on a cart hold, because a browser has none (SD-023, 29 September)."},"holderCartId":{"type":"string","format":"uuid","nullable":true,"description":"The holding cart (`orders.cart`) when `holderKind` is `cart` (SD-023, 29 September)."},"convertedOrderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The paid order the hold was converted for, set by `convertInventoryHold`."},"convertedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"parentLeaseId":{"type":"string","nullable":true,"description":"Present when sub-leased from a venue edge node."},"requestedUnits":{"type":"integer"},"channel":{"allOf":[{"$ref":"#/components/schemas/Channel"}],"description":"Allocation this lease draws from."},"grantedUnits":{"type":"integer","description":"May be less than requested — a partial grant is not an error. Constrained by the channel's remaining allocation plus the general pool, never by raw capacity.\n"},"consumedUnits":{"type":"integer"},"status":{"$ref":"#/components/schemas/LeaseStatus"},"acquiredAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"releasedAt":{"type":"string","format":"date-time","nullable":true},"forceReleasedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"forceReleaseReason":{"type":"string","nullable":true}}},
"InventoryHoldHolderKind": {"type":"string","enum":["workstation","cart"],"default":"workstation","description":"**Who holds the units** (decided 29 September, SD-023). A till, kiosk or edge node holds as a `workstation`; a guest's web or app cart holds as a `cart`, acquired by the order service. A browser has no workstation, so a cart hold carries `cartId` and no `holderWorkstationId`.\n"},
"LeaseStatus": {"type":"string","description":"`states/lease.yaml`. **`expired` is set by that model's timer transition when `expiresAt` passes without a renewal**, not by any operation in this contract. The job that runs the timer is the sweeper ADR-0037 deferred: it returns an expired hold's unconsumed units to `remaining` in the same guarded statement as a release (SD-023, 29 September), and **writes `inventoryHold.expired` to the outbox in the same transaction** (SD-023/SD-033, applied 30 September; `events/inventoryHold-expired.yaml`), so the cart that held the units hears of it before checkout. A `converted` hold is never swept.\n**`converted` is set by `convertInventoryHold`** when the order that holds the units is paid (decided 29 September, SD-023); its units are `sold` and the sweeper never touches it.\n","enum":["active","expired","released","forceReleased","converted"]},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"**The catalogue variant this item links to, for reporting, stock and tax class only. It is not where the price comes from** (Chinmay, 2 October, workbook Q34; CHG-CSA-009). F&B owns its own catalogue: F&B prices were migrated into the F&B service so ticketing scales as an isolated service (ADR-0028), and the price an outlet sells at is `price` on this item. The central catalogue prices tickets and single-price booths; it never reprices a dish. A menu belongs to one outlet, so `price` is that outlet's price, and an outlet may set its own; it changes through `updateMenu`, `setMenuSections` or `applyMenuActions` (`reprice`). Tax is computed on the order line by the tax engine. (Replaces the earlier text \"pricing and tax come from there — a menu is a presentation of the catalogue\", which was stale.)\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"dailyCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**How many portions the kitchen set for today** (`setMenuItemDailyCount`; Chinmay, 2 October, workbook Q194; CHG-CSA-017). Null means the item is not counted. Reset at the venue day start.\n"},"remainingCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**What is left of `dailyCount`** (\"6 left\" on the till and the guest menu). Each sale takes from it; **at zero the item is marked unavailable automatically**, with an `EightySixEvent` whose `source` is `dailyCount`. Null where the item is not counted.\n"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"OfflineOrder": {"x-ticvai-persistence":"none — client-side journal, not server storage","allOf":[{"$ref":"#/components/schemas/CreateOrderRequest"},{"type":"object","required":["sequence","payments"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. Processed in this order."},"payments":{"type":"array","items":{"$ref":"#/components/schemas/CreatePaymentRequest"}}}}]},
"OfflinePolicy": {"type":"object","x-ticvai-persistence":"platform.offline_policy","description":"Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n","required":["scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$","description":"**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"},"maxOfflineHours":{"type":"integer","default":24,"minimum":1,"maximum":72,"description":"**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"},"allowedOffline":{"type":"array","description":"**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n","items":{"type":"string","enum":["sale","refund","exchange","entitlementIssue","entitlementValidate","loyaltyAccrual","loyaltyRedemption","walletSpend","priceOverride","discount","voidLine","noSale"]}},"offlineValueCeiling":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"},"offlineTransactionCeiling":{"type":"integer","nullable":true,"minimum":1,"maximum":5000,"description":"**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"},"onCeilingBreach":{"type":"string","enum":["warn","blockNewSales","blockAll"],"default":"blockNewSales"},"requiresManagerToExtend":{"type":"boolean","default":true}}},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."},"endsNextDay":{"type":"boolean","default":false,"description":"**A late-night window is one window past midnight** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). A bar open 23:00 to 01:00 on Friday is `day: fri`, `from: '23:00'`, `to: '01:00'`, `endsNextDay: true`: one service period, and its takings belong to Friday's trading day, not split across two days. With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours.\n"}}},
"OrderSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer"},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"First entry that hit a **transient** failure (SD-028, 29 September): a refusal on the merits no longer stops the batch. Null when every entry was accepted, duplicate or quarantined. The client retries from here and never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string","format":"uuid","description":"The `OfflineOrder.id` this result is about."},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","rejected","blockedByRejection"],"description":"`rejected`: refused on its merits and quarantined in `sync.rejection`; the batch continues. `blockedByRejection`: depends on a rejected entry for the same order (a void, a refund, a later payment) and is quarantined with it (SD-028, 29 September)."},"orderNumber":{"type":"string","nullable":true},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Posted to the variance account. Not surfaced to the cashier."},"varianceExceedsThreshold":{"type":"boolean","description":"True when review is required per the venue's variance threshold."},"rejectionId":{"type":"string","nullable":true,"description":"For a `rejected` or `blockedByRejection` entry, the `sync.rejection` row it was quarantined into (SD-028). The batch carried on past it."},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200,"description":"The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005)."},"nameTranslations":{"$ref":"#/components/schemas/OutletNameTranslations"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"outletType":{"allOf":[{"$ref":"#/components/schemas/OutletType"}],"nullable":true,"description":"The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail."},"departmentId":{"type":"string","format":"uuid","nullable":true,"description":"**The department the outlet belongs to** (DI-319: department, sub-department, cost centre and status; DEC-196; CHG-CSP-005): an `OrgUnit` of kind department, as `Workstation.departmentId`. The outlet itself is the sub-department, so it needs no second field.\n"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"paymentTiming":{"allOf":[{"$ref":"#/components/schemas/OutletPaymentTiming"}],"default":"sendFirst","description":"Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004)."},"admissionContext":{"allOf":[{"$ref":"#/components/schemas/OutletAdmissionContext"}],"default":"insideVenue","description":"Inside the venue (needs an admission ticket) or standalone (no ticket) (DEC-070; CHG-CSP-004)."},"producesForOutletIds":{"type":"array","default":[],"description":"**One kitchen serving several outlets is a producing outlet** (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: \"Yes: via a producing outlet (one kitchen outlet produces for several)\"; DEC-188; CHG-CSP-005). The outlets this one prepares food for, in the same venue. The model stays per outlet (DI-330): each outlet keeps its own menu and stations, and an order at a listed outlet may route to this outlet's kitchen stations (fnb `KitchenStation`). Empty on an outlet that only produces for itself. An outlet may not list itself, an outlet of another venue (`422 outlet-not-in-venue`), or one that lists it back.\n","items":{"type":"string","format":"uuid"}},"saleBoardId":{"type":"string","format":"uuid","nullable":true,"description":"**The till layout every till in this outlet uses, unless a till overrides it** (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006). DI-326 puts the layout at the outlet; MATRIX 2.1.9 binds a board to a workstation. Both hold: a workstation with no board of its own (`ConfigureWorkstationRequest.saleBoardId` absent or null) uses this one, and `Workstation.saleBoardSource` says which applied.\n"},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletAdmissionContext": {"type":"string","description":"**Whether an outlet sits behind the admission gate** (decided 2 October 2026, Chinmay, batch 1, WEB-036: \"Inside the venue, a ticket is needed. A restaurant outside the venue (standalone) can sell without one\"; DEC-070; CHG-CSP-004). `insideVenue` (the default): a guest ordering food needs an admission ticket or a place inside, as DI-292 (14 August) decided. `standalone`: a restaurant outside the gate, which may sell takeaway and delivery (DI-1039) with no ticket. DI-292 is amended for standalone outlets only. The admission check itself stays in Access (ADR-0068). F&B keeps its own payment and its own receipt either way. **The canonical name** (2 October 2026, CHG-CLN-008): the field is `admissionContext` on the outlet and on F&B's guest `DiningOutlet`; common `OutletSiting` and the word \"siting\" are deprecated aliases of this.\n","enum":["insideVenue","standalone"]},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"OutletNameTranslations": {"type":"object","x-ticvai-persistence":"none — jsonb column on platform.outlet","description":"**The outlet's name in other languages, keyed by ISO 639-1 code** (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: \"Yes, where a country needs it: the local language plus English\"; DEC-031; CHG-CSP-005). `Outlet.name` stays the English name. Where the region requires a local name (`RegionSettings.localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. The same shape as catalogue's `LocalisedText` (DI-210).\n","additionalProperties":{"type":"string","maxLength":200}},
"OutletPaymentTiming": {"type":"string","description":"**When an F&B order is paid, set per outlet** (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). `sendFirst`, the default and R261's rule: the order goes to the kitchen, then the till charges (table service, and quick service where the venue wants the kitchen started while the guest pays). `payFirst`: the till charges before anything reaches the kitchen; an unpaid order at a `payFirst` outlet is never sent (`fnb.createFnbOrder`, `fnb.fireCourse`). Shared because the outlet (tenancy `Outlet`) holds it and F&B enforces it.\n","enum":["sendFirst","payFirst"],"default":"sendFirst"},
"OutletType": {"type":"string","description":"**How an F&B or retail outlet trades, which switches features on or off** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: \"Add both fields: outlet type and department (DI-319)\"; DEC-196; CHG-CSP-005). DI-319: a quick-service outlet needs no table booking, a fine-dining outlet needs a table layout. `kind` stays the physical place (a shop, a restaurant, a kiosk); this is the service model inside it. `commissary` is a producing kitchen (DEC-186, DEC-188).\n","enum":["fineDining","casualDining","quickService","coffeeShop","barLounge","foodCourt","buffet","commissary","retail"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PathClosureResult": {"description":"What `setPathClosure` returns: the path, and **what a forced closure cut off**, named.\n","allOf":[{"$ref":"#/components/schemas/VenuePath"},{"type":"object","properties":{"strandedPoints":{"type":"array","readOnly":true,"description":"Points no longer reachable because of this closure. Empty unless `force` was used.\n","items":{"$ref":"#/components/schemas/StrandedPoint"}}}}]},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"PerformanceCancellationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["performanceId","dryRun","affectedOrders","refundExposure"],"properties":{"performanceId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"affectedOrders":{"type":"integer"},"affectedGuests":{"type":"integer"},"refundExposure":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"},"bulkRefundBatchId":{"type":"string","nullable":true,"description":"**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"},"notificationsQueued":{"type":"integer"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"PrepSheet": {"type":"object","x-ticvai-persistence":"none — rendered from the production plan and the template","description":"A production plan rendered through the venue's prep-sheet template (`printPrepSheet`, CHG-CSA-014).","required":["planId","sections"],"properties":{"planId":{"type":"string","format":"uuid"},"renderedAt":{"type":"string","format":"date-time"},"sections":{"type":"array","items":{"type":"object","properties":{"stationId":{"type":"string","format":"uuid","nullable":true},"title":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"item":{"type":"string"},"plannedQuantity":{"type":"number"},"suggestedQuantity":{"type":"number","nullable":true},"unit":{"type":"string"},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}}}}}},"printedTo":{"type":"array","description":"The printers each station's part was sent to (`target` `stationPrinters`).","items":{"type":"object","properties":{"stationId":{"type":"string","format":"uuid"},"deviceId":{"type":"string","format":"uuid"}}}},"notPrinted":{"type":"array","description":"Stations in the plan with no printer assigned; never silently skipped.","items":{"type":"string","format":"uuid"}}}},
"ProductionPlan": {"type":"object","x-ticvai-persistence":"fnb.production_plan + fnb.production_plan_line","description":"Board 2M. **Forecast demand against recipes, producing a prep list.** Built from `requestSuggestion(kind=prepPlan)` and then edited — **a forecast a chef cannot overrule is a forecast a chef ignores.**\n**A plan is not a production run and the separation is deliberate.** A plan is drafted, argued over and edited; releasing it creates the runs. **A plan that creates runs as it is drafted creates runs nobody asked for.**\n","required":["id","forDate","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"forDate":{"type":"string","format":"date","description":"The trading day this prep list is for, in the Region's time zone."},"status":{"type":"string","enum":["draft","released","superseded","cancelled"]},"basedOnSuggestionId":{"type":"string","format":"uuid","nullable":true,"description":"**The forecast it started from.** Kept so plan-against-forecast can be compared later — which is the label `recordSuggestionOutcome` needs.\n"},"lines":{"type":"array","items":{"type":"object","required":["itemId","plannedQuantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"suggestedQuantity":{"type":"number","nullable":true},"plannedQuantity":{"type":"number"},"uom":{"type":"string"},"stationId":{"type":"string","format":"uuid","nullable":true}}}},"releasedRunIds":{"type":"array","items":{"type":"string","format":"uuid"},"readOnly":true}}},
"ProductionRun": {"type":"object","x-ticvai-persistence":"fnb.production_run","description":"BL-129. **A central kitchen makes 400 portions at 6am for four outlets**, and nothing modelled that — orders consume stock and no operation produced any.\n**Production converts ingredients into a sellable item**, which is a stock movement in both directions at once, and treating it as two unrelated adjustments loses the yield.\n","required":["id","recipeId","plannedQuantity","status"],"properties":{"id":{"type":"string","format":"uuid"},"recipeId":{"type":"string","format":"uuid"},"productionPlanId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The plan whose release created this run. Null for a run planned directly."},"stationId":{"type":"string","format":"uuid","nullable":true,"description":"**The station whose prep list this run is on.** Copied from the plan line on release, where runs are grouped by station (audit R125 (7)).\n"},"producingOutletId":{"type":"string","format":"uuid"},"forOutletIds":{"type":"array","description":"**Where it goes.** A central kitchen produces for outlets that did not make it.\n","items":{"type":"string","format":"uuid"}},"plannedQuantity":{"type":"number"},"actualQuantity":{"type":"number","nullable":true,"description":"BL-126. **Theoretical against actual is the whole point of recording this.** A recipe says 400 portions from the ingredients issued; the run says how many were made, and the gap is waste, theft or a recipe that is wrong.\n"},"scheduledFor":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["planned","inProgress","completed","cancelled"]},"varianceReason":{"type":"string","nullable":true}}},
"Recipe": {"x-ticvai-persistence":"fnb.recipe + fnb.recipe_ingredient","type":"object","required":["menuItemId","ingredients"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"yield":{"type":"number","minimum":0,"description":"Portions produced by one execution."},"ingredients":{"type":"array","minItems":1,"items":{"type":"object","required":["inventoryItemId","quantity","unit"],"properties":{"inventoryItemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"},"isOptional":{"type":"boolean","default":false}}}},"costPerPortion":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Computed, never entered** (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided by `yield`. Recomputed when the recipe or an ingredient cost changes.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**The recipe's own id** (4 October 2026, CHG-FXC-003; the Sprint 1-2 judging found no operation returned one, so `listIngredientSubstitutes`, `setIngredientSubstitutes` and `SubstitutionRule.recipeId` had nothing to send). One recipe per menu item: `setRecipe` upserts on `menuItemId` and returns the id it kept."}}},
"SaleBoard": {"x-ticvai-persistence":"platform.sale_board","type":"object","required":["id","code","name","venueId","kind","pages"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"pages":{"type":"array","minItems":1,"items":{"type":"object","required":["name","sortOrder","tiles"],"properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"tiles":{"type":"array","items":{"type":"object","required":["position","kind"],"properties":{"position":{"type":"integer"},"kind":{"type":"string","enum":["product","category","action","spacer"]},"variantId":{"type":"string","format":"uuid","nullable":true},"label":{"type":"string"},"colour":{"type":"string","nullable":true},"imageAssetRef":{"type":"string","nullable":true}}}}}}},"isActive":{"type":"boolean"}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"SeatAvailability": {"x-ticvai-persistence":"none — computed from seat, hold and block","type":"object","required":["performanceId","seatMapId","renderMode","totals","seats"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"renderMode":{"type":"string","enum":["graphical","list"],"description":"The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"buffered":{"type":"integer"}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"available":{"type":"integer"},"sold":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"sections":{"type":"array","description":"The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n","items":{"type":"object","required":["code","name"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"description":"As `Section.viewAssetId`. Null means render the view from geometry."},"boundary":{"type":"array","nullable":true,"items":{"$ref":"#/components/schemas/Point"},"description":"As `Section.boundary`. Null when `renderMode` is `list`."}}}},"seats":{"type":"array","items":{"type":"object","required":["seatId","status"],"properties":{"seatId":{"type":"string"},"status":{"$ref":"#/components/schemas/SeatStatus"},"categoryId":{"type":"string","format":"uuid","nullable":true},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`, as on `Seat`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true,"description":"The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."}}}}}},
"SeatRecommendation": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatIds","totalPrice","isContiguous","rank"],"properties":{"seatIds":{"type":"array","items":{"type":"string"}},"displayLabels":{"type":"array","items":{"type":"string"}},"totalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryId":{"type":"string","format":"uuid"},"isContiguous":{"type":"boolean"},"rank":{"type":"integer","description":"Best first."},"rationale":{"type":"string","description":"Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"}}},
"SeatRecommendationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["partySize","strategy"],"properties":{"partySize":{"type":"integer","minimum":1,"maximum":50},"strategy":{"$ref":"#/components/schemas/SeatRecommendationStrategy"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maxPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accessibleCount":{"type":"integer","default":0,"description":"Wheelchair spaces in the party. Companions are added automatically."},"maxOptions":{"type":"integer","default":3,"maximum":10}}},
"SeatRecommendationStrategy": {"type":"string","enum":["bestAvailable","bestValue","closestToStage","accessible","contiguous"]},
"SeatStatus": {"type":"string","enum":["available","held","sold","blocked","buffered","unavailable"]},
"StockTransfer": {"x-ticvai-persistence":"inventory.transfer + inventory.transfer_line","type":"object","required":["id","fromLocationId","toLocationId","status","lines","dispatchedAt"],"properties":{"id":{"type":"string","format":"uuid"},"transferNumber":{"type":"string"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/TransferStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"dispatchedQuantity":{"type":"number"},"receivedQuantity":{"type":"number","nullable":true},"discrepancy":{"type":"number","nullable":true},"discrepancyReason":{"type":"string","nullable":true}}}},"dispatchedByPrincipalId":{"type":"string","format":"uuid"},"receivedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"dispatchedAt":{"type":"string","format":"date-time"},"receivedAt":{"type":"string","format":"date-time","nullable":true},"closeShortReason":{"type":"string","nullable":true,"description":"Why the balance was written off, from `closeTransferShort`."},"closeShortSignedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor whose step-up closed the transfer short (audit R144)."},"fromVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `fromLocationId`. Set by the server (audit R183)."},"toVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `toLocationId`. Set by the server (audit R183)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). `fromLocationId` and `toLocationId` give the endpoints; **this gives the owner**, the source venue's scope.\n\n**Both venues see a transfer between them** (decided 28 September, audit R183). It used to sit at the tenant above both, where neither venue could see it. The row is owned at the source venue and `toScopePath` admits the destination venue too."},"toScopePath":{"type":"string","readOnly":true,"description":"The destination venue's scope. Row-level security admits a caller whose scope matches `scopePath` or `toScopePath`, so both venues read the transfer (decided 28 September, audit R183).\n"}}},
"StrandedPoint": {"type":"object","x-ticvai-persistence":"none — computed from the graph","required":["pointId","name","kind","isCritical"],"properties":{"pointId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string"},"isCritical":{"type":"boolean","description":"First aid, an emergency exit or an assembly point, the same set as `GraphValidation.criticalUnreachable`. **The one the operator must read first.**\n"}}},
"SubstitutionRule": {"type":"object","x-ticvai-persistence":"fnb.substitution_rule","description":"Board 2L, 24 August. **What may replace what, and under what conditions.** A kitchen substitutes constantly — a supplier is short, an item is 86'd, a guest asks — and the package had no way to say which swaps are allowed.\n**The rule exists so `verifyAllergens` has something to check against.** A substitution with no rule behind it is a decision made at the pass by whoever is standing there.\n**`allergensAdded` and `allergensRemoved` are the fields this table is for.** Swapping butter for margarine removes dairy and may add soy — **and a dish still labelled dairy-free after a swap nobody checked is the failure this prevents.**\n","required":["id","recipeId","fromIngredientId","toIngredientId"],"properties":{"id":{"type":"string","format":"uuid"},"recipeId":{"type":"string","format":"uuid","description":"**The recipe the rule applies to** (decided 28 September, audit R125 (10)). Not a menu item and not the whole venue: a swap that is safe in one dish is not safe in another.\n"},"fromIngredientId":{"type":"string","format":"uuid"},"toIngredientId":{"type":"string","format":"uuid"},"ratio":{"type":"number","default":1,"description":"**Not always one to one.** Fresh herbs to dried is roughly three to one, and a rule that assumes parity produces a dish nobody would serve.\n"},"allergensAdded":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"allergensRemoved":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"conditions":{"type":"array","items":{"type":"string","enum":["outOfStock","seasonal","guestRequest","costSaving","always"]}},"requiresApproval":{"type":"boolean","default":false,"description":"**True where the swap changes an allergen.** A chef may substitute freely within a claim; changing the claim is somebody else's decision.\n"},"isActive":{"type":"boolean","default":true}}},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"TransferStatus": {"type":"string","enum":["dispatched","inTransit","received","partiallyReceived","cancelled"]},
"UpsellPlacement": {"type":"string","enum":["productDetail","cart","checkout","postPurchase","atGate","inVenue"]},
"UpsellRule": {"x-ticvai-persistence":"promotions.upsell_rule","type":"object","required":["id","name","placement","triggerVariantIds","suggestedVariantIds"],"properties":{"id":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid","readOnly":true,"description":"The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's region scope on create.\n"},"name":{"type":"string","maxLength":200},"placement":{"$ref":"#/components/schemas/UpsellPlacement"},"triggerVariantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"triggerCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"suggestedVariantIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"suggestedBundleId":{"type":"string","format":"uuid","nullable":true},"channels":{"type":"array","description":"Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience inconsistency.\n","items":{"type":"string"}},"priority":{"type":"integer","default":0},"maxSuggestions":{"type":"integer","default":3},"isActive":{"type":"boolean"}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"WaitlistEntry": {"type":"object","x-ticvai-persistence":"catalogue.waitlist_entry","required":["performanceId","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"performanceId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"contactPoint":{"type":"string","description":"**Where the offer goes.** An entry with no way to reach the guest is an entry that can never be honoured, so this is required even for an anonymous guest.\n"},"partySize":{"type":"integer","minimum":1},"status":{"allOf":[{"$ref":"#/components/schemas/WaitlistStatus"}],"readOnly":true,"description":"Set by the server. `joinWaitlist` does not take it; a new entry is `waiting`."},"position":{"type":"integer","readOnly":true,"description":"First in, first offered. Shown to the guest, because not knowing is worse than waiting."},"offeredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"offerExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**The offer moves on when this passes.** Notifying everyone at once produces a race the fastest guest wins; holding indefinitely for someone asleep leaves the seat unsold.\n"},"joinedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaitlistStatus": {"type":"string","enum":["waiting","offered","converted","expired","left"]},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
