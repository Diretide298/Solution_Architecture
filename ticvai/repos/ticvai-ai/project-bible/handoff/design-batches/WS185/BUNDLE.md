# WS185 — Upsell,CrossSellEngine board 6

**10 screens · 10 operations · 10 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, AI_USE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-689` | Recommendation Performance Command Center | B–D | 2 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-690` | Recommendation Strategy & Placement Analytics | B–D | 0 | 30 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-691` | Recommendation Experiment & A/B Test Studio | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-692` | Experiment Results & Winner Decision Workspace | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-693` | Recommendation Attribution & Incrementality Analytics | B–D | 5 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-694` | AI Model Performance & Drift Monitor | B–D | 0 | 24 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `ADM-695` | Recommendation Governance & Deployment Control | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-696` | AI Risk, Fairness, Explainability & Safety Center | B–D | 3 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-697` | Recommendation Audit, Decision Trace & Investigation | B–D | 2 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-698` | AI Optimization & Recommendation Intelligence Lab | B–D | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-690, ADM-694, ADM-697 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-689` Recommendation Performance Command Center

**Provide executive and operational visibility across the complete Recommendation Engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-performance-command-center-adm-689` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Executive view of the recommendation engine.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getRecommendationPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getRecommendationPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search recommendation performance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by upsell, cross-sell, membership, bundle, f&b, retail and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

#### Outputs: what the screen shows and produces

**Shown**

**Recommendations Generated** (metric tile)

**Recommendations Presented** (metric tile)

**Recommendations Accepted** (metric tile)

**Recommendation Conversion** (metric tile)

**Upsell Revenue** (metric tile)

**Cross-Sell Revenue** (metric tile)

**Estimated Incremental Revenue** (metric tile)

**AOV Uplift** (metric tile)

**Attach Rate** (metric tile)

**Incremental Margin** (metric tile)

**AI Recommendation Share** (metric tile)

**Rule-Based Recommendation Share** (metric tile)

**Suppression Rate** (metric tile)

**Active Experiments** (metric tile)

**Model Health** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPIs**: As ADM-639. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance)*

**Data it reads**: `getRecommendationPerformance` (onLoad, The headline numbers)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-690` Recommendation Strategy & Placement Analytics: *Recommendation Strategy & Placement Analytics*
- → `ADM-691` Recommendation Experiment & A/B Test Studio: *Recommendation Experiment & A/B Test Studio*
- → `ADM-692` Experiment Results & Winner Decision Workspace: *Experiment Results & Winner Decision Workspace*
- → `ADM-693` Recommendation Attribution & Incrementality Analytics: *Recommendation Attribution & Incrementality Analytics*
- → `ADM-694` AI Model Performance & Drift Monitor: *AI Model Performance & Drift Monitor*
- → `ADM-695` Recommendation Governance & Deployment Control: *Recommendation Governance & Deployment Control*
- → `ADM-696` AI Risk, Fairness, Explainability & Safety Center: *AI Risk, Fairness, Explainability & Safety Center*
- → `ADM-697` Recommendation Audit, Decision Trace & Investigation: *Recommendation Audit, Decision Trace & Investigation*
- → `ADM-698` AI Optimization & Recommendation Intelligence Lab: *AI Optimization & Recommendation Intelligence Lab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  incremental: AED 96,000.00 a month
```

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-689` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-689`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 1: Opens Recommendation Performance Command Center → Provide executive and operational visibility across the complete Recommendation Engine.
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F292 branch at step 1 (expected): when Nothing has been set up on Recommendation Performance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F292 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-689?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-690`, `ADM-691`, `ADM-692`, `ADM-693`, `ADM-694`, `ADM-695`, `ADM-696`, `ADM-697`, `ADM-698`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-690` Recommendation Strategy & Placement Analytics

**Determine which recommendation strategies, placements, channels and journey stages perform best.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-strategy-placement-analytics-adm-690` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Which strategies, placements, channels and stages perform best.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getRecommendationPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getRecommendationPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every recommendation strategy placement** (data table)

| Shows | Format | Notes |
|---|---|---|
| Ticket selection | text | not in the schema: `Ticket Selection` |
| Cart | text | not in the schema: `Cart` |
| Checkout | text | not in the schema: `Checkout` |
| Confirmation | text | not in the schema: `Confirmation` |
| Pre visit | text | not in the schema: `Pre-Visit` |
| Mobile app | text | not in the schema: `Mobile App` |
| In venue | text | not in the schema: `In-Venue` |
| Post visit | text | not in the schema: `Post-Visit` |
| B2 c | text | not in the schema: `B2C` |
| App | text | not in the schema: `App` |
| POS | text | not in the schema: `POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| B2 b | text | not in the schema: `B2B` |
| Call center | text | not in the schema: `Call Center` |
| Api/partner | text | not in the schema: `API/Partner` |

**The selected recommendation strategy placement** (detail panel): The pack groups this record's detail under its own headings: “Strategy”, “Max”, “Relevance”, “Cart conversion”, “Checkout conversion”.

| Shows | Format | Notes |
|---|---|---|
| Ticket selection | text | not in the schema: `Ticket Selection` |
| Cart | text | not in the schema: `Cart` |
| Checkout | text | not in the schema: `Checkout` |
| Confirmation | text | not in the schema: `Confirmation` |
| Pre visit | text | not in the schema: `Pre-Visit` |
| Mobile app | text | not in the schema: `Mobile App` |
| In venue | text | not in the schema: `In-Venue` |
| Post visit | text | not in the schema: `Post-Visit` |
| B2 c | text | not in the schema: `B2C` |
| App | text | not in the schema: `App` |
| POS | text | not in the schema: `POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| B2 b | text | not in the schema: `B2B` |
| Call center | text | not in the schema: `Call Center` |
| Api/partner | text | not in the schema: `API/Partner` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **breakdown**: By strategy and placement. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance)*

**Data it reads**: `getRecommendationPerformance` (onLoad, By strategy and placement)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation strategy placement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation strategy placement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation strategy placement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation strategy placement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  placement: checkout
  acceptance: 11%
```

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-690` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-690`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 2: Works in Recommendation Strategy & Placement Analytics → Determine which recommendation strategies, placements, channels and journey stages perform best.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-690?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-691` Recommendation Experiment & A/B Test Studio

**Allow TICVAI to scientifically test recommendation strategies rather than relying only on assumptions. Increase Family Meal cross-sell.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Measure) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-experiment-a-b-test-studio-adm-691` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**Known gaps.** **Recommendation Experiment & A/B Test Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A/B tests of recommendation strategies; allocation fixed at creation.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRecommendationExperiments return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRecommendationExperiments; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Conversion** (metric tile)

**Attach rate** (metric tile)

**Net revenue** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Incremental revenue** (metric tile)

**AOV** (metric tile)

**Margin** (metric tile)

**Customer response** (metric tile)

**Recommendation fatigue** (metric tile)

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Create experiment**: Strategies and split; allocation cannot change afterwards. *(source: contracts/satellite/promotions.yaml#createRecommendationExperiment)*

**Data it reads**: `listRecommendationExperiments` (onLoad, Experiments running)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation experiment test list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation experiment test untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation experiment test yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation experiment test are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
experiment:
  goal: Increase family meal cross-sell
  split: 50/50
```

#### Permissions

- `listRecommendationExperiments` → `PRODUCT_VIEW` (read) · staff
- `createRecommendationExperiment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.24 | System shall support recommendation A/B testing. | Unified Operations Dashboard | CONTRACTED | `createRecommendationExperiment` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-691` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-691`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 4: Works in Recommendation Experiment & A/B Test Studio → Allow TICVAI to scientifically test recommendation strategies rather than relying only on assumptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-691?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-692` Experiment Results & Winner Decision Workspace

**Evaluate experiments and decide whether a recommendation strategy should be deployed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `experimentId` (navigation) |
| Route | `/commercial/experiment-results-winner-decision-workspace-adm-692` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Evaluate experiments and declare a winner explicitly.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRecommendationExperiments return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRecommendationExperiments; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Declare Winner, Extend Test, Stop Test, Reject Result, Create Deployment Draft, Send for Approval. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Declare winner**: Rolls the winner out. *(source: contracts/satellite/promotions.yaml#concludeRecommendationExperiment)*

**Data it reads**: `listRecommendationExperiments` (onLoad, Results so far)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The experiment results winner list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the experiment results winner untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No experiment results winner yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the experiment results winner are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `winningVariant` does not name one of the experiment's own variants.; 409 The experiment is not `running`. A draft never ran, and a concluded or abandoned experiment already has its outcome. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  winner: B
  uplift: +1.8 pts
  significance: 95%
```

#### Permissions

- `listRecommendationExperiments` → `PRODUCT_VIEW` (read) · staff
- `concludeRecommendationExperiment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-692` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-692`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 6: Works in Experiment Results & Winner Decision Workspace → Evaluate experiments and decide whether a recommendation strategy should be deployed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-692?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-693` Recommendation Attribution & Incrementality Analytics

**Determine whether a recommendation genuinely created additional commercial value. This is essential. A customer purchasing a recommended product does not automatically mean the recommendation caused the purchase.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/recommendation-attribution-incrementality-analytics-adm-693` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Recommendation tracking ID, Last recommendation, First recommendation, A/B experiment. Each needs an …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether recommendations created extra value: attributed vs incremental.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Recommendation tracking ID, Last recommendation, First recommendation, A/B experiment.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-693; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) getRecommendationPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getRecommendationPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Same session | select field | — | — | — | — | — | — |
| 24 hours | select field | — | — | — | — | — | — |
| 7 days | select field | — | — | — | — | — | — |
| Until visit | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Recommendation tracking ID (primary button) | navigation or local | — | — | — | — |
| Last recommendation (secondary button) | navigation or local | — | — | — | — |
| First recommendation (secondary button) | navigation or local | — | — | — | — |
| A/B experiment (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **incrementality**: Attributed and incremental shown apart. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance)*

**Data it reads**: `getRecommendationPerformance` (onLoad, Attributed against incremental)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation attribution incrementality configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation attribution incrementality untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation attribution incrementality configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result:
  attributed: AED 312,000.00
  incremental: AED 96,000.00
```

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-693` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-693`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 8: Works in Recommendation Attribution & Incrementality Analytics → Determine whether a recommendation genuinely created additional commercial value. This is essential. A customer purchasing a recommended product does not automatically mean the recommendation caused …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-693?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Recommendation tracking ID, Last recommendation, First recommendation, A/B experiment.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-694` AI Model Performance & Drift Monitor

**Monitor whether recommendation and propensity models continue performing correctly after deployment. This screen is critical if TICVAI wants a serious AI architecture.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show; Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-model-performance-drift-monitor-adm-694` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Contract gap recorded 2 October 2026 (CHG-WIR-027): An AI model performance and drift read (ai process); getRecommendationPerformance carries no model metrics.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recommendation and propensity model performance and drift after deployment.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) getRecommendationPerformance return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of getRecommendationPerformance carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Model drift is read from recommendation performance, which carries no model metrics. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getRecommendationPerformance` ?from |
| To | date and time picker | — | — | `getRecommendationPerformance` ?to |
| Group by | radio group | — | Strategy · Placement · Channel · Product · Experiment | `getRecommendationPerformance` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every model performance drift** (data table)

| Shows | Format | Notes |
|---|---|---|
| Model | text | not in the schema: `Model` |
| Version | text | not in the schema: `Version` |
| Purpose | text | not in the schema: `Purpose` |
| Deployment date | text | not in the schema: `Deployment date` |
| Status | text | not in the schema: `Status` |
| Last evaluation | text | not in the schema: `Last evaluation` |
| Data freshness | text | not in the schema: `Data freshness` |
| Input drift | text | not in the schema: `Input drift` |
| Behavioral drift | text | not in the schema: `Behavioral drift` |
| Performance drift | text | not in the schema: `Performance drift` |
| Segment drift | text | not in the schema: `Segment drift` |
| Product mix change | text | not in the schema: `Product mix change` |

**The selected model performance drift** (detail panel): The pack groups this record's detail under its own headings: “Models Could Include”.

| Shows | Format | Notes |
|---|---|---|
| Model | text | not in the schema: `Model` |
| Version | text | not in the schema: `Version` |
| Purpose | text | not in the schema: `Purpose` |
| Deployment date | text | not in the schema: `Deployment date` |
| Status | text | not in the schema: `Status` |
| Last evaluation | text | not in the schema: `Last evaluation` |
| Data freshness | text | not in the schema: `Data freshness` |
| Input drift | text | not in the schema: `Input drift` |
| Behavioral drift | text | not in the schema: `Behavioral drift` |
| Performance drift | text | not in the schema: `Performance drift` |
| Segment drift | text | not in the schema: `Segment drift` |
| Product mix change | text | not in the schema: `Product mix change` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **drift**: Model metrics over time with drift alerts. *(source: contracts/satellite/promotions.yaml#getRecommendationPerformance)*

**Data it reads**: `getRecommendationPerformance` (onLoad, Model performance over time)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The model performance drift list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the model performance drift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No model performance drift yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the model performance drift are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
model:
  name: Propensity v2
  auc: 0.78
  drift: low
```

#### Permissions

- `getRecommendationPerformance` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.21 | System shall support recommendation performance analytics. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.27 | System shall support recommendation dashboards. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |
| 8.6.28 | System shall support recommendation reporting. | Unified Operations Dashboard | CONTRACTED | `getRecommendationPerformance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-694` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-694`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 10: Works in AI Model Performance & Drift Monitor → Monitor whether recommendation and propensity models continue performing correctly after deployment. This screen is critical if TICVAI wants a serious AI architecture.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-694?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-695` Recommendation Governance & Deployment Control

**Control how new strategies, rules, models and AI changes move into production.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor) and no metric row |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/commercial/recommendation-governance-deployment-control-adm-695` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Channel rollout, Venue rollout. Each needs an operation, or needs removing from the screen; this is the … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How strategies, rules and models move into production.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Channel rollout, Venue rollout.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-695; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listRecommendationStrategies return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/promotions.yaml#listRecommendationStrategies; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every recommendation governance deployment** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected recommendation governance deployment** (detail panel): The pack groups this record's detail under its own headings: “Draft”, “Testing”, “Simulation”, “Approval”, “Scheduled”, “Active”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Channel rollout (primary button) | navigation or local | — | — | — | — |
| Venue rollout (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Change strategy**: Validate-only first, then save. *(source: contracts/satellite/promotions.yaml#updateRecommendationStrategy)*

**Data it reads**: `listRecommendationStrategies` (onLoad, What is deployed where)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation governance deployment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation governance deployment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation governance deployment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation governance deployment are still there. The pack's own statuses are Recommendation strategy — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
change:
  strategy: Checkout add-ons
  version: 4
  state: awaiting approval
```

#### Permissions

- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff
- `updateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-695` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-695`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 12: Works in Recommendation Governance & Deployment Control → Control how new strategies, rules, models and AI changes move into production.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-695?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Channel rollout, Venue rollout.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-696` AI Risk, Fairness, Explainability & Safety Center

**Provide governance over how AI recommendation decisions behave across customer populations and business contexts.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE` (2 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionId` (navigation), `capabilityKey` (navigation), `releaseId` (navigation) |
| Route | `/commercial/ai-risk-fairness-explainability-safety-center-adm-696` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Disable model, Disable recommendation type, Disable specific relationship, Raise confidence threshold … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Risk, fairness and safety for recommendations: how decisions behave across customer groups and contexts, and the controls to disable a model, a recommendation type or a relationship, raise the confidence threshold or suspend. The one thing to get right: each control states its effect (e.g. "Disable model - the rules answer takes over"), and emergency suspend is the same kill switch as elsewhere.

**Fixed on main** (the package already carries these; draw what it says): Disable / raise threshold / suspend buttons bind no operation; only explainRecommendationDecision is declared. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**Form: Suspend** (modal, opened by *Suspend*; *Suspend* calls `pauseAiCapability`, *Cancel* sends nothing)

**Collects what `pauseAiCapability` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `pauseAiCapability` body |
| Incident `incidentId` | picker: choose an incident | optional | — | — | shows names, sends the id | — | `pauseAiCapability` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already paused.

**Form: Roll back** (modal, opened by *Roll back*; *Roll back* calls `rollbackAiRelease`, *Cancel* sends nothing)

**Collects what `rollbackAiRelease` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `rollbackAiRelease` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back to (`no-previous-release`).

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Disable model (destructive button) | navigation or local | — | — | — | — |
| Disable recommendation type (destructive button) | navigation or local | — | — | — | — |
| Disable specific relationship (destructive button) | navigation or local | — | — | — | — |
| Raise confidence threshold (secondary button) | navigation or local | — | — | — | — |
| Emergency suspend (secondary button) | navigation or local | — | — | — | — |
| Suspend (secondary button) | `pauseAiCapability` POST `/governance/capabilities/{capabilityKey}/pause` | inline | AiCapabilityRegistration | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already paused. | opens modal first |
| Roll back (secondary button) | `rollbackAiRelease` POST `/releases/{releaseId}/rollback` | inline | AiRelease | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back to (`no-previous-release`). | opens modal first |

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Emergency suspend / Disable model**: Pauses the recommendation capability (slot left empty) or rolls back the model release to the rules answer. *(source: contracts/satellite/ai.yaml#pauseAiCapability / contracts/satellite/ai.yaml#rollbackAiRelease)*

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

**What opens over it**

- confirmDialog *Disable model*: **Disable model on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable recommendation type*: **Disable recommendation type on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Disable specific relationship*: **Disable specific relationship on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The risk fairness explainability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the risk fairness explainability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No risk fairness explainability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the risk fairness explainability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already paused.; 409 Nothing to roll back to (`no-previous-release`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
check: Offer rate by nationality group within ±5% of overall; no group excluded from membership offers
```

#### Permissions

- `explainRecommendationDecision` → `AI_USE` (operate) · staff
- `pauseAiCapability` → `AI_CONFIGURE` (configure) · staff
- `rollbackAiRelease` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.20 | System shall support recommendation explainability. | Unified Operations Dashboard | CONTRACTED | `explainRecommendationDecision` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-696` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-696`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 14: Works in AI Risk, Fairness, Explainability & Safety Center → Provide governance over how AI recommendation decisions behave across customer populations and business contexts.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-696?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Disable model, Disable recommendation type, Disable specific relationship, Raise confidence threshold, Emergency suspend, Suspend, Roll back.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-697` Recommendation Audit, Decision Trace & Investigation

**Provide transaction-level explainability for Customer Service, Commercial, Audit, and technical investigation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionId` (navigation) |
| Route | `/commercial/recommendation-audit-decision-trace-investigation-adm-697` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Transaction-level investigation of a recommendation for support, commercial and audit: find it by recommendation id, transaction, customer or session (where permitted), product, channel, model or strategy, and see the full explanation. The one thing to get right: customer search is permission-gated and the explanation shows each candidate removal with its rule.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search recommendation audit decision | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by recommendation id, transaction, customer/session where permitted, ticket, product, date and 3 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **explanation**: Candidates, removals with reasons, ranking, the template reason shown to the guest, and what the guest did (shown, clicked, added, declined, bought). *(source: contracts/satellite/ai.yaml#explainRecommendationDecision / MoM 21 Sep 4.6)*

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation audit decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation audit decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation audit decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation audit decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
decision:
  id: rd-55a1
  shown:
  - Family Day Pass
  - Locker
  removed:
  - VIP Tour - capacity 0
  - Annual Pass - already owned
  guest: added Family Day Pass
```

#### Permissions

- `explainRecommendationDecision` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.20 | System shall support recommendation explainability. | Unified Operations Dashboard | CONTRACTED | `explainRecommendationDecision` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-697` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-697`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 16: Works in Recommendation Audit, Decision Trace & Investigation → Provide transaction-level explainability for Customer Service, Commercial, Audit, and technical investigation.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-697?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-698` AI Optimization & Recommendation Intelligence Lab

**Turn all Recommendation Engine data into actionable improvement opportunities. This is the final optimization screen for Module 2.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track; Measure) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/ai-optimization-recommendation-intelligence-lab-adm-698` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Simulate, Create Experiment, Create Draft, Send for Approval, Dismiss, Snooze. Each needs an operation, or … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Recommendation data turned into improvement opportunities.

**Known correction pending (do not draw the wrong version)**

- **Pack actions with no operation: Simulate, Create Experiment, Create Draft, Send for Approval, Dismiss, Snooze.** Why: The workshop pack names them on this screen and no operation serves them; each needs an operation or removal from the screen. *(source: screens/P08-venue-back-office.yaml#ADM-698; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only simulateRecommendationStrategy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRecommendationStrategies` ?status |
| Placement | text field | — | — | `listRecommendationStrategies` ?placement |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every optimization recommendation intelligence** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Strategies** (data table, from `listRecommendationStrategies`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Objective | chip: Attach revenue, Average order value, Upgrade rate, Visit frequency, Inventory … | — |
| Kinds | list or chips (count when long) | — |
| Item kinds | list or chips (count when long) | What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18) … |
| Placements | list or chips (count when long) | `homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements … |
| Channels | list or chips (count when long) | — |
| Max recommendations | 1,234 | A guardrail before it is a layout choice. Nine upsells at checkout is not a denser page, it is an abandoned basket. |
| Min confidence | 1,234.5 | — |
| Ranking weights | grouped details | Propensity, margin, inventory pressure, affinity, recency. |
| Require availability | yes / no (icon or chip) | — |
| Exclude in basket | yes / no (icon or chip) | — |
| Guardrails | grouped details | — |
| Max discount percent | 1,234.5 | — |
| Min margin percent | 1,234.5 | — |
| Never recommend categorys | list or chips (count when long) | — |
| Require human approval | yes / no (icon or chip) | — |
| Status | chip: Draft, Active, Paused, Retired | — |
| Effective from | 1 Oct 2026 | — |

**The selected optimization recommendation intelligence** (detail panel): The pack groups this record's detail under its own headings: “Product Relationships”, “Ranking”, “Journey”, “Timing”, “Suppression”, “Strategy”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Simulate (primary button) | navigation or local | — | — | — | — |
| Create Experiment (secondary button) | navigation or local | — | — | — | — |
| Create Draft (secondary button) | navigation or local | — | — | — | — |
| Send for Approval (secondary button) | navigation or local | — | — | — | — |
| Dismiss (secondary button) | navigation or local | — | — | — | — |
| Snooze (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Simulate improvement**: As ADM-648. *(source: contracts/satellite/promotions.yaml#simulateRecommendationStrategy)*

**Data it reads**: `listRecommendationStrategies` (onLoad, The strategies a simulation can replay)

**Where the user goes next**

- → `ADM-689` Recommendation Performance Command Center: *Back to Recommendation Performance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The optimization recommendation intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the optimization recommendation intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No optimization recommendation intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the optimization recommendation intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
opportunity: 'Move Fast Track to the product page: +AED 4,100.00 a week'
```

#### Permissions

- `simulateRecommendationStrategy` → `PRODUCT_CONFIGURE` (configure) · staff
- `listRecommendationStrategies` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-698` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-698`
- Workshop pack: Upsell,CrossSellEngine.pdf board 6
- Flow F292 *Upsell,CrossSellEngine board 6: Recommendation Performance Command Center*, step 18: Works in AI Optimization & Recommendation Intelligence Lab → Turn all Recommendation Engine data into actionable improvement opportunities. This is the final optimization screen for Module 2.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-698?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Simulate, Create Experiment, Create Draft, Send for Approval, Dismiss, Snooze.
- [ ] Every transition is wired: `ADM-689`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"concludeRecommendationExperiment": {"method":"POST","path":"/recommendation-experiments/{experimentId}/conclude","contract":"promotions","summary":"Declare a winner and roll it out","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationExperiment"},
"createRecommendationExperiment": {"method":"POST","path":"/recommendation-experiments","contract":"promotions","summary":"Split traffic between strategies","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecommendationExperiment","responds":"RecommendationExperiment"},
"explainRecommendationDecision": {"method":"GET","path":"/recommendations/decisions/{decisionId}/explanation","contract":"ai","summary":"Why these recommendations","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiRecommendationExplanation"},
"getRecommendationPerformance": {"method":"GET","path":"/recommendation-performance","contract":"promotions","summary":"Impressions, acceptance, revenue and incremental lift","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"listRecommendationExperiments": {"method":"GET","path":"/recommendation-experiments","contract":"promotions","summary":"A/B tests on placements and strategies","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RecommendationExperiment"},
"listRecommendationStrategies": {"method":"GET","path":"/recommendation-strategies","contract":"promotions","summary":"The strategies deciding what gets offered where","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"placement","in":"query","required":null}],"requestBody":null,"responds":"RecommendationStrategy"},
"pauseAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/pause","contract":"ai","summary":"Stop a capability now","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"rollbackAiRelease": {"method":"POST","path":"/releases/{releaseId}/rollback","contract":"ai","summary":"Roll a release back","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRelease"},
"simulateRecommendationStrategy": {"method":"POST","path":"/recommendation-simulations","contract":"promotions","summary":"Replay a strategy against history before it goes live","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecommendationPerformance"},
"updateRecommendationStrategy": {"method":"PUT","path":"/recommendation-strategies/{strategyId}","contract":"promotions","summary":"Change a strategy","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RecommendationStrategy","responds":"RecommendationStrategy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRecommendationExplanation": {"type":"object","x-ticvai-persistence":"none — built from ai.rec_decision and its decision record","description":"Why these items (AIR-193..202), at three depths each gated by permission (AIC-195): business, governance, technical.","required":["decisionId","depth"],"properties":{"decisionId":{"type":"string","format":"uuid"},"depth":{"type":"string","enum":["business","governance","technical"]},"funnel":{"type":"object","additionalProperties":true},"exclusions":{"type":"object","additionalProperties":true},"items":{"type":"array","items":{"type":"object","properties":{"trackingId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"reasons":{"type":"array","items":{"type":"string"}},"scoreBreakdown":{"type":"object","additionalProperties":true,"nullable":true}}}},"versions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Strategy, model and feature-set versions. `technical` depth only."}}},
"AiRelease": {"type":"object","x-ticvai-persistence":"ai.release","description":"**The release pointer per capability and tenant** (design 3.5): draft, offline evaluation, shadow, canary, production, monitored. Rollback is a pointer switch. **A model goes live only when a person promotes it** (design 3.12, decided 29 September).","required":["capabilityKey","artefactKind","candidateRef","layer","stage"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"artefactKind":{"type":"string","enum":["model","prompt","routing","embedding","retrieval","rule"]},"candidateRef":{"type":"string"},"currentRef":{"type":"string","nullable":true,"description":"What production runs now: the rule, or the previously promoted artefact."},"previousRef":{"type":"string","nullable":true,"readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"nullable":true,"description":"**Whose AI this release is, and so who promotes it** (Chinmay, 2 October, workbook Q7: \"AI release promotion goes to whoever holds it\"; CHG-FUP-004). For a tenant release, `promoteAiRelease` requires the permission `contracts/shared/permissions.yaml` `x-ticvai-module-ai-publish` names for this module; a tenant release with no module cannot be promoted (`409 module-required`). Set when the release is registered, from the capability's module. Null on a platform release, which `PLATFORM_AI_MANAGE` promotes."},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true,"description":"Where the capability answers a `requestSuggestion` kind: promotion rewrites that kind's assignment in `AiPolicy.suggestionProviders`."},"stage":{"type":"string","enum":["draft","offlineEval","shadow","canary","production","monitored","rolledBack","rejected"],"readOnly":true},"shadowStartedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"gatePassedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the shadow run passed its gate and `promotionReady` was raised."},"canaryScope":{"type":"object","additionalProperties":true,"nullable":true,"description":"Venues or share of traffic in canary."},"promotedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"promotedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"rolledBackByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"rolledBackAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"RecommendationExperiment": {"type":"object","x-ticvai-persistence":"promotions.recommendation_experiment","description":"Boards 6.3 and 6.4. **Fixed allocation, explicit conclusion, and a holdout.**","required":["code","variants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"placement":{"type":"string","nullable":true},"variants":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"strategyId":{"type":"string","format":"uuid","nullable":true},"allocationPercent":{"type":"integer"}}}},"holdoutPercent":{"type":"integer","default":5},"primaryMetric":{"type":"string"},"minimumSampleSize":{"type":"integer","nullable":true},"startedAt":{"type":"string","format":"date-time","nullable":true},"endedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["draft","running","concluded","abandoned"]},"winningVariant":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"RecommendationPerformance": {"type":"object","description":"Board 6.5. **Attributed and incremental reported apart** — the first flatters.","properties":{"key":{"type":"string"},"label":{"type":"string"},"impressions":{"type":"integer"},"clicks":{"type":"integer"},"accepted":{"type":"integer"},"acceptanceRate":{"type":"number"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"holdoutAcceptanceRate":{"type":"number","nullable":true},"lift":{"type":"number","nullable":true}}},
"RecommendationStrategy": {"type":"object","x-ticvai-persistence":"promotions.recommendation_strategy","description":"Upsell board 1. **Objective, placement, ranking and guardrail in one record**, because any one of them alone produces a recommender that is either aimless or dangerous.\n","required":["code","name","objective"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"objective":{"type":"string","enum":["attachRevenue","averageOrderValue","upgradeRate","visitFrequency","inventoryBalance","guestSatisfaction"]},"kinds":{"type":"array","items":{"type":"string","enum":["upsell","upgrade","crossSell","bundle","nextBestOffer","reactivation"]}},"itemKinds":{"type":"array","description":"What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour before), `offer` (a live promotion marked `recommendable`), `reward` (a marketing-crm loyalty reward the guest can redeem) and `challenge` (a challenge they can join). Mirrors `ai.decideRecommendations` item kinds.","default":["product"],"items":{"type":"string","enum":["product","offer","reward","challenge"]}},"placements":{"type":"array","description":"`homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills.","items":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisitEmail","inVenueApp","kiosk","pos","signage","callCentre","homepage","loyalty"]}},"channels":{"type":"array","items":{"type":"string"}},"maxRecommendations":{"type":"integer","default":3,"description":"**A guardrail before it is a layout choice.** Nine upsells at checkout is not a denser page, it is an abandoned basket.\n"},"minConfidence":{"type":"number","nullable":true},"rankingWeights":{"type":"object","additionalProperties":{"type":"number"},"description":"Propensity, margin, inventory pressure, affinity, recency."},"requireAvailability":{"type":"boolean","default":true},"excludeInBasket":{"type":"boolean","default":true},"guardrails":{"type":"object","properties":{"maxDiscountPercent":{"type":"number","nullable":true},"minMarginPercent":{"type":"number","nullable":true},"neverRecommendCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requireHumanApproval":{"type":"boolean","default":false}}},"status":{"type":"string","enum":["draft","active","paused","retired"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]}
}
```
