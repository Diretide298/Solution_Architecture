# WS137 — Marketing CRM Configuration Reference v1.0 board 3

**10 screens · 12 operations · 15 schemas · 4 permissions**

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
  `AI_USE, MARKETING_MANAGE, MARKETING_VIEW, PRICE_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-754` | Audience Intelligence | D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-755` | Dynamic Segment Builder | A | 21 | 23 | 6 | 10 | 1 | 6 | — | notStarted (—) |
| `BO-756` | Static Lists & Imports | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-757` | Behavioral Segmentation | D | 0 | 20 | 6 | 13 | 1 | 6 | — | notStarted (—) |
| `BO-758` | Membership & Loyalty Segments | D | 0 | 0 | 6 | 12 | 1 | 6 | — | notStarted (—) |
| `BO-759` | Demographic & Geographic | D | 0 | 0 | 6 | 9 | 0 | 0 | — | notStarted (—) |
| `BO-760` | Revenue & Engagement Segments | D | 0 | 0 | 6 | 12 | 0 | 6 | — | notStarted (—) |
| `BO-761` | AI Audience Discovery | C | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-762` | Predictive Audiences | D | 0 | 0 | 6 | 14 | 0 | 0 | — | notStarted (—) |
| `BO-763` | Activation & Governance | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-754, BO-755, BO-756, BO-758, BO-759, BO-760, BO-761, BO-762 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-754` Audience Intelligence

**Give marketers and CRM teams an overview of addressable audience health. Show total guests, reachable guests, active segments, consent-eligible audience, high-value and churn-risk populations. Visualize growth, overlap, duplication, suppression and reachability by channel, brand, venue and region. Identify stale, shrinking, high-performing or conflicting audiences and link to the responsible definitions. Provide explainable AI observations without modifying or activating segments automatically. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-754 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/audience-intelligence-bo-754` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The health of the addressable audience: total guests against reachable guests, active segments, consent-eligible audience, high-value and churn-risk populations, and how audiences overlap. Reachable is the number that matters and it is always smaller than the total; the screen leads with it.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Segments | text field | — | — | `getAudienceOverlap` ?segmentIds |
| Channel | text field | — | — | `getAudienceOverlap` ?channel |
| Search | text field | — | max length 200 | `listSegments` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Reachable by channel**: Per channel, guests with consent, a valid address and no suppression; shown beside the total, never alone. *(source: contracts/satellite/marketing-crm.yaml#getAudienceOverlap; contracts/satellite/marketing-crm.yaml#previewSegment)*
- **Overlap**: A matrix of selected segments with the shared count, so two campaigns do not hit the same guests unknowingly. *(source: contracts/satellite/marketing-crm.yaml#getAudienceOverlap)*
- **Segment health**: Stale (not used in 90 days), shrinking, high-performing, each linking to its definition. *(source: screens/P08-venue-back-office.yaml#BO-754)*

**Data it reads**: `getAudienceOverlap` (onLoad, Reachability and overlap); `listSegments` (onLoad, Active segments)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-755` Dynamic Segment Builder: *Dynamic Segment Builder*; carries `segmentId`
- → `BO-756` Static Lists & Imports: *Static Lists & Imports*
- → `BO-757` Behavioral Segmentation: *Behavioral Segmentation*; carries `segmentId`
- → `BO-758` Membership & Loyalty Segments: *Membership & Loyalty Segments*; carries `segmentId`
- → `BO-759` Demographic & Geographic: *Demographic & Geographic*
- → `BO-760` Revenue & Engagement Segments: *Revenue & Engagement Segments*; carries `segmentId`
- → `BO-761` AI Audience Discovery: *AI Audience Discovery*
- → `BO-762` Predictive Audiences: *Predictive Audiences*; carries `segmentId`
- → `BO-763` Activation & Governance: *Activation & Governance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-755`: Same matching and reachable figures.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
totals:
  guests: 48210
  reachableEmail: 29410
  reachableWhatsApp: 26030
  reachableSms: 10606
overlap: Lapsed pass holders x Kids Club parents - 1,120 shared
```

#### Permissions

- `getAudienceOverlap` → `MARKETING_VIEW` (read) · staff
- `listSegments` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-754` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-754`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 1: Opens Audience Intelligence → Give marketers and CRM teams an overview of addressable audience health. Show total guests, reachable guests, active segments, consent-eligible audience, high-value and churn-risk populations. …
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F246 branch at step 1 (expected): when Nothing has been set up on Audience Intelligence yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F246 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-754?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-755`, `BO-756`, `BO-757`, `BO-758`, `BO-759`, `BO-760`, `BO-761`, `BO-762`, `BO-763`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-755` Dynamic Segment Builder

**Allow authorized users to create automatically refreshed rule-based audiences. Provide nested AND/OR/NOT logic across profile, behavior, transaction, membership, loyalty, wallet and custom attributes. Show live audience count, reachable count, exclusions, consent impact and representative sample guests while rules are edited. Support effective dates, refresh frequency, ownership, tags, descriptions, approvals and reusable rule groups. Validate incompatible conditions, excessive complexity and restricted attributes before save or activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-BO-755 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `segmentId` (navigation) |
| Route | `/engagement-support/dynamic-segment-builder-bo-755` |

**Known gaps.** **Dynamic Segment Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The marketer builds a rule-based segment that refreshes itself. It shows a live matching count and, separately, the REACHABLE count per channel after consent and suppression. A segment of 50,000 with 3,000 email consents is a 3,000-person campaign, and the builder must say so before anyone plans a send.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- CreateSegmentRequest supports a flat list of criteria with match all or any; the purpose requires nested AND/OR/NOT groups, effective dates, refresh frequency, ownership, tags and approval. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): previewSegment works only on a saved segment (POST /segments/{segmentId}/preview). (CHG-SBO-013); The screen has list states but no list operation (listSegments is not declared here). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Search | text field | — | max length 200 | `listSegments` ?search |

**Form: Create segment** (modal, opened by *Create segment*; *Create segment* calls `createSegment`, *Cancel* sends nothing)

**Collects what `createSegment` sends before it is called.** Required: `name`, `criteria`. Optional: `description`, `venueId`, `match`, `excludeSegmentIds`, `ruleGroups`, `effectiveFrom`, `effectiveTo`, `ownerPrincipalId`, `requiresApproval`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createSegment` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createSegment` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createSegment` body |
| Match `match` | segmented control | optional | All | All · Any | — | — | `createSegment` body |
| Criteria `criteria` | repeatable rows | required | — | at least 1 | — | — | `createSegment` body |
| Attribute `criteria[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createSegment` body |
| Operator `criteria[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createSegment` body |
| Value `criteria[].value` | field | optional | — | — | — | — | `createSegment` body |
| Values `criteria[].values` | list of values (chips) | optional | — | — | — | — | `createSegment` body |
| Exclude segments `excludeSegmentIds` | multi-picker: choose exclude segments | optional | — | — | — | — | `createSegment` body |
| Rule groups `ruleGroups` | repeatable rows | optional | — | — | — | Nested AND / OR / NOT groups (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by `match`) AND every group here. | `createSegment` body |
| Operator `ruleGroups[].operator` | segmented control | optional | — | And · Or · Not | — | — | `createSegment` body |
| Criteria `ruleGroups[].criteria` | repeatable rows | optional | — | — | — | Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). | `createSegment` body |
| Groups `ruleGroups[].groups` | repeatable rows | optional | — | — | — | — | `createSegment` body |
| Operator `ruleGroups[].groups[].operator` | segmented control | optional | — | And · Or · Not | — | — | `createSegment` body |
| Criteria `ruleGroups[].groups[].criteria` | repeatable rows | optional | — | — | — | Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). | `createSegment` body |
| Groups `ruleGroups[].groups[].groups` | repeatable rows | optional | — | — | — | — | `createSegment` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | The segment is evaluated for sends only from this time. | `createSegment` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createSegment` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | Who answers for the segment; defaults to its creator. | `createSegment` body |
| Requires approval `requiresApproval` | toggle | optional | off | — | — | Where true, a campaign may use the segment only after an `approvals` request on it is approved. | `createSegment` body |

Errors to draw in the form: 400 Criteria are contradictory or reference unknown attributes

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Rules**: Attribute, operator, value rows (equals, not equals, greater than, less than, between, in, not in, exists, not exists, within days). Attributes cover profile, visits, spend, products bought, membership, tier, wallet, language, wishlist and behaviour. Match all or any. The purpose asks for nested AND/OR/NOT groups (see corrections). *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SegmentCriterion; contracts/satellite/marketing-crm.yaml#createSegment; DI-381)*
- **Wallet balance attribute**: Segments on cash credit only. A separate "credit expiring within N days" rule targets promotional credit about to lapse. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SegmentCriterion)*
- **Household attributes**: A household total must never be messaged to every member. Warn when a portfolio attribute is used in a segment meant for sends. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SegmentCriterion)*
- **Exclude segments**: Pick segments to exclude (e.g. "Complained in the last 30 days"); the exclusions count shows how many each removes. *(source: contracts/satellite/marketing-crm.yaml#createSegment)*

#### Outputs: what the screen shows and produces

**Shown**

**Segments** (data table, from `listSegments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Match | chip: All, Any | — |
| Criteria | list or chips (count when long) | — |
| Attribute | text | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. |
| Operator | chip: Equals, Not equals, Greater than, Less than, Between, In… | — |
| Value | text | — |
| Values | list or chips (count when long) | — |
| Exclude segments | list or chips (count when long) | — |
| Rule groups | list or chips (count when long) | Nested AND / OR / NOT groups (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by … |
| Operator | chip: And, Or, Not | — |
| Criteria | list or chips (count when long) | Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). |
| Groups | list or chips (count when long) | — |
| Effective from | 1 Oct 2026, 14:30 | The segment is evaluated for sends only from this time. |
| Effective to | 1 Oct 2026, 14:30 | — |
| Owner principal | the name it points at, never the id | Who answers for the segment; defaults to its creator. |
| Requires approval | yes / no (icon or chip) | Where true, a campaign may use the segment only after an `approvals` request on it is approved. |
| ID | the name it points at, never the id | — |

**Matching guests** (metric tile, from `previewSegmentDraft`): Counts on the rules as edited, before anything is saved.

| Shows | Format | Notes |
|---|---|---|
| Matching count | 1,234 | — |
| Reachable | text | — |
| Evaluated at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | `createSegment` POST `/segments` | CreateSegmentRequest | Segment | 400 Criteria are contradictory or reference unknown attributes | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Counts**: Matching count, then reachable per channel (email, SMS, WhatsApp, push) after consent and suppression, with "evaluated at 10:42". Reachable is always shown beside matching, never instead of it. *(source: contracts/satellite/marketing-crm.yaml#previewSegment)*
- **Sample guests**: Up to 10 representative guests (masked contact) to sanity-check the rules. *(source: screens/P08-venue-back-office.yaml#BO-755)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Save segment**: Saves the definition, not a list. It is evaluated whenever it is used, so it cannot go stale. *(source: contracts/satellite/marketing-crm.yaml#createSegment)*

**Data it reads**: `listSegments` (onLoad, The segments to open and edit)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic segment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic segment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic segment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic segment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes; 400 Validation failed |

#### Edge cases to draw

- **The rules match nobody**: Show 0 with the rule that removed the most guests highlighted, rather than an empty preview. *(source: designer default)*
- **A restricted attribute (health-adjacent, minors)**: Dietary and accessibility needs and minors' data are refused for marketing segments, with the reason shown. *(source: contracts/satellite/marketing-crm.yaml#updateMyProfile; R205)*

#### Consistency with other screens

- Match `BO-754`: Segment list and audience intelligence use the same matching and reachable counts.
- Match `BO-767`: The campaign's audience step reuses this preview (matching and reachable per channel).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
name: Lapsed annual pass holders - no visit in 90 days
rules:
- Membership = Annual Pass (active)
- Last visit not within 90 days
- Language in (Arabic, English)
exclude:
- Complained in the last 30 days
counts:
  matching: 4812
  email: 2930
  whatsapp: 3410
  sms: 1206
  push: 1880
```

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `listSegments` → `MARKETING_VIEW` (read) · staff
- `previewSegmentDraft` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-755` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-755`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 2: Works in Dynamic Segment Builder → Allow authorized users to create automatically refreshed rule-based audiences. Provide nested AND/OR/NOT logic across profile, behavior, transaction, membership, loyalty, wallet and custom …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-755?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-756` Static Lists & Imports

**Manage governed fixed audiences and externally supplied lists. Create lists manually or through secure file import with field mapping, validation, deduplication and error handling. Configuration Scope of Work / Version 1.0 16 Match imported members to the Customer Master and control whether unmatched records may create leads or remain quarantined. Record source, owner, purpose, consent basis, expiry, refresh history and file provenance. Support additions, removals, suppression and export under RBAC/PBAC and audit controls. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-756 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/static-lists-imports-bo-756` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Fixed audiences and supplied lists: created by hand or imported (CSV or Excel) with field mapping, validation, de-duplication and error handling. Imported rows are matched to the guest master, and the rows that do not match either create a lead or stay quarantined - the two honest answers. Every list records its source, owner, purpose, consent basis and expiry.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Import formats and validation rules for customer and segment migration are pending a dedicated data-migration workshop.** → Drawn default accepted: CSV and XLSX with a downloadable template (first name, last name, email, mobile, language, external id). *(decided by Chinmay, 2026-10-02; DEC-279 / CHG-NOTE-002)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **File and mapping**: Upload, map columns to guest fields, preview the first 20 rows, see validation errors per row before importing. *(source: contracts/satellite/marketing-crm.yaml#importAudienceList)*
- **Unmatched rows**: Create leads or quarantine; there is no third option. *(source: contracts/satellite/marketing-crm.yaml#importAudienceList)*
- **Consent basis**: Required. An imported list does not grant marketing consent; imported guests without consent are listed but not reachable. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentSource; DI-378)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import audience list (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Import result**: Rows read, matched, new leads, quarantined, rejected (with a downloadable error file). *(source: contracts/satellite/marketing-crm.yaml#importAudienceList)*

**Data it reads**: `listAudienceLists` (onLoad, Lists held)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The static lists imports list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the static lists imports untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No static lists imports yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the static lists imports are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
list: Corporate partners 2026 - imported 28 Sep 2026 - 1,450 rows - 1,212 matched - 180 leads - 58 quarantined
consentBasis: Existing customers, email consent recorded at source (import)
```

#### Permissions

- `importAudienceList` → `MARKETING_MANAGE` (configure) · staff
- `listAudienceLists` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-756` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-756`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 4: Works in Static Lists & Imports → Manage governed fixed audiences and externally supplied lists. Create lists manually or through secure file import with field mapping, validation, deduplication and error handling. Configuration …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-756?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import audience list, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-757` Behavioral Segmentation

**Build audiences from observable guest activity. Use purchase, visit, ticket scan, reservation, cart, app, web, campaign, chatbot, survey and review events. Support recency, frequency, count, value, sequence, absence-of-event and time-window conditions. Preview top behaviors, sources and data freshness and exclude bot, employee, test or fraudulent activity. Refresh segments through event streams and expose rule/version provenance for each inclusion. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-757 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `segmentId` (navigation) |
| Route | `/engagement-support/behavioral-segmentation-bo-757` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Segments from what guests did: purchases, visits, scans, reservations, carts, app and web sessions, campaign opens, chatbot, surveys, reviews. Conditions on recency, frequency, value, sequence, and the absence of an event in a window. Bots, employees and test or fraudulent activity are excluded.

**Fixed on main** (the package already carries these; draw what it says): Only createSegment is declared; no preview, no list. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Search | text field | — | max length 200 | `listSegments` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Event condition**: Event, count or value, within a time window, or "did not happen within N days"; behavioural examples from the meeting are cart abandoned, app session, campaign opened, survey completed. *(source: DI-381; contracts/satellite/marketing-crm.yaml#/components/schemas/SegmentCriterion)*
- **Event-state precision**: "Visited" means a scanned ticket, not a purchase; the picker shows the precise state. *(source: DI-561)*

#### Outputs: what the screen shows and produces

**Shown**

**Segments** (data table, from `listSegments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Match | chip: All, Any | — |
| Criteria | list or chips (count when long) | — |
| Attribute | text | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. |
| Operator | chip: Equals, Not equals, Greater than, Less than, Between, In… | — |
| Value | text | — |
| Values | list or chips (count when long) | — |
| Exclude segments | list or chips (count when long) | — |
| Rule groups | list or chips (count when long) | Nested AND / OR / NOT groups (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by … |
| Operator | chip: And, Or, Not | — |
| Criteria | list or chips (count when long) | Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). |
| Groups | list or chips (count when long) | — |
| Effective from | 1 Oct 2026, 14:30 | The segment is evaluated for sends only from this time. |
| Effective to | 1 Oct 2026, 14:30 | — |
| Owner principal | the name it points at, never the id | Who answers for the segment; defaults to its creator. |
| Requires approval | yes / no (icon or chip) | Where true, a campaign may use the segment only after an `approvals` request on it is approved. |
| ID | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Preview (secondary button) | `previewSegment` POST `/segments/{segmentId}/preview` | — | SegmentPreview | — | — |

**Data it reads**: `listSegments` (onLoad, The behavioural segments to open)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The behavioral segmentation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the behavioral segmentation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No behavioral segmentation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the behavioral segmentation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Consistency with other screens

- Match `BO-755`: Same rule builder and preview; this screen pre-selects the behavioural attributes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
segment: Cart abandoned (membership only) in last 3 days, cart over AED 500, no purchase since
counts:
  matching: 214
  whatsapp: 160
```

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `listSegments` → `MARKETING_VIEW` (read) · staff
- `previewSegment` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |
| 22.1.6 | Audience Selection | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `previewSegment` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-757` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-757`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 6: Works in Behavioral Segmentation → Build audiences from observable guest activity. Use purchase, visit, ticket scan, reservation, cart, app, web, campaign, chatbot, survey and review events. Support recency, frequency, count, value …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-757?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel, Preview.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-758` Membership & Loyalty Segments

**Create audiences using membership, loyalty and wallet state. Filter by membership type, status, start, expiry, renewal, freeze, benefit use and upgrade eligibility. Filter by loyalty tier, points, earn/redemption history, reward use, milestone and tier movement. Use wallet balance, top-up, spend, low-balance and dormancy conditions while protecting financial data. Combine these signals with profile and behavior rules and show reachable audience before activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-758 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `segmentId` (navigation) |
| Route | `/engagement-support/membership-loyalty-segments-bo-758` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Segments on membership, loyalty and wallet state: membership type, status, expiry, renewal, freeze, benefit use; tier, points, earn and redemption history, milestones, tier movement; wallet balance, top-ups, spend, low balance, dormancy. Financial data is protected: wallet balance segments on cash credit only, and expiring promotional credit is its own condition.

**Fixed on main** (the package already carries these; draw what it says): Only createSegment is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Wallet conditions**: Cash balance bands, low balance, dormancy, "credit expiring within N days"; never a household total messaged to each member. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/SegmentCriterion)*
- **Loyalty conditions**: Tier, points band, points expiring within N days, tier moved up or down in a period. *(source: screens/P08-venue-back-office.yaml#BO-758; DI-382)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Preview (secondary button) | `previewSegment` POST `/segments/{segmentId}/preview` | — | SegmentPreview | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership loyalty segments list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership loyalty segments untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership loyalty segments yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership loyalty segments are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
segment: Silver members within 500 points of Gold
counts:
  matching: 640
  email: 410
```

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `previewSegment` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.1.6 | Audience Selection | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.4 | Audience Targeting | Marketing & CRM | CONTRACTED | `previewSegment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-758` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-758`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 8: Works in Membership & Loyalty Segments → Create audiences using membership, loyalty and wallet state. Filter by membership type, status, start, expiry, renewal, freeze, benefit use and upgrade eligibility. Filter by loyalty tier, points …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-758?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel, Preview.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-759` Demographic & Geographic

**Configure demographic and location-based audiences responsibly. Use age band, household, language, country, city, postcode, visitor type, nationality where lawful and custom demographics. Support location radius, venue proximity, travel market, timezone and resident/tourist classification. Display consent, fairness, minimum-audience and restricted-attribute warnings before use. Allow jurisdiction-specific field availability and prevent prohibited sensitive targeting. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-759 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/demographic-geographic-bo-759` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Demographic and location audiences, used responsibly: age band, household, language, country, city, nationality where lawful, resident or tourist, radius from a venue, travel market. Restricted attributes and minimum audience sizes are warned before use, and prohibited combinations are blocked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Restricted attributes**: Nationality and age show a warning and require a stated purpose; minors (no date of birth counts as minor) are excluded from marketing segments. *(source: screens/P08-venue-back-office.yaml#BO-759; R205)*
- **Minimum audience size**: A segment under the minimum cannot be used for sends, to protect individuals. *(source: screens/P08-venue-back-office.yaml#BO-759)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The demographic geographic list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the demographic geographic untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No demographic geographic yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the demographic geographic are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
segment: UAE residents in Dubai and Sharjah, Arabic-speaking, families with children 4-12
counts:
  matching: 6120
  whatsapp: 4380
```

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-759` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-759`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 10: Works in Demographic & Geographic → Configure demographic and location-based audiences responsibly. Use age band, household, language, country, city, postcode, visitor type, nationality where lawful and custom demographics. Support …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-759?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-760` Revenue & Engagement Segments

**Create value- and engagement-based audiences. Configuration Scope of Work / Version 1.0 17 Use total revenue, LTV, average order value, purchase frequency, category spend, refund behavior and propensity. Use engagement score, campaign interaction, app activity, visit frequency, inactivity and product affinity. Define bands, percentiles, scoring periods and calculation sources and preview distribution before publishing. Protect against circular attribution and record the data snapshot and scoring version used. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-760 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `segmentId` (navigation) |
| Route | `/engagement-support/revenue-engagement-segments-bo-760` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Value and engagement segments: revenue, LTV, average order value, frequency, category spend, refund behaviour, engagement score, campaign interaction, inactivity and affinity, as bands or percentiles over a stated scoring period. The distribution is previewed before the segment is published.

**Fixed on main** (the package already carries these; draw what it says): Only createSegment is declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Preview (secondary button) | `previewSegment` POST `/segments/{segmentId}/preview` | — | SegmentPreview | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Distribution preview**: Histogram of the chosen measure with the band boundaries, scoring period and source stated. *(source: screens/P08-venue-back-office.yaml#BO-760)*

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue engagement segments list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue engagement segments untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue engagement segments yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue engagement segments are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
segment: Top 10% by 12-month spend (over AED 3,800)
engagementTiers:
- new
- active
- occasional
- lapsing
- lapsed
- dormant
```

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `previewSegment` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.1.6 | Audience Selection | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.4 | Audience Targeting | Marketing & CRM | CONTRACTED | `previewSegment` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-760` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-760`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 12: Works in Revenue & Engagement Segments → Create value- and engagement-based audiences. Configuration Scope of Work / Version 1.0 17 Use total revenue, LTV, average order value, purchase frequency, category spend, refund behavior and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-760?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel, Preview.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-761` AI Audience Discovery

**Discover meaningful customer clusters using explainable AI. Present suggested clusters with dominant traits, size, reachability, value, engagement and observed opportunity. Show contributing variables, confidence, stability, bias/fairness checks and excluded sensitive attributes. Allow users to inspect sample profiles and convert a recommendation into an editable governed segment. Require human approval and retain feedback, model/version and final segment definition. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-BO-761 |
| Who uses it | venue staff holding `AI_USE`, `PRICE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/ai-audience-discovery-bo-761` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** AI-suggested customer clusters and lookalike audiences inside the tenant's own guests, each with traits, size, value and confidence; a person saves the segment.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listAudienceDiscoveryTargeting return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listAudienceDiscoveryTargeting carry no identifier. (CHG-SBO-005)

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

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **cluster card**: Dominant traits, size, estimated reach, confidence and basis; "Save as segment" is a human act. *(source: contracts/satellite/ai.yaml#proposeLookalikeSegment)*

**Data it reads**: `listAudienceDiscoveryTargeting` (onLoad, AI Audience Discovery & Targeting Optimization)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience discovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience discovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience discovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience discovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Neither seed was sent (`seed-required`), or the seed has fewer than 50 consented guests (`seed-too-small`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cluster:
  name: Weekend families, two children
  size: 8420
  reach: 7100
  confidence: 0.81
```

#### Permissions

- `listAudienceDiscoveryTargeting` → `PRICE_VIEW` (read) · staff
- `proposeLookalikeSegment` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.31 | System shall provide customer-segment-based discount recommendations. | Unified Operations Dashboard | CONTRACTED | `listAudienceDiscoveryTargeting` |
| 22.14.11 | AI Audience Discovery | Marketing & CRM | CONTRACTED | `listAudienceDiscoveryTargeting` |
| 22.14.12 | AI Lookalike Audiences | Marketing & CRM | CONTRACTED | `proposeLookalikeSegment` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-761` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-761`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 14: Works in AI Audience Discovery → Discover meaningful customer clusters using explainable AI. Present suggested clusters with dominant traits, size, reachability, value, engagement and observed opportunity. Show contributing …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-761?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `AI_USE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-762` Predictive Audiences

**Create model-based audiences for future behavior and opportunity. Support lookalike, churn, reactivation, membership upgrade, next purchase and high-value propensity audiences. Display prediction window, threshold, audience size, confidence, lift and primary model factors. Allow threshold simulation and exclusions and monitor drift, performance and fairness after activation. Never use predictive status to override consent, eligibility, pricing, capacity or service policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-762 |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `segmentId` (navigation), `actionId` (navigation) |
| Route | `/engagement-support/predictive-audiences-bo-762` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Model-based audiences: lookalike, churn, reactivation, upgrade, next purchase, high-value propensity. Each shows the prediction window, threshold, size, confidence, lift and main factors. A predicted status never overrides consent, eligibility or pricing rules. Lookalikes expand only within the tenant's own guests.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Threshold**: A slider with the audience size and expected lift updating; exclusions apply. *(source: screens/P08-venue-back-office.yaml#BO-762)*
- **Lookalike seed**: A segment or list; expansion stays inside the tenant's guests, no pooled or third-party data. *(source: contracts/satellite/ai.yaml#proposeLookalikeSegment)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Accept AI proposal**: A person approves; saving the segment happens under their own permission. *(source: contracts/satellite/ai.yaml#decideProposedAction)*

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The predictive audiences list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the predictive audiences untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No predictive audiences yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the predictive audiences are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 422 Neither seed was sent (`seed-required`), or the seed has fewer than 50 consented guests (`seed-too-small`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
audience: Likely to renew annual pass in 30 days - threshold 0.7 - 1,880 guests - lift 2.4x - model renew-v1
```

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `previewSegment` → `MARKETING_VIEW` (read) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `proposeLookalikeSegment` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.1.6 | Audience Selection | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.4 | Audience Targeting | Marketing & CRM | CONTRACTED | `previewSegment` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-762` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-762`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 16: Works in Predictive Audiences → Create model-based audiences for future behavior and opportunity. Support lookalike, churn, reactivation, membership upgrade, next purchase and high-value propensity audiences. Display prediction …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-762?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-763` Activation & Governance

**Control where audiences are used and how they remain compliant. Activate to campaigns, journeys, website, mobile app and approved external platforms through secured connectors. Configure suppression, consent enforcement, frequency limits, destination mapping, refresh schedule and expiry. Require approval for sensitive, high-volume or external activation and provide a pre-flight impact summary. Configuration Scope of Work / Version 1.0 18 Track synchronization, failures, member counts, destination use, versions and the complete activation audit trail. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 19 Board 4 - Campaign Management & Attribution Figure 4. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 20**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-763 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/activation-governance-bo-763` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Where audiences are used and whether they stay compliant: activation to campaigns, journeys, website, app and approved external platforms. Sending an audience to an external advertising platform is a data export, so it needs approval and carries suppression and consent enforcement.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Destination**: Campaign, journey, website, app, or an approved external connector; external needs approval and the third-party-sharing consent. *(source: contracts/satellite/marketing-crm.yaml#activateAudience; contracts/satellite/marketing-crm.yaml#/components/schemas/ConsentPurpose)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Pre-flight summary**: Who will be sent, who is excluded and why, refresh schedule and expiry. *(source: contracts/satellite/marketing-crm.yaml#activateAudience)*
- **Sync status**: Each activation with last sync and drift. *(source: contracts/satellite/marketing-crm.yaml#listAudienceActivations)*

**Data it reads**: `listAudienceActivations` (onLoad, Where audiences are in use)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The activation governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the activation governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No activation governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the activation governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Blocked by consent, volume or approval |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
activation: Lapsed pass holders -> Meta custom audience - pending approval - 2,104 with third-party sharing consent
  of 4,812
```

#### Permissions

- `activateAudience` → `MARKETING_MANAGE` (configure) · staff
- `listAudienceActivations` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-763` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-763`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 18: Works in Activation & Governance → Control where audiences are used and how they remain compliant. Activate to campaigns, journeys, website, mobile app and approved external platforms through secured connectors. Configure suppression …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-763?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"activateAudience": {"method":"POST","path":"/audience-activations","contract":"marketing-crm","summary":"Push an audience to a campaign, journey or external platform","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AudienceActivation","responds":null},
"createSegment": {"method":"POST","path":"/segments","contract":"marketing-crm","summary":"Create a segment","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateSegmentRequest","responds":"Segment"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getAudienceOverlap": {"method":"GET","path":"/audience-overlap","contract":"marketing-crm","summary":"How much audiences overlap, and how many are reachable","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"segmentIds","in":"query","required":true},{"name":"channel","in":"query","required":null}],"requestBody":null,"responds":"AudienceOverlap"},
"importAudienceList": {"method":"POST","path":"/audience-lists","contract":"marketing-crm","summary":"Load a supplied list, matched against the guest master","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AudienceList","responds":"AudienceList"},
"listAudienceActivations": {"method":"GET","path":"/audience-activations","contract":"marketing-crm","summary":"Where audiences are being used, and whether they are still in sync","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAudienceDiscoveryTargeting": {"method":"GET","path":"/audience-discovery-targeting","contract":"promotions","summary":"AI Audience Discovery & Targeting Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAudienceDiscoveryTargetingOptimizationView"},
"listAudienceLists": {"method":"GET","path":"/audience-lists","contract":"marketing-crm","summary":"Static and imported audiences","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSegments": {"method":"GET","path":"/segments","contract":"marketing-crm","summary":"List segments","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"previewSegment": {"method":"POST","path":"/segments/{segmentId}/preview","contract":"marketing-crm","summary":"Estimate segment size and reachability","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SegmentPreview"},
"previewSegmentDraft": {"method":"POST","path":"/segments/preview","contract":"marketing-crm","summary":"Estimate an unsaved segment's size and reachability","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":"CreateSegmentRequest","responds":"SegmentDraftPreview"},
"proposeLookalikeSegment": {"method":"POST","path":"/ai/segment-suggestions","contract":"ai","summary":"Propose a lookalike segment from a seed, for a person to save","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiLookalikeSegmentProposal"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAudienceDiscoveryTargetingOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What AI Audience Discovery & Targeting Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"narrowAudience":{"type":"string","description":"Narrow audience"},"expandAudience":{"type":"string","description":"Expand audience"},"excludeLowValueSegment":{"type":"string","description":"Exclude low-value segment"},"changeEligibility":{"type":"string","description":"Change eligibility"},"changeChannel":{"type":"string","description":"Change channel"},"changeTiming":{"type":"string","description":"Change timing"},"changePromotion":{"type":"string","description":"Change promotion"},"reduceFrequency":{"type":"string","description":"Reduce frequency"},"membershipTierEligibility":{"type":"string","description":"Membership/tier eligibility"},"membershipAndLoyaltyEligibility":{"type":"string","description":"Membership and loyalty eligibility"},"audienceName":{"type":"string","description":"Discovered audience"},"audienceSize":{"type":"integer","description":"Audience size"},"suggestedOffer":{"type":"string","description":"Suggested offer"},"predictedConversion":{"type":"number","description":"Predicted conversion, percent"},"estimatedIncrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated incremental revenue"},"rationale":{"type":"string","description":"Why this audience (explainable factors)"}}},
"AiLookalikeSegmentProposal": {"type":"object","x-ticvai-persistence":"none — the draft is an ai.proposed_action row (kind audience); the evidence is its decision record","description":"A lookalike segment as rules a person can read, edit and save (22.14.12). The criteria are shaped as `marketing-crm` `SegmentCriterion` (attribute, operator, value) and restated here because a satellite cannot reference another satellite.","required":["proposedActionId","criteria","estimatedReach"],"properties":{"proposedActionId":{"type":"string","format":"uuid","description":"The `ai.proposed_action` row whose payload is the `marketing-crm.createSegment` body."},"name":{"type":"string","nullable":true},"criteria":{"type":"array","items":{"type":"object","required":["attribute","operator"],"properties":{"attribute":{"type":"string"},"operator":{"type":"string"},"value":{"description":"As `SegmentCriterion.value` in marketing-crm (any type)."},"weight":{"type":"number","nullable":true,"description":"How much this attribute separated the seed from everyone else."}}}},"similarityBasis":{"type":"array","items":{"type":"object","properties":{"attribute":{"type":"string"},"seedShare":{"type":"number","description":"Share of the seed holding the value."},"populationShare":{"type":"number","description":"Share of the tenant's consented guests holding it."}}}},"estimatedReach":{"type":"integer","description":"Consented guests the criteria select, excluding the seed where `excludeSeed`."},"seedSize":{"type":"integer"},"overlapWithSeed":{"type":"number","minimum":0,"maximum":1,"description":"Share of the seed the criteria would also select; a check that the rules describe the seed."},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid"}}},
"AudienceActivation": {"type":"object","x-ticvai-persistence":"marketing.audience_activation","description":"Board 3.10. **Consent is enforced at activation, not at definition.**","required":["segmentId","destination"],"properties":{"id":{"type":"string","format":"uuid"},"segmentId":{"type":"string","format":"uuid"},"destination":{"type":"string","enum":["campaign","journey","website","mobileApp","externalAdPlatform","partnerFeed"]},"destinationReference":{"type":"string","nullable":true},"external":{"type":"boolean","default":false},"suppressionListIds":{"type":"array","items":{"type":"string","format":"uuid"}},"enforceConsent":{"type":"boolean","default":true},"frequencyCapPerWeek":{"type":"integer","nullable":true},"refreshSchedule":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true},"preFlight":{"type":"object","readOnly":true,"properties":{"members":{"type":"integer"},"reachable":{"type":"integer"},"suppressed":{"type":"integer"},"consentBlocked":{"type":"integer"},"frequencyBlocked":{"type":"integer"}}},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["draft","pendingApproval","active","failed","expired"]},"lastSyncedAt":{"type":"string","format":"date-time","nullable":true},"lastSyncErrors":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"AudienceList": {"type":"object","x-ticvai-persistence":"marketing.audience_list","description":"Board 3.3. **Consent basis is required on the import, not optional metadata.**","required":["name"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["manual","imported","suppression"]},"assetId":{"type":"string","format":"uuid","nullable":true},"fieldMapping":{"type":"object","additionalProperties":{"type":"string"}},"rowsRead":{"type":"integer","readOnly":true},"matched":{"type":"integer","readOnly":true},"unmatched":{"type":"integer","readOnly":true},"duplicatesRemoved":{"type":"integer","readOnly":true},"rejected":{"type":"integer","readOnly":true},"unmatchedHandling":{"type":"string","enum":["createLead","quarantine"],"default":"quarantine","description":"**The two honest answers.** Silently dropping them tells a marketer their list of ten thousand reached ten thousand.\n"},"source":{"type":"string"},"owner":{"type":"string","format":"uuid"},"purpose":{"type":"string"},"consentBasis":{"type":"string"},"expiresAt":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"AudienceOverlap": {"type":"object","description":"Board 3.1. **Reachable is always smaller, and it is the number that matters.**","properties":{"segments":{"type":"array","items":{"type":"object","properties":{"segmentId":{"type":"string","format":"uuid"},"name":{"type":"string"},"members":{"type":"integer"},"reachable":{"type":"integer"},"suppressed":{"type":"integer"},"consentBlocked":{"type":"integer"},"duplicates":{"type":"integer"}}}},"pairwiseOverlap":{"type":"array","items":{"type":"object","properties":{"segmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"shared":{"type":"integer"},"sharedPercent":{"type":"number"}}}},"totalUnique":{"type":"integer"},"totalReachable":{"type":"integer"}}},
"CreateSegmentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","criteria"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"match":{"type":"string","enum":["all","any"],"default":"all"},"criteria":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/SegmentCriterion"}},"excludeSegmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ruleGroups":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"**Nested AND / OR / NOT groups** (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by `match`) AND every group here. Absent keeps the flat list.","items":{"$ref":"#/components/schemas/SegmentRuleGroup"}},"effectiveFrom":{"type":"string","format":"date-time","nullable":true,"description":"The segment is evaluated for sends only from this time."},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who answers for the segment; defaults to its creator."},"requiresApproval":{"type":"boolean","default":false,"description":"Where true, a campaign may use the segment only after an `approvals` request on it is approved."}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"Segment": {"x-ticvai-persistence":"marketing.segment + marketing.segment_criterion","allOf":[{"$ref":"#/components/schemas/CreateSegmentRequest"},{"type":"object","required":["id","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"lastEvaluatedSize":{"type":"integer","nullable":true},"lastEvaluatedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]},
"SegmentCriterion": {"x-ticvai-persistence":"marketing.segment_criterion","type":"object","required":["attribute","operator"],"properties":{"attribute":{"type":"string","description":"Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language.\n**Free-form rather than an enum, which is why 22.14.8, 5.3.19 and 5.5.17b were readable as gaps and are not.** `walletBalance`, `engagementTier` and `portfolioScope` are expressible today; what was missing was anybody saying so.\n**Three that need saying, because the naive reading is wrong:**\n`walletBalance` should segment on **`cash` credit only**. A guest with 200 dirhams of promotional credit expiring Friday is a different campaign from one with 200 of their own money, and treating them alike sends a spend-it-now message to somebody who was given it.\n`walletBalance.expiringWithinDays` is the segment that earns the attribute — **credit about to expire unspent is a guest about to be disappointed and a venue about to book breakage**, and only one of those is worth a message.\n`portfolioScope` aggregates across a `DelegatedAccess` delegation (CF-132) and **must not message every member about a household total** — that is how a venue tells a teenager what their parent spends.\n`entitlementExpiringWithinDays` (29 September, build pass, group G2; 5.5.30): the guest holds a ticket or pass in `issued` or `partiallyConsumed` whose `validTo` is within that many days, kept current from `entitlement.expiringSoon` and the entitlement read model. **Unused passes about to lapse** are this attribute with `entitlementRemainingUses` greater than zero.\n"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","exists","notExists","withinDays"]},"value":{},"values":{"type":"array","items":{}}}},
"SegmentDraftPreview": {"x-ticvai-persistence":"none — evaluated live","type":"object","description":"The preview of an unsaved segment (`previewSegmentDraft`, CHG-CSA-045); `SegmentPreview` without a segment id.","properties":{"matchingCount":{"type":"integer"},"reachable":{"$ref":"#/components/schemas/SegmentPreview/properties/reachable"},"evaluatedAt":{"type":"string","format":"date-time"}}},
"SegmentPreview": {"x-ticvai-persistence":"none — evaluated live","type":"object","required":["segmentId","matchingCount","reachable"],"properties":{"segmentId":{"type":"string","format":"uuid"},"matchingCount":{"type":"integer"},"reachable":{"type":"array","description":"Per channel, after consent and suppression. A segment of 50,000 with 3,000 email consents is a 3,000-person campaign.\n","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/MessageChannel"},"reachableCount":{"type":"integer"},"excludedNoConsent":{"type":"integer"},"excludedSuppressed":{"type":"integer"},"excludedNoAddress":{"type":"integer"}}}},"evaluatedAt":{"type":"string","format":"date-time"}}},
"SegmentRuleGroup": {"x-ticvai-persistence":"none — stored with the segment as jsonb","type":"object","description":"One group of a segment's nested rules (CHG-CSA-045). `operator` combines the group's `criteria` and its child `groups`; `not` negates the group (it takes one child, criteria or group).","properties":{"operator":{"type":"string","enum":["and","or","not"]},"criteria":{"type":"array","description":"Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). Typed loosely here so the new optional field adds no required member to `createSegment`'s body for clients built at r1; the server validates each entry as a `SegmentCriterion` (400 otherwise).","items":{"type":"object","additionalProperties":true}},"groups":{"type":"array","items":{"$ref":"#/components/schemas/SegmentRuleGroup"}}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]}
}
```
