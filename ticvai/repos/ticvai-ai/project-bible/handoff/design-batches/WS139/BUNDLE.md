# WS139 — Marketing CRM Configuration Reference v1.0 board 5

**10 screens · 10 operations · 13 schemas · 4 permissions**

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
  `AI_USE, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW`. A control nobody can use must say so,
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

### Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers)

Customer & marketing is how a venue knows its guests and talks to them. There is ONE guest profile per person across ticketing, F&B and retail, so a guest who books online and later dines is the same profile (DI-339). A profile needs at least an email or a mobile, never neither (DI-372). Profiles are created by registration, by guest checkout, or by staff at a till or desk. Repeat guest checkouts with the same verified email or phone attach to the same profile automatically (DI-941, R120 default). Two records that might be the same person are NEVER merged automatically: the guest is asked to confirm, and an admin review queue runs alongside (DI-377). Each candidate shows why it matched; the record that loses is superseded, not deleted; consent takes the narrower of the two positions (DI-808). Around the profile sit three things that must never be confused. CONSENT is what the law allows: per purpose and per channel, append-only, with the notice version and the source (recordConsent). It is Given, Withdrawn or Not asked. A SUBSCRIPTION is what the guest asked to receive, e.g. a newsletter list (MarketingSubscription). A PREFERENCE is what they like: table, dietary, accessibility (updateGuestPreferences). An anonymous visitor's cookie decision is recorded against a device key (recordDeviceConsent) and attaches to the guest when they sign in (claimDeviceConsent). Marketing consent at GUEST CHECKOUT is an open client question, and the design follows its default: an unticked opt-in beside the terms, one per channel and purpose. It is recorded with source "checkout" against the order and the verified contact, and nothing is sent without it. Whether that is sufficient consent under PDPL is the client DPO's call (M18-15 (audit R-M18-15), DI-954, DI-940). Marketing reads profiles through SEGMENTS (rules, evaluated when used) and static LISTS (imported). It reaches guests by CAMPAIGNS (one send to an audience) and JOURNEYS (automations started by an event, with waits and branches). Journeys may offer only pre-configured offers, never a free-typed discount (MoM 2026-08-20 4.6). Everything goes through ONE communications module that every other module uses (MoM 2026-08-31 4.6). Consent and suppression are applied at send time, and the number excluded, with the reasons, is reported before anything goes out (launchCampaign). Transactional messages (tickets, receipts, queue calls, case replies) do not need marketing consent and must never carry marketing. LOYALTY pays for spend: points, tiers, rewards and expiry. GAMIFICATION pays for behaviour: challenges, badges, streaks, referrals and leaderboards (createChallenge). A guest reads their own loyalty position (getLoyaltyPosition). A till, the back office or support reads a named guest's (getGuestLoyalty, or identifyGuest at a till). SERVICE: one Case object covers lost property, complaints, questions, accessibility and refund requests (CaseKind). A guest raises one with raiseMyCase, which needs the connection …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Guest | The person the venue serves, signed in or not. In body copy on every surface. | Customer, User, Subject, Contact, Patron | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestProfile |
| Guest profile | The CRM record of one person (details, consent, preferences, history). Distinct from the Account, which is how a guest signs in. | Customer record, Contact, Subject | contracts/satellite/marketing-crm.yaml#getGuestProfile |
| Consent - Given / Withdrawn / Not asked | What the law allows, per purpose (marketing, personalisation, profiling, third-party sharing, AI processing, transactional) and per channel. "Not asked" is not "Withdrawn" and must look different. | Opted in/out as a status, Accepted, Declined, Revoked, Unsubscribed (that is a subscription) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentDecision |
| Subscription | A list the guest asked to receive (a newsletter, event news), per channel. Unsubscribing from a list is not withdrawing consent. | Consent, Opt-in | contracts/satellite/marketing-crm.yaml#/components/schemas/MarketingSubscription |
| Preferences | What the guest likes or needs (seating, drinks, dietary, accessibility, contact channel). Never grants permission. | Consents, Settings | contracts/satellite/marketing-crm.yaml#updateGuestPreferences |
| Send me offers and news | The marketing opt-in label beside the terms at checkout, unticked, one per channel and purpose. | I agree to marketing, Pre-ticked boxes, Keep me updated ticked by default | DI-954 |
| Points / Tier / Points to next tier / Expiring points | The loyalty position. Points are a liability earned per programme; tiers are ranked (Bronze, Silver, Gold, Platinum in the meetings). | Credits, Coins, Balance alone (wallet money is "credit"), Level | DI-382 |
| Pending points | Points earned on a purchase still inside its refund window; shown apart from spendable points. | Available points for pending ones | contracts/satellite/marketing-crm.yaml#getLoyaltyPosition |
| Reward | What points can be turned into (rewards catalogue). | Prize (games redemption uses prize), Voucher unless it is one | contracts/satellite/marketing-crm.yaml#listRewards |
| Challenge / Badge / Streak / Referral | Gamification - rewards for behaviour, not spend. Status badges such as Explorer, Adventurer, Legend. | Mission and Quest used interchangeably on one screen, Loyalty tier for a badge | DI-392 |
| Case | One service record - lost property, complaint, question, accessibility, refund request or other - with a number (venue prefix plus sequence), a status and an SLA. | Ticket (a ticket is an admission product), Issue, Incident (that is maintenance and safety) | contracts/satellite/marketing-crm.yaml#/components/schemas/CaseKind |
| Reply to guest / Internal note | The two kinds of case message. The agent always chooses one explicitly; there is no default. | Comment, Message (ambiguous) | F05 step 2 |
| Conversation | A live chat session (web chat, in-app, WhatsApp, SMS, email, kiosk, voice). With the assistant, then queued, then with an agent. It is not a case. | Ticket, Case (until one is raised from it) | contracts/satellite/marketing-crm.yaml#/components/schemas/ConversationState |
| Segment / List / Audience | A segment is rules evaluated when used. A list is static, imported or hand-picked. The audience is what a campaign or journey targets. | Group, Cohort, Target list for a segment | DI-381 |
| Campaign / Journey | A campaign is one send (one-off, scheduled, triggered or recurring) to an audience. A journey is an automation started by an event, with steps, waits and branches. | Flow (booking flows use it), Automation for a one-off send, Blast | R146 |
| Offer | A pre-configured, system-validated discount or benefit that a campaign or journey references. It is never typed into the builder. | Discount field, Coupon (unless the offer is a coupon code) | MoM 2026-08-20 4.6 |
| Reachable | How many guests in an audience can actually be sent to on a channel after consent and suppression. Always shown beside the matching count. | Audience size alone | contracts/satellite/marketing-crm.yaml#previewSegment |
| Possible duplicate / Merge | Two profiles that may be one person. Never called "Duplicate" as a verdict. Merging needs confirmation and stays reversible for 30 days. | Duplicate (as a status), Combine, Auto-merge | DI-808 |
| Data request | A guest's privacy request - a copy of my data, a correction, erasure, a restriction - with a legal clock. Statuses submitted, in progress, completed. | DSAR on guest screens, Subject data, Ticket | DI-379 |
| Waiver / Consent question | A waiver is a signed, versioned form. A consent question ("Are you able to swim?", "I accept the risk") is a single question asked per person or per booking and recorded as consent. | Contract, Disclaimer, Form for a waiver in guest copy | DI-1062 |
| Lost item / Found item / Possible match | The two directions of lost property and the suggested pairing between them. | Lost case, Claim before it is claimed | contracts/satellite/marketing-crm.yaml#/components/schemas/LostItem |
| Wishlist | Products and dates a guest saved to buy later, including F&B and retail to buy on site. | Favourites (used for transport routes), Saved for later on one surface and Wishlist on another | DI-202 |
| Notification / Message | A notification is an item in the guest's in-app feed. A message is one send on a channel (email, SMS, WhatsApp, push, in-app). | Alert for marketing content, Inbox for the guest feed | contracts/satellite/marketing-crm.yaml#/components/schemas/GuestNotification |
| Template | A reusable message body per channel and language with merge fields. Transactional and marketing templates are separate kinds. | Layout, Design | contracts/satellite/marketing-crm.yaml#createMessageTemplate |

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
| `BO-774` | Journey Automation Center | B–D | 0 | 10 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-775` | Visual Journey Builder | B–D | 0 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-776` | Trigger Event Catalog | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-777` | Decision Logic & Timing | B–D | 0 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-778` | Abandoned Cart Recovery | B–D | 0 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-779` | Lifecycle Journeys | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-780` | Guest Engagement Journeys | B–D | 0 | 20 | 6 | 9 | 1 | 6 | — | notStarted (—) |
| `BO-781` | Cross-Sell & Service Recovery | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-782` | AI Journey Optimization | B–D | 0 | 0 | 6 | 13 | 0 | 6 | — | notStarted (—) |
| `BO-783` | Journey Analytics & Audit | B–D | 0 | 10 | 6 | 0 | 0 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-774, BO-775, BO-776, BO-777, BO-778, BO-779, BO-780, BO-781, BO-782, BO-783 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-774` Journey Automation Center

**Monitor the health and value of automated customer journeys. Show active journeys, enrolled guests, conversions, recovered revenue, exits, errors and upcoming actions. Compare journey performance by objective, lifecycle, brand, venue, audience, channel and owner. Surface paused nodes, delivery failures, SLA risk and data or consent problems requiring intervention. Provide drill-down and explainable optimization opportunities without automatically changing live flows. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `journeyId` (navigation) |
| Route | `/engagement-support/journey-automation-center-bo-774` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Health and value of automated journeys: active journeys, guests enrolled, conversions, recovered revenue, exits, errors, upcoming actions, and nodes paused by data or consent problems. Optimisation suggestions are shown, not applied.

**Fixed on main** (the package already carries these; draw what it says): Only listJourneys is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Journey performance** (detail panel, from `getJourneyPerformance`)

| Shows | Format | Notes |
|---|---|---|
| Journey | the name it points at, never the id | — |
| Entrants | 1,234 | Everyone who entered, in any status. |
| By status | grouped details | Entrants per `JourneyEntrant.status`. |
| Active | 1,234 | — |
| Paused | 1,234 | — |
| Completed | 1,234 | — |
| Exited | 1,234 | — |
| Suppressed | 1,234 | — |
| Goal reached | 1,234 | The number that matters. Entrants who left at a step of kind `goal` — their `JourneyEntrant.stepId` when they exited. |
| Goal rate | 12.5% | `goalReached` over `entrants`. Null while there are no entrants. |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Journey row**: Name, template, status, entrants, goal rate (the number that matters, not open rate), errors. *(source: contracts/satellite/marketing-crm.yaml#getJourneyPerformance)*

**Data it reads**: `listJourneys` (onLoad, Journeys running)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-775` Visual Journey Builder: *Visual Journey Builder*; carries `journeyId`
- → `BO-776` Trigger Event Catalog: *Trigger Event Catalog*
- → `BO-777` Decision Logic & Timing: *Decision Logic & Timing*
- → `BO-778` Abandoned Cart Recovery: *Abandoned Cart Recovery*
- → `BO-779` Lifecycle Journeys: *Lifecycle Journeys*
- → `BO-780` Guest Engagement Journeys: *Guest Engagement Journeys*
- → `BO-781` Cross-Sell & Service Recovery: *Cross-Sell & Service Recovery*; carries `journeyId`
- → `BO-782` AI Journey Optimization: *AI Journey Optimization*
- → `BO-783` Journey Analytics & Audit: *Journey Analytics & Audit*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journey automation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journey automation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No journey automation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the journey automation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-120`: Same journey list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journeys:
- '{name: Abandoned cart - membership, entrants7d: 214, goalRate: 11%, recovered: AED 18,900.00}'
```

#### Permissions

- `listJourneys` → `MARKETING_VIEW` (read) · staff
- `getJourneyPerformance` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-774` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-774`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 1: Opens Journey Automation Center → Monitor the health and value of automated customer journeys. Show active journeys, enrolled guests, conversions, recovered revenue, exits, errors and upcoming actions. Compare journey performance by …
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F248 branch at step 1 (expected): when Nothing has been set up on Journey Automation Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F248 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-774?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-775`, `BO-776`, `BO-777`, `BO-778`, `BO-779`, `BO-780`, `BO-781`, `BO-782`, `BO-783`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-775` Visual Journey Builder

**Create multi-step journeys through a visual no-code canvas. Provide trigger, audience, decision, wait, message, offer, case, task, webhook and goal nodes. Support branches, merges, reusable subflows, annotations, zoom, validation and realistic test execution. Show node configuration, eligible count, dependencies and errors without leaving the canvas. Version drafts, compare changes and require approval before a published journey is replaced. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_SEND` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `journeyId` (navigation) |
| Route | `/engagement-support/visual-journey-builder-bo-775` |

**Known gaps.** **Visual Journey Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The visual canvas for multi-step journeys: trigger, audience, decision, wait, message, offer, case, task, webhook and goal nodes, with branches and validation. The canvas renders the journey graph the contract holds. A journey is a draft until activated, and pausing keeps guests where they are.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Wait node**: Same day, a week, a month, or a custom period. *(source: DI-384)*
- **Offer node**: Picks only a pre-configured, system-validated offer; no free discount value. *(source: DI-385)*
- **Message node**: Channel and template; checks the guest's consent for the purpose at the moment of sending. *(source: DI-386; contracts/satellite/marketing-crm.yaml#launchCampaign)*
- **Re-entry**: Never, after completion, or always. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/Journey)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create journey (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Activate or pause**: Activation needs MARKETING_SEND; pausing does not evict guests already in the journey. *(source: contracts/satellite/marketing-crm.yaml#activateJourney)*

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visual journey yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visual journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The graph does not terminate, or a step points at nothing. Refused at creation rather than discovered by a guest stuck in a loop. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journey: Abandoned cart - membership only
nodes:
- Trigger cart abandoned (membership, over AED 500)
- Wait 2 hours
- WhatsApp reminder
- Wait 1 day
- Decision purchased?
- Email with offer MEMBER10
- Goal membership purchased
```

#### Permissions

- `createJourney` → `MARKETING_MANAGE` (configure) · staff
- `activateJourney` → `MARKETING_SEND` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: offer blocks in the Visual Journey Builder pick only from pre-configured, system-validated offers (product/ticket-type scoped, from the Offers module: coupon code, dynamic discount or auto-discount URL); ad-hoc discount values cannot be typed in the builder. *(agreed · MoM 20 Aug 2026, 4.6 Marketing Automation; 5. Key Decisions · DI-385)*
- Visual Journey Builder triggers rule-based touchpoints (e.g. abandoned-cart recovery) with configurable wait periods (same-day, one week, one month), audience segment and optional incentive (e.g. coupon code). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-384)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-775` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-775`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 2: Works in Visual Journey Builder → Create multi-step journeys through a visual no-code canvas. Provide trigger, audience, decision, wait, message, offer, case, task, webhook and goal nodes. Support branches, merges, reusable subflows …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-775?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create journey, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_SEND`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-776` Trigger Event Catalog

**Govern the events that can start, update or stop a journey. Configure purchase, cart abandonment, first visit, membership expiry, loyalty milestone, wallet top-up, birthday, reservation and case events. Configuration Scope of Work / Version 1.0 26 Define source, event schema, required attributes, deduplication, freshness, eligibility and sample payload. Support API/webhook events and scheduled conditions with authentication and retry controls. Version and test event definitions and display consuming journeys before deactivation or change. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/trigger-event-catalog-bo-776` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The catalogue of events that can start, update or stop a journey or fire a message: purchase, cart abandonment, first visit, membership expiry, loyalty milestone, top-up, birthday, reservation, case events. Triggers key off precise event states (a post-visit survey only when the ticket was scanned).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Event and state**: Event, required state (e.g. ticket used), delay, and whether it fires transactional or marketing messages; marketing triggers check consent. *(source: contracts/satellite/marketing-crm.yaml#setMessageTrigger; DI-561)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save message trigger (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listMessageTriggers` (onLoad, The trigger catalogue)

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The trigger event catalog list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the trigger event catalog untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No trigger event catalog yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the trigger event catalog are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `sendTimeMode` `optimised` on a trigger whose `priority` is `operational` or `transactional` (29 September, build pass, group G2), or an `event` not in the … |

#### Consistency with other screens

- Match `ADM-042`: Platform-level event-to-notification mapping; venue triggers sit on top.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
triggers:
- Ticket scanned -> post-visit survey after 3 hours
- Order completed -> confirmation (transactional)
```

#### Permissions

- `listMessageTriggers` → `MARKETING_VIEW` (read) · staff
- `setMessageTrigger` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Notification triggers must key off precise event states where needed: a post-visit survey only when the ticket was actually scanned/used, whereas a "how was your experience" follow-up can trigger off the sale. Trigger mapping must expose such event states. *(agreed · MoM 31 Aug 2026, 4.6 Communications & Notifications · DI-561)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-776` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-776`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 4: Works in Trigger Event Catalog → Govern the events that can start, update or stop a journey. Configure purchase, cart abandonment, first visit, membership expiry, loyalty milestone, wallet top-up, birthday, reservation and case …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-776?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save message trigger, Cancel.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-777` Decision Logic & Timing

**Control journey branching, timing and re-entry. Build nested AND/OR conditions using guest, event, segment, transaction, product, channel and engagement data. Configure waits, dates, timezones, send windows, blackout periods, frequency limits and expiry. Define re-entry, concurrency, suppression, exit and goal conditions and behavior when data is missing. Simulate paths for representative guests and block publication when a branch has no safe outcome. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/decision-logic-timing-bo-777` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-007): No operation simulates a marketing journey.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Journey branching, timing and re-entry: conditions, waits, dates, time zones, send windows, blackouts, frequency limits, expiry, exit and goal conditions, and what happens when data is missing. A branch with no safe outcome blocks publication.

**Fixed on main** (the package already carries these; draw what it says): The screen's only operation is createJourney. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Journeys** (data table, from `listJourneys`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Template kind | chip: Abandoned cart, Membership lifecycle, Loyalty lifecycle, Wallet lifecycle … | Which named lifecycle this implements. Set for reporting and for the library, not for behaviour — the steps decide what happens. |
| Entry event | text | 22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes. |
| Entry conditions | grouped details | Narrows entry — a segment, a tier, a venue. Evaluated once at entry, unlike step conditions. |
| Steps | list or chips (count when long) | 22.3.1b. What the builder produces. |
| ID | text | — |
| Kind | chip: Send, Wait, Branch, Exit, Goal | — |
| Template | the name it points at, never the id | For `send`. Channel is resolved from the guest's preference at the moment of sending. |
| Send time mode | chip: Fixed, Optimised | For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's … |
| Channel mode | chip: Preference, Optimised | For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16). |
| Channel preference | list or chips (count when long) | 22.3.3b. Ordered fallback — email, then SMS, then push. |
| Wait minutes | 1,234 | — |
| Wait until | grouped details | 22.3.5b. Business hours, time zone and blackout windows — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are … |
| Condition | grouped details | 22.3.4b. IF/THEN over guest profile, behaviour and prior steps. |
| On true | text | Next step id. |
| On false | text | — |
| Next | text | — |
| Goal event | text | For `goal`. The event that means this journey worked and the guest should leave it — a purchase for abandoned cart, a renewal for … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create journey (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Path simulation**: Pick representative guests and see which path each takes and why. *(source: screens/P08-venue-back-office.yaml#BO-777)*

**Data it reads**: `listJourneys` (onLoad, The journeys to open and branch)

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The decision logic timing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the decision logic timing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No decision logic timing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the decision logic timing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The graph does not terminate, or a step points at nothing. Refused at creation rather than discovered by a guest stuck in a loop. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: If no purchase within 24 hours and consent for WhatsApp, send reminder; else exit
```

#### Permissions

- `createJourney` → `MARKETING_MANAGE` (configure) · staff
- `listJourneys` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Visual Journey Builder triggers rule-based touchpoints (e.g. abandoned-cart recovery) with configurable wait periods (same-day, one week, one month), audience segment and optional incentive (e.g. coupon code). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-384)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-777` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-777`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 6: Works in Decision Logic & Timing → Control journey branching, timing and re-entry. Build nested AND/OR conditions using guest, event, segment, transaction, product, channel and engagement data. Configure waits, dates, timezones, send …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-777?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create journey, Cancel.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-778` Abandoned Cart Recovery

**Configure automated recovery of incomplete ticketing and commerce transactions. Define abandonment event, cart-value threshold, product/inventory checks, eligibility and recovery window. Configure staged reminders across email, SMS, WhatsApp and push with fallback and frequency limits. Apply approved incentives through the Promotion Engine and prevent discount leakage or expired inventory offers. Track recovered cart, revenue, margin, attribution and exit when purchase or cancellation occurs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/abandoned-cart-recovery-bo-778` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Carts that lapsed without checkout, feeding recovery; carts the guest emptied on purpose are excluded.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since | date and time picker | — | — | `listAbandonedCarts` ?since |
| Min value | text field | — | pattern `^\d+(\.\d{1,4})?$` | `listAbandonedCarts` ?minValue |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **abandoned carts**: Value, items, guest, lapsed when; consent shown before any recovery. *(source: contracts/spine/orders.yaml#listAbandonedCarts)*

**Data it reads**: `listAbandonedCarts` (onLoad, Carts that lapsed without checking out)

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The abandoned cart recovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the abandoned cart recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No abandoned cart recovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the abandoned cart recovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cart:
  guest: Hessa Al Mazrouei
  value: AED 590.00
  lapsed: 2 h ago
  consent: true
```

#### Permissions

- `listAbandonedCarts` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*
- Visual Journey Builder triggers rule-based touchpoints (e.g. abandoned-cart recovery) with configurable wait periods (same-day, one week, one month), audience segment and optional incentive (e.g. coupon code). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-384)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-778` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-778`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 8: Works in Abandoned Cart Recovery → Configure automated recovery of incomplete ticketing and commerce transactions. Define abandonment event, cart-value threshold, product/inventory checks, eligibility and recovery window. Configure …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-778?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-779` Lifecycle Journeys

**Manage reusable membership, loyalty and wallet lifecycle automations. Provide onboarding, benefit-awareness, renewal, expiry, lapse, freeze and upgrade membership journeys. Provide loyalty enrollment, tier movement, milestone, reward availability and points-expiry journeys. Provide wallet onboarding, top-up, low-balance, dormancy and bonus-credit journeys. Configure eligibility, channels, goals, stop conditions, ownership, versions and lifecycle-specific KPIs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 27**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/lifecycle-journeys-bo-779` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Reusable lifecycle journeys for membership (onboarding, renewal, expiry, lapse, upgrade), loyalty (enrolment, tier movement, milestone, points expiry) and wallet (top-up, low balance, dormancy, bonus credit expiry). Each has eligibility, channels, goals and stop conditions.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create journey (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The lifecycle journeys list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the lifecycle journeys untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No lifecycle journeys yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the lifecycle journeys are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The graph does not terminate, or a step points at nothing. Refused at creation rather than discovered by a guest stuck in a loop. |

#### Consistency with other screens

- Match `BO-775`: Templates open in the builder.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
library:
- Membership renewal - 30/7/1 days before expiry
- Points expiring - 14 days before
- Wallet bonus credit expiring - 7 days before
```

#### Permissions

- `createJourney` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-779` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-779`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 10: Works in Lifecycle Journeys → Manage reusable membership, loyalty and wallet lifecycle automations. Provide onboarding, benefit-awareness, renewal, expiry, lapse, freeze and upgrade membership journeys. Provide loyalty …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-779?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create journey, Cancel.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-780` Guest Engagement Journeys

**Configure recurring guest relationship journeys. Support birthdays, anniversaries, welcome/onboarding, first-visit follow-up, inactivity and re- engagement. Personalize by profile, language, interests, visit history, loyalty, membership and preferred channel. Apply quiet hours, consent, frequency and household/minor rules before every communication. Measure engagement, conversion, return visits, retention and incremental value by journey. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/guest-engagement-journeys-bo-780` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Relationship journeys: birthdays, anniversaries, welcome, first-visit follow-up, inactivity and re-engagement, personalised by language, interests and preferred channel. Quiet hours, consent, frequency and household and minor rules apply before every message.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table, from `listJourneys`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Template kind | chip: Abandoned cart, Membership lifecycle, Loyalty lifecycle, Wallet lifecycle … | Which named lifecycle this implements. Set for reporting and for the library, not for behaviour — the steps decide what happens. |
| Entry event | text | 22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes. |
| Entry conditions | grouped details | Narrows entry — a segment, a tier, a venue. Evaluated once at entry, unlike step conditions. |
| Steps | list or chips (count when long) | 22.3.1b. What the builder produces. |
| ID | text | — |
| Kind | chip: Send, Wait, Branch, Exit, Goal | — |
| Template | the name it points at, never the id | For `send`. Channel is resolved from the guest's preference at the moment of sending. |
| Send time mode | chip: Fixed, Optimised | For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's … |
| Channel mode | chip: Preference, Optimised | For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16). |
| Channel preference | list or chips (count when long) | 22.3.3b. Ordered fallback — email, then SMS, then push. |
| Wait minutes | 1,234 | — |
| Wait until | grouped details | 22.3.5b. Business hours, time zone and blackout windows — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are … |
| Condition | grouped details | 22.3.4b. IF/THEN over guest profile, behaviour and prior steps. |
| On true | text | Next step id. |
| On false | text | — |
| Next | text | — |
| Goal event | text | For `goal`. The event that means this journey worked and the guest should leave it — a purchase for abandoned cart, a renewal for … |

**Data it reads**: `listJourneys` (onLoad, Every guest engagement journey)

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest engagement journeys list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest engagement journeys untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest engagement journeys yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest engagement journeys are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Birthday of a minor**: The message goes to the guardian, never to the child; no marketing to minors. *(source: R205; screens/P08-venue-back-office.yaml#BO-780)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journey: Birthday reward - 7 days before - free entry for the birthday guest - WhatsApp
```

#### Permissions

- `listJourneys` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.1 | Visual Journey Builder | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.6 | Abandoned Cart Recovery Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.7 | Membership Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.8 | Loyalty Lifecycle Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.9 | Wallet Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.10 | Birthday & Anniversary Campaigns | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.14 | Cross-Sell & Upsell Automation | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.21 | Automation Analytics Dashboard | Marketing & CRM | CONTRACTED | data `Journey` |
| 22.3.22 | Automation Audit Trail | Marketing & CRM | CONTRACTED | data `Journey` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-780` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-780`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 12: Works in Guest Engagement Journeys → Configure recurring guest relationship journeys. Support birthdays, anniversaries, welcome/onboarding, first-visit follow-up, inactivity and re- engagement. Personalize by profile, language …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-780?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-781` Cross-Sell & Service Recovery

**Coordinate revenue-growth and recovery actions after guest events. Recommend and automate eligible cross-sell or upsell offers after purchase, booking or visit. Trigger reservation follow-up, survey request, complaint recovery and post-case resolution journeys. Create cases, tasks, refunds, vouchers, loyalty points or wallet credit subject to approval limits. Stop or alter a journey when sentiment, case status, refund, opt-out or service outcome changes. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `journeyId` (navigation) |
| Route | `/engagement-support/cross-sell-service-recovery-bo-781` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Cross-sell and service recovery after guest events: eligible upsell after purchase or visit; reservation follow-up, survey request, complaint recovery and post-case journeys. Compensation (voucher, points, credit, refund) stays within approval limits, and a journey stops when sentiment, case status, refund or opt-out changes.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Recovery performance**: Entrants, completions, goals reached (return visit after recovery). *(source: contracts/satellite/marketing-crm.yaml#getJourneyPerformance)*

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-sell service recovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-sell service recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-sell service recovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-sell service recovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The guest opted out or a case is still open**: Upsell steps stop; recovery steps continue only as transactional case messages. *(source: screens/P08-venue-back-office.yaml#BO-781)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journey: Complaint recovery - case resolved -> apology with 500 points -> survey after 2 days
```

#### Permissions

- `getJourneyPerformance` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Cart-abandonment triggers filter by minimum cart value and product type (e.g. only membership-ticket abandonment). Other journeys: birthday rewards, anniversary reminders, cross-sell/upsell, reservation/survey requests — all gated by customer consent. *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-386)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-781` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-781`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 14: Works in Cross-Sell & Service Recovery → Coordinate revenue-growth and recovery actions after guest events. Recommend and automate eligible cross-sell or upsell offers after purchase, booking or visit. Trigger reservation follow-up, survey …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-781?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-782` AI Journey Optimization

**Use explainable AI to improve paths, content, offers and timing. Recommend branch order, wait duration, channel, message, offer and send time with expected uplift. Display supporting evidence, confidence, affected audience, risks and policy constraints. Allow scenario comparison, selective approval and rollback and prevent AI from editing live journeys directly. Monitor applied recommendation results and retain model/version, reviewer feedback and realized impact. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `insightId` (navigation) |
| Route | `/engagement-support/ai-journey-optimization-bo-782` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** AI journey optimisation: recommendations on a journey's branch order, waits, channel, message, offer and send time with expected uplift, evidence, affected audience, risks and policy constraints, compared as scenarios. The one thing to get right: each recommendation shows its basis and constraints and is applied by a person.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Target kind | segmented control | — | Campaign · Journey | `listMarketingRecommendations` ?targetKind |
| Target ref | text field | — | — | `listMarketingRecommendations` ?targetRef |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listMarketingRecommendations` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **recommendation card**: Change, expected uplift range, audience size, evidence, constraint (e.g. quiet hours, frequency cap), accept/reject. *(source: contracts/satellite/ai.yaml#listMarketingRecommendations / contracts/satellite/ai.yaml#decideAiInsight)*

**Data it reads**: `listJourneys` (onLoad, Automated journeys); `listMarketingRecommendations` (onLoad, AI recommendations on this campaign or journey, with …)

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journey optimization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journey optimization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No journey optimization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the journey optimization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The move is not allowed from the insight's state.; 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card:
  journey: Membership expiring
  change: Wait 3 days not 7 before the second reminder
  uplift: +1 to +3 renewals per 100
```

#### Permissions

- `listJourneys` → `MARKETING_VIEW` (read) · staff
- `listMarketingRecommendations` → `AI_USE` (operate) · staff
- `decideAiInsight` → `AI_USE` (operate) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.16 | AI Campaign Recommendations | Marketing & CRM | CONTRACTED | `listMarketingRecommendations` |
| 22.3.17 | AI Journey Recommendations | Marketing & CRM | CONTRACTED | `listMarketingRecommendations` |
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.8.15 | AI predicts potential food waste and recommends actions. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 5.4.24 | Segment customers automatically. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.27 | Recommend staffing adjustments, ride allocation, and queue balancing. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.36 | The system shall estimate queue wait times using historical and real-time operational data. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 8.9.9 | AI shall identify operational risks, anomalies, congestion, capacity issues, device failures, staffing shortages, and service disruptions and provide recommendations. | Unified Operations Dashboard | CONTRACTED | `requestSuggestion` |
| 15.4.7 | Inventory Optimization - System shall optimize inventory levels. | Inventory Management | CONTRACTED_PARTIAL | `requestSuggestion` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-782` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-782`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 16: Works in AI Journey Optimization → Use explainable AI to improve paths, content, offers and timing. Recommend branch order, wait duration, channel, message, offer and send time with expected uplift. Display supporting evidence …
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-782?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-783` Journey Analytics & Audit

**Measure journey behavior at node and end-goal level. Show triggered, eligible, enrolled, reached, clicked, converted, exited and failed stages. Analyze node drop-off, branch performance, time-to-conversion, revenue, attribution and cost. Provide error log, delivery trace, suppression reason, version comparison and guest-level path where authorized. Audit creation, edits, approvals, publication, pauses, AI recommendations and administrative actions. Configuration Scope of Work / Version 1.0 28 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 29 Board 6 - Newsletter, Notifications & Message Delivery Figure 6. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 30**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `journeyId` (navigation) |
| Route | `/engagement-support/journey-analytics-audit-bo-783` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Journey behaviour at node and goal level: triggered, eligible, enrolled, reached, clicked, converted, exited and failed, with drop-off per node, suppression reasons and an audit of edits, approvals and pauses.

**Fixed on main** (the package already carries these; draw what it says): Only listJourneys is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Journey analytics** (detail panel, from `getJourneyPerformance`)

| Shows | Format | Notes |
|---|---|---|
| Journey | the name it points at, never the id | — |
| Entrants | 1,234 | Everyone who entered, in any status. |
| By status | grouped details | Entrants per `JourneyEntrant.status`. |
| Active | 1,234 | — |
| Paused | 1,234 | — |
| Completed | 1,234 | — |
| Exited | 1,234 | — |
| Suppressed | 1,234 | — |
| Goal reached | 1,234 | The number that matters. Entrants who left at a step of kind `goal` — their `JourneyEntrant.stepId` when they exited. |
| Goal rate | 12.5% | `goalReached` over `entrants`. Null while there are no entrants. |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Suppression reasons**: Counts by reason (no consent, quiet hours, frequency cap, minor, already converted). *(source: screens/P08-venue-back-office.yaml#BO-783)*

**Data it reads**: `listJourneys` (onLoad, Automated journeys)

**Where the user goes next**

- → `BO-774` Journey Automation Center: *Back to Journey Automation Center*; carries `journeyId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journey analytics audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journey analytics audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No journey analytics audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the journey analytics audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
funnel:
  triggered: 1200
  eligible: 860
  enrolled: 860
  reached: 790
  converted: 95
```

#### Permissions

- `listJourneys` → `MARKETING_VIEW` (read) · staff
- `getJourneyPerformance` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-783` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS74 Marketing CRM Configuration Reference v1.0 Board 5.dc.html#bo-783`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 5
- Flow F248 *Marketing CRM Configuration Reference v1.0 board 5: Journey Automation Center*, step 18: Works in Journey Analytics & Audit → Measure journey behavior at node and end-goal level. Show triggered, eligible, enrolled, reached, clicked, converted, exited and failed stages. Analyze node drop-off, branch performance …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-783?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-774`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"activateJourney": {"method":"POST","path":"/journeys/{journeyId}/activate","contract":"marketing-crm","summary":"Start it, or stop it","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Journey"},
"createJourney": {"method":"POST","path":"/journeys","contract":"marketing-crm","summary":"Define an automated journey","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Journey","responds":"Journey"},
"decideAiInsight": {"method":"POST","path":"/insights/{insightId}/decide","contract":"ai","summary":"Review, accept, reject or mark an insight actioned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiInsight"},
"getJourneyPerformance": {"method":"GET","path":"/journeys/{journeyId}/performance","contract":"marketing-crm","summary":"Entrants, completions, goals reached","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"JourneyPerformance"},
"listAbandonedCarts": {"method":"GET","path":"/carts/abandoned","contract":"orders","summary":"Carts that lapsed without checking out","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"since","in":"query","required":null},{"name":"minValue","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listJourneys": {"method":"GET","path":"/journeys","contract":"marketing-crm","summary":"Automated journeys","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMarketingRecommendations": {"method":"GET","path":"/marketing-recommendations","contract":"ai","summary":"Recommendations on marketing campaigns and journeys","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"targetKind","in":"query","required":true},{"name":"targetRef","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMessageTriggers": {"method":"GET","path":"/message-triggers","contract":"marketing-crm","summary":"What fires a message, and when","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"setMessageTrigger": {"method":"POST","path":"/message-triggers","contract":"marketing-crm","summary":"Fire a message from a platform event","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MessageTrigger","responds":"MessageTrigger"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AbandonedCart": {"type":"object","x-ticvai-persistence":"none — a projection of orders.cart","properties":{"cartId":{"type":"string","format":"uuid"},"token":{"type":"string"},"subjectId":{"type":"string","format":"uuid","nullable":true},"hasContactPoint":{"type":"boolean","description":"**An anonymous cart with no email cannot be recovered.** Worth counting, because it sizes what a sign-in prompt earlier in the journey would be worth.\n"},"venueId":{"type":"string","format":"uuid"},"lineCount":{"type":"integer"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"topProductName":{"type":"string"},"abandonedAt":{"type":"string","format":"date-time"},"remindersSent":{"type":"integer"}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMarketingRecommendation": {"type":"object","x-ticvai-persistence":"none — read from ai.insight (kind marketingRecommendation)","description":"One recommendation on a campaign or journey (22.1.16, 22.3.17), decided through `decideAiInsight` and applied by a person in marketing-crm.","required":["insightId","targetKind","targetRef","recommendation","status"],"properties":{"insightId":{"type":"string","format":"uuid","description":"The `ai.insight` row; `decideAiInsight` takes it."},"targetKind":{"type":"string","enum":["campaign","journey"]},"targetRef":{"type":"string"},"recommendation":{"type":"string","enum":["changeSegment","changeChannel","changeTiming","changeOffer","changeContent","addStep","removeStep","reorderSteps","startJourneyFromTemplate"]},"parameters":{"type":"object","additionalProperties":true,"nullable":true,"description":"What to change to, e.g. the channel, the send hour, the step to drop."},"expectedImpact":{"type":"object","nullable":true,"properties":{"metric":{"type":"string"},"low":{"type":"number"},"high":{"type":"number"}},"description":"A range on the named metric (conversion, open rate, revenue), never a single number (design 5.6)."},"rationale":{"type":"string"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"priority":{"type":"string","enum":["low","medium","high","critical"]},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"]},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"detectedAt":{"type":"string","format":"date-time"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"Journey": {"type":"object","x-ticvai-persistence":"marketing.journey + marketing.journey_step","description":"22.3.1b to 22.3.10b, CF-137. **A journey is a sequence with branches; a `MessageTrigger` is one step of it.** The trigger already handles *\"send this when that happens\"* — a journey is what you need when the next message depends on what the guest did about the last one.\nFive of the ten requirements are named lifecycles — abandoned cart, membership, loyalty, wallet, birthday. **They are not five features.** Each is a journey with a different entry event and a different set of steps, which is why this is one entity and a template library rather than five contracts.\n**Consent is checked at every send, not at entry.** A guest who opts out mid-journey stops receiving, and the journey does not need to know — the same rule `MessageTrigger` follows and the one PDPL Article 17(1) makes unconditional.\n","required":["id","name","entryEvent","status","steps"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"templateKind":{"type":"string","nullable":true,"enum":["abandonedCart","membershipLifecycle","loyaltyLifecycle","walletLifecycle","birthday","onboarding","winBack","custom"],"description":"Which named lifecycle this implements. **Set for reporting and for the library**, not for behaviour — the steps decide what happens.\n"},"entryEvent":{"type":"string","description":"22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes.\n"},"entryConditions":{"type":"object","nullable":true,"description":"Narrows entry — a segment, a tier, a venue. **Evaluated once at entry**, unlike step conditions.\n"},"steps":{"type":"array","description":"22.3.1b. What the builder produces. **The visual builder is a frontend over this** — the contract holds the graph and the canvas is a rendering of it.\n","items":{"$ref":"#/components/schemas/JourneyStep"}},"status":{"readOnly":true,"type":"string","enum":["draft","active","paused","archived"]},"maxDurationDays":{"type":"integer","default":30,"description":"**A journey with no end is a guest who never leaves it.** After this, entrants exit wherever they are.\n"},"reentryPolicy":{"type":"string","enum":["never","afterCompletion","always"],"default":"afterCompletion","description":"22.3.6b. **Abandoned cart is the case that needs this.** A guest who abandons three carts in an hour should not get three recovery sequences, and `never` is wrong too — they may genuinely abandon one next month.\n"},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"JourneyPerformance": {"type":"object","x-ticvai-persistence":"none — aggregated from marketing.journey_enrollment","required":["journeyId","entrants"],"properties":{"journeyId":{"type":"string","format":"uuid"},"entrants":{"type":"integer","description":"Everyone who entered, in any status."},"byStatus":{"type":"object","description":"Entrants per `JourneyEntrant.status`.","properties":{"active":{"type":"integer"},"paused":{"type":"integer"},"completed":{"type":"integer"},"exited":{"type":"integer"},"suppressed":{"type":"integer"}}},"goalReached":{"type":"integer","description":"**The number that matters.** Entrants who left at a step of kind `goal` — their `JourneyEntrant.stepId` when they exited.\n"},"goalRate":{"type":"number","nullable":true,"description":"`goalReached` over `entrants`. Null while there are no entrants."}}},
"JourneyStep": {"type":"object","description":"One node. **A step either sends, waits, or branches** — three kinds rather than a general graph, because a marketing user drawing an arbitrary graph draws a loop.\n","required":["id","kind"],"properties":{"id":{"type":"string"},"kind":{"type":"string","x-ticvai-column":"type","enum":["send","wait","branch","exit","goal"]},"templateId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-column":"message_template_id","description":"For `send`. Channel is resolved from the guest's preference at the moment of sending."},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours and inside `waitUntil`; no suggestion or AI off sends at once, as `fixed`."},"channelMode":{"type":"string","enum":["preference","optimised"],"default":"preference","description":"For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16)."},"channelPreference":{"type":"array","nullable":true,"description":"22.3.3b. Ordered fallback — email, then SMS, then push. **A guest with no email address does not get an email step**, and the step does not fail, it moves down the list.\n","items":{"type":"string","enum":["email","sms","whatsapp","push","inApp"]}},"waitMinutes":{"type":"integer","nullable":true},"waitUntil":{"type":"object","nullable":true,"description":"22.3.5b. **Business hours, time zone and blackout windows** — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are venue configuration rather than a property of this step.\n","properties":{"businessHoursOnly":{"type":"boolean","default":false},"timezone":{"type":"string","nullable":true},"respectQuietHours":{"type":"boolean","default":true},"notBefore":{"type":"string","nullable":true}}},"condition":{"type":"object","nullable":true,"description":"22.3.4b. IF/THEN over guest profile, behaviour and prior steps. **The most common condition is whether the previous message worked** — a recovery sequence must stop when the guest buys.\n","properties":{"field":{"type":"string"},"operator":{"type":"string","enum":["eq","neq","gt","lt","contains","exists","notExists"]},"value":{"type":"string","nullable":true}}},"onTrue":{"type":"string","nullable":true,"description":"Next step id."},"onFalse":{"type":"string","nullable":true},"next":{"type":"string","nullable":true,"x-ticvai-column":"next_journey_step_id"},"goalEvent":{"type":"string","nullable":true,"description":"For `goal`. **The event that means this journey worked and the guest should leave it** — a purchase for abandoned cart, a renewal for membership. **Reaching a goal exits immediately**, which is what stops a recovered cart from being chased.\n"}}},
"MessageTrigger": {"type":"object","x-ticvai-persistence":"marketing.message_trigger","description":"**What fires a message.** Before, during and after a visit are one mechanism with a different sign on the offset.\n","required":["id","event","templateId","isActive"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"event":{"type":"string","description":"The platform event that fires it — `order.completed`, `access.validated`, `queue.turnApproaching`. **Named from the event catalogue** (`BusinessEvent.eventType`), so a trigger cannot bind to something nothing publishes. Its conditions are `MessageTriggerCondition` rows.\n**`entitlement.expiringSoon` is in the catalogue since 29 September** (build pass, group G2; 5.5.30): the pre-expiry reminder for a ticket or pass. Its anchor is the event time; the notice period is the template's `expiryNoticeDays`, so `offsetMinutes` is normally 0.\n"},"templateId":{"type":"string","format":"uuid"},"offsetMinutes":{"type":"integer","default":0,"description":"Negative fires before the anchor, positive after. **A reminder the day before a visit is -1440 against the performance**, not a separate concept.\n"},"anchor":{"type":"string","enum":["eventTime","performanceStart","visitEnd"],"default":"eventTime"},"priority":{"type":"string","enum":["operational","transactional","marketing"],"default":"transactional","description":"**A queue-turn alert and a monthly newsletter are not the same urgency and were the same dispatch.** `operational` bypasses batching and quiet hours; `marketing` never does.\n"},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"**Only for `priority` `marketing`** (29 September, build pass, group G2; 22.9.16): `optimised` holds the notification to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours, on the suggested consented channel. `operational` and `transactional` messages are never delayed for it, and a `setMessageTrigger` asking for it on them is refused (400)."},"isActive":{"type":"boolean","default":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]}
}
```
