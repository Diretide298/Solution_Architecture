# WS174 — Seat Management Venue Mapping Reference v1.0 board 10

**8 screens · 11 operations · 22 schemas · 4 permissions**

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
  `AI_USE, CAPACITY_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-1043` | Revenue Command Center | B | 0 | 20 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-1044` | Dynamic Seat Pricing | B | 0 | 20 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1045` | Price Bands & Categories | A | 36 | 11 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1046` | Inventory Forecasting | B | 0 | 20 | 6 | 3 | 0 | 4 | — | notStarted (—) |
| `BO-1047` | Section Revenue Forecast | B | 0 | 20 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-1048` | Seat Upsell Recommendations | D | 0 | 0 | 6 | 40 | 0 | 6 | — | notStarted (—) |
| `BO-1049` | Scenario & What-If Planning | B | 15 | 0 | 6 | 12 | 0 | 0 | — | notStarted (—) |
| `BO-1050` | Revenue Analytics & Audit | B | 0 | 20 | 6 | 1 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1043, BO-1044, BO-1046, BO-1047, BO-1048, BO-1049, BO-1050 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1043` Revenue Command Center

**Provide a live executive and revenue-management view of seat performance. Show revenue, yield, occupancy, sales pace, average ticket price, remaining inventory and forecast variance. Analyze by tenant, venue, event, performance, section, category, price band, channel and time to event. Surface underperforming sections, demand spikes, inventory imbalance and pricing opportunities with drill-down. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29800 (VM-BO-1043) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/revenue-command-center-bo-1043` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Seat revenue at a glance: revenue, yield, occupancy, pace, average ticket price, remaining inventory and forecast variance by event, performance, section and price band.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listRevenue` ?venue |
| Automation mode | radio group | — | Advisory · Human in the loop · Conditional autonomous · Autonomous | `listRevenue` ?automationMode |
| Urgency | radio group | — | Low · Medium · High · Critical | `listRevenue` ?urgency |
| Rank by | select | — | Revenue opportunity · Revenue risk · Event proximity · Confidence · Inventory position · Demand variance · Urgency | `listRevenue` ?rankBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table, from `listRevenue`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Event product | text | Event/Product |
| Performance | text | Performance |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Forecast revenue | AED 1,234.50 | Forecast Revenue |
| Expected uplift | 1,234.5 | Expected Uplift, percent |
| Confidence | 1,234.5 | Confidence, percent |
| Automation mode | chip: Advisory, Human in the loop, Conditional autonomous, Autonomous | Automation Mode in force for this scope |
| Approval status | text | Approval Status: notRequired, pending, approved or rejected. |
| Execution status | text | Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack, from the latest price_execution: scheduled queued … |
| Revenue risk | AED 1,234.50 | Revenue Risk if no action is taken |
| Event proximity | 1,234 | Event Proximity: days until the event |
| Inventory position | 1,234.5 | Inventory Position: remaining inventory, percent |
| Demand variance | 1,234.5 | Demand Variance against forecast, percent |
| Urgency | chip: Low, Medium, High, Critical | Urgency |
| Optimization | text | Optimisation id |
| Recommendation | text | Recommendation id |
| Revenue opportunity | AED 1,234.50 | Revenue Opportunity |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPI row and table**: KPI cards with deltas (DI-041), then a table by section; amounts per PR-2. *(source: contracts/spine/catalogue.yaml#listRevenue / DI-041)*

**Data it reads**: `listRevenue` (onLoad, Revenue Optimization Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1044` Dynamic Seat Pricing: *Dynamic Seat Pricing*
- → `BO-1045` Price Bands & Categories: *Price Bands & Categories*
- → `BO-1046` Inventory Forecasting: *Inventory Forecasting*
- → `BO-1047` Section Revenue Forecast: *Section Revenue Forecast*
- → `BO-1048` Seat Upsell Recommendations: *Seat Upsell Recommendations*
- → `BO-1049` Scenario & What-If Planning: *Scenario & What-If Planning*
- → `BO-1050` Revenue Analytics & Audit: *Revenue Analytics & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  revenue: AED 1,284,300.00
  occupancy: 78%
  avgPrice: AED 312.40
  pace: +6% vs target
```

#### Permissions

- `listRevenue` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.30 | System shall support revenue optimization. | Unified Operations Dashboard | CONTRACTED | `listRevenue` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1043` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1043`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 1: Opens Revenue Command Center → Provide a live executive and revenue-management view of seat performance. Show revenue, yield, occupancy, sales pace, average ticket price, remaining inventory and forecast variance. Analyze by …
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F283 branch at step 1 (expected): when Nothing has been set up on Revenue Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F283 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1044`, `BO-1045`, `BO-1046`, `BO-1047`, `BO-1048`, `BO-1049`, `BO-1050`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1044` Dynamic Seat Pricing

**Configure rules that adjust assigned-seat prices within controlled boundaries. Apply rules by section, row, seat, category, event, performance, sales pace, demand, remaining inventory and time to event. Set base price, adjustment type, floor, ceiling, step, maximum frequency, freeze window and competitor/manual inputs where approved. Preview affected inventory, customer display, active carts, taxes/fees, promotions and forecast impact before activation. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29801 (VM-BO-1044) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/dynamic-seat-pricing-bo-1044` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A write for seat-level dynamic pricing rules (section, row and seat, with floor, ceiling and step) and its read.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rules that move assigned-seat prices within bounds (by section, row, category, pace, demand, time to event) using the venue's dynamic pricing strategies.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The screen only lists strategies; nothing writes a seat pricing rule. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Strategy type | select | — | Demand based · Occupancy based · Availability based · Inventory based · Booking velocity · Time to event · Seasonal · Day of week · Timeslot · Channel · Segment · Location … | `listDynamicPricingStrategy` ?strategyType |
| Status | select | — | Draft · Ready · Scheduled · Active · Paused · Frozen · Expired · Retired | `listDynamicPricingStrategy` ?status |
| Automation level | radio group | — | Advisory · Human in the loop · Conditional autonomous · Autonomous | `listDynamicPricingStrategy` ?automationLevel |
| Venue | text field | — | — | `listDynamicPricingStrategy` ?venue |
| Search | text field | — | — | `listDynamicPricingStrategy` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table, from `listDynamicPricingStrategy`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Strategy | text | Strategy ID |
| Strategy name | text | Strategy Name |
| Strategy type | chip: Demand based, Occupancy based, Availability based, Inventory based, Booking … | Strategy Type (pack pp.75-76) |
| Product event | text | Product or event the strategy controls |
| Venue | text | Venue's name, through tenancy#scopeRecords by venue_id (ADAM CR-423) |
| Base price source | text | Base price source: the Board 1 price list and rate the strategy moves from, e.g. |
| Current price | AED 1,234.50 | Current resolved dynamic price: the newPrice of the strategy's newest deployed or partiallyDeployed price_execution where the strategy … |
| Adjustment range | grouped details | Adjustment range allowed by the strategy |
| Min percent | 1,234.5 | Lowest adjustment from base, percent |
| Max percent | 1,234.5 | Highest adjustment from base, percent |
| Rule count | 1,234 | Rule Count |
| Effective period | grouped details | Effective period |
| From | 1 Oct 2026, 14:30 | Effective from |
| To | 1 Oct 2026, 14:30 | Effective to; empty for open-ended |
| Automation level | chip: Advisory, Human in the loop, Conditional autonomous, Autonomous | Automation level, from the most specific dynamic_pricing_control covering the strategy (strategy, product, event, venue, market, global) … |
| Status | text | Status: draft, ready (a draft with a ladder and at least one rule, whose scope is not frozen), scheduled (active, with effectiveFrom after … |
| Owner | text | Owner, the owner principal's display name through identity#principalRecords (ADAM CR-423) |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **strategies for seated events**: Strategies scoped to seated events with their floor and ceiling. *(source: contracts/spine/catalogue.yaml#listDynamicPricingStrategy)*

**Data it reads**: `listDynamicPricingStrategy` (onLoad, Dynamic pricing in force)

**Where the user goes next**

- → `BO-1043` Revenue Command Center: *Back to Revenue Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic seat pricing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic seat pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic seat pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic seat pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
strategy:
  name: Desert Symphony floor seats
  type: occupancyBased
  floor: AED 350.00
  ceiling: AED 520.00
```

#### Permissions

- `listDynamicPricingStrategy` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1044` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1044`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 2: Works in Dynamic Seat Pricing → Configure rules that adjust assigned-seat prices within controlled boundaries. Apply rules by section, row, seat, category, event, performance, sales pace, demand, remaining inventory and time to …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1044?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1043`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1045` Price Bands & Categories

**Maintain the commercial hierarchy applied to seat inventory. Configure price band, seat category, display label, color, currency, channel, customer segment and effective period. Map bands to venue sections, rows or seats and support event/performance overrides with inheritance. Detect overlapping dates, unmapped inventory, invalid currency, missing products and conflicting priority. Configuration Scope of Work / Version 1.0 42 Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 1 · needs the `seating` module |
| Block | Block A · ticket #28035 (APP-SETUP-BO-1045) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Seat categories listed with the selected one's price bands edited beside it (defined 4 October 2026 from SeatCategory and SeatPriceBand, CHG-FXS-001). |
| Offline | online only |
| Opens with | `seatCategoryId` (navigation) |
| Route | `/access-venue/price-bands-categories-bo-1045` |

**What the spec says about it.** **Defined 4 October 2026 from SeatCategory and SeatPriceBand (R275 d): categories in rank order, each with its price bands by channel and effective period. Mapping bands to sections, rows or seats is the seat map editor's (the remaining gap)** (CHG-FXS-001)

**Known gaps.** Mapping bands to sections, rows or seats, and event or performance overrides, are not in the contract (SeatCategory carries priceBands since R275 d).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The seat categories of a venue and the priced bands on each (code, label, colour, amount, channel, customer segment, from and to dates), with rank used for best-seat assignment. Bands apply to sales from their date and never to seats already sold.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- listSeatCategories returns no described schema. (CHG-SBO-005)
- List operation(s) listSeatCategories return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The screen's gap says the contract has no price bands; SeatCategory now carries priceBands (R275 d). (CHG-SBO-010).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Code | text field | optional | — | — | — | Set at creation. | `SeatCategory.code` |
| Name | text field | optional | — | — | — | — | `SeatCategory.name` |
| Colour | text field | optional | — | — | — | Hex colour shown on the seat map; keeps 3:1 contrast with the map background. | `SeatCategory.displayColour` |
| Rank | number field | optional | — | — | — | Ordering for best-seat assignment. Lower is better. | `SeatCategory.rank` |
| Band code | text field | optional | — | max length 64 | — | Unique within the category. | `SeatPriceBand.code` |
| Band label | text field | optional | — | max length 200 | — | — | `SeatPriceBand.displayLabel` |
| Band price | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | In the venue's currency (Money; the currency comes from the region). | `SeatPriceBand.amount` |
| Band channel | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Empty means every channel. | `SeatPriceBand.channel` |
| Effective from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `SeatPriceBand.effectiveFrom` |
| Effective to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Null means open-ended. | `SeatPriceBand.effectiveTo` |

**Sent by *Create seat category*** (`createSeatCategory`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createSeatCategory` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createSeatCategory` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createSeatCategory` body |
| Display colour `displayColour` | colour picker | optional | — | — | #RRGGBB | — | `createSeatCategory` body |
| Rank `rank` | number field | optional | — | — | — | Ordering for best-seat assignment. Lower is better. | `createSeatCategory` body |
| Price bands `priceBands` | repeatable rows | optional | — | — | — | The category's price bands (decided 28 September, audit R275 (d)). | `createSeatCategory` body |
| Code `priceBands[].code` | text field | required | — | max length 64 | — | Unique within the category. | `createSeatCategory` body |
| Display label `priceBands[].displayLabel` | text field | required | — | max length 200 | — | — | `createSeatCategory` body |
| Display colour `priceBands[].displayColour` | colour picker | optional | — | — | #RRGGBB | — | `createSeatCategory` body |
| Amount `priceBands[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createSeatCategory` body |
| Channel `priceBands[].channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Null means every channel. | `createSeatCategory` body |
| Customer segment `priceBands[].customerSegmentId` | picker: choose a customer segment | optional | — | — | shows names, sends the id | A `marketing-crm` customer segment; null means everyone. | `createSeatCategory` body |
| Effective from `priceBands[].effectiveFrom` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createSeatCategory` body |
| Effective to `priceBands[].effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Null means open-ended. | `createSeatCategory` body |

**Sent by *Save changes*** (`updateSeatCategory`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateSeatCategory` body |
| Display colour `displayColour` | colour picker | optional | — | — | #RRGGBB | — | `updateSeatCategory` body |
| Rank `rank` | number field | optional | — | — | — | — | `updateSeatCategory` body |
| Price bands `priceBands` | repeatable rows | optional | — | — | — | — | `updateSeatCategory` body |
| Code `priceBands[].code` | text field | required | — | max length 64 | — | Unique within the category. | `updateSeatCategory` body |
| Display label `priceBands[].displayLabel` | text field | required | — | max length 200 | — | — | `updateSeatCategory` body |
| Display colour `priceBands[].displayColour` | colour picker | optional | — | — | #RRGGBB | — | `updateSeatCategory` body |
| Amount `priceBands[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateSeatCategory` body |
| Channel `priceBands[].channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Null means every channel. | `updateSeatCategory` body |
| Customer segment `priceBands[].customerSegmentId` | picker: choose a customer segment | optional | — | — | shows names, sends the id | A `marketing-crm` customer segment; null means everyone. | `updateSeatCategory` body |
| Effective from `priceBands[].effectiveFrom` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateSeatCategory` body |
| Effective to `priceBands[].effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Null means open-ended. | `updateSeatCategory` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **priceBands**: Edited as a table per category; sending the list replaces it, so removing a row removes the band; colour as a swatch (#RRGGBB); currency is the region's (PR-2). *(source: contracts/satellite/seating.yaml#updateSeatCategory / contracts/satellite/seating.yaml#/components/schemas/SeatPriceBand)*
- **rank**: Lower is better for best-available assignment; shown as an ordered list of categories. *(source: contracts/satellite/seating.yaml#createSeatCategory)*

#### Outputs: what the screen shows and produces

**Shown**

**Seat categories** (data table, from `listSeatCategories`): The venue in session (query venueId), in rank order.

| Shows | Format | Notes |
|---|---|---|
| Rank | 1,234 | Ordering for best-seat assignment. Lower is better. |
| Code | text | — |
| Name | text | — |
| Display colour | text | — |
| Seat count | 1,234 | — |

**Price bands** (data table, from `listSeatCategories`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Unique within the category. |
| Display label | text | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Null means every channel. |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | Null means open-ended. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New seat category (primary button) | navigation or local | — | — | — | — |
| Add band (secondary button) | navigation or local | — | — | — | — |
| Create seat category (primary button) | `createSeatCategory` POST `/seat-categories` | inline | SeatCategory | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | — |
| Save changes (primary button) | `updateSeatCategory` PATCH `/seat-categories/{seatCategoryId}` | inline | SeatCategory | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 Two bands with the same `code`, or a band whose `effectiveTo` is not after its `effectiveFrom` (audit R275 (d)). | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatCategories` (onLoad, Price bands against categories)

**Where the user goes next**

- → `BO-1043` Revenue Command Center: *Back to Revenue Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat categories yet. Carries New seat category. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the price bands categories are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listSeatCategories` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `createSeatCategory`, `updateSeatCategory`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 Two bands with the same `code`, or a band whose `effectiveTo` is not after its `effectiveFrom` (audit R275 (d)). |

#### Edge cases to draw

- **Two bands overlapping in dates for the same channel and segment**: Flag the overlap before save (the pack's validation list: overlapping dates, unmapped inventory, missing products). *(source: screens/P08-venue-back-office.yaml#BO-1045)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
categories:
- code: PLAT
  name: Platinum
  colour: '#0B1324'
  rank: 1
  bands:
  - code: STD
    label: Standard
    amount: AED 450.00
  - code: EARLY
    label: Early bird
    amount: AED 380.00
    to: '2026-11-30'
- code: GOLD
  name: Gold
  colour: '#00B8FF'
  rank: 2
```

#### Permissions

- `listSeatCategories` → `PRODUCT_VIEW` (read) · staff
- `createSeatCategory` → `CAPACITY_CONFIGURE` (configure) · staff
- `updateSeatCategory` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listSeatCategories` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CAPACITY_CONFIGURE` for `createSeatCategory`, `updateSeatCategory`.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1045` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1045`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 4: Works in Price Bands & Categories → Maintain the commercial hierarchy applied to seat inventory. Configure price band, seat category, display label, color, currency, channel, customer segment and effective period. Map bands to venue …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (36), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: New seat category, Add band, Create seat category, Save changes, Cancel.
- [ ] Every transition is wired: `BO-1043`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1046` Inventory Forecasting

**Predict remaining inventory and sell-through by event day. Forecast seats remaining, sell-through, sold-out probability and over/under supply by section and category. Account for active locks, holds, scheduled releases, blocks, expected cancellations and group allocations. Highlight categories likely to sell out early or remain unsold and link to recommended actions. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29802 (VM-BO-1046) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/inventory-forecasting-bo-1046` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Remaining seats and sell-through by event day and section, accounting for holds, scheduled releases and expected cancellations.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listDemandBookingCurve` ?venue |
| Product | text field | — | — | `listDemandBookingCurve` ?product |
| Event | text field | — | — | `listDemandBookingCurve` ?event |
| Performance | text field | — | — | `listDemandBookingCurve` ?performance |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDemandBookingCurve` ?channel |
| Horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listDemandBookingCurve` ?horizon |
| Date from | date picker | — | — | `listDemandBookingCurve` ?dateFrom |
| Date to | date picker | — | — | `listDemandBookingCurve` ?dateTo |
| Price category | picker: choose a price category | — | — | `listDemandBookingCurve` ?priceCategory |
| Section code | text field | — | — | `listDemandBookingCurve` ?sectionCode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table, from `listDemandBookingCurve`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue id |
| Product | text | Product id |
| Event | text | Event id |
| Performance | text | Performance id |
| Date | 1 Oct 2026 | Date |
| Timeslot | text | Timeslot |
| Price category | text | Price category |
| Section code | text | Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build … |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Channel |
| Confidence | 1,234.5 | Forecast Confidence, percent (`DemandForecast.confidence` x 100; ADAM CR-405) |
| Forecast final occupancy | 1,234.5 | Forecast Final Occupancy, percent |
| Demand | 1,234 | Forecast demand |
| Attendance | 1,234 | Forecast attendance |
| Occupancy | 1,234.5 | Forecast occupancy, percent |
| Sell through | 1,234.5 | Forecast sell-through, percent |
| Expected sell out time | 1 Oct 2026, 14:30 | Expected Sell-Out Time; empty if no sell-out forecast |
| Revenue | AED 1,234.50 | Forecast revenue |
| Conversion | 1,234.5 | Forecast conversion, percent |
| Remaining inventory | 1,234 | Forecast remaining inventory at event |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **forecast**: Seats remaining and sold-out probability per section and day. *(source: contracts/spine/catalogue.yaml#listDemandBookingCurve)*

**Data it reads**: `listDemandBookingCurve` (onLoad, Forecast against the curve)

**Where the user goes next**

- → `BO-1043` Revenue Command Center: *Back to Revenue Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory forecasting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory forecasting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory forecasting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
forecast:
  event: Desert Symphony
  section: Balcony
  remaining: 140
  soldOutProbability: 72%
```

#### Permissions

- `listDemandBookingCurve` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.11.2 | Seat Demand Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.3 | Seat Inventory Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.4 | Revenue Forecasting by Section | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1046` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1046`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 6: Works in Inventory Forecasting → Predict remaining inventory and sell-through by event day. Forecast seats remaining, sell-through, sold-out probability and over/under supply by section and category. Account for active locks, holds …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1046?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1043`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1047` Section Revenue Forecast

**Plan expected revenue at the venue-section level. Show capacity, sold, held, available, average price, forecast occupancy, forecast revenue and variance. Provide map heat view and ranking by revenue opportunity, yield gap and risk. Reconcile forecast totals with performance and finance dimensions and preserve scenario assumptions. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29803 (VM-BO-1047) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/section-revenue-forecast-bo-1047` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Expected revenue per venue section with a map heat view and ranking by opportunity and risk.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listDemandBookingCurve` ?venue |
| Product | text field | — | — | `listDemandBookingCurve` ?product |
| Event | text field | — | — | `listDemandBookingCurve` ?event |
| Performance | text field | — | — | `listDemandBookingCurve` ?performance |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDemandBookingCurve` ?channel |
| Horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listDemandBookingCurve` ?horizon |
| Date from | date picker | — | — | `listDemandBookingCurve` ?dateFrom |
| Date to | date picker | — | — | `listDemandBookingCurve` ?dateTo |
| Price category | picker: choose a price category | — | — | `listDemandBookingCurve` ?priceCategory |
| Section code | text field | — | — | `listDemandBookingCurve` ?sectionCode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table, from `listDemandBookingCurve`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue id |
| Product | text | Product id |
| Event | text | Event id |
| Performance | text | Performance id |
| Date | 1 Oct 2026 | Date |
| Timeslot | text | Timeslot |
| Price category | text | Price category |
| Section code | text | Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build … |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | Channel |
| Confidence | 1,234.5 | Forecast Confidence, percent (`DemandForecast.confidence` x 100; ADAM CR-405) |
| Forecast final occupancy | 1,234.5 | Forecast Final Occupancy, percent |
| Demand | 1,234 | Forecast demand |
| Attendance | 1,234 | Forecast attendance |
| Occupancy | 1,234.5 | Forecast occupancy, percent |
| Sell through | 1,234.5 | Forecast sell-through, percent |
| Expected sell out time | 1 Oct 2026, 14:30 | Expected Sell-Out Time; empty if no sell-out forecast |
| Revenue | AED 1,234.50 | Forecast revenue |
| Conversion | 1,234.5 | Forecast conversion, percent |
| Remaining inventory | 1,234 | Forecast remaining inventory at event |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **section heat map**: Seat map coloured by forecast revenue vs capacity. *(source: contracts/spine/catalogue.yaml#listDemandBookingCurve)*

**Data it reads**: `listDemandBookingCurve` (onLoad, By section)

**Where the user goes next**

- → `BO-1043` Revenue Command Center: *Back to Revenue Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The section revenue forecast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the section revenue forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No section revenue forecast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the section revenue forecast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sections:
- section: Floor
  forecast: AED 640,000.00
  variance: -4%
```

#### Permissions

- `listDemandBookingCurve` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.11.2 | Seat Demand Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.3 | Seat Inventory Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.4 | Revenue Forecasting by Section | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1047` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1047`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 8: Works in Section Revenue Forecast → Plan expected revenue at the venue-section level. Show capacity, sold, held, available, average price, forecast occupancy, forecast revenue and variance. Provide map heat view and ranking by revenue …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1043`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1048` Seat Upsell Recommendations

**Configure revenue-positive seat offers that remain fair and eligible. Rank upgrade pairs by view improvement, distance, amenities, price delta, availability and customer eligibility. Set channels, offer window, frequency, minimum improvement, margin, membership/loyalty benefit and exclusion rules. Track offer, acceptance, incremental revenue, original-seat resale and guest outcome. Configuration Scope of Work / Version 1.0 43 Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block D · task VM-BO-1048 |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/seat-upsell-recommendations-bo-1048` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-014): No operation stores seat-upgrade offer rules.

**From the AI & Intelligence process.** Seat upsell rules: offer better seats (view, distance, amenities) for a price difference, within channels, offer window, frequency, minimum improvement, margin, membership benefits and exclusions. Seat selection itself stays deterministic in Seating; upgrades are upsell placements of the one engine. The one thing to get right: an upgrade is only offered if it is genuinely better by the configured minimum and available at offer time.

**Known correction pending (do not draw the wrong version)**

- **Only decideRecommendations is declared; no operation stores the seat-upgrade rules the purpose describes.** Why: Seat upgrade strategy belongs to Promotions configuration (ADR-0052); declare its write. *(source: ADR-0052; AI & Intelligence)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **upgrade rule**: Minimum improvement, price delta range in AED, channels, offer window (e.g. 48 h to 2 h before the show), frequency cap, exclusions. *(source: screens/P08-venue-back-office.yaml#BO-1048 (purpose) / ADR-0052)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1043` Revenue Command Center: *Back to Revenue Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat upsell recommendations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat upsell recommendations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat upsell recommendations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat upsell recommendations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
offer:
  from: Upper tier U12 row K
  to: Lower tier L4 row D
  improvement: 38 m closer, centre view
  delta: AED 120.00
  window: 48 h-2 h before
```

#### Permissions

- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `AI_USE`

#### Requirements it meets

40 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 28 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1048` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1048`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 10: Works in Seat Upsell Recommendations → Configure revenue-positive seat offers that remain fair and eligible. Rank upgrade pairs by view improvement, distance, amenities, price delta, availability and customer eligibility. Set channels …
- ADR-0052 *One recommendation engine; runtime in AI, configuration in Promotions* (`docs/adr/0052-one-recommendation-engine.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-1043`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1049` Scenario & What-If Planning

**Compare alternative price, demand and inventory decisions before publication. Adjust capacity, price, discount, holdback, release timing, demand uplift and sales pace assumptions. Calculate seats sold, occupancy, revenue, yield, gross margin, sell-out timing and downside risk. Save, compare, comment, share and approve scenarios without changing live prices or inventory. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29804 (VM-BO-1049) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/access-venue/scenario-what-if-planning-bo-1049` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the saved what-if scenarios and their assumptions that simulatePriceBreakdownCalculation writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Try a price or inventory decision before publishing it: price a scenario through the full calculation (product, channel, date, promotion, payment method) and compare channels.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The request carries a currency. (CHG-SBO-005)
- No read operation: the screen declares only simulatePriceBreakdownCalculation and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card … | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Entitlement template | picker: choose an entitlement template | — | The Entitlement templates screen (BO-1192) lists them under each template, and `archiveEntitlementTemplate` is refused while any of them is not retired. | `listProducts` ?entitlementTemplateId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listProducts` ?channel |

**Form: Run simulation** (modal, opened by *Run simulation*; *Run simulation* calls `simulatePriceBreakdownCalculation`, *Cancel* sends nothing)

**Collects what `simulatePriceBreakdownCalculation` sends before it is called.** Required: nothing. Optional: `customerId`, `productId`, `productVariantId`, `quantity`, `venueId`, `eventId`, `channel`, `date`, `timeslotId`, `membershipId`, `promotionCode`, `paymentMethod`, `deliveryMethod`, `currency`, `compareChannels`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Customer `customerId` | text field | optional | — | — | — | Customer. | `simulatePriceBreakdownCalculation` body |
| Product `productId` | text field | optional | — | — | — | Product | `simulatePriceBreakdownCalculation` body |
| Product variant `productVariantId` | picker: choose a product variant | optional | — | — | shows names, sends the id | The variant priced; a variant of productId, required when the product has more than one sellable variant, else 400 validation on productVariantId (ADAM CR-419) | `simulatePriceBreakdownCalculation` body |
| Quantity `quantity` | number field | optional | — | min 1 | — | Quantity | `simulatePriceBreakdownCalculation` body |
| Venue `venueId` | text field | optional | — | — | — | Venue | `simulatePriceBreakdownCalculation` body |
| Event `eventId` | text field | optional | — | — | — | Event | `simulatePriceBreakdownCalculation` body |
| Channel `channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Channel | `simulatePriceBreakdownCalculation` body |
| Date `date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Date of visit | `simulatePriceBreakdownCalculation` body |
| Timeslot `timeslotId` | text field | optional | — | — | — | Timeslot | `simulatePriceBreakdownCalculation` body |
| Membership `membershipId` | text field | optional | — | — | — | Membership, the catalogue.membership_programme the simulated customer holds; the one membership rule whose membershipProgramme condition lists it adjusts the rate at the … | `simulatePriceBreakdownCalculation` body |
| Promotion code `promotionCode` | text field | optional | — | — | — | Promotion. | `simulatePriceBreakdownCalculation` body |
| Payment method `paymentMethod` | text field | optional | — | — | — | Payment Method | `simulatePriceBreakdownCalculation` body |
| Delivery method `deliveryMethod` | text field | optional | — | — | — | Delivery Method | `simulatePriceBreakdownCalculation` body |
| Currency `currency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | Currency: ISO 4217 code | `simulatePriceBreakdownCalculation` body |
| Compare channels `compareChannels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Channel Comparison (p.51): run the same transaction through these channels too; empty for none | `simulatePriceBreakdownCalculation` body |

Errors to draw in the form: 400 `validation` on `productVariantId`: it is not a variant of `productId`, or it is missing while the product has more than one sellable variant (ADAM CR-419).; 422 `no-selected-rate`: no price resolves for the variant at the venue on the channel on the date (catalogue#variantPriceRecords; ADAM CR-455), or the main …

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **scenario**: Product, quantity, date and slot, channel, membership, promotion code; "compare channels" shows the same basket priced on each. *(source: contracts/spine/catalogue.yaml#simulatePriceBreakdownCalculation)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run simulation (primary button) | `simulatePriceBreakdownCalculation` PUT `/price-breakdown-calculation` | PriceBreakdownCalculationSimulationExplainabilityInput | PriceBreakdownCalculationSimulationExplainabilityView | 400 `validation` on `productVariantId`: it is not a variant of `productId`, or it is missing while the product has more than one sellable variant (ADAM CR-419).; 422 `no-selected-rate`: no price resolves for the variant … | opens modal first |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **breakdown**: Base, adjustments, discounts, tax (on pre-discount price where the region says so), fees, rounding, total, each line explained. *(source: contracts/spine/catalogue.yaml#simulatePriceBreakdownCalculation / DI-598)*

**Data it reads**: `listEvents` (onLoad, The events, to pick the simulated event in Run simulation); `listProducts` (onLoad, The products, to pick the simulated product in Run …)

**Where the user goes next**

- → `BO-1043` Revenue Command Center: *Back to Revenue Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scenario what-if planning list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scenario what-if planning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scenario what-if planning yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the scenario what-if planning are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A public guest read of venue data named no venue (`venue-required`; ADAM CR-198, CHG-R10ID-022): send `X-Venue-Id`.; 400 No `venueId` or `X-Venue-Id` from a caller with no venue (`venue-required`); or a venue, from either, that is not a … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenario:
  product: Day Pass Adult
  quantity: 2
  channel: Website
  promotion: RESIDENT-15
  result: AED 501.50 incl. VAT AED 23.88
```

#### Permissions

- `simulatePriceBreakdownCalculation` → `PRODUCT_CONFIGURE` (configure) · staff
- `listEvents` → `PRODUCT_VIEW` (read) · staff, guest, anonymous
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `PRODUCT_CONFIGURE`

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 1.1.13 | The system should allow combination of multiple properties for all type of tickets. For example, there can be a VIP child ticket and a normal adult ticket. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.32 | Ability to create and book dynamic performances based on the event start time. Dynamic performance to be chosen by customer 2 - 3 - 4 hour (for pods or Spaces) | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.33 | Book per time slot | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.34 | Book variable amount of minutes per individual 30 minute session. Can be at different times of the day and different times of the week / month. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.37 | As above, If individuals purchase X number of minutes, they want the ability to book varying time slots on varying dates | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.38 | For example: If a skydiver or first time flyer wishes to “just turn up”.. we need the ability to sell to that individual and enter them onto the system and create a “ There and then” booking. Can be … | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.39 | Pre purchased number of minutes with variable price based on time slots . Peak, Off Peak, Super Prime etc etc etc . We need the ability to change these periods easily ie , if I wanted to make Prime … | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.40 | Ability for specific profiles to add minutes to their account. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 3.6.29 | Attribute-driven product architecture that lets teams add ticket types, add-ons, and bundles without duplicating SKUs (single definition, multi-variant) | Admission and Access | CONTRACTED | `listProductVariants` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1049` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1049`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 12: Works in Scenario & What-If Planning → Compare alternative price, demand and inventory decisions before publication. Adjust capacity, price, discount, holdback, release timing, demand uplift and sales pace assumptions. Calculate seats …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run simulation, Cancel.
- [ ] Every transition is wired: `BO-1043`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1050` Revenue Analytics & Audit

**Measure actual financial outcomes and preserve decision evidence. Compare realized versus forecast revenue, occupancy, yield, average price and sell-through by section/category. Attribute change to price actions, holds/releases, promotions, demand shifts, channels and model recommendations. Retain rule, input data version, model/version, recommendation, approval, publication, override and rollback history. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 44 Board 11 - Seat Reporting & Analytics Figure 11. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 45**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | Block B · ticket #29805 (VM-BO-1050) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/revenue-analytics-audit-bo-1050` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Realised against forecast revenue, occupancy and yield by section and category, with the decisions (price actions, holds, promotions) that explain the difference.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listRevenue` ?venue |
| Automation mode | radio group | — | Advisory · Human in the loop · Conditional autonomous · Autonomous | `listRevenue` ?automationMode |
| Urgency | radio group | — | Low · Medium · High · Critical | `listRevenue` ?urgency |
| Rank by | select | — | Revenue opportunity · Revenue risk · Event proximity · Confidence · Inventory position · Demand variance · Urgency | `listRevenue` ?rankBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table, from `listRevenue`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Event product | text | Event/Product |
| Performance | text | Performance |
| Current price | AED 1,234.50 | Current Price |
| Recommended price | AED 1,234.50 | Recommended Price |
| Forecast revenue | AED 1,234.50 | Forecast Revenue |
| Expected uplift | 1,234.5 | Expected Uplift, percent |
| Confidence | 1,234.5 | Confidence, percent |
| Automation mode | chip: Advisory, Human in the loop, Conditional autonomous, Autonomous | Automation Mode in force for this scope |
| Approval status | text | Approval Status: notRequired, pending, approved or rejected. |
| Execution status | text | Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack, from the latest price_execution: scheduled queued … |
| Revenue risk | AED 1,234.50 | Revenue Risk if no action is taken |
| Event proximity | 1,234 | Event Proximity: days until the event |
| Inventory position | 1,234.5 | Inventory Position: remaining inventory, percent |
| Demand variance | 1,234.5 | Demand Variance against forecast, percent |
| Urgency | chip: Low, Medium, High, Critical | Urgency |
| Optimization | text | Optimisation id |
| Recommendation | text | Recommendation id |
| Revenue opportunity | AED 1,234.50 | Revenue Opportunity |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **variance attribution**: Waterfall from forecast to actual by cause. *(source: contracts/spine/catalogue.yaml#listRevenue)*

**Data it reads**: `listRevenue` (onLoad, Revenue Optimization Command Center)

**Where the user goes next**

- → `BO-1043` Revenue Command Center: *Back to Revenue Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue analytics audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue analytics audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue analytics audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue analytics audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
variance:
  forecast: AED 1,200,000.00
  actual: AED 1,284,300.00
  byCause:
    priceActions: +AED 52,000.00
    promotions: -AED 18,000.00
```

#### Permissions

- `listRevenue` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `PRODUCT_VIEW`

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.5.30 | System shall support revenue optimization. | Unified Operations Dashboard | CONTRACTED | `listRevenue` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1050` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1050`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 10
- Flow F283 *Seat Management Venue Mapping Reference v1.0 board 10: Revenue Command Center*, step 14: Works in Revenue Analytics & Audit → Measure actual financial outcomes and preserve decision evidence. Compare realized versus forecast revenue, occupancy, yield, average price and sell-through by section/category. Attribute change to …
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1043`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createSeatCategory": {"method":"POST","path":"/seat-categories","contract":"seating","summary":"Create a seat category","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatCategory"},
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"listDemandBookingCurve": {"method":"GET","path":"/demand-booking-curve","contract":"catalogue","summary":"AI Demand Forecasting & Booking Curve Studio","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"horizon","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"priceCategory","in":"query","required":false},{"name":"sectionCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPricingStrategy": {"method":"GET","path":"/dynamic-pricing-strategy","contract":"catalogue","summary":"Dynamic Pricing Strategy Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"strategyType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"automationLevel","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEvents": {"method":"GET","path":"/events","contract":"catalogue","summary":"List events","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVariants": {"method":"GET","path":"/products/{productId}/variants","contract":"catalogue","summary":"List generated variants","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"entitlementTemplateId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":"channel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRevenue": {"method":"GET","path":"/revenue","contract":"catalogue","summary":"Revenue Optimization Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"automationMode","in":"query","required":false},{"name":"urgency","in":"query","required":false},{"name":"rankBy","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeatCategories": {"method":"GET","path":"/seat-categories","contract":"seating","summary":"List seat categories","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"SeatCategory"},
"simulatePriceBreakdownCalculation": {"method":"PUT","path":"/price-breakdown-calculation","contract":"catalogue","summary":"Price Breakdown, Calculation Simulation & Explainability","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceBreakdownCalculationSimulationExplainabilityInput","responds":"PriceBreakdownCalculationSimulationExplainabilityView"},
"updateSeatCategory": {"method":"PATCH","path":"/seat-categories/{seatCategoryId}","contract":"seating","summary":"Rename, re-rank or re-price a seat category","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatCategory"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiDemandForecastingBookingCurveStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue id"},"product":{"type":"string","description":"Product id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"date":{"type":"string","description":"Date","format":"date"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"priceCategory":{"type":"string","description":"Price category","nullable":true},"sectionCode":{"type":"string","nullable":true,"description":"Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"confidence":{"type":"number","description":"Forecast Confidence, percent (`DemandForecast.confidence` x 100; ADAM CR-405)"},"forecastFinalOccupancy":{"type":"number","description":"Forecast Final Occupancy, percent"},"demand":{"type":"integer","description":"Forecast demand"},"attendance":{"type":"integer","description":"Forecast attendance"},"occupancy":{"type":"number","description":"Forecast occupancy, percent"},"sellThrough":{"type":"number","description":"Forecast sell-through, percent"},"expectedSellOutTime":{"type":"string","description":"Expected Sell-Out Time; empty if no sell-out forecast","format":"date-time","nullable":true},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast revenue"},"conversion":{"type":"number","description":"Forecast conversion, percent"},"remainingInventory":{"type":"integer","description":"Forecast remaining inventory at event"},"mape":{"type":"number","description":"MAPE over closed forecasts at this level, percent"},"forecastBias":{"type":"number","description":"Forecast Bias (positive = over-forecast), percent"},"overForecast":{"type":"number","description":"Share of closed forecasts that over-forecast, percent"},"underForecast":{"type":"number","description":"Share of closed forecasts that under-forecast, percent"},"forecastId":{"type":"string","description":"Forecast id"},"horizon":{"type":"string","description":"Forecast Horizon","enum":["intraday","tomorrow","days7","days30","eventHorizon","seasonalHorizon"]},"bookingCurve":{"type":"array","items":{"type":"object","properties":{"daysBeforeEvent":{"type":"integer","description":"T minus days"},"historicalExpectedPercentSold":{"type":"number","description":"Historical expected curve, percent sold"},"actualPercentSold":{"type":"number","nullable":true,"description":"Current actual curve, percent sold (empty for future points)"},"forecastPercentSold":{"type":"number","description":"AI forecast curve, percent sold"}}},"description":"Booking Curve"},"signalContributions":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category"},"contributionPercent":{"type":"number","description":"Explanatory share of the forecast"}}},"description":"Model Inputs: which signals contributed"},"confidenceReasons":{"type":"array","items":{"type":"string","enum":["strongHistoricalData","stableBookingPattern","reliableExternalSignals","limitedHistoricalData","volatileBookingPattern","degradedExternalSignals"]},"description":"Reasons behind the forecast confidence"},"modelVersion":{"type":"string","description":"Model version that produced the forecast"},"generatedAt":{"type":"string","description":"When the forecast was produced","format":"date-time"}}},
"AiRecommendationItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList","description":"One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).","required":["trackingId","rank"],"properties":{"trackingId":{"type":"string","format":"uuid","description":"Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."},"variantId":{"type":"string","format":"uuid","nullable":true,"description":"**What the guest adds to the cart, when there is nothing to choose** (r8, ORDERS-MONEY-C40, the lead's option A): for a product item whose product has one default variant, that variant, resolved from the Pricing price reference the item carries; the add-to-cart asks only the quantity (and a date for a timed product). Null when the product has several variants: the screen lets the guest choose (`catalogue.listProductVariants`, option B). Null on non-product kinds (offer, reward, challenge), which have their own action, never addCartLine."},"performanceId":{"type":"string","format":"uuid","nullable":true,"description":"For a timed product with exactly one bookable performance in the context the engine was given (the cart's date), that performance (r8, ORDERS-MONEY-C40); otherwise null and the screen asks for the date."},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."},"couponRef":{"type":"string","nullable":true,"description":"For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."},"rewardId":{"type":"string","format":"uuid","nullable":true,"description":"For `reward`, a marketing-crm loyalty reward the guest can redeem."},"challengeId":{"type":"string","format":"uuid","nullable":true,"description":"For `challenge`, a marketing-crm challenge the guest can join."},"kind":{"type":"string","enum":["upsell","crossSell","upgrade","bundle","addOn","membership","nextBestOffer","offer","reward","challenge"]},"rank":{"type":"integer","minimum":1},"priceRef":{"type":"string","nullable":true,"description":"The Pricing reference the channel resolves to a price. AI never computes a price."},"reasonTemplateKey":{"type":"string","nullable":true,"description":"The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."},"reasonText":{"type":"string","nullable":true,"description":"The rendered template in the session locale, where the channel shows reasons."},"confidenceBand":{"type":"string","enum":["high","medium","low"],"description":"Design 5.6: a band, never a bare percentage."},"score":{"type":"number","nullable":true,"description":"Normalised score. **Returned to staff callers only**; a guest response omits it."}}},
"AiRecommendationResult": {"type":"object","x-ticvai-persistence":"none — written as ai.rec_decision after the response","description":"The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.","required":["decisionId","mode","items","expiresAt"],"properties":{"decisionId":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"]},"items":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationItem"}},"expiresAt":{"type":"string","format":"date-time"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"DynamicPricingStrategyCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Dynamic Pricing Strategy Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeStrategies":{"type":"integer","description":"Active Strategies"},"draftStrategies":{"type":"integer","description":"Draft Strategies"},"productsUnderDynamicPricing":{"type":"integer","description":"Products Under Dynamic Pricing"},"eventsUnderDynamicPricing":{"type":"integer","description":"Events Under Dynamic Pricing"},"performancesUnderDynamicPricing":{"type":"integer","description":"Performances Under Dynamic Pricing"},"rulesActive":{"type":"integer","description":"Rules Active"},"currentPriceAdjustments":{"type":"integer","description":"Current Price Adjustments, the targets of the listed strategies whose newest price_execution is deployed or partiallyDeployed (ADAM CR-423)"},"pricesAtMaximumGuardrail":{"type":"integer","description":"Prices at Maximum Guardrail, those targets whose newPrice is at or above the governing dynamic_pricing_control's absoluteMaximumPrice, or the ladder's maximumPrice where no control sets one (ADAM CR-423)"},"pricesAtMinimumGuardrail":{"type":"integer","description":"Prices at Minimum Guardrail, those targets whose newPrice is at or below the governing control's absoluteMinimumPrice, or the ladder's minimumPrice where no control sets one (ADAM CR-423)"},"ruleConflicts":{"type":"integer","description":"Rule Conflicts: always present, and 0 until conflict detection is decided (ADAM CR-423, the correction of 3 November 2026 on #35286)"},"frozenStrategies":{"type":"integer","description":"Frozen Strategies"},"upcomingActivations":{"type":"integer","description":"Upcoming Activations: strategies scheduled to activate within 7 days (decided 29 September, readiness close-out)"},"operationalAlerts":{"type":"array","items":{"type":"string"},"description":"Operational Alerts (pack p.76): a code for each condition that holds, pricesAtUpperBand, unresolvedRuleConflicts or activatingWithin48Hours; the screen words them (ADAM CR-423). unresolvedRuleConflicts is never listed until conflict detection is decided (the correction of 3 November 2026 on #35286)"}}},
"DynamicPricingStrategyCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Pricing Strategy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"strategyId":{"type":"string","description":"Strategy ID"},"strategyName":{"type":"string","description":"Strategy Name"},"strategyType":{"type":"string","enum":["demandBased","occupancyBased","availabilityBased","inventoryBased","bookingVelocity","timeToEvent","seasonal","dayOfWeek","timeslot","channel","segment","location","hybrid"],"description":"Strategy Type (pack pp.75-76)"},"productEvent":{"type":"string","description":"Product or event the strategy controls"},"venue":{"type":"string","description":"Venue's name, through tenancy#scopeRecords by venue_id (ADAM CR-423)"},"basePriceSource":{"type":"string","description":"Base price source: the Board 1 price list and rate the strategy moves from, e.g. UAE Standard Admission -> Adult"},"currentPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Current resolved dynamic price: the newPrice of the strategy's newest deployed or partiallyDeployed price_execution where the strategy prices one target (singleProduct, or an event with at most one performance); otherwise null (ADAM CR-423)","nullable":true},"adjustmentRange":{"type":"object","properties":{"minPercent":{"type":"number","description":"Lowest adjustment from base, percent"},"maxPercent":{"type":"number","description":"Highest adjustment from base, percent"}},"description":"Adjustment range allowed by the strategy"},"ruleCount":{"type":"integer","description":"Rule Count"},"effectivePeriod":{"type":"object","properties":{"from":{"type":"string","format":"date-time","description":"Effective from"},"to":{"type":"string","format":"date-time","description":"Effective to; empty for open-ended","nullable":true}},"description":"Effective period"},"automationLevel":{"type":"string","enum":["advisory","humanInTheLoop","conditionalAutonomous","autonomous"],"description":"Automation level, from the most specific dynamic_pricing_control covering the strategy (strategy, product, event, venue, market, global); advisory where there is none (replaces automationMode; ADAM CR-423, CR-417)"},"status":{"type":"string","description":"Status: draft, ready (a draft with a ladder and at least one rule, whose scope is not frozen), scheduled (active, with effectiveFrom after now), active, paused, frozen, expired or retired; ready and scheduled are derived, the rest as stored, and testing is not answered (ADAM CR-423; LO-CR423-001)"},"owner":{"type":"string","description":"Owner, the owner principal's display name through identity#principalRecords (ADAM CR-423)"}}},
"Event": {"x-ticvai-persistence":"catalogue.event","type":"object","required":["id","code","name","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentEventId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.event","description":"For grouped events. The parent is an existing event at the same venue, not the event itself, and has no parent of its own (one level; ADAM CR-256). Declared as a key onto `catalogue.event`."},"performanceCount":{"type":"integer","readOnly":true,"description":"How many performances the event has. Counted by the server; never sent by a client."},"isActive":{"type":"boolean"},"lifecycleState":{"type":"string","readOnly":true,"enum":["draft","planned","onSale","live","closed","cancelled","archived"],"description":"**Where the event is in its lifecycle** (4 October 2026, CHG-FXC-003; catalogue.event had nowhere to keep it). Written only by `setEventLifecycleState` and the event lifecycle job, which check the transition against `states/event.yaml` (ADAM CR-109); `createEvent` and `cloneEvent` create an event in `draft`. `isActive` stays the switch that hides an event from sale without changing its state."},"lifecycleStateChangedAt":{"type":"string","format":"date-time","readOnly":true,"nullable":true},"scheduledLifecycleState":{"type":"string","readOnly":true,"nullable":true,"enum":["draft","planned","onSale","live","closed","cancelled","archived"],"description":"**A move waiting for its effectiveFrom** (ADAM CR-109, option 2; CHG-R10CAT-009): written by `setEventLifecycleState` when `effectiveFrom` is in the future, applied and cleared by the event lifecycle job in the workers host at `scheduledLifecycleAt`. Null when nothing waits."},"scheduledLifecycleAt":{"type":"string","format":"date-time","readOnly":true,"nullable":true,"description":"When the waiting move is applied (the request's `effectiveFrom`; ADAM CR-109)."},"scheduledLifecycleReason":{"type":"string","maxLength":500,"readOnly":true,"nullable":true,"description":"The reason given with the waiting move, carried on `event.lifecycleChanged` when it is applied (ADAM CR-109)."}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceBreakdownCalculationSimulationExplainabilityInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Price Breakdown, Calculation Simulation & Explainability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"customerId":{"type":"string","nullable":true,"description":"Customer. Not read: a simulation never looks up a real guest (ADAM CR-419)"},"productId":{"type":"string","description":"Product"},"productVariantId":{"type":"string","format":"uuid","nullable":true,"description":"The variant priced; a variant of productId, required when the product has more than one sellable variant, else 400 validation on productVariantId (ADAM CR-419)"},"quantity":{"type":"integer","description":"Quantity","minimum":1},"venueId":{"type":"string","nullable":true,"description":"Venue"},"eventId":{"type":"string","nullable":true,"description":"Event"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Channel"},"date":{"type":"string","format":"date","description":"Date of visit"},"timeslotId":{"type":"string","nullable":true,"description":"Timeslot"},"membershipId":{"type":"string","nullable":true,"description":"Membership, the catalogue.membership_programme the simulated customer holds; the one membership rule whose membershipProgramme condition lists it adjusts the rate at the contextualRateSelection step (ADAM CR-419, CR-439, CR-455)"},"promotionCode":{"type":"string","nullable":true,"description":"Promotion. Until Promotions' evaluatePromotions is built, a request with a promotionCode answers 422 promotion-evaluation-unavailable and computes nothing (ADAM CR-439)"},"paymentMethod":{"type":"string","nullable":true,"description":"Payment Method"},"deliveryMethod":{"type":"string","nullable":true,"description":"Delivery Method"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"compareChannels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"description":"Channel Comparison (p.51): run the same transaction through these channels too; empty for none"}}},
"PriceBreakdownCalculationSimulationExplainabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Breakdown, Calculation Simulation & Explainability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"finalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final Payable"},"components":{"type":"array","items":{"type":"object","properties":{"sequence":{"type":"integer"},"componentType":{"type":"string","enum":["selectedRate","memberAdjustment","dynamicAdjustment","promotion","packageAdjustment","fee","surcharge","waiver","tax","rounding"]},"label":{"type":"string","description":"e.g. Booking Fee, VAT"},"source":{"type":"string","description":"Source: the price list, rule, fee or tax profile"},"rule":{"type":"string","description":"Rule: id of the rule applied, e.g. FE-021, TAX-UAE-01"},"formula":{"type":"string"},"input":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Input amount"},"output":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Output amount (negative for a reduction)"},"reason":{"type":"string"},"taxTreatment":{"type":"string","nullable":true}}},"description":"Explainability Panel and Rule Trace (p.51), in sequence"},"selectedRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Selected Rate x quantity"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discounts and adjustments total"},"feeTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fees total"},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Subtotal before tax"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tax total"},"calculationVersion":{"type":"string","description":"Calculation version used, the calculation profile's code and version (ADAM CR-419)"},"channelComparison":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"finalPayable":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Absent (null) for a channel with no catalogue channel, `api` or `backOffice` (ADAM CR-537): no price list prices the variant there."},"difference":{"type":"string","description":"Why it differs, e.g. Call Center Booking Fee; for `api` or `backOffice`, that no price list prices this variant on that channel (ADAM CR-537)"}}},"description":"Channel Comparison results"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI observations for this screen; advisory only, never applied automatically. Answered as an empty list until an AI producer exists (ADAM CR-419; LO-CR419-001)"}}},
"Product": {"x-ticvai-persistence":"catalogue.product + catalogue.product_media","x-ticvai-index":[["venueId","displayOrder","id"]],"type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"bookingEntry":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["dateFirst","productFirst","venueMap","timeWindow","bundle"],"description":"**Which booking screen Book opens** (ADAM CR-591, Chinmay, 3 November 2026; CHG-CR591-001). Worked out on read and never stored; set on every guest or visitor read that answers a product (`listProducts`, `getProduct`) and on every `searchCatalogue` result, null on staff reads, and null when the product has no Book (info-only). In this order: (a) kind `bundle` gives `bundle` while `bundleId` is set; with no such bundle it is null and the card opens Item Detail as now. (b) `requiresTimeWindow` true gives `timeWindow`. (c) Otherwise the product's published booking flow by `getPublishedBookingFlow`'s rule (the product's flow, then its category's, then the venue's enabled default for its kind, with the same tie rule), from `white-label#publishedBookingFlowSteps`: its first enabled step, skipping `location` and `helpMeChoose`; `resourceMap` gives `venueMap`; `date`, `time` or `performance` gives `dateFirst`; any other step gives `productFirst`. If no flow resolves, the same test is applied to the default order of the flow type the kind rule picks. Book opens: `dateFirst` GST-007, `productFirst` GST-008, `venueMap` GST-074, `timeWindow` GST-075, each with `productId`; `bundle` GST-056 with `bundleId`."},"bundleId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"Set only when `bookingEntry` is `bundle` (ADAM CR-591; CHG-CR591-001): the id of the promotions bundle whose `variant_id` is this product's variant, while `getGuestBundle` would return it (published, active, in its window). Never taken from a search result's `id`: for a bundle that is the bundle's catalogue product, not the bundle."},"fromPrice":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**The lowest list price on the caller's channel now** (ADAM CR-358, option (a); CHG-CR358-001): the lowest `listPrice` among the product's sellable variants on the caller's channel, in the same currency as `ProductVariant.listPrice`, by the same price-list rule as `searchCatalogue`'s `fromPrice` and `ProductVariant.listPrice`. Set by `listProducts` (its description says how); not stored and ignored on input. Null where no price list prices it on that channel, and null from every other operation that answers `Product` for now."},"displayOrder":{"type":"integer","nullable":true,"default":100,"description":"Where this product sorts among the venue's products in listProducts, lower first. Not alphabetical: the order the venue wants guests to see. (ADAM CR-581, Chinmay, 3 November 2026; CHG-CR581-001.) Stored on `catalogue.product` as `display_order`, nullable with default 100 like `catalogue.product_category.display_order`; existing rows take 100. Set by `createProduct` (100 when not sent) and `updateProduct` (changed only when the body carries it; null stores null), and returned by every operation that answers `Product`, `getProduct` and the till's catalogue bundle included. No back-office product screen shows or edits it."},"isFeatured":{"type":"boolean","default":false,"description":"**The plan card's Most popular badge** (ADAM CR-482, decided by Chinmay on 2 November 2026): the venue marks a product featured. Stored on `catalogue.product` as `is_featured`, set by `createProduct` and `updateProduct`, returned by `listProducts` and `getProduct`. WEB-022 shows the badge on a featured plan."},"compareAtPrice":{"x-ticvai-column":"compare_at_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**What the same visits cost bought singly** (ADAM CR-482): the comparison price behind the plan card's saving. Stored on `catalogue.product` as `compare_at_amount` in the venue's trading currency, set by `createProduct` and `updateProduct`, returned by `listProducts` and `getProduct`. WEB-022 shows the saving as `compareAtPrice` minus `fromPrice` when `compareAtPrice` is the greater; null shows no saving, never a made-up value."},"highlightBadge":{"type":"object","nullable":true,"additionalProperties":{"type":"string","maxLength":20},"description":"**The card's highlight badge** (ADAM CR-504; Chinmay, 3 November 2026; CHG-CR504-001), e.g. POPULAR or BEST VALUE, keyed by ISO 639-1 code like `LocalisedText`, at most 20 characters per language (longer is `400 validation`). Stored in the nullable jsonb column `catalogue.product.highlight_badge`, set with `createProduct` and `updateProduct` by a caller holding `PRODUCT_CONFIGURE`, and answered by every operation that answers Product, to every audience. WEB-005's card shows the value for the guest's language, falling back to the English value, as the pill on the card image in capitals; null shows no badge."},"rating":{"type":"object","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"required":["average","count"],"properties":{"average":{"type":"number","minimum":1.0,"maximum":5.0,"multipleOf":0.1,"description":"The average rating, 1.0 to 5.0, one decimal."},"count":{"type":"integer","minimum":1,"description":"How many reviews the average is over."}},"description":"**The card's rating summary** (ADAM CR-504; Chinmay, 3 November 2026; CHG-CR504-001): readOnly, not stored on the product. `listProducts` answers it; every other operation answers null. It is null until the rating source is decided, and nothing invents a value meanwhile. WEB-005 shows it as the star line under the display tags (a star, the average, then `count` followed by reviews) whenever it is not null."},"nameLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"**The product's name in each of the tenant's enabled languages** (6 October 2026, CHG-R4-011; the tenant's languages, not the venue's: CHG-R8PRD-009, ADAM CR-213), keyed by ISO 639-1 code, e.g. `{\"en\": \"Aquarium entry\", \"ar\": \"دخول الأكواريوم\"}`. Every guest surface shows the entry for the guest's language and falls back to `name`, which stays the name staff search and reports print. Null, or a language missing from it, means `name` is shown. At most 200 characters per language, as `name`.\n"},"descriptionLocalised":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"The product's description in each language, as `nameLocalised`; falls back to `description` (6 October 2026, CHG-R4-011).\n"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-staff-only":"Omitted from the response when the caller is a guest or a visitor (R164).","description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-staff-only":"Omitted from the response when the caller is a guest or a visitor (R164)."},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"**The last moment the product's entitlements are valid; null means the same as `onSaleTo`** (ADAM CR-167 as the lead ruled it, 26 October 2026; CHG-R10OPN-003). A season pass stops selling at `onSaleTo` and is used until `validTo`: an entitlement template's `expiryAnchor` of `seasonEnd` ends here (`access#issueOrderEntitlements`). Sales closing is not validity ending.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`, as white-label `getPublishedBookingFlow`'s kind rule picks it where several of the venue's enabled defaults list the kind (ADAM CR-427, 31 October 2026). A venue that wants a different flow for a product sets this or the category's `bookingFlowId`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"x-ticvai-persistence-column":"jsonb","x-ticvai-persistence-kind":"valueObject","type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"addOnProductIds":{"type":"array","uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The add-ons offered with this product, in display order** (accepted 26 October 2026, Chinmay, ADAM CR-252 option A): each a `kind: addOn` product of the same venue (a coffee break, a working lunch, an AV technician offered with a meeting-room type), set in the back office. `listProducts` answers it, so WEB-048 and GST-075 read a room type's add-ons from the load they already make and fetch those products; the guest adds one as a cart line with `parentLineId`. An id that is not a `kind: addOn` product of the same venue is `400 validation` on `addOnProductIds`. Empty when none is offered."},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.event","description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."},"createdAt":{"type":"string","format":"date-time","readOnly":true,"description":"**When the product was created** (ADAM CR-204, option A, decided 25 October 2026; CHG-R10CAT-007): `catalogue.product.created_at`, NOT NULL DEFAULT now(), set by the server and never by a request. Rows that predate it are backfilled by the migration task (the earliest of the product's first version's `published_at` and the migration time), then the NOT NULL and the DEFAULT are set. `listProductLifecycle` orders and filters on it."},"updatedAt":{"type":"string","format":"date-time","readOnly":true,"nullable":true,"description":"**When the product last changed** (ADAM CR-204): set by `updateProduct` and by every product sub-resource PUT and bulk change that versions the product; null until the first change after creation. `listProductLifecycle`'s `lastModifiedAt` and `modifiedSince` read it."}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n\n**`walletTopUp` added 20 October 2026** (r8 re-walk, CHG-R8RW-001): the product a wallet top-up is sold as, so the money for a top-up is taken on an order like any other sale and `createPayment` has its `orderId`. A venue has one, with one variant. Orders prices its line at the line's `quotedUnitPrice` (the amount being loaded; no tax, since stored value is a liability and not a supply), and the line may share a sale with anything else (the client-approved till's \"Add top-up to sale\", CHG-R8RW-009); once the order is paid, wallet `topUpWallet` credits that line's amount, once per line. A value added to a response enum, so a breaking change under ADR-0026, approved as BC-460 to BC-462; a client that does not know it shows the product as a plain product.\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard","walletTopUp"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`.","x-ticvai-references":"assets.media_asset"},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"url":{"type":"string","format":"uri","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The asset's stable CDN address, for a guest card** (ADAM CR-221, option A, decided 25 October 2026; CHG-R10CAT-014): the asset library's public address for the asset, set on guest-facing reads (`searchCatalogue`, `listProducts` and `getProduct` for a guest or a visitor) when the asset is public and `ready`, as `getPublishedTenantConfig` returns white-label assets (`brandUrls`). Null otherwise, and on staff reads, which are unchanged. Catalogue reads the asset in process, a read the lead granted across deployables (XDR-005, 25 October 2026; CHG-R10CAT-015)."},"thumbnailUrl":{"type":"string","format":"uri","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The asset library's thumbnail address for the asset, on the same reads and with the same rule as `url` (ADAM CR-221)."},"altText":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"x-ticvai-data-class":"business","type":"string","maxLength":32,"nullable":true},"email":{"x-ticvai-data-class":"business","type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProductVariant": {"x-ticvai-persistence":"catalogue.variant","type":"object","required":["id","productId","sku","axisValues","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"listPrice":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**The list price on the caller's channel now**, resolved on read from the price lists (`listProductVariants`; R8 blocker cause GPS-C27, CHG-R8SPN-028). Not stored on the variant and ignored on input. Null where no price list prices it on that channel. The list price, not the total: promotions and bundles are applied at the basket."},"referencePrice":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The price a saving is measured against** (accepted 26 October 2026, Chinmay, ADAM CR-253 option C), set by the back office on the variant (`updateProductVariant`). Null where the variant claims no saving, which is the default. In the same currency as `listPrice`."},"savingPercent":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**Computed by the server, never in the browser** (ADAM CR-253): with a `referencePrice` and a `listPrice` below it, the whole percent the list price saves, `floor((referencePrice - listPrice) / referencePrice * 100)` (rounded down, so the label never overstates; proposed, client to correct); null otherwise. A length tile shows *Save n%* only when this is set."},"productId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"axisValues":{"type":"object","additionalProperties":{"type":"string"}},"name":{"type":"string","maxLength":150,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"},"isDefault":{"type":"boolean","default":false,"description":"Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"},"isActive":{"type":"boolean","description":"False when retired. Retired variants are never deleted — orders reference them."},"priceCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The variant's price category, a `catalogue.price_category` id (ADAM CR-455): the winning price assignment's category rate for it replaces the price (`catalogue#variantPriceRecords`); null for none. Set by `updateProductVariant`."},"description":{"allOf":[{"$ref":"#/components/schemas/catalogue::LocalisedText"}],"nullable":true,"description":"**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"}}},
"RevenueOptimizationCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Revenue Optimization Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"revenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Opportunity"},"incrementalRevenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Incremental Revenue Generated"},"activeOptimizations":{"type":"integer","description":"Active Optimizations"},"recommendationsAwaitingAction":{"type":"integer","description":"Recommendations Awaiting Action"},"pendingSimulations":{"type":"integer","description":"Pending Simulations"},"autoExecutedChanges":{"type":"integer","description":"Auto-Executed Changes"},"approvalRequired":{"type":"integer","description":"Approval Required: changes waiting for an approver"},"activeABTests":{"type":"integer","description":"Active A/B Tests"},"pricingExceptions":{"type":"integer","description":"Pricing Exceptions"},"revenueAtRisk":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue at Risk"},"forecastAccuracy":{"type":"number","description":"Forecast Accuracy over the last 30 days (decided 29 September, readiness close-out), percent"},"optimizationSuccessRate":{"type":"number","description":"Optimization Success Rate: executed changes with a positive measured outcome, percent"},"aiRevenueBrief":{"type":"array","items":{"type":"string"},"description":"AI Revenue Brief, e.g. AED 284,000 of opportunity in the next seven days. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"}}},
"RevenueOptimizationCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Revenue Optimization Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue"},"eventProduct":{"type":"string","description":"Event/Product"},"performance":{"type":"string","description":"Performance","nullable":true},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Price"},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Recommended Price"},"forecastRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast Revenue"},"expectedUplift":{"type":"number","description":"Expected Uplift, percent"},"confidence":{"type":"number","description":"Confidence, percent"},"automationMode":{"type":"string","description":"Automation Mode in force for this scope","enum":["advisory","humanInTheLoop","conditionalAutonomous","autonomous"]},"approvalStatus":{"type":"string","description":"Approval Status: notRequired, pending, approved or rejected. notRequired where the latest execution's source is conditionalAutonomous or autonomous; else pending for pending, sentToSimulation or sentForApproval, approved for accepted or modified, rejected for rejected (ADAM CR-408)"},"executionStatus":{"type":"string","description":"Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack, from the latest price_execution: scheduled queued, executing processing, deployed live, partiallyDeployed partial, failed failed, reverted rolledBack, none notStarted (ADAM CR-408)"},"revenueRisk":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Risk if no action is taken"},"eventProximity":{"type":"integer","description":"Event Proximity: days until the event"},"inventoryPosition":{"type":"number","description":"Inventory Position: remaining inventory, percent"},"demandVariance":{"type":"number","description":"Demand Variance against forecast, percent"},"urgency":{"type":"string","description":"Urgency","enum":["low","medium","high","critical"]},"optimizationId":{"type":"string","description":"Optimisation id"},"recommendationId":{"type":"string","description":"Recommendation id","nullable":true},"revenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Opportunity"},"priorityRank":{"type":"integer","description":"Priority rank (1 = act first)"},"nextAction":{"type":"string","description":"Suggested next action (the pack's Action column)","enum":["review","simulate","approve"]}}},
"SeatCategory": {"x-ticvai-persistence":"seating.seat_category","type":"object","required":["id","code","name","venueId","rank"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"venue"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"displayColour":{"type":"string","nullable":true},"rank":{"type":"integer","description":"Ordering for best-seat assignment. Lower is better."},"seatCount":{"type":"integer"},"priceBands":{"type":"array","description":"What a seat in this category costs, by band (decided 28 September, audit R275 (d), from the BO-1045 pack). Written by `createSeatCategory` and `updateSeatCategory`. A band may be narrowed to a sales channel or a customer segment and to a window; where several match a sale, the narrowest wins.\n","items":{"$ref":"#/components/schemas/SeatPriceBand"}}}},
"SeatPriceBand": {"x-ticvai-rls":"grant-holder-read","x-ticvai-persistence":"seating.seat_price_band","x-ticvai-unique-together":[["seatCategoryId","code"]],"type":"object","description":"One price band on a seat category (decided 28 September, audit R275 (d)). The currency is `amount.currency`, resolved from the region like every `Money` (ADR-0018), so the band carries no currency of its own.\n","required":["code","displayLabel","amount","effectiveFrom","scopePath"],"properties":{"scopePath":{"type":"string","readOnly":true,"description":"Where the row is owned: the path of the scope that wrote it (its venue, or the region or tenant that configured it), set by the server from the caller's scope and never taken from a request. Row-level security reads it, so a venue writes and reads its own rows (MOD audit, 14 October 2026, CHG-MOD-007)."},"id":{"type":"string","format":"uuid","readOnly":true},"seatCategoryId":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64,"description":"Unique within the category."},"displayLabel":{"type":"string","maxLength":200},"displayColour":{"type":"string","nullable":true,"pattern":"^#[0-9A-Fa-f]{6}$"},"amount":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"nullable":true,"description":"Null means every channel.","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}]},"customerSegmentId":{"type":"string","format":"uuid","nullable":true,"description":"A `marketing-crm` customer segment; null means everyone."},"effectiveFrom":{"type":"string","format":"date-time"},"effectiveTo":{"type":"string","format":"date-time","nullable":true,"description":"Null means open-ended."}}}
}
```
