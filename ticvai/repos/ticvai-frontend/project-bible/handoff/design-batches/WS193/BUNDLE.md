# WS193 — Wallet Configuration Backend Structure v1.0 board 8

**10 screens · 16 operations · 13 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AUDIT_VIEW, RISK_INVESTIGATE, RISK_REVIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1153` | Wallet Security & Risk Command Center | C | 2 | 30 | 6 | 2 | 0 | 6 | — | notStarted (—) |
| `BO-1154` | Wallet Risk Policy Configuration | C | 11 | 0 | 6 | 2 | 0 | 6 | — | notStarted (—) |
| `BO-1155` | Transaction Risk Scoring Engine | C | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-1156` | Velocity & Behavioral Rule Configuration | C | 14 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-1157` | Device, Credential & Account Security | C | 0 | 54 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1158` | AI Fraud & Anomaly Detection Studio | C | 0 | 2 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-1159` | Automated Security Action Orchestration | C | 12 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-1160` | Fraud Alert & Investigation Case Management | D | 0 | 90 | 6 | 15 | 1 | 0 | — | notStarted (—) |
| `BO-1161` | Security Rules Testing, Simulation & AI Sandbox | B | 0 | 24 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1162` | Security Governance, Audit & Rule Publication | A | 4 | 33 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1155, BO-1160, BO-1161 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1153` Wallet Security & Risk Command Center

**Provide Security, Risk, Finance and authorized Operations teams with a real-time overview of wallet security. Dashboard KPIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1153 |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-security-risk-command-center-bo-1153` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet risk rules that setWalletRiskRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Wallet security at a glance: rules tripped, wallets frozen, risk scores.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletRiskRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search wallet security risk | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, wallet type, customer, risk level, channel and 4 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every wallet security risk** (data table)

| Shows | Format | Notes |
|---|---|---|
| Transactions screened | text | not in the schema: `Transactions Screened` |
| Transactions approved | text | not in the schema: `Transactions Approved` |
| Transactions challenged | text | not in the schema: `Transactions Challenged` |
| Transactions declined | text | not in the schema: `Transactions Declined` |
| Transactions held | text | not in the schema: `Transactions Held` |
| High risk transactions | text | not in the schema: `High-Risk Transactions` |
| Wallets under review | text | not in the schema: `Wallets Under Review` |
| Blocked wallets | text | not in the schema: `Blocked Wallets` |
| Suspicious transfers | text | not in the schema: `Suspicious Transfers` |
| Suspicious top ups | text | not in the schema: `Suspicious Top-Ups` |
| Account takeover alerts | text | not in the schema: `Account-Takeover Alerts` |
| Credential security alerts | text | not in the schema: `Credential Security Alerts` |
| Open fraud cases | text | not in the schema: `Open Fraud Cases` |
| Prevented value | text | not in the schema: `Prevented Value` |
| Risk distribution | text | not in the schema: `Risk Distribution` |

**The selected wallet security risk** (detail panel): The pack groups this record's detail under its own headings: “Display transactions as”, “Break down”.

| Shows | Format | Notes |
|---|---|---|
| Transactions screened | text | not in the schema: `Transactions Screened` |
| Transactions approved | text | not in the schema: `Transactions Approved` |
| Transactions challenged | text | not in the schema: `Transactions Challenged` |
| Transactions declined | text | not in the schema: `Transactions Declined` |
| Transactions held | text | not in the schema: `Transactions Held` |
| High risk transactions | text | not in the schema: `High-Risk Transactions` |
| Wallets under review | text | not in the schema: `Wallets Under Review` |
| Blocked wallets | text | not in the schema: `Blocked Wallets` |
| Suspicious transfers | text | not in the schema: `Suspicious Transfers` |
| Suspicious top ups | text | not in the schema: `Suspicious Top-Ups` |
| Account takeover alerts | text | not in the schema: `Account-Takeover Alerts` |
| Credential security alerts | text | not in the schema: `Credential Security Alerts` |
| Open fraud cases | text | not in the schema: `Open Fraud Cases` |
| Prevented value | text | not in the schema: `Prevented Value` |
| Risk distribution | text | not in the schema: `Risk Distribution` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **risk overview**: Tripped rules today, actions taken. *(source: contracts/satellite/wallet.yaml#setWalletRiskRules)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1154` Wallet Risk Policy Configuration: *Wallet Risk Policy Configuration*
- → `BO-1155` Transaction Risk Scoring Engine: *Transaction Risk Scoring Engine*
- → `BO-1156` Velocity & Behavioral Rule Configuration: *Velocity & Behavioral Rule Configuration*
- → `BO-1157` Device, Credential & Account Security: *Device, Credential & Account Security*
- → `BO-1158` AI Fraud & Anomaly Detection Studio: *AI Fraud & Anomaly Detection Studio*
- → `BO-1159` Automated Security Action Orchestration: *Automated Security Action Orchestration*
- → `BO-1160` Fraud Alert & Investigation Case Management: *Fraud Alert & Investigation Case Management*
- → `BO-1161` Security Rules Testing, Simulation & AI Sandbox: *Security Rules Testing, Simulation & AI Sandbox*
- → `BO-1162` Security Governance, Audit & Rule Publication: *Security Governance, Audit & Rule Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet security risk list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet security risk untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet security risk yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet security risk are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
today:
  rulesTripped: 14
  walletsFrozen: 2
```

#### Permissions

- `setWalletRiskRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.31 | Apply fraud and security controls. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |
| 4.3.32 | AI identifies suspicious wallet activity. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1153` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1153`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 1: Opens Wallet Security & Risk Command Center → Provide Security, Risk, Finance and authorized Operations teams with a real-time overview of wallet security. Dashboard KPIs
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F300 branch at step 1 (expected): when Nothing has been set up on Wallet Security & Risk Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F300 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1153?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1154`, `BO-1155`, `BO-1156`, `BO-1157`, `BO-1158`, `BO-1159`, `BO-1160`, `BO-1161`, `BO-1162`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1154` Wallet Risk Policy Configuration

**Create reusable risk policies controlling wallet activities. Risk Policy Types**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1154 |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure policies for) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-risk-policy-configuration-bo-1154` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet risk rules that setWalletRiskRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Reusable risk policies; each rule names its action (score only, challenge, hold, block).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletRiskRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet Funding | select field | — | — | — | — | — | — |
| Wallet Spending | select field | — | — | — | — | — | — |
| P2P Transfers | select field | — | — | — | — | — | — |
| Refunds | select field | — | — | — | — | — | — |
| Gift Cards | select field | — | — | — | — | — | — |
| Vouchers | select field | — | — | — | — | — | — |
| Wearables | select field | — | — | — | — | — | — |
| Offline Transactions | select field | — | — | — | — | — | — |
| Administrative Adjustments | select field | — | — | — | — | — | — |
| API Transactions | select field | — | — | — | — | — | — |
| Risk Conditions | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rule action**: Required per rule; a rule without action is a report. *(source: contracts/satellite/wallet.yaml#setWalletRiskRules)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet risk policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet risk policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet risk policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  name: Rapid top-ups
  condition: 5 top-ups in 10 min
  action: challenge
```

#### Permissions

- `setWalletRiskRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.31 | Apply fraud and security controls. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |
| 4.3.32 | AI identifies suspicious wallet activity. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1154` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1154`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 2: Works in Wallet Risk Policy Configuration → Create reusable risk policies controlling wallet activities. Risk Policy Types

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1154?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1155` Transaction Risk Scoring Engine

**Calculate a real-time risk score for sensitive wallet operations. Example Risk Score**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1155 |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/transaction-risk-scoring-engine-bo-1155` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet risk rules that setWalletRiskRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The real-time risk score of sensitive operations and its components.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletRiskRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save wallet risk rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **score breakdown**: Components adding up to the score with thresholds. *(source: contracts/satellite/wallet.yaml#setWalletRiskRules)*

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The transaction risk scoring list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the transaction risk scoring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No transaction risk scoring yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the transaction risk scoring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
score:
  total: 72
  components:
    velocity: 30
    newDevice: 25
    amount: 17
```

#### Permissions

- `setWalletRiskRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.31 | Apply fraud and security controls. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |
| 4.3.32 | AI identifies suspicious wallet activity. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Transactions get a risk score; high-risk transactions are flagged and routed to the operations team for manual cross-verification, never auto-approved or auto-declined. *(agreed · MoM 27 Aug 2026, 4.10 Transaction risk scoring engine · DI-537)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1155` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1155`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 4: Works in Transaction Risk Scoring Engine → Calculate a real-time risk score for sensitive wallet operations. Example Risk Score

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1155?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save wallet risk rules, Cancel.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1156` Velocity & Behavioral Rule Configuration

**Detect abnormal activity based on frequency, amount and behavioral patterns. Requirement 4.3.31 requires controls for suspicious transactions, spending restrictions, transfer restrictions and high-risk activity. Velocity Rules**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1156 |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/velocity-behavioral-rule-configuration-bo-1156` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet risk rules that setWalletRiskRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Velocity and behavioural rules for suspicious activity.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletRiskRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Transactions per minute | select field | — | — | — | — | — | — |
| Transactions per hour | select field | — | — | — | — | — | — |
| Transactions per day | select field | — | — | — | — | — | — |
| Value per hour | select field | — | — | — | — | — | — |
| Value per day | select field | — | — | — | — | — | — |
| Top-ups per hour | select field | — | — | — | — | — | — |
| Transfers per hour | select field | — | — | — | — | — | — |
| Refunds per day | select field | — | — | — | — | — | — |
| Failed attempts | select field | — | — | — | — | — | — |
| Different devices used | select field | — | — | — | — | — | — |
| Different credentials used | select field | — | — | — | — | — | — |
| Number of recipients | select field | — | — | — | — | — | — |
| Number of venues | select field | — | — | — | — | — | — |
| Example | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **velocity rule**: Count or value over a window. *(source: contracts/satellite/wallet.yaml#setWalletRiskRules)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Hold additional transfers + Risk Review (primary button) | navigation or local | — | — | — | — |
| High-Risk Alert (secondary button) | navigation or local | — | — | — | — |
| Behavioral Baseline (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The velocity behavioral rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the velocity behavioral rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No velocity behavioral rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: More than AED 1,000.00 transferred in 1 hour
```

#### Permissions

- `setWalletRiskRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.31 | Apply fraud and security controls. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |
| 4.3.32 | AI identifies suspicious wallet activity. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1156` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1156`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 6: Works in Velocity & Behavioral Rule Configuration → Detect abnormal activity based on frequency, amount and behavioral patterns. Requirement 4.3.31 requires controls for suspicious transactions, spending restrictions, transfer restrictions and …

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1156?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Hold additional transfers + Risk Review, High-Risk Alert, Behavioral Baseline.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1157` Device, Credential & Account Security

**Detect compromised accounts, shared credentials and suspicious device behavior. Requirement 4.3.32 specifically includes detection of account sharing and unauthorized access patterns. Device Intelligence**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1157 |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track; Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/device-credential-account-security-bo-1157` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Compromised accounts, shared credentials and suspicious devices.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listWalletDisputes return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/satellite/wallet.yaml#listWalletDisputes; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listWalletDisputes` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every device credential account** (data table)

| Shows | Format | Notes |
|---|---|---|
| Device ID | text | not in the schema: `Device ID` |
| First seen | text | not in the schema: `First seen` |
| Last seen | text | not in the schema: `Last seen` |
| Customer association | text | not in the schema: `Customer association` |
| Wallet associations | text | not in the schema: `Wallet associations` |
| Trusted/untrusted status | text | not in the schema: `Trusted/untrusted status` |
| Failed authentications | text | not in the schema: `Failed authentications` |
| Credential changes | text | not in the schema: `Credential changes` |
| Risk history | text | not in the schema: `Risk history` |
| Credential monitoring | text | not in the schema: `Credential Monitoring` |
| Same credential used simultaneously | text | not in the schema: `Same credential used simultaneously` |
| Same wallet on excessive devices | text | not in the schema: `Same wallet on excessive devices` |
| Lost/stolen credential use | text | not in the schema: `Lost/stolen credential use` |
| New device + high value transaction | text | not in the schema: `New device + high-value transaction` |
| Rapid device switching | text | not in the schema: `Rapid device switching` |
| Repeated PIN failures | text | not in the schema: `Repeated PIN failures` |
| Repeated OTP failures | text | not in the schema: `Repeated OTP failures` |
| Suspicious account recovery | text | not in the schema: `Suspicious account recovery` |
| Credential cloning indicators | text | not in the schema: `Credential cloning indicators` |
| Administrative actions | text | not in the schema: `Administrative Actions` |
| Trust device | text | not in the schema: `Trust Device` |
| Untrust device | text | not in the schema: `Untrust Device` |
| Revoke session | text | not in the schema: `Revoke Session` |
| Suspend credential | text | not in the schema: `Suspend Credential` |
| Force reauthentication | text | not in the schema: `Force Reauthentication` |
| Reset credential | text | not in the schema: `Reset Credential` |
| Block wallet | text | not in the schema: `Block Wallet` |

**The selected device credential account** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Device ID | text | not in the schema: `Device ID` |
| First seen | text | not in the schema: `First seen` |
| Last seen | text | not in the schema: `Last seen` |
| Customer association | text | not in the schema: `Customer association` |
| Wallet associations | text | not in the schema: `Wallet associations` |
| Trusted/untrusted status | text | not in the schema: `Trusted/untrusted status` |
| Failed authentications | text | not in the schema: `Failed authentications` |
| Credential changes | text | not in the schema: `Credential changes` |
| Risk history | text | not in the schema: `Risk history` |
| Credential monitoring | text | not in the schema: `Credential Monitoring` |
| Same credential used simultaneously | text | not in the schema: `Same credential used simultaneously` |
| Same wallet on excessive devices | text | not in the schema: `Same wallet on excessive devices` |
| Lost/stolen credential use | text | not in the schema: `Lost/stolen credential use` |
| New device + high value transaction | text | not in the schema: `New device + high-value transaction` |
| Rapid device switching | text | not in the schema: `Rapid device switching` |
| Repeated PIN failures | text | not in the schema: `Repeated PIN failures` |
| Repeated OTP failures | text | not in the schema: `Repeated OTP failures` |
| Suspicious account recovery | text | not in the schema: `Suspicious account recovery` |
| Credential cloning indicators | text | not in the schema: `Credential cloning indicators` |
| Administrative actions | text | not in the schema: `Administrative Actions` |
| Trust device | text | not in the schema: `Trust Device` |
| Untrust device | text | not in the schema: `Untrust Device` |
| Revoke session | text | not in the schema: `Revoke Session` |
| Suspend credential | text | not in the schema: `Suspend Credential` |
| Force reauthentication | text | not in the schema: `Force Reauthentication` |
| Reset credential | text | not in the schema: `Reset Credential` |
| Block wallet | text | not in the schema: `Block Wallet` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Digital Key (primary button) | navigation or local | — | — | — | — |
| Customer Login (secondary button) | navigation or local | — | — | — | — |
| API Credential (secondary button) | navigation or local | — | — | — | — |
| Security Rules (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **device signals**: Credential, devices seen, flags. *(source: contracts/satellite/wallet.yaml#listWalletDisputes)*

**Data it reads**: `listWalletDisputes` (onLoad, Where it went wrong)

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device credential account list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device credential account untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device credential account yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device credential account are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already bound to another wallet |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signal:
  credential: WB-0098812
  devices: 3
  flag: used at two gates 2 min apart
```

#### Permissions

- `linkWalletCredential` → `WALLET_OPERATE` (operate) · staff
- `listWalletDisputes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1157` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1157`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 8: Works in Device, Credential & Account Security → Detect compromised accounts, shared credentials and suspicious device behavior. Requirement 4.3.32 specifically includes detection of account sharing and unauthorized access patterns. Device …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (54 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1157?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Digital Key, Customer Login, API Credential, Security Rules.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1158` AI Fraud & Anomaly Detection Studio

**Configure AI-driven detection of suspicious wallet behavior that fixed rules may not identify. Requirement 4.3.32 explicitly requires AI monitoring for unusual top-ups, abnormal spending, account sharing, rapid transfers, duplicate transactions and unauthorized access. AI Detection Categories**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1158 |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Every AI alert should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/ai-fraud-anomaly-detection-studio-bo-1158` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **AI Fraud & Anomaly Detection Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet risk rules that setWalletRiskRules writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI detection of unusual top-ups, spending and sharing that fixed rules miss.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletRiskRules and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **AI rule**: Sensitivity and action as for other rules. *(source: contracts/satellite/wallet.yaml#setWalletRiskRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Every fraud anomaly detection** (data table)

| Shows | Format | Notes |
|---|---|---|
| Why was this flagged? | text | not in the schema: `Why was this flagged?` |

**The selected fraud anomaly detection** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Why was this flagged? | text | not in the schema: `Why was this flagged?` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Duplicate Transactions (primary button) | navigation or local | — | — | — | — |
| Unauthorized Access (secondary button) | navigation or local | — | — | — | — |
| Refund Abuse (secondary button) | navigation or local | — | — | — | — |
| Gift Card Abuse (secondary button) | navigation or local | — | — | — | — |
| Voucher Abuse (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fraud anomaly detection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fraud anomaly detection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fraud anomaly detection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the fraud anomaly detection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
model:
  sensitivity: medium
  action: score only
```

#### Permissions

- `setWalletRiskRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.31 | Apply fraud and security controls. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |
| 4.3.32 | AI identifies suspicious wallet activity. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1158` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1158`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 10: Works in AI Fraud & Anomaly Detection Studio → Configure AI-driven detection of suspicious wallet behavior that fixed rules may not identify. Requirement 4.3.32 explicitly requires AI monitoring for unusual top-ups, abnormal spending, account …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1158?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Duplicate Transactions, Unauthorized Access, Refund Abuse, Gift Card Abuse, Voucher Abuse.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1159` Automated Security Action Orchestration

**Determine what TICVAI automatically does when a security or fraud condition occurs. Available Actions Low Risk → Approve Medium Risk → Approve + Monitor Elevated Risk → Step-Up Authentication High Risk → Hold Transaction Very High Risk → Restrict Function Critical → Block Wallet + Create Case Granular Restrictions Instead of always blocking the whole wallet, TICVAI can: Block P2P transfers Disable top-ups Disable online payments Disable wearable payments Disable specific credential Freeze specific credit type Require MFA Set temporary spending limit Allow balance inquiry only**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1159 |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_OPERATE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/automated-security-action-orchestration-bo-1159` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the wallet risk rules and their automated actions that setWalletRiskRules and setWalletRestriction writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** What happens automatically at each risk level: approve, monitor, step-up, hold, block.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setWalletRiskRules, setWalletRestriction and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Trigger | select field | — | — | — | — | — | — |
| Risk score | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Duration | select field | — | — | — | — | — | — |
| Customer notification | select field | — | — | — | — | — | — |
| Security notification | select field | — | — | — | — | — | — |
| Case creation | select field | — | — | — | — | — | — |
| Approval for release | select field | — | — | — | — | — | — |
| Automatic expiry | select field | — | — | — | — | — | — |
| Escalation | select field | — | — | — | — | — | — |
| Example | select field | — | — | — | — | — | — |
| Suspected credential compromise | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **level to action**: A ladder of levels to actions. *(source: contracts/satellite/wallet.yaml#setWalletRiskRules / contracts/satellite/wallet.yaml#setWalletRestriction)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The automated security action configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the automated security action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No automated security action configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ladder:
- 'low: approve'
- 'medium: approve and monitor'
- 'elevated: step-up'
- 'high: freeze'
```

#### Permissions

- `setWalletRiskRules` → `WALLET_CONFIGURE` (configure) · staff
- `setWalletRestriction` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.31 | Apply fraud and security controls. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |
| 4.3.32 | AI identifies suspicious wallet activity. | Bundles and Promotions | CONTRACTED | `setWalletRiskRules` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1159` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1159`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 12: Works in Automated Security Action Orchestration → Determine what TICVAI automatically does when a security or fraud condition occurs. Available Actions Low Risk → Approve Medium Risk → Approve + Monitor Elevated Risk → Step-Up Authentication High …

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1159?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_OPERATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1160` Fraud Alert & Investigation Case Management

**Provide security teams with a structured investigation workspace. Alert Queue**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block D · task VM-BO-1160 |
| Who uses it | venue staff holding `RISK_INVESTIGATE`, `RISK_REVIEW`, `WALLET_VIEW` (2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `alertId` (navigation), `caseId` (navigation) |
| Route | `/orders-money/fraud-alert-investigation-case-management-bo-1160` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** The venue's fraud and risk investigation workspace: an alert queue (wallet, payments, credentials), triage, and cases with evidence and outcome. Flagged transactions are never auto-approved or auto-declined; they wait for a person. The one thing to get right: risk score and AI score are distinguished - the deterministic rules triggered and the AI's composite score - and both are explained.

**Known correction pending (do not draw the wrong version)**

- **The table carries 45 board columns.** Why: Keep the queue to about 10 columns; the rest belong in the case detail. *(source: screens/P08-venue-back-office.yaml#BO-1160; AI & Intelligence)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listWalletDisputes` ?status |
| Status | radio group | — | Open · Monitoring · Dismissed · False positive · Escalated | `listRiskAlerts` ?status |
| Band | radio group | — | Low · Medium · High · Critical | `listRiskAlerts` ?band |
| Kind | select | — | Transaction · Velocity · Entity · Network · Staff leakage · Scan abuse · Account takeover · Chargeback | `listRiskAlerts` ?kind |
| Entity type | select | — | Customer · Account · Device · Payment token · Credential · Cluster · Staff · Wallet · Ip address | `listRiskAlerts` ?entityType |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every fraud alert investigation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Alert ID | text | not in the schema: `Alert ID` |
| Wallet | text | not in the schema: `Wallet` |
| Customer | text | not in the schema: `Customer` |
| Transaction | text | not in the schema: `Transaction` |
| Amount | text | not in the schema: `Amount` |
| Risk score | text | not in the schema: `Risk score` |
| AI score | text | not in the schema: `AI score` |
| Triggered rules | text | not in the schema: `Triggered rules` |
| Device | text | not in the schema: `Device` |
| Credential | text | not in the schema: `Credential` |
| Venue | text | not in the schema: `Venue` |
| Date/time | text | not in the schema: `Date/time` |
| Priority | text | not in the schema: `Priority` |
| Status | text | not in the schema: `Status` |
| Case workflow | text | not in the schema: `Case Workflow` |
| New | text | not in the schema: `New` |
| → triage | text | not in the schema: `→ Triage` |
| → under investigation | text | not in the schema: `→ Under Investigation` |
| → customer verification | text | not in the schema: `→ Customer Verification` |
| → escalated | text | not in the schema: `→ Escalated` |
| → confirmed fraud / false positive | text | not in the schema: `→ Confirmed Fraud / False Positive` |
| → resolved | text | not in the schema: `→ Resolved` |
| → closed | text | not in the schema: `→ Closed` |
| Investigator workspace | text | not in the schema: `Investigator Workspace` |
| Wallet timeline | text | not in the schema: `Wallet timeline` |
| Transaction history | text | not in the schema: `Transaction history` |
| Funding history | text | not in the schema: `Funding history` |
| Transfer network | text | not in the schema: `Transfer network` |
| Devices | text | not in the schema: `Devices` |
| Credentials | text | not in the schema: `Credentials` |
| … 15 more | | `schemas.json` |

**The selected fraud alert investigation** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Alert ID | text | not in the schema: `Alert ID` |
| Wallet | text | not in the schema: `Wallet` |
| Customer | text | not in the schema: `Customer` |
| Transaction | text | not in the schema: `Transaction` |
| Amount | text | not in the schema: `Amount` |
| Risk score | text | not in the schema: `Risk score` |
| AI score | text | not in the schema: `AI score` |
| Triggered rules | text | not in the schema: `Triggered rules` |
| Device | text | not in the schema: `Device` |
| Credential | text | not in the schema: `Credential` |
| Venue | text | not in the schema: `Venue` |
| Date/time | text | not in the schema: `Date/time` |
| Priority | text | not in the schema: `Priority` |
| Status | text | not in the schema: `Status` |
| Case workflow | text | not in the schema: `Case Workflow` |
| New | text | not in the schema: `New` |
| → triage | text | not in the schema: `→ Triage` |
| → under investigation | text | not in the schema: `→ Under Investigation` |
| → customer verification | text | not in the schema: `→ Customer Verification` |
| → escalated | text | not in the schema: `→ Escalated` |
| → confirmed fraud / false positive | text | not in the schema: `→ Confirmed Fraud / False Positive` |
| → resolved | text | not in the schema: `→ Resolved` |
| → closed | text | not in the schema: `→ Closed` |
| Investigator workspace | text | not in the schema: `Investigator Workspace` |
| Wallet timeline | text | not in the schema: `Wallet timeline` |
| Transaction history | text | not in the schema: `Transaction history` |
| Funding history | text | not in the schema: `Funding history` |
| Transfer network | text | not in the schema: `Transfer network` |
| Devices | text | not in the schema: `Devices` |
| Credentials | text | not in the schema: `Credentials` |
| … 15 more | | `schemas.json` |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **alert queue**: Alert, wallet/customer, transaction and amount in AED, rules triggered, AI score band, device, credential, venue, time, priority, status. *(source: contracts/satellite/ai.yaml#listRiskAlerts / DI-537 / ADR-0053)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Triage / open case / close**: As ADM-633. *(source: contracts/satellite/ai.yaml#decideRiskAlert / contracts/satellite/ai.yaml#createRiskCase / contracts/satellite/ai.yaml#closeRiskCase)*

**Data it reads**: `listWalletDisputes` (onLoad, Fraud cases); `listRiskAlerts` (onLoad, Risk alerts)

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fraud alert investigation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fraud alert investigation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fraud alert investigation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the fraud alert investigation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already closed, or a proposed action is still awaiting approval (`case-actions-open`).; 409 The alert is already decided (`alert-not-open`). |

#### Consistency with other screens

- Match `ADM-633`: Same case component and decisions.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alert:
  wallet: W-20931
  transaction: Top-up AED 2,000.00
  rules:
  - 3 top-ups in 10 min
  aiScore: high
  status: Held for review
```

#### Permissions

- `listWalletDisputes` → `WALLET_VIEW` (read) · staff
- `listRiskAlerts` → `RISK_REVIEW` (operate) · staff
- `decideRiskAlert` → `RISK_REVIEW` (operate) · staff
- `createRiskCase` → `RISK_INVESTIGATE` (operate) · staff
- `getRiskCase` → `RISK_INVESTIGATE` (operate) · staff
- `closeRiskCase` → `RISK_INVESTIGATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.55 | Detect suspicious access patterns including unusual login locations, failed login spikes, privilege escalation attempts and abnormal transaction behavior. | F&B POS | CONTRACTED | `listRiskAlerts` |
| 8.3.10 | System shall generate payment fraud alerts. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.15 | System shall generate chargeback risk alerts. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.18 | System shall detect excessive refunds by employee. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.22 | System shall generate refund fraud alerts. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.30 | System shall generate ticket abuse alerts. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.31 | System shall detect unusual login activity. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.32 | System shall detect impossible travel scenarios. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.34 | System shall detect unusual password reset activity. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.35 | System shall detect credential stuffing attempts. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.36 | System shall detect account enumeration attempts. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| 8.3.37 | System shall generate account takeover alerts. | Unified Operations Dashboard | CONTRACTED | `listRiskAlerts` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Transactions get a risk score; high-risk transactions are flagged and routed to the operations team for manual cross-verification, never auto-approved or auto-declined. *(agreed · MoM 27 Aug 2026, 4.10 Transaction risk scoring engine · DI-537)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1160` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1160`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 14: Works in Fraud Alert & Investigation Case Management → Provide security teams with a structured investigation workspace. Alert Queue

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (90 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1160?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `RISK_INVESTIGATE`, `RISK_REVIEW`, `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1161` Security Rules Testing, Simulation & AI Sandbox

**Test new fraud rules and AI configurations before applying them to live transactions. This screen is particularly important because overly aggressive security rules can create large numbers of false declines. Simulation Modes Single Transaction Test**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-1161 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/security-rules-testing-simulation-ai-sandbox-bo-1161` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-025): simulateCreditConsumption simulates credit spending, not risk rule testing; a security sandbox needs a rule backtest, recorded as a contract gap (design-notes … Contract gap recorded 2 October 2026 (CHG-WIR-027): A wallet risk-rule backtest or simulation (rules against sample or historical transactions) and a read of the rules under test.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Test new fraud rules on past transactions before going live, to see false positives.

**Fixed on main** (the package already carries these; draw what it says): The simulation operation is credit consumption, not risk rule testing. (CHG-WIR-025); No read operation: the screen declares only simulateCreditConsumption and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every security rules testing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Transactions evaluated → 1,245,000 | text | not in the schema: `Transactions Evaluated → 1,245,000` |
| 4% | text | not in the schema: `Would Approve → 98.4%` |
| 1% | text | not in the schema: `Would Challenge → 1.1%` |
| 4% | text | not in the schema: `Would Hold → 0.4%` |
| 1% | text | not in the schema: `Would Decline → 0.1%` |
| Impact analysis | text | not in the schema: `Impact Analysis` |
| Potential fraud detected | text | not in the schema: `Potential fraud detected` |
| Potential false positives | text | not in the schema: `Potential false positives` |
| Customer impact | text | not in the schema: `Customer impact` |
| Financial exposure | text | not in the schema: `Financial exposure` |
| Channels affected | text | not in the schema: `Channels affected` |
| Wallet types affected | text | not in the schema: `Wallet types affected` |

**The selected security rules testing** (detail panel): The pack groups this record's detail under its own headings: “Enter”.

| Shows | Format | Notes |
|---|---|---|
| Transactions evaluated → 1,245,000 | text | not in the schema: `Transactions Evaluated → 1,245,000` |
| 4% | text | not in the schema: `Would Approve → 98.4%` |
| 1% | text | not in the schema: `Would Challenge → 1.1%` |
| 4% | text | not in the schema: `Would Hold → 0.4%` |
| 1% | text | not in the schema: `Would Decline → 0.1%` |
| Impact analysis | text | not in the schema: `Impact Analysis` |
| Potential fraud detected | text | not in the schema: `Potential fraud detected` |
| Potential false positives | text | not in the schema: `Potential false positives` |
| Customer impact | text | not in the schema: `Customer impact` |
| Financial exposure | text | not in the schema: `Financial exposure` |
| Channels affected | text | not in the schema: `Channels affected` |
| Wallet types affected | text | not in the schema: `Wallet types affected` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **backtest**: Would-have-tripped count and examples. *(source: contracts/satellite/wallet.yaml#simulateCreditConsumption)*

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The security rules testing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the security rules testing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No security rules testing yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the security rules testing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
backtest:
  rule: Rapid top-ups
  wouldTrip: 38
  falsePositives: est. 30
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1161` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1161`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 16: Works in Security Rules Testing, Simulation & AI Sandbox → Test new fraud rules and AI configurations before applying them to live transactions. This screen is particularly important because overly aggressive security rules can create large numbers of false …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1161?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1162` Security Governance, Audit & Rule Publication

**Govern how wallet security policies, fraud models and automated actions are changed and released.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-BO-1162 |
| Who uses it | venue staff holding `AUDIT_VIEW`, `WALLET_CONFIGURE`, `WALLET_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `ruleCode` (navigation), `version` (navigation) |
| Route | `/orders-money/security-governance-audit-rule-publication-bo-1162` |

**What the spec says about it.** **Applies to the whole tenant (design-note correction, 2 October 2026):** the wallet configuration is tenant-scoped, so the header says "Tenant-wide wallet security" and the screen opens only to a tenant administrator holding the wallet configuration right. **The risk rules are read with getWalletRiskRules (agreed, ledger) 4 October 2026, so the status actions have a ruleCode** (CHG-FXS-003)

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How wallet configuration and risk rules are changed and released: versions, a field-level diff, restore as a draft, publish with validation findings, and switching one risk rule off at once without republishing. A rollback is as deliberate as the change that caused it.

**Fixed on main** (the package already carries these; draw what it says): The purpose text is the financial-control layer (liabilities, breakage, reconciliation), not security governance. (CHG-WIR-026); The operations are tenant-scoped while the screen sits in the venue back office. (CHG-SBO-010).

#### Inputs: what the user enters or picks

**Sent by *Rollback*** (`restoreWalletConfigurationVersion`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | — | `restoreWalletConfigurationVersion` body |

**Sent by *Emergency disable*** (`setWalletRiskRuleStatus`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Active · Suspended · Emergency disabled | — | — | `setWalletRiskRuleStatus` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required unless `status` is `active`. | `setWalletRiskRuleStatus` body |
| Until `until` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Only with `suspended`. Empty means until reactivated. | `setWalletRiskRuleStatus` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every security governance audit** (data table)

| Shows | Format | Notes |
|---|---|---|
| Risk policies | text | not in the schema: `Risk policies` |
| Rule versions | text | not in the schema: `Rule versions` |
| AI configuration version | text | not in the schema: `AI configuration version` |
| Thresholds | text | not in the schema: `Thresholds` |
| Automated actions | text | not in the schema: `Automated actions` |
| Effective dates | text | not in the schema: `Effective dates` |
| Applicable tenants | text | not in the schema: `Applicable tenants` |
| Applicable venues | text | not in the schema: `Applicable venues` |
| Owner | text | not in the schema: `Owner` |
| Approval status | text | not in the schema: `Approval status` |
| Change governance | text | not in the schema: `Change Governance` |

**Risk rules** (data table, from `getWalletRiskRules`): Each rule with its code and status; Emergency disable and Suspend act on the selected rule's ruleCode.

| Shows | Format | Notes |
|---|---|---|
| Rules | list or chips (count when long) | — |
| Code | text | — |
| Signal | chip: Velocity count, Velocity amount, New credential, Geography jump, Device change … | 4.3.32 (29 September, build pass). `accountSharing`: one wallet or credential used from more devices or places at once than one person can … |
| Threshold | 1,234.5 | — |
| Window minutes | 1,234 | — |
| Action | chip: Score only, Challenge, Hold transaction, Freeze wallet, Raise case | — |
| Minimum confidence | 1,234.5 | Required before an automated freeze. A rule that freezes on a false positive will eventually freeze a family in a queue. |
| Alert on action | yes / no (icon or chip) | — |
| Status | chip: Active, Suspended, Emergency disabled | Set by `setWalletRiskRuleStatus`, not by publishing the rule set. A rule not `active` is evaluated for nothing (VM close-out, 29 September). |
| Status reason | text | — |
| Status until | 1 Oct 2026, 14:30 | When a `suspended` rule returns to `active` by itself. |

**The selected security governance audit** (detail panel): The pack groups this record's detail under its own headings: “Every change records”, “Maintain history for”, “Then”, “The module progression is now”.

| Shows | Format | Notes |
|---|---|---|
| Risk policies | text | not in the schema: `Risk policies` |
| Rule versions | text | not in the schema: `Rule versions` |
| AI configuration version | text | not in the schema: `AI configuration version` |
| Thresholds | text | not in the schema: `Thresholds` |
| Automated actions | text | not in the schema: `Automated actions` |
| Effective dates | text | not in the schema: `Effective dates` |
| Applicable tenants | text | not in the schema: `Applicable tenants` |
| Applicable venues | text | not in the schema: `Applicable venues` |
| Owner | text | not in the schema: `Owner` |
| Approval status | text | not in the schema: `Approval status` |
| Change governance | text | not in the schema: `Change Governance` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Version comparison (primary button) | `diffWalletConfigurationVersion` GET `/wallet-configuration/versions/{version}/diff` | — | WalletConfigurationDiff | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Rollback (destructive button) | `restoreWalletConfigurationVersion` POST `/wallet-configuration/versions/{version}/restore` | inline | WalletConfigurationVersion | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Emergency disable (secondary button) | `setWalletRiskRuleStatus` POST `/wallet-risk-rules/{ruleCode}/status` | inline | WalletRiskRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 No `reason` for `suspended` or `emergencyDisabled`, or `until` given with a status other than `suspended`, or … | — |
| Rule suspension (secondary button) | `setWalletRiskRuleStatus` POST `/wallet-risk-rules/{ruleCode}/status` | inline | WalletRiskRules | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 No `reason` for `suspended` or `emergencyDisabled`, or `until` given with a status other than `suspended`, or … | — |
| Security Audit (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **diff**: Changes grouped by area (credit types, consumption, channel rules, authentication, risk rules, accounting, reconciliation, integration) with before and after values. *(source: contracts/satellite/wallet.yaml#diffWalletConfigurationVersion)*
- **audit**: Who changed what, where and when, filterable by area. *(source: contracts/spine/tenancy.yaml#listAuditRecords)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Restore version**: Copies it into the working draft with its findings; it does not publish. *(source: contracts/satellite/wallet.yaml#restoreWalletConfigurationVersion)*
- **Suspend or emergency-disable a rule**: Immediate, no new version; suspended may carry an "until" and returns to active by itself; emergency-disabled stays off. *(source: contracts/satellite/wallet.yaml#setWalletRiskRuleStatus)*

**Data it reads**: `listWalletConfigurationVersions` (onLoad, Wallet configuration versions, newest first); `getWalletRiskRules` (onLoad, The risk rules in force, each with the ruleCode …)

**Where the user goes next**

- → `BO-1153` Wallet Security & Risk Command Center: *Back to Wallet Security & Risk Command Center*

**What opens over it**

- confirmDialog *Rollback*: **Rollback on a security governance audit is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The security governance audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the security governance audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No security governance audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the security governance audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WALLET_VIEW`, which `listWalletConfigurationVersions` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AUDIT_VIEW` for `listAuditRecords`; `WALLET_CONFIGURE` for `publishWalletConfiguration`, `restoreWalletConfigurationVersion` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 No `reason` for `suspended` or `emergencyDisabled`, or `until` given with a status other than `suspended`, or `until` in the past. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- v: 14
  published: 2026-10-28 18:05
  by: Fatima Rahman
  note: Velocity limits for top-ups
- v: 13
  published: '2026-10-12'
rule:
  code: VEL-TOPUP-01
  status: suspended
  until: 2026-11-15 08:00
  reason: False positives on corporate cards
```

#### Permissions

- `publishWalletConfiguration` → `WALLET_CONFIGURE` (configure) · staff
- `listAuditRecords` → `AUDIT_VIEW` (read) · staff
- `listWalletConfigurationVersions` → `WALLET_VIEW` (read) · staff
- `diffWalletConfigurationVersion` → `WALLET_VIEW` (read) · staff
- `restoreWalletConfigurationVersion` → `WALLET_CONFIGURE` (configure) · staff
- `setWalletRiskRuleStatus` → `WALLET_CONFIGURE` (configure) · staff
- `getWalletRiskRules` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WALLET_VIEW`, which `listWalletConfigurationVersions` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AUDIT_VIEW` for `listAuditRecords`; `WALLET_CONFIGURE` for `publishWalletConfiguration`, `restoreWalletConfigurationVersion` …

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1162` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1162`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 8
- Flow F300 *Wallet Configuration Backend Structure v1.0 board 8: Wallet Security & Risk …*, step 18: Works in Security Governance, Audit & Rule Publication → Govern how wallet security policies, fraud models and automated actions are changed and released. Configuration Areas

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403, 404, 422).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1162?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, Version comparison, Rollback, Emergency disable, Rule suspension, Security Audit.
- [ ] Every transition is wired: `BO-1153`.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `WALLET_CONFIGURE`, `WALLET_VIEW`.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"closeRiskCase": {"method":"POST","path":"/risk/cases/{caseId}/close","contract":"ai","summary":"Close a case with an outcome","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskCase"},
"createRiskCase": {"method":"POST","path":"/risk/cases","contract":"ai","summary":"Open an investigation","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskCase"},
"decideRiskAlert": {"method":"POST","path":"/risk/alerts/{alertId}/decide","contract":"ai","summary":"Dismiss, monitor, mark false positive, or escalate","permission":"RISK_REVIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRiskAlert"},
"diffWalletConfigurationVersion": {"method":"GET","path":"/wallet-configuration/versions/{version}/diff","contract":"wallet","summary":"Compare a wallet configuration version against another or the working draft","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"against","in":"query","required":null}],"requestBody":null,"responds":"WalletConfigurationDiff"},
"getRiskCase": {"method":"GET","path":"/risk/cases/{caseId}","contract":"ai","summary":"A case with its evidence and actions","permission":"RISK_INVESTIGATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiRiskCaseDetail"},
"getWalletRiskRules": {"method":"GET","path":"/wallet-risk-rules","contract":"wallet","summary":"The wallet risk rules","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WalletRiskRules"},
"linkWalletCredential": {"method":"POST","path":"/wallet-credentials","contract":"wallet","summary":"Bind a wristband, card or device to a wallet","permission":"WALLET_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletCredential","responds":"WalletCredential"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRiskAlerts": {"method":"GET","path":"/risk/alerts","contract":"ai","summary":"Risk alerts","permission":"RISK_REVIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"band","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"entityType","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWalletConfigurationVersions": {"method":"GET","path":"/wallet-configuration/versions","contract":"wallet","summary":"Wallet configuration versions, newest first","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWalletDisputes": {"method":"GET","path":"/wallet-disputes","contract":"wallet","summary":"Contested transactions and operational exceptions","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"WalletDispute"},
"publishWalletConfiguration": {"method":"POST","path":"/wallet-configuration/publish","contract":"wallet","summary":"Validate and publish the wallet configuration as a version","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletConfigurationVersion"},
"restoreWalletConfigurationVersion": {"method":"POST","path":"/wallet-configuration/versions/{version}/restore","contract":"wallet","summary":"Put a previous wallet configuration back as the working draft","permission":"WALLET_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletConfigurationVersion"},
"setWalletRestriction": {"method":"POST","path":"/wallet-restrictions","contract":"wallet","summary":"Block, freeze or restrict a wallet","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletRestriction","responds":"WalletRestriction"},
"setWalletRiskRuleStatus": {"method":"POST","path":"/wallet-risk-rules/{ruleCode}/status","contract":"wallet","summary":"Suspend, emergency-disable or reactivate one risk rule","permission":"WALLET_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletRiskRules"},
"setWalletRiskRules": {"method":"PUT","path":"/wallet-risk-rules","contract":"wallet","summary":"Velocity, behaviour and what happens when a rule trips","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletRiskRules","responds":"WalletRiskRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiRiskAlert": {"type":"object","x-ticvai-persistence":"ai.risk_alert","description":"**A risk alert** (AIP-109): raised by scoring or re-scoring. **Alert, case and confirmed fraud are kept distinct** (AIP-163): an alert is a signal to look, not a finding.","required":["kind","entityType","entityRef","band","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["transaction","velocity","entity","network","staffLeakage","scanAbuse","accountTakeover","chargeback"]},"entityType":{"type":"string","enum":["customer","account","device","paymentToken","credential","cluster","staff","wallet","ipAddress"]},"entityRef":{"type":"string"},"score":{"type":"integer","minimum":0,"maximum":100},"band":{"type":"string","enum":["low","medium","high","critical"],"description":"Design 5.6: a risk score and band, never a probability."},"reasonCodes":{"type":"array","items":{"type":"string"}},"correlationKey":{"type":"string","nullable":true},"assessmentId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["open","monitoring","dismissed","falsePositive","escalated"],"readOnly":true},"caseId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.risk_case"},"raisedAt":{"type":"string","format":"date-time","readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionNote":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskCase": {"type":"object","x-ticvai-persistence":"ai.risk_case","description":"**An investigation** (AIP-150..160). Its evidence and actions are `ai.case_evidence` and `ai.case_action`. The summary is written by a model from structured evidence only (AIP-153); the outcome is a person's.","required":["reference","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"reference":{"type":"string","readOnly":true},"title":{"type":"string"},"status":{"type":"string","enum":["open","investigating","pendingAction","closed"],"readOnly":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"entities":{"type":"array","items":{"type":"object","properties":{"entityType":{"type":"string","enum":["customer","account","device","paymentToken","credential","cluster","staff"]},"entityRef":{"type":"string"}}}},"alertIds":{"type":"array","items":{"type":"string","format":"uuid"}},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"summary":{"type":"string","nullable":true,"readOnly":true},"outcome":{"type":"string","enum":["confirmedFraud","notFraud","inconclusive"],"nullable":true,"readOnly":true},"closureNote":{"type":"string","nullable":true,"readOnly":true},"openedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"openedAt":{"type":"string","format":"date-time","readOnly":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskCaseAction": {"type":"object","x-ticvai-persistence":"ai.case_action","description":"**A restrictive action proposed from a case** (AIP-136). It goes to the owning module through the action pipeline, never straight from review; at the first-release ceiling (L1 advisory, design 3.8) it is a recommendation the owning module's operator applies. **Scoped through its case.**","required":["caseId","action","targetContract"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"caseId":{"type":"string","format":"uuid","x-ticvai-references":"ai.risk_case"},"action":{"type":"string","enum":["blockPaymentToken","suspendAccount","restrictWallet","revokeEntitlement","flagCustomer","requireStepUp","holdRefunds","lockIdentity"]},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"targetRef":{"type":"string"},"rationale":{"type":"string"},"status":{"type":"string","enum":["recommended","planned","awaitingApproval","applied","rejected","failed"],"readOnly":true},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan"},"proposedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"proposedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AiRiskCaseDetail": {"type":"object","x-ticvai-persistence":"none — ai.risk_case with its evidence, actions and alerts","description":"A case with everything attached to it.","required":["case"],"properties":{"case":{"$ref":"#/components/schemas/AiRiskCase"},"evidence":{"type":"array","items":{"$ref":"#/components/schemas/AiRiskCaseEvidence"}},"actions":{"type":"array","items":{"$ref":"#/components/schemas/AiRiskCaseAction"}},"alerts":{"type":"array","items":{"$ref":"#/components/schemas/AiRiskAlert"}}}},
"AiRiskCaseEvidence": {"type":"object","x-ticvai-persistence":"ai.case_evidence","description":"**Case evidence** (AIP-155): `jsonb` plus an immutable Blob copy. **Scoped through its case** (`platform.apply_parent_rls`). Never edited; a correction is new evidence.","required":["caseId","kind","label"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"caseId":{"type":"string","format":"uuid","x-ticvai-references":"ai.risk_case"},"kind":{"type":"string","enum":["assessment","alert","transaction","networkSnapshot","note","document"]},"ref":{"type":"string","nullable":true},"content":{"type":"object","additionalProperties":true,"nullable":true},"blobRef":{"type":"string","nullable":true,"readOnly":true,"description":"The immutable (WORM) copy."},"label":{"type":"string","enum":["source","derived","modelInferred"]},"contentHash":{"type":"string","readOnly":true},"addedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"addedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"WalletConfigurationDiff": {"x-ticvai-persistence":"none — computed from wallet.configuration_version_snapshot (a published version) against the area tables (the working draft)","type":"object","description":"Board 8, p.98. Field-level comparison of two wallet configuration versions, shaped as white-label `ConfigDiff`.","required":["fromVersion","toVersion","changes"],"properties":{"fromVersion":{"type":"integer"},"toVersion":{"type":"integer","nullable":true,"description":"Null when compared against the working draft."},"changes":{"type":"array","items":{"type":"object","required":["area","path","changeKind"],"properties":{"area":{"type":"string","enum":["walletTypes","creditTypes","consumptionPolicy","fundingRules","channelRules","authenticationPolicy","transferRules","refundPolicy","riskRules","accountingMapping","reconciliationSources","integrationMappings"]},"path":{"type":"string"},"changeKind":{"type":"string","enum":["added","removed","modified"]},"before":{"type":"string","nullable":true},"after":{"type":"string","nullable":true}}}}}},
"WalletConfigurationVersion": {"type":"object","x-ticvai-persistence":"wallet.configuration_version","description":"Boards 1.10 and 10.8. **Ten boards of configuration that interact.**","properties":{"version":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"publishedBy":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"code":{"type":"string"},"message":{"type":"string"}}}},"scopePath":{"type":"string"}}},
"WalletCredential": {"type":"object","x-ticvai-persistence":"wallet.credential","description":"Boards 6.4 and 6.5. **A credential is not the wallet** — a lost wristband is relinked, not refunded.\n","required":["walletId","kind","identifier"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["card","wristband","nfc","rfid","qr","mobileApp","digitalKey"]},"identifier":{"type":"string"},"linkedAt":{"type":"string","format":"date-time"},"unlinkedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","lost","replaced","blocked","expired"]},"replacedByCredentialId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"WalletDispute": {"type":"object","x-ticvai-persistence":"wallet.dispute","description":"Board 7.9. **Internal, and the venue decides it** — unlike a card chargeback.","required":["walletId","description"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"transactionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"description":{"type":"string"},"raisedBy":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["open","investigating","escalated","upheld","rejected","withdrawn"],"description":"`escalated` added with `resolveWalletDispute` (VM close-out, 29 September). `upheld`, `rejected` and `withdrawn` are closed."},"resolution":{"type":"string","nullable":true},"escalatedToRoleId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"reprocessedTransactionIds":{"type":"array","readOnly":true,"description":"Transactions created by a `reprocess` action.","items":{"type":"string","format":"uuid"}},"resolvedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"adjustmentId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"WalletRestriction": {"type":"object","x-ticvai-persistence":"wallet.restriction","description":"Board 7.8. **Freeze, block and restrict are three different things.**","required":["walletId","kind","reason"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["freeze","block","restrict","none"],"description":"**`freeze` stops spending and allows funding** — what you do while investigating. **`block` stops both** — a confirmed fraud. **`restrict` limits channels or categories** — what a parent asked for.\n"},"blockedChannels":{"type":"array","items":{"type":"string"}},"blockedCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string"},"appliedBy":{"type":"string","format":"uuid"},"appliedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"WalletRiskRules": {"type":"object","x-ticvai-persistence":"wallet.risk_rules + wallet.risk_rule","description":"Boards 8.2 to 8.7. **A risk rule with no action is a report.**","properties":{"rules":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"signal":{"type":"string","enum":["velocityCount","velocityAmount","newCredential","geographyJump","deviceChange","dormantThenLarge","repeatedFailure","refundPattern","accountSharing","duplicateTransaction","aiRiskScore"],"description":"4.3.32 (29 September, build pass). **`accountSharing`**: one wallet or credential used from more devices or places at once than one person can be (`threshold` concurrent devices within `windowMinutes`). **`duplicateTransaction`**: the same amount at the same acceptance point within `windowMinutes` (`threshold` repeats). **`aiRiskScore`**: the score the `ai` risk engine returns for the wallet operation (`scoreTransactionRisk`, rules first and statistical baselines as history builds, ai-system-design 3.10); `threshold` is the score at or above which the rule acts. The wallet keeps its own rules and actions; the AI finding and its case are the `ai` contract's (`listRiskAlerts`)."},"threshold":{"type":"number"},"windowMinutes":{"type":"integer"},"action":{"type":"string","enum":["scoreOnly","challenge","holdTransaction","freezeWallet","raiseCase"]},"minimumConfidence":{"type":"number","nullable":true,"description":"**Required before an automated freeze.** A rule that freezes on a false positive will eventually freeze a family in a queue.\n"},"alertOnAction":{"type":"boolean","x-ticvai-column":"does_alert_on_action","default":true},"status":{"type":"string","readOnly":true,"enum":["active","suspended","emergencyDisabled"],"default":"active","description":"Set by `setWalletRiskRuleStatus`, not by publishing the rule set. A rule not `active` is evaluated for nothing (VM close-out, 29 September)."},"statusReason":{"type":"string","nullable":true,"readOnly":true},"statusUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a `suspended` rule returns to `active` by itself."}}}},"scopePath":{"type":"string"}}}
}
```
