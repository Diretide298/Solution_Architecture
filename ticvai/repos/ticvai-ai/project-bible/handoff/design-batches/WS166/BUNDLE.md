# WS166 — Seat Management Venue Mapping Reference v1.0 board 2

**10 screens · 14 operations · 20 schemas · 3 permissions**

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
  `AI_USE, CAPACITY_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-963` | Import Command Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-964` | PDF & Image Import | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-965` | SVG & CAD Import | B–D | 0 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `BO-966` | CSV & Excel Import | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-967` | AI Section Recognition | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-968` | AI Row & Seat Recognition | B–D | 0 | 0 | 6 | 6 | 2 | 6 | — | notStarted (—) |
| `BO-969` | AI Aisle, VIP & Accessibility | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-970` | AI Numbering & Labeling | B–D | 0 | 0 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `BO-971` | Validation & Correction | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-972` | AI Venue Designer & Publish | B–D | 0 | 38 | 6 | 1 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-963, BO-964, BO-965, BO-966, BO-967, BO-968, BO-969, BO-970, BO-971 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-963` Import Command Center

**Monitor every seat-map import from submission to publication. Show queued, processing, completed, failed and review-required jobs with source format, venue, owner and elapsed time. Display average confidence, issue counts, model version and jobs blocked by malware, unsupported content or validation failures. Support retry, cancel, duplicate, assign reviewer, open result and download controlled error reports. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `importId` (navigation), `jobId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/import-command-center-bo-963` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every seat map import from submission to publication: queued, processing, review required, completed, failed; what was detected, confidence, what could not be read.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **import jobs**: Source format, venue, owner, elapsed, outcome; an unreadable list with low confidence is shown differently from a named failure. *(source: contracts/satellite/seating.yaml#getSeatMapImport / contracts/satellite/seating.yaml#getImportJob)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-964` PDF & Image Import: *PDF & Image Import*; carries `jobId`, `seatMapId`
- → `BO-965` SVG & CAD Import: *SVG & CAD Import*; carries `jobId`, `seatMapId`
- → `BO-966` CSV & Excel Import: *CSV & Excel Import*; carries `jobId`, `seatMapId`
- → `BO-967` AI Section Recognition: *AI Section Recognition*; carries `importId`, `seatMapId`
- → `BO-968` AI Row & Seat Recognition: *AI Row & Seat Recognition*; carries `importId`, `seatMapId`
- → `BO-969` AI Aisle, VIP & Accessibility: *AI Aisle, VIP & Accessibility*; carries `importId`, `seatMapId`
- → `BO-970` AI Numbering & Labeling: *AI Numbering & Labeling*; carries `seatMapId`
- → `BO-971` Validation & Correction: *Validation & Correction*; carries `importId`, `seatMapId`
- → `BO-972` AI Venue Designer & Publish: *AI Venue Designer & Publish*; carries `jobId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The import list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the import untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No import yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the import are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
job:
  file: amphitheatre-seating.pdf
  status: reviewRequired
  seats: 3142
  confidence: 0.88
```

#### Permissions

- `getSeatMapImport` → `PRODUCT_VIEW` (read) · staff
- `getImportJob` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-963` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-963`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 1: Opens Import Command Center → Monitor every seat-map import from submission to publication. Show queued, processing, completed, failed and review-required jobs with source format, venue, owner and elapsed time. Display average …
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F275 branch at step 1 (expected): when Nothing has been set up on Import Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F275 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-963?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-964`, `BO-965`, `BO-966`, `BO-967`, `BO-968`, `BO-969`, `BO-970`, `BO-971`, `BO-972`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-964` PDF & Image Import

**Ingest PDF, PNG, JPG and supported scanned map sources. Provide drag-and-drop upload, page selection, preview, crop, rotation, de-skew, contrast and noise-reduction controls. Calibrate scale using known distance, dimensions or reference objects and capture venue orientation and focal point. Require file validation, malware scanning, size limits and a clear unsupported-or-low-quality recovery path. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `jobId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/pdf-image-import-bo-964` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Import a PDF or image plan, with an Excel or CSV seat manifest, into a draft map a person accepts.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **source and manifest**: Plan file plus optional manifest (section, row, seat); scale calibrated from a known dimension. *(source: contracts/satellite/seating.yaml#importSeatMap / DI-145 / TRACKER Actions row 110)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import seat map (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `jobId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pdf image import list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pdf image import untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pdf image import yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pdf image import are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
import:
  plan: SampleAmphitheater_Seating.pdf
  manifest: Seating_Manifest.xlsx (396 seats, 4 sections)
```

#### Permissions

- `importSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `getImportJob` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-964` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-964`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 2: Works in PDF & Image Import → Ingest PDF, PNG, JPG and supported scanned map sources. Provide drag-and-drop upload, page selection, preview, crop, rotation, de-skew, contrast and noise-reduction controls. Calibrate scale using …
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-964?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import seat map, Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-965` SVG & CAD Import

**Convert vector and CAD geometry while preserving useful source layers. Support approved SVG, DXF and DWG workflows with unit, scale, origin, coordinate and rotation mapping. Map source layers to sections, rows, seats, aisles, stage, text, amenities, obstructions and ignored content. Simplify excessive geometry, close open paths, remove duplicates and preview the transformed result before recognition. Configuration Scope of Work / Version 1.0 10 Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `jobId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/svg-cad-import-bo-965` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Import SVG or CAD-origin geometry, mapping source layers (seats, accessible seating, steps) to sections and seats.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **layerMapping**: Source layers listed with a target per layer; unmapped layers shown. *(source: contracts/satellite/seating.yaml#importSeatGeometry)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import seat geometry (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `jobId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The svg cad import list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the svg cad import untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No svg cad import yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the svg cad import are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
layers:
  SEATS: seats
  WC-SEATS: accessible
  STEPS: ignore
```

#### Permissions

- `importSeatGeometry` → `CAPACITY_CONFIGURE` (configure) · staff
- `getImportJob` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.2.1 | PDF Seat Map Import | Seat Management & Venue Mapping | CONTRACTED | `importSeatGeometry` |
| 21.2.2 | SVG Seat Map Import | Seat Management & Venue Mapping | CONTRACTED | `importSeatGeometry` |
| 21.2.5 | CSV Seat Map Import | Seat Management & Venue Mapping | CONTRACTED | `importSeatGeometry` |
| 21.2.6 | Excel Seat Map Import | Seat Management & Venue Mapping | CONTRACTED | `importSeatGeometry` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-965` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-965`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 4: Works in SVG & CAD Import → Convert vector and CAD geometry while preserving useful source layers. Support approved SVG, DXF and DWG workflows with unit, scale, origin, coordinate and rotation mapping. Map source layers to …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-965?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import seat geometry, Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-966` CSV & Excel Import

**Build maps or update seat master data from structured rows. Map columns for venue, level, section, row, seat, coordinates, type, category, price band, accessibility and status. Configure delimiter, header, encoding, sheet, data type, defaults and transformation rules with a sample-data preview. Detect missing identifiers, duplicates, invalid coordinates, inconsistent row sequences and unmapped values before import. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `jobId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/csv-excel-import-bo-966` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Build or update seat master data from rows (section, row, seat, category, price band, accessibility); the manifest is the authority for which seats exist but carries no geometry.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **column mapping**: Columns mapped to fields with a preview of the first rows. *(source: contracts/satellite/seating.yaml#importSeatManifest)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import seat manifest (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `jobId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The csv excel import list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the csv excel import untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No csv excel import yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the csv excel import are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
manifest:
  file: Seating_Manifest.xlsx
  rows: 396
```

#### Permissions

- `importSeatManifest` → `CAPACITY_CONFIGURE` (configure) · staff
- `getImportJob` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-966` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-966`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 6: Works in CSV & Excel Import → Build maps or update seat master data from structured rows. Map columns for venue, level, section, row, seat, coordinates, type, category, price band, accessibility and status. Configure delimiter …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-966?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import seat manifest, Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-967` AI Section Recognition

**Recognize venue levels, sections and standing zones from source geometry. Display detected boundaries, labels, hierarchy, capacity estimate and per-object confidence on the source preview. Allow accept, reject, merge, split, rename and redraw with AI correction suggestions and reason capture. Flag ambiguous, overlapping, disconnected or unlabelled areas and prevent silent assignment to the wrong level. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `importId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/ai-section-recognition-bo-967` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Review the sections, levels and standing zones the import recognised, with per-object confidence.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **detected sections**: Boundaries on the source preview with confidence; low confidence first. *(source: contracts/satellite/seating.yaml#getSeatMapImport)*

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `importId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The section recognition list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the section recognition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No section recognition yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the section recognition are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
detected:
  section: Lower 105
  confidence: 0.62
```

#### Permissions

- `getSeatMapImport` → `PRODUCT_VIEW` (read) · staff
- `validateSeatMap` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-967` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-967`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 8: Works in AI Section Recognition → Recognize venue levels, sections and standing zones from source geometry. Display detected boundaries, labels, hierarchy, capacity estimate and per-object confidence on the source preview. Allow …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-967?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-968` AI Row & Seat Recognition

**Detect rows and individual seat positions at production scale. Recognize row curves, direction, gaps, seat dots, repeated symbols and wheelchair spaces with confidence heat maps. Allow threshold, gap, snap, spacing and symbol-class controls followed by selective reprocessing. Present detected counts by section and reconcile them with stated capacities, labels and expected patterns. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `importId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/ai-row-seat-recognition-bo-968` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Review detected rows and seat positions and correct them in bulk.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seats (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **confidence heat map**: Seats coloured by detection confidence. *(source: contracts/satellite/seating.yaml#getSeatMapImport / contracts/satellite/seating.yaml#updateSeats)*

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `importId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The row seat recognition list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the row seat recognition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No row seat recognition yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the row seat recognition are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Map is published and the change is structural |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
  detected: 118
  lowConfidence: 7
```

#### Permissions

- `getSeatMapImport` → `PRODUCT_VIEW` (read) · staff
- `updateSeats` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.30 | Bulk Configuration and Updates AI can: Apply seat categories to thousands of seats simultaneously. Update pricing zones across multiple venues. Clone and modify existing seat maps. Generate … | Ticketing Catalogue | CONTRACTED | `updateSeats` |
| 21.1.1 | Drag & Drop Venue Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.2 | Section Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.3 | Row Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.4 | Seat Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.2.15 | Manual Adjustment Layer | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chinmay: near-term AI can generate a map/seating layout and the related ticket configuration once a venue uploads its map schema and layout image. *(client request · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-281)*
- Qossai: AI-assisted layout generation from AutoCAD/DXF (best) or PDF (fallback, via OCR), targeting ~90–95% automation with the client correcting the rest; sample input is a PDF seating diagram plus an Excel manifest of section/row/seat numbers. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-145)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-968` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-968`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 10: Works in AI Row & Seat Recognition → Detect rows and individual seat positions at production scale. Recognize row curves, direction, gaps, seat dots, repeated symbols and wheelchair spaces with confidence heat maps. Allow threshold …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-968?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seats, Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-969` AI Aisle, VIP & Accessibility

**Recognize special geometry and operational attributes that affect seating. Detect aisles, entrances, exits, stages, VIP areas, suites, boxes, wheelchair positions and accessible routes. Show confidence, source evidence and conflicts where a detected object overlaps inventory or breaks route continuity. Allow the reviewer to change object class, boundary and attributes without restarting the full import. Configuration Scope of Work / Version 1.0 11 Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `importId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/ai-aisle-vip-accessibility-bo-969` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Review detected aisles, entrances, VIP areas, suites and wheelchair positions.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save map zones (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **special geometry**: Detected items by kind with confidence and accept or correct. *(source: contracts/satellite/seating.yaml#getSeatMapImport)*

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `importId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The aisle vip accessibility list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the aisle vip accessibility untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No aisle vip accessibility yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the aisle vip accessibility are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
detected:
  wheelchairPositions: 16
  aisles: 9
```

#### Permissions

- `getSeatMapImport` → `PRODUCT_VIEW` (read) · staff
- `setMapZones` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-969` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-969`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 12: Works in AI Aisle, VIP & Accessibility → Recognize special geometry and operational attributes that affect seating. Detect aisles, entrances, exits, stages, VIP areas, suites, boxes, wheelchair positions and accessible routes. Show …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-969?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save map zones, Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-970` AI Numbering & Labeling

**Generate consistent section, row and seat identifiers from recognized geometry. Configure alphabetic, numeric, alphanumeric, odd/even, continuous, reset-by-row and venue-specific numbering patterns. Preview before/after labels, direction, padding, skipped values, reserved labels and accessible-seat suffixes. Detect duplicates, gaps, reversals and conflicts with existing venue identifiers before applying changes. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `CAPACITY_CONFIGURE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation), `actionId` (navigation), `planId` (navigation) |
| Route | `/access-venue/ai-numbering-labeling-bo-970` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-012): "Save seats" called updateSeats directly next to the AI proposal; applying the AI's proposal goes through its approval (decideProposedAction, declared), not a …

**From the AI & Intelligence process.** AI numbering and labelling of seats: generate consistent section, row and seat labels from the recognised geometry (alphabetic, numeric, odd/even, continuous, reset by row), preview before/after, then approve. The one thing to get right: the AI proposes; a person previews and approves every map change (decided 21 August).

**Fixed on main** (the package already carries these; draw what it says): "Save seats" calls updateSeats directly next to the AI proposal. (CHG-WIR-012).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Propose numbering**: A proposal with before/after labels; approve applies it through Seating. *(source: contracts/satellite/ai.yaml#proposeSeatMapChanges / ADR-0020)*

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The numbering labeling list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the numbering labeling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No numbering labeling yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the numbering labeling are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 422 The input the kind needs is missing (`numberingScheme` for `numbering`, `stagePosition` for `stageVariant`), or the map has no focal zone for `categories` … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
proposal:
  section: L4
  scheme: rows A-T, seats odd left / even right
  conflicts: 2 duplicate labels found in row K
```

#### Permissions

- `decideProposedAction` → `AI_USE` (operate) · staff
- `proposeSeatMapChanges` → `CAPACITY_CONFIGURE` (configure) · staff
- `getActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| 1.4.23 | Event-Specific Configurations For multi-purpose venues, AI can: Create different seat maps for concerts, sports events, exhibitions, and conferences. Configure temporary seating arrangements. … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.25 | Intelligent Seat Numbering Automatically assign row names (A, B, C, etc.) and seat numbers based on configurable rules. Validate numbering sequences and identify duplicates or missing seats. Apply … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.26 | Seat Category Configuration AI can recommend seat categories based on: Distance from the stage or attraction. Viewing angles and sightlines. Elevation and seating tier. Historical sales performance. … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.29 | Validation and Quality Assurance AI can automatically identify: Duplicate seat numbers. Missing rows or seats. Incorrect category assignments. Accessibility compliance issues. Capacity mismatches … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-970` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-970`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 14: Works in AI Numbering & Labeling → Generate consistent section, row and seat identifiers from recognized geometry. Configure alphabetic, numeric, alphanumeric, odd/even, continuous, reset-by-row and venue-specific numbering patterns. …
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-970?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `AI_USE`, `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-971` Validation & Correction

**Provide one controlled workspace for resolving AI and import exceptions. Compare the source and generated map side by side with issue list, filters, severity and confidence. Offer manual draw, move, split, merge, add, delete, renumber, relabel and property-edit tools on a correction layer. Re-run selected recognizers, validate affected objects and preserve every AI suggestion, human edit and reviewer decision. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `importId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/validation-correction-bo-971` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** One workspace to resolve import exceptions: source and generated map side by side with the issue list.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **side by side**: Source left, map right, issue list below linked to both. *(source: contracts/satellite/seating.yaml#validateSeatMap)*

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `importId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation correction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation correction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation correction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validation correction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
issue:
  kind: seat outside section
  where: Upper 202 row B seat 1
```

#### Permissions

- `validateSeatMap` → `PRODUCT_VIEW` (read) · staff
- `getSeatMapImport` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-971` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-971`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 16: Works in Validation & Correction → Provide one controlled workspace for resolving AI and import exceptions. Compare the source and generated map side by side with issue list, filters, severity and confidence. Offer manual draw, move …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-971?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-972` AI Venue Designer & Publish

**Generate or refine a seat map from a natural-language brief and release the approved result. Accept venue type, dimensions, levels, target capacity, stage, section mix, accessibility and circulation requirements. Generate multiple explainable variants with capacity, sightline, accessible inventory and constraint summaries. Require full map validation, human review, approval and controlled one-click publication with version and rollback. Retain source files, model/version, confidence, reviewer corrections and publication evidence; never allow AI output to bypass validation or approval. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 12 Board 3 - Layouts, Templates & Versions Figure 3. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 13**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `jobId` (navigation), `seatMapId` (navigation) |
| Route | `/access-venue/ai-venue-designer-publish-bo-972` |

**Known gaps.** **AI Venue Designer & Publish declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Generate or refine a seat map from a brief or an import and release the approved result: apply the parsed import, then validate and publish.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only commitImportJob, publishSeatMap and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Import progress and findings** (detail panel, from `getImportJob`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Kind | chip: Manifest, Geometry | — |
| Status | chip: Parsing, Preview ready, Committing, Committed, Failed | — |
| Parsed seat count | 1,234 | — |
| Matched seat count | 1,234 | Geometry imports — seats successfully joined to the manifest. |
| Unmatched seat count | 1,234 | Present in one source but not the other. A seat in the plan with no manifest entry is a finding, not a seat. |
| Outcome | chip: Parsed, Parsed with findings, No seats found, No layers matched, Unreadable | All four CF-122 defects failed silently — an import that found nothing reported success. |
| Layers found | list or chips (count when long) | Every layer name in the source, decoded. Shown whether or not extraction worked, so an operator can map a role by reading rather than by … |
| Findings | list or chips (count when long) | — |
| Kind | chip: Duplicate seat number, Gap in row, Missing geometry, Seat outside section … | — |
| Severity | chip: Error, Warning, Info | — |
| Message | text | — |
| Section code | text | — |
| Row label | text | — |
| Seat numbers | list or chips (count when long) | — |
| Affected count | 1,234 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**Read a seat map with its structure** (detail panel, from `getSeatMap`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Status | chip: Draft, Validated, Published, Archived | — |
| Seat count | 1,234 | — |
| Section count | 1,234 | — |
| Has geometry | yes / no (icon or chip) | False when only a manifest has been imported. Such a map can be sold from a list but not rendered. |
| Published at | 1 Oct 2026, 14:30 | — |
| Description | text | — |
| View box | grouped details | Coordinate space for rendering. Absent when there is no geometry. |
| Width | 1,234.5 | — |
| Height | 1,234.5 | — |
| Stage position | grouped details | — |
| X | 1,234.5 | — |
| Y | 1,234.5 | — |
| Sections | list or chips (count when long) | — |
| Code | text | — |
| Name | text | — |
| Row count | 1,234 | — |
| Seat count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Apply import**: Applies the previewed import to a draft; refuses an import that found nothing. *(source: contracts/satellite/seating.yaml#commitImportJob)*

**Data it reads**: `getImportJob` (onLoad, Import progress and findings); `getSeatMap` (onLoad, Read a seat map with its structure)

**Where the user goes next**

- → `BO-963` Import Command Center: *Back to Import Command Center*; carries `jobId`, `seatMapId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue designer publish list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue designer publish untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue designer publish yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue designer publish are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Job has errors, or has already been committed (ValidationProblem); 409 Validation failed. (ValidationProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
brief: 3,000-seat amphitheatre, end stage, 12 sections, 16 wheelchair positions
```

#### Permissions

- `commitImportJob` → `CAPACITY_CONFIGURE` (configure) · staff
- `publishSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `getImportJob` → `PRODUCT_VIEW` (read) · staff
- `getSeatMap` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.2.16 | One-Click Publishing | Seat Management & Venue Mapping | CONTRACTED | `publishSeatMap` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: besides manual drag-and-drop building, AI-assisted import — upload a PDF/image of the layout (AI recognises sections) plus an Excel/CSV of row/seat naming — generates a draft seat map for validation before publishing. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-417)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-972` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS141 Seat Management Venue Mapping Reference v1.0 Board 2.dc.html#bo-972`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 2
- Flow F275 *Seat Management Venue Mapping Reference v1.0 board 2: Import Command Center*, step 18: Works in AI Venue Designer & Publish → Generate or refine a seat map from a natural-language brief and release the approved result. Accept venue type, dimensions, levels, target capacity, stage, section mix, accessibility and circulation …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-972?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-963`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"commitImportJob": {"method":"POST","path":"/seat-maps/{seatMapId}/import/{jobId}","contract":"seating","summary":"Apply a parsed import","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ImportJob"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getImportJob": {"method":"GET","path":"/seat-maps/{seatMapId}/import/{jobId}","contract":"seating","summary":"Import progress and findings","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ImportJob"},
"getSeatMap": {"method":"GET","path":"/seat-maps/{seatMapId}","contract":"seating","summary":"Read a seat map with its structure","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatMap"},
"getSeatMapImport": {"method":"GET","path":"/seat-map-imports/{importId}","contract":"seating","summary":"How the import went","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatMapImportJob"},
"importSeatGeometry": {"method":"POST","path":"/seat-maps/{seatMapId}/import/geometry","contract":"seating","summary":"Import seat geometry from a plan","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ImportGeometryRequest","responds":null},
"importSeatManifest": {"method":"POST","path":"/seat-maps/{seatMapId}/import/manifest","contract":"seating","summary":"Import the logical seat structure","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ImportManifestRequest","responds":null},
"importSeatMap": {"method":"POST","path":"/seat-map-imports","contract":"seating","summary":"Import a seat map from a plan or a manifest","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMapImportJob"},
"proposeSeatMapChanges": {"method":"POST","path":"/ai/seat-maps/{seatMapId}/proposals","contract":"ai","summary":"Propose changes to an existing seat map, as a plan a person approves","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiSeatMapProposal"},
"publishSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/publish","contract":"seating","summary":"Validate and publish a seat map","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"setMapZones": {"method":"PUT","path":"/seat-maps/{seatMapId}/zones","contract":"seating","summary":"Standing areas, suites, stages and obstructions","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MapZone"},
"updateSeats": {"method":"PATCH","path":"/seat-maps/{seatMapId}/seats","contract":"seating","summary":"Bulk-amend seats","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"BulkUpdateSeatsRequest","responds":null},
"validateSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/validate","contract":"seating","summary":"Run validation without publishing","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationReport"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiSeatMapProposal": {"type":"object","x-ticvai-persistence":"none — the plan is ai.action_plan and ai.action_step, presented as one ai.proposed_action; the findings are the evidence of its decision record","description":"What `proposeSeatMapChanges` proposed: findings with the seats they concern, and except for `consistency` the plan a person approves (1.4.23, 1.4.25, 1.4.26, 1.4.29).","required":["kind","findings"],"properties":{"kind":{"type":"string","enum":["categories","numbering","stageVariant","consistency"]},"seatMapId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.action_plan`, readable with `getActionPlan`. Null for `consistency`."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.proposed_action` a person decides. Null for `consistency`."},"summary":{"type":"object","additionalProperties":true,"description":"Counts: seats re-categorised or relabelled, seats blocked, capacity by category before and after."},"findings":{"type":"array","items":{"type":"object","required":["code","severity"],"properties":{"code":{"type":"string","description":"e.g. `accessibleSeatWithoutAccessiblePrice`, `restrictedViewInPremium`, `companionWithoutWheelchairSpace`, `sightLineLost`, `behindStage`, `numberingGap`, `duplicateLabel`, `categoryChange`, `labelChange`."},"severity":{"type":"string","enum":["blocking","warning","info"]},"seatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"sectionId":{"type":"string","format":"uuid","nullable":true},"current":{"type":"string","nullable":true},"proposed":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true}}}},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid"}}},
"BulkUpdateSeatsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["selection"],"properties":{"selection":{"type":"object","description":"Seats to amend. Combine filters; an empty selection is rejected.","properties":{"seatIds":{"type":"array","items":{"type":"string"}},"sectionCodes":{"type":"array","items":{"type":"string"}},"rowLabels":{"type":"array","items":{"type":"string"}}}},"categoryId":{"type":"string","format":"uuid"},"attribute":{"$ref":"#/components/schemas/SeatAttribute"},"isActive":{"type":"boolean"}}},
"ImportGeometryRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["fileReference","format"],"properties":{"fileReference":{"type":"string"},"format":{"type":"string","enum":["svgPlan","pdfPlan"]},"layerMapping":{"type":"object","description":"Named layers in the source. Layer-aware extraction is far more reliable than shape recognition, so it is preferred wherever the source supports it — **and the client's amphitheatre file confirms the bet**: `VC-Seats`, `VC-wheelchairseating` and `VC-Steps` map straight onto the three roles below.\n**Each role takes a list, not a name** (CF-122). The same file carries two distinct layers both named `Layer 1`, steps drawn on both `steps` and `VC-Steps`, and AutoCAD's default `0`. A single string silently kept one and dropped the rest.\n**Names are decoded before matching.** PDF layer names arrive UTF-16BE and read as mojibake if taken as bytes, so a role that looks unmatched may simply be undecoded.\n","properties":{"seatsLayer":{"type":"array","items":{"type":"string"}},"accessibleSeatsLayer":{"type":"array","items":{"type":"string"}},"sectionBoundaryLayer":{"type":"array","items":{"type":"string"}},"stepsLayer":{"type":"array","items":{"type":"string"}},"stageLayer":{"type":"array","items":{"type":"string"}},"unmappedLayers":{"type":"array","readOnly":true,"description":"Layers found in the source and claimed by no role. **Reported rather than ignored** — a plan with an unmapped layer is a plan where something was not extracted, and the operator is the only one who knows whether it mattered.\n","items":{"type":"string"}}}},"digitNormalisation":{"type":"boolean","default":true,"description":"**Section codes carrying Arabic-Indic digits never join to the manifest** (CF-122). `A١` and `A1` are the same section to a person and two sections to a string comparison, and the failure is silent — the row simply does not match.\nNormalised before the join. Disable only where a venue genuinely uses both forms as distinct codes, which would be its own problem.\n"},"joinOn":{"type":"string","enum":["sectionAndRow","labelText","ordinal"],"default":"sectionAndRow","description":"How plan geometry is matched to manifest seats."}}},
"ImportJob": {"x-ticvai-persistence":"seating.import_job","type":"object","required":["id","seatMapId","kind","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["manifest","geometry"]},"status":{"$ref":"#/components/schemas/ImportJobStatus"},"parsedSeatCount":{"type":"integer"},"matchedSeatCount":{"type":"integer","description":"Geometry imports — seats successfully joined to the manifest."},"unmatchedSeatCount":{"type":"integer","description":"Present in one source but not the other. A seat in the plan with no manifest entry is a finding, not a seat.\n"},"outcome":{"type":"string","readOnly":true,"enum":["parsed","parsedWithFindings","noSeatsFound","noLayersMatched","unreadable"],"description":"**All four CF-122 defects failed silently — an import that found nothing reported success.** A job that parses zero seats is not a parsed job, and the operator was left to notice an empty seat map later.\n`noLayersMatched` is the specific one worth separating: **the file was readable and no role claimed a layer**, which almost always means the names needed decoding or a role needed a second entry rather than that the file was wrong.\n"},"layersFound":{"type":"array","readOnly":true,"description":"Every layer name in the source, decoded. **Shown whether or not extraction worked**, so an operator can map a role by reading rather than by guessing.\n","items":{"type":"string"}},"findings":{"type":"array","items":{"$ref":"#/components/schemas/ValidationFinding"}},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"ImportJobStatus": {"type":"string","enum":["parsing","previewReady","committing","committed","failed"]},
"ImportManifestRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["fileReference","format","columnMapping"],"properties":{"fileReference":{"type":"string","description":"Object storage reference. The file is not posted through this API."},"format":{"type":"string","enum":["csvManifest","xlsxManifest"]},"sheetName":{"type":"string","description":"Spreadsheets only. Trailing spaces in sheet names are common — quote exactly."},"headerRow":{"type":"integer","default":1},"columnMapping":{"type":"object","description":"Which column holds what. Required because manifests arrive with different headings from every venue.\n","required":["sectionColumn","rowColumn","seatColumn"],"properties":{"sectionColumn":{"type":"string"},"rowColumn":{"type":"string"},"seatColumn":{"type":"string"},"categoryColumn":{"type":"string"},"attributeColumn":{"type":"string"}}},"replaceExisting":{"type":"boolean","default":false,"description":"False merges. True replaces, and is refused where tickets are sold against the map.\n"}}},
"MapZone": {"type":"object","x-ticvai-persistence":"seating.zone","description":"BL-166. **`seating` is strong on everything that is a seat and the map itself was only seats.**\n**A standing area is a capacity without individual seats**, and modelling it as seats means inventing seat numbers nobody prints and a guest cannot find. A suite is the opposite — one sellable unit containing many seats, sold whole.\nNon-sellable zones matter too: **a stage, an entry and a sightline obstruction are not inventory and they change what the seats beside them are worth.**\n","required":["id","seatMapId","kind","name"],"properties":{"id":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["standing","suite","box","lounge","accessiblePlatform","stage","entry","exit","concourse","obstruction","camera","aisle"]},"name":{"type":"string"},"capacity":{"type":"integer","nullable":true,"description":"**For a standing zone this is the inventory** — sold as a count rather than as seats. Null for a stage or an obstruction, which sell nothing.\n"},"seatCategoryId":{"type":"string","format":"uuid","nullable":true},"containsSeatIds":{"type":"array","description":"For a suite or box. **Sold whole, so the seats inside are held together** — selling one seat of a suite is not a thing a venue does.\n","items":{"type":"string","format":"uuid"}},"obstructsZoneIds":{"type":"array","description":"What this blocks the view of. **A pillar is not inventory and it decides what the seats behind it are worth**, which is the only reason to draw it.\n","items":{"type":"string","format":"uuid"}},"geometry":{"type":"string","nullable":true}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"SeatAttribute": {"type":"string","description":"BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n","enum":["standard","accessible","companion","obstructedView","restrictedLegroom","premium","houseSeat","buffer","aisle","endOfRow","extraLegroom","powerOutlet","tableService","shaded","covered","nearExit","nearAccessibleWc","wheelchairTransfer","limitedRecline","sofa","beanbag"]},
"SeatMap": {"x-ticvai-persistence":"seating.seat_map","allOf":[{"$ref":"#/components/schemas/SeatMapSummary"},{"type":"object","required":["sections"],"properties":{"description":{"type":"string","nullable":true},"viewBox":{"type":"object","description":"Coordinate space for rendering. Absent when there is no geometry.","nullable":true,"properties":{"width":{"type":"number"},"height":{"type":"number"}}},"stagePosition":{"$ref":"#/components/schemas/Point"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/Section"}},"isActive":{"type":"boolean"}}}]},
"SeatMapImportJob": {"type":"object","description":"**AI-assisted import from a PDF, an image or a spreadsheet** (21 August decision). A venue arriving with a printed plan and a seat manifest should not rebuild 396 rows by hand.\n\n**It proposes and a person accepts — it never publishes.** ADR-0020: a suggestion proposes, a person decides. An imported map lands as a draft with its confidence and whatever it could not read, because **a seat map wrong by two rows is worse than one that took an afternoon.**","required":["id","status","source"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["queued","reading","proposed","accepted","rejected","failed"]},"source":{"type":"string","enum":["pdf","image","excel","csv"]},"seatMapId":{"type":"string","format":"uuid","nullable":true,"description":"The draft it produced, once it has one."},"seatsDetected":{"type":"integer","nullable":true},"sectionsDetected":{"type":"integer","nullable":true},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1},"unreadable":{"type":"array","items":{"type":"string"},"description":"**What it could not read, named.** A blank list and a low confidence are different problems: the first is a bad scan, the second is a plan it half-understood."},"basis":{"type":"string","enum":["heuristic","model"],"description":"ADR-0020 — the same abstraction as every other suggestion."}}},
"SeatMapSummary": {"x-ticvai-persistence":"seating.seat_map","type":"object","required":["id","name","venueId","status","seatCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/SeatMapStatus"},"seatCount":{"type":"integer"},"sectionCount":{"type":"integer"},"hasGeometry":{"type":"boolean","description":"False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"},"publishedAt":{"type":"string","format":"date-time","nullable":true}}},
"Section": {"x-ticvai-persistence":"seating.section","type":"object","required":["code","name","rowCount","seatCount"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"rowCount":{"type":"integer"},"seatCount":{"type":"integer"},"boundary":{"type":"array","items":{"$ref":"#/components/schemas/Point"},"description":"Polygon for rendering. Absent without geometry."},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"assets.MediaAsset","description":"**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"},"rows":{"type":"array","items":{"type":"object","required":["label","seatCount"],"properties":{"label":{"type":"string"},"seatCount":{"type":"integer"},"numberingDirection":{"type":"string","enum":["leftToRight","rightToLeft"],"description":"Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"ValidationFinding": {"x-ticvai-persistence":"none — computed","type":"object","required":["kind","severity","message"],"properties":{"kind":{"$ref":"#/components/schemas/ValidationFindingKind"},"severity":{"$ref":"#/components/schemas/ValidationSeverity"},"message":{"type":"string"},"sectionCode":{"type":"string","nullable":true},"rowLabel":{"type":"string","nullable":true},"seatNumbers":{"type":"array","items":{"type":"string"}},"affectedCount":{"type":"integer"}}},
"ValidationReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatMapId","passed","errorCount","warningCount","findings"],"properties":{"seatMapId":{"type":"string","format":"uuid"},"passed":{"type":"boolean","description":"False when any finding has severity `error`."},"errorCount":{"type":"integer"},"warningCount":{"type":"integer"},"findings":{"type":"array","items":{"$ref":"#/components/schemas/ValidationFinding"}}}}
}
```
