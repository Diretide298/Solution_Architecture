# WS138 — Marketing CRM Configuration Reference v1.0 board 4

**10 screens · 15 operations · 29 schemas · 7 permissions**

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
  `AI_USE, APPROVAL_REQUEST, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW, PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |

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
| `BO-764` | Campaign Command Center | D | 0 | 0 | 6 | 2 | 1 | 6 | — | notStarted (—) |
| `BO-765` | Campaign Library & Calendar | C | 0 | 7 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-766` | Campaign Builder | A | 44 | 0 | 6 | 21 | 0 | 6 | — | notStarted (—) |
| `BO-767` | Audience & Offer Selection | D | 0 | 0 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `BO-768` | Multichannel Composer | D | 0 | 14 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-769` | Schedule & Trigger Rules | D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-770` | Campaign Approval Workflow | C | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-771` | Budget, Goals & Forecast | B | 0 | 0 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `BO-772` | A/B & AI Optimization | A | 0 | 0 | 6 | 26 | 0 | 0 | — | notStarted (—) |
| `BO-773` | Attribution & Audit | D | 0 | 0 | 6 | 6 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-764, BO-765, BO-767, BO-768, BO-769, BO-770, BO-771, BO-773 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-764` Campaign Command Center

**Provide a real-time overview of campaign operations and commercial performance. Show active, scheduled, paused and completed campaigns with sends, reach, conversions, revenue, ROI and budget pacing. Compare email, SMS, WhatsApp, push, in-app, web and external-channel delivery and conversion. Display upcoming launches, approval bottlenecks, errors, capacity risks and underperforming campaigns. Provide explainable AI recommendations and drill-down to campaign, audience, channel and transaction detail. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-764 |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/campaign-command-center-bo-764` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The campaign operations overview: active, scheduled, paused and completed campaigns with sends, reach, conversions, revenue and budget pacing; channel comparison; upcoming launches, approvals waiting, errors and under-performers; AI recommendations to change segment, channel, timing or offer that a person accepts.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Scheduled · Sending · Paused · Completed · Stopped · Failed | `listCampaigns` ?status |
| Target kind | segmented control | — | Campaign · Journey | `listMarketingRecommendations` ?targetKind |
| Target ref | text field | — | — | `listMarketingRecommendations` ?targetRef |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listMarketingRecommendations` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Campaign row**: Name, status (draft, scheduled, sending, paused, completed, stopped, failed), channel, sent, delivered, conversion against its target (e.g. 80%), attributed revenue in AED. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CampaignStatus; DI-383)*
- **Recommendations**: Each with its reason and expected effect; never applied automatically. *(source: contracts/satellite/ai.yaml#listMarketingRecommendations)*

**Data it reads**: `listCampaigns` (onLoad, List campaigns); `listMarketingRecommendations` (onLoad, AI recommendations on this campaign or journey, with …)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-765` Campaign Library & Calendar: *Campaign Library & Calendar*
- → `BO-766` Campaign Builder: *Campaign Builder*; carries `campaignId`
- → `BO-767` Audience & Offer Selection: *Audience & Offer Selection*; carries `campaignId`
- → `BO-768` Multichannel Composer: *Multichannel Composer*; carries `campaignId`
- → `BO-769` Schedule & Trigger Rules: *Schedule & Trigger Rules*; carries `campaignId`
- → `BO-770` Campaign Approval Workflow: *Campaign Approval Workflow*
- → `BO-771` Budget, Goals & Forecast: *Budget, Goals & Forecast*; carries `campaignId`
- → `BO-772` A/B & AI Optimization: *A/B & AI Optimization*; carries `campaignId`
- → `BO-773` Attribution & Audit: *Attribution & Audit*; carries `campaignId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-118`: Same list and statuses (see BO-118 correction).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaigns:
- name: Kids Club half-term
  status: sending
  channel: Email
  sent: 8240
  conversion: 3.1% (target 4%)
  revenue: AED 42
  600.0: null
- name: Autumn comeback
  status: scheduled 15 Oct
  channel: WhatsApp
  reach: 3410
```

#### Permissions

- `listCampaigns` → `MARKETING_VIEW` (read) · staff
- `listMarketingRecommendations` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.16 | AI Campaign Recommendations | Marketing & CRM | CONTRACTED | `listMarketingRecommendations` |
| 22.3.17 | AI Journey Recommendations | Marketing & CRM | CONTRACTED | `listMarketingRecommendations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Campaign tracking shows click-through, conversion and revenue attribution per campaign, with configurable success criteria (e.g. 80% conversion target). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-383)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-764` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-764`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 1: Opens Campaign Command Center → Provide a real-time overview of campaign operations and commercial performance. Show active, scheduled, paused and completed campaigns with sends, reach, conversions, revenue, ROI and budget pacing. …
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F247 branch at step 1 (expected): when Nothing has been set up on Campaign Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F247 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-764?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-765`, `BO-766`, `BO-767`, `BO-768`, `BO-769`, `BO-770`, `BO-771`, `BO-772`, `BO-773`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-765` Campaign Library & Calendar

**Organize campaigns, templates and execution schedules. Provide table, card and calendar views filtered by owner, brand, venue, region, objective, channel and status. Support reusable templates for ticketing, events, membership, loyalty, wallet, seasonal, retention and abandoned-cart campaigns. Allow clone, archive, compare, tag and controlled bulk actions while preserving lineage and versions. Show schedule conflicts, blackout periods, audience fatigue and related journey activity. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-BO-765 |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/campaign-library-calendar-bo-765` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Promotions and campaigns on a calendar timeline (day, week, month) filtered by owner, venue, channel and status.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- List operation(s) listCampaignCalendarTimeline return a bare array, not the paged list envelope (items, nextCursor, hasMore). (CHG-SBO-005)

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listCampaignCalendarTimeline` ?venue |
| Product | text field | — | — | `listCampaignCalendarTimeline` ?product |
| Attraction | text field | — | — | `listCampaignCalendarTimeline` ?attraction |
| Channel | text field | — | — | `listCampaignCalendarTimeline` ?channel |
| Campaign | text field | — | — | `listCampaignCalendarTimeline` ?campaign |
| Promotion family | text field | — | — | `listCampaignCalendarTimeline` ?promotionFamily |
| View | radio group | — | Day · Week · Month · Quarter · Campaign timeline | `listCampaignCalendarTimeline` ?view |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listCampaignCalendarTimeline`): Campaigns placed across their run dates. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Calendar state | chip: Active, Upcoming, Ending soon, Expired, Pending approval, Conflicting… | How the calendar marks this promotion. |
| Promotion | text | Promotion ID |
| Promotion name | text | Promotion Name |
| Start date | 1 Oct 2026, 14:30 | Start Date |
| End date | 1 Oct 2026, 14:30 | End Date |
| Venue | text | Venue |
| Channel | text | Channel |

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **timeline**: Bars per promotion coloured by status; overlaps visible. *(source: contracts/satellite/promotions.yaml#listCampaignCalendarTimeline / DI-919)*

**Data it reads**: `listCampaignCalendarTimeline` (onLoad, Campaign Calendar & Timeline)

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign calendar yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
timeline:
- promotion: Winter Family 2026
  from: 15 Nov
  to: 15 Jan
  status: Scheduled
```

#### Permissions

- `listCampaignCalendarTimeline` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-765` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-765`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 2: Works in Campaign Library & Calendar → Organize campaigns, templates and execution schedules. Provide table, card and calendar views filtered by owner, brand, venue, region, objective, channel and status. Support reusable templates for …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-765?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-766` Campaign Builder

**Guide authorized users through complete campaign creation. Capture campaign name, objective, brand, venue, owner, products, commercial goal and measurement model. Configuration Scope of Work / Version 1.0 21 Support ticket, event, membership, loyalty, wallet, seasonal, retention, capacity and last-minute sales use cases. Provide a staged flow for objective, audience, offer, channels, schedule, review and activation. Validate required data, consent, inventory, offer, budget, channel and approval conditions before submission. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-BO-766 |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE`, `MARKETING_SEND`, `MARKETING_VIEW` (2 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/engagement-support/campaign-builder-bo-766` |

**Known gaps.** **Campaign Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The marketer creates a campaign in stages: objective, audience, offer, channels and content, schedule, review, activation. Each stage validates before the next. The review stage shows how many guests will actually receive it after consent and suppression. Offers come only from the pre-configured offers list; nobody types a discount here.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- CreateCampaignRequest has no objective, success target, owner, brand, products or budget fields, and no offer reference. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The screen's create action is createInvitationCampaign ("Create invitation campaign"). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Draft · Scheduled · Sending · Paused · Completed · Stopped · Failed | `listCampaigns` ?status |

**Form: Create campaign** (modal, opened by *Create campaign*; *Create campaign* calls `createCampaign`, *Cancel* sends nothing)

**Collects what `createCampaign` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCampaign` body |
| Kind `kind` | radio group | required | — | One off · Scheduled · Triggered · Recurring | — | — | `createCampaign` body |
| Channel `channel` | select | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `createCampaign` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCampaign` body |
| Segment `segmentId` | picker: choose a segment | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Content `content` | group | required | — | — | — | — | `createCampaign` body |
| Template `content.templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `createCampaign` body |
| Subject override `content.subjectOverride` | key and value settings | optional | — | — | — | — | `createCampaign` body |
| Merge defaults `content.mergeDefaults` | key and value settings | optional | — | — | — | Fallback values for the template's `mergeFields`, by name, used where a guest has no value. | `createCampaign` body |
| Promotion `content.promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Offer carried by the campaign. Coupon codes are issued from it. | `createCampaign` body |
| Trigger `trigger` | group | optional | — | — | — | — | `createCampaign` body |
| Event `trigger.event` | select | optional | — | Booking confirmed · Visit completed · Membership expiring · Birthday · Abandoned cart · First visit · Inactivity · Entitlement expiring | — | `entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's … | `createCampaign` body |
| Delay hours `trigger.delayHours` | number field (hours) | optional | — | — | — | — | `createCampaign` body |
| Conditions `trigger.conditions` | repeatable rows | optional | — | — | — | — | `createCampaign` body |
| Attribute `trigger.conditions[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createCampaign` body |
| Operator `trigger.conditions[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createCampaign` body |
| Value `trigger.conditions[].value` | field | optional | — | — | — | — | `createCampaign` body |
| Values `trigger.conditions[].values` | list of values (chips) | optional | — | — | — | — | `createCampaign` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCampaign` body |
| Consent purpose `consentPurpose` | select | optional | Marketing | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `createCampaign` body |
| Send window `sendWindow` | group | optional | — | — | — | Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen. | `createCampaign` body |
| Start time `sendWindow.startTime` | text field | optional | — | — | — | — | `createCampaign` body |
| End time `sendWindow.endTime` | text field | optional | — | — | — | — | `createCampaign` body |
| Time zone `sendWindow.timeZone` | text field | optional | — | — | — | — | `createCampaign` body |
| Send time mode `sendTimeMode` | segmented control | optional | Fixed | Fixed · Optimised | — | `optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). | `createCampaign` body |
| Optimise channel `optimiseChannel` | toggle | optional | off | — | — | With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). | `createCampaign` body |
| Variants `variants` | repeatable rows | optional | — | at most 5 | — | A/B (or up to five-way) content and subject variants (29 September, build pass, group G2; 22.1.17, BO-772). | `createCampaign` body |
| Label `variants[].label` | text field | required | — | max length 20 | — | A, B, C... | `createCampaign` body |
| Subject override `variants[].subjectOverride` | key and value settings | optional | — | — | — | Subject line by locale. | `createCampaign` body |
| Template `variants[].templateId` | picker: choose a template | optional | — | — | shows names, sends the id | A different template for this variant; null uses the campaign's `content.templateId`. | `createCampaign` body |
| Split percent `variants[].splitPercent` | stepper or slider | optional | — | min 1; max 100 | — | Share of the test group; null splits evenly. | `createCampaign` body |
| Source `variants[].source` | segmented control | optional | Manual | Manual · AI draft | — | — | `createCampaign` body |
| AI decision record `variants[].aiDecisionRecordId` | text field | optional | — | — | — | The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`. | `createCampaign` body |
| Ab test `abTest` | group | optional | — | Required when `variants` has two or more. | — | How the variants are tested. Required when `variants` has two or more. | `createCampaign` body |
| Test percent `abTest.testPercent` | stepper or slider | optional | 20 | min 5; max 100 | — | Share of the audience the variants are tested on; 100 splits everyone and picks no winner. | `createCampaign` body |
| Success metric `abTest.successMetric` | radio group | optional | Click rate | Open rate · Click rate · Conversion rate · Attributed revenue | — | — | `createCampaign` body |
| Decide after hours `abTest.decideAfterHours` | number field (hours) | optional | 4 | min 1; max 168 | — | — | `createCampaign` body |
| Winner rule `abTest.winnerRule` | segmented control | optional | Automatic | Automatic · Manual | — | — | `createCampaign` body |
| Minimum sample per variant `abTest.minimumSamplePerVariant` | number field | optional | 500 | min 1 | — | Below this many sends per variant no winner is declared automatically; a person picks. | `createCampaign` body |
| Winning variant `abTest.winningVariantId` | picker: choose a winning variant | optional | — | — | shows names, sends the id | Set by the automatic rule, or by a person through `updateCampaign`. | `createCampaign` body |

Errors to draw in the form: 400 Validation failed

**Form: Send test** (modal, opened by *Send test*; *Send test* calls `testSendCampaign`, *Cancel* sends nothing)

**Collects what `testSendCampaign` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recipients `recipients` | list of values (chips) | required | — | at least 1; at most 10 | — | — | `testSendCampaign` body |
| Sample subject `sampleSubjectId` | picker: choose a sample subject | optional | — | — | shows names, sends the id | Personalise using this guest's data. Otherwise placeholders are used. | `testSendCampaign` body |

**Sent by *Launch campaign*** (`launchCampaign`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `launchCampaign` body |
| Confirm audience size `confirmAudienceSize` | number field | optional | — | When supplied and the evaluated size differs beyond tolerance, the launch is refused. | — | Guard against a segment that has grown unexpectedly. When supplied and the evaluated size differs beyond tolerance, the launch is refused. | `launchCampaign` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Objective and success criteria**: Objective (ticket sales, membership, loyalty, wallet, seasonal, retention, capacity, last-minute) and a measurable target, e.g. 80% conversion. *(source: DI-383; screens/P08-venue-back-office.yaml#BO-766)*
- **Kind**: One-off, scheduled, triggered (by an event such as a booking, a visit or a birthday) or recurring. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CampaignKind)*
- **Audience**: One segment (required); the matching and reachable counts from the segment preview are shown on the stage. *(source: contracts/satellite/marketing-crm.yaml#createCampaign; contracts/satellite/marketing-crm.yaml#previewSegment)*
- **Offer**: Picked from pre-configured, system-validated offers (coupon code, dynamic discount or auto-discount link), product-scoped; no free-text discount field exists. *(source: MoM 2026-08-20 4.6)*
- **Consent purpose**: Defaults to marketing; only the purposes the venue configured are offered. *(source: contracts/satellite/marketing-crm.yaml#createCampaign)*
- **Send window**: Start and end hours and time zone (Gulf Standard Time default); nothing promotional sends outside it. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CreateCampaignRequest)*
- **Send time**: Fixed, or optimised per guest inside the window; with optimised, the channel may also be chosen per guest among the channels they consented to. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CreateCampaignRequest)*
- **Variants (A/B)**: Up to 5 variants; with two or more, a test share of 5 to 100% (default 20%) and a success metric. A variant may come from an AI draft that a person edited. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CreateCampaignRequest; contracts/satellite/ai.yaml#proposeMarketingContent)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create campaign (secondary button) | `createCampaign` POST `/campaigns` | CreateCampaignRequest | Campaign | 400 Validation failed | opens modal first |
| Send test (secondary button) | `testSendCampaign` POST `/campaigns/{campaignId}/test-send` | inline | inline | — | opens modal first |
| Launch campaign (secondary button) | `launchCampaign` POST `/campaigns/{campaignId}/launch` | inline | LaunchResult | 403 Authenticated but not permitted at the requested scope; 409 Already launched (`alreadyLaunched`), audience size differs beyond tolerance (`audienceSizeChanged`), or every recipient was excluded … | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Review stage**: Audience matching count, reachable per channel, the exclusions by reason (no consent, suppressed, withdrawn since the segment was built), the offer, schedule, variants, and the approval state. *(source: contracts/satellite/marketing-crm.yaml#launchCampaign)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Send test**: Sends to named staff recipients only, personalised with a sample guest, marked as a test and never counted in performance. *(source: contracts/satellite/marketing-crm.yaml#testSendCampaign)*
- **Launch or schedule**: Consent is checked again at send time. The launch carries the audience size the marketer saw and is refused if the segment has grown unexpectedly, so "Audience changed - review again" is a state. *(source: contracts/satellite/marketing-crm.yaml#launchCampaign)*
- **Draft with AI**: The AI writes drafts of the subject, body and variants for the channel's length limits; a person edits and applies. Nothing is published by AI. *(source: contracts/satellite/ai.yaml#proposeMarketingContent)*

**Data it reads**: `listCampaigns` (onLoad, The library and calendar)

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Already launched (`alreadyLaunched`), audience size differs beyond tolerance (`audienceSizeChanged`), or every recipient was excluded (`noReachableRecipients`). (CampaignStateProblem); 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and … |

#### Edge cases to draw

- **The guest's language has no template body**: Flagged at review ("No Arabic version - 1,204 Arabic-speaking guests"); never silently sent in English. *(source: contracts/satellite/marketing-crm.yaml#createMessageTemplate; DI-019)*
- **Reachable is zero on the chosen channel**: The schedule stage cannot continue; suggest the channels with reach. *(source: contracts/satellite/marketing-crm.yaml#previewSegment)*

#### Consistency with other screens

- Match `BO-767`: The audience and offer stage is the same component as BO-767.
- Match `BO-768`: The channel and content stage is the multichannel composer.
- Match `BO-764`: Campaign statuses (draft, scheduled, sending, paused, completed, stopped, failed) read the same in the command centre.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
campaign: Autumn comeback - annual pass holders
objective: Retention - 15% of lapsed pass holders visit by 30 Nov 2026
segment: Lapsed annual pass holders - no visit in 90 days (matching 4,812; email 2,930; WhatsApp 3,410)
offer: COMEBACK20 - 20% off F&B on next visit (pre-configured)
schedule: Thu 15 Oct 2026, window 10:00-20:00 GST, optimised send time
variants:
- A - "We miss you at Coastal Aqua"
- B - "Your pass misses you too"
```

#### Permissions

- `listCampaigns` → `MARKETING_VIEW` (read) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `createCampaign` → `MARKETING_MANAGE` (configure) · staff
- `testSendCampaign` → `MARKETING_MANAGE` (configure) · staff
- `launchCampaign` → `MARKETING_SEND` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

21 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.1.1 | Campaign Creation | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.4 | Campaign Scheduling | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.12 | Ticketing Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.13 | Membership Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.14 | Loyalty Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| … 9 more | | | | `traceability.json` |

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-766` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-766`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 4: Works in Campaign Builder → Guide authorized users through complete campaign creation. Capture campaign name, objective, brand, venue, owner, products, commercial goal and measurement model. Configuration Scope of Work / …

#### Acceptance for the design

- [ ] Every input above is drawn (44), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-766?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create campaign, Send test, Launch campaign.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`, `MARKETING_SEND`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-767` Audience & Offer Selection

**Connect governed audiences with eligible commercial offers. Select one or more segments, exclusions and suppression lists and show reachable, consent-eligible count by channel. Configure discounts, vouchers, promo codes, bundles, loyalty rewards, wallet bonuses and membership benefits through the Promotion Engine. Validate eligibility, stackability, redemption limits, dates, capacity, ticket inventory and product availability. Estimate exposure, cost, revenue and margin before proceeding. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-767 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/engagement-support/audience-offer-selection-bo-767` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Connect the audience to an eligible offer: segments, exclusions and suppression lists with reachable counts by channel, then an offer from the promotion engine (discount, voucher, promo code, bundle, loyalty reward, wallet bonus, membership benefit). Offers are only pre-configured, validated offers; no ad-hoc discount values.

**Known correction pending (do not draw the wrong version)**

- **CreateCampaignRequest has no offer reference.** Why: The stage selects an offer that the campaign cannot store (see BO-766). *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CreateCampaignRequest; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Offer**: Picked from the Offers module (coupon code, dynamic discount, auto-discount link), scoped to products or ticket types; eligibility, stackability, redemption limits, dates and inventory validated on selection. *(source: DI-385; MoM 2026-08-20 4.6)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create campaign (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Exposure estimate**: Reachable guests times expected redemption, with the offer's limits. *(source: screens/P08-venue-back-office.yaml#BO-767)*

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience offer selection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience offer selection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience offer selection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience offer selection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `content` amended on a campaign that is no longer in `draft` (`statusDoesNotPermit`). (CampaignStateProblem) |

#### Consistency with other screens

- Match `BO-766`: This is the builder's audience-and-offer stage.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
audience: Gold members (1,240) minus Complained in last 30 days (32)
offer: GOLD-FNB15 - 15% off F&B - max 1 per guest - valid to 31 Dec 2026
```

#### Permissions

- `createCampaign` → `MARKETING_MANAGE` (configure) · staff
- `updateCampaign` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.1 | Campaign Creation | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.4 | Campaign Scheduling | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.12 | Ticketing Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.13 | Membership Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.1.14 | Loyalty Campaigns | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.4.8 | Product & Event Integration | Marketing & CRM | CONTRACTED | `createCampaign` |
| 22.9.14 | Marketing Notifications | Marketing & CRM | CONTRACTED | `createCampaign` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: offer blocks in the Visual Journey Builder pick only from pre-configured, system-validated offers (product/ticket-type scoped, from the Offers module: coupon code, dynamic discount or auto-discount URL); ad-hoc discount values cannot be typed in the builder. *(agreed · MoM 20 Aug 2026, 4.6 Marketing Automation; 5. Key Decisions · DI-385)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-767` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-767`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 6: Works in Audience & Offer Selection → Connect governed audiences with eligible commercial offers. Select one or more segments, exclusions and suppression lists and show reachable, consent-eligible count by channel. Configure discounts …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-767?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create campaign, Cancel.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-768` Multichannel Composer

**Create personalized content for every selected communication channel. Provide channel-specific email, SMS, WhatsApp, push, in-app and website-banner editors and previews. Insert approved personalization tokens, products, events, tickets, QR codes, vouchers, payment links and media assets. Support brand and language variants, accessibility checks, link validation and character/channel constraints. Maintain common campaign intent while allowing controlled channel variations and version history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-768 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/engagement-support/multichannel-composer-bo-768` |

**Known gaps.** **Multichannel Composer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Content for every selected channel: email, SMS, WhatsApp, push, in-app, web banner, each with its own editor and preview, approved personalisation tokens, and language variants (English and Arabic right-to-left). The campaign intent stays common while each channel respects its limits.

**Fixed on main** (the package already carries these; draw what it says): listSegments is declared on the composer, but no template read (listMessageTemplates) is. (CHG-WIR-005).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listMessageTemplates` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Channel editors**: SMS shows segment count; WhatsApp needs the approved provider template; push shows the truncation; email has subject per language. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/MessageTemplate; DI-019)*
- **Tokens**: From a picker (guest first name, booking, voucher code, payment link); a missing value has a fallback. *(source: screens/P08-venue-back-office.yaml#BO-768)*

#### Outputs: what the screen shows and produces

**Shown**

**Templates** (data table, from `listMessageTemplates`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Subjects | grouped details | Per language. Email only. |
| Bodies | grouped details | Per language, keyed by ISO 639-1 code. |
| Merge fields | list or chips (count when long) | — |
| Missing languages | list or chips (count when long) | Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect. |
| Provider template | text | Required for WhatsApp, where templates are pre-approved by the provider. |
| Brand | the name it points at, never the id | The brand whose identity the template carries; null for the tenant default. |
| Ownership | chip: Platform, Crm | `platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save campaign (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Unsubscribe and identity**: Every marketing message carries the unsubscribe link and the brand's sender identity; a transactional template cannot be chosen for a marketing campaign. *(source: contracts/satellite/marketing-crm.yaml#setMarketingSubscription; DI-560)*

**Data it reads**: `listMessageTemplates` (onLoad, Start from a template)

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multichannel composer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multichannel composer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multichannel composer yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multichannel composer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `content` amended on a campaign that is no longer in `draft` (`statusDoesNotPermit`). (CampaignStateProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
email:
  subjectEn: Your pass misses you too
  subjectAr: تذكرتك تشتاق إليك
sms: Coastal Aqua - 20% off food on your next visit with COMEBACK20. Stop? Reply STOP
```

#### Permissions

- `updateCampaign` → `MARKETING_MANAGE` (configure) · staff
- `listMessageTemplates` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.3 | The system should support email templates for e-ticket purchase confirmation supporting dynamic parameters. The email templates should be configurable per site, per event | Ticketing Sales | CONTRACTED | `listMessageTemplates` |
| 2.6.26 | It is expected that confirmation email can be generated including the number of tickets, the cost, the order number. | Ticketing Sales | CONTRACTED | `listMessageTemplates` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-768` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-768`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 8: Works in Multichannel Composer → Create personalized content for every selected communication channel. Provide channel-specific email, SMS, WhatsApp, push, in-app and website-banner editors and previews. Insert approved …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-768?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save campaign, Cancel.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-769` Schedule & Trigger Rules

**Configure when and under what conditions a campaign executes. Support immediate, scheduled, recurring, event-triggered and API/webhook execution. Configure timezone, send windows, blackout dates, frequency caps, re-entry, expiry and audience refresh timing. Map events such as purchase, expiry, birthday, milestone, top-up, first visit and abandoned cart. Provide schedule summary, conflict detection and pre-flight audience/inventory revalidation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 22**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-769 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/engagement-support/schedule-trigger-rules-bo-769` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** When and under what conditions a campaign runs: immediately, scheduled, recurring, event-triggered or by webhook; time zone, send window, blackout dates, frequency caps, re-entry, expiry, audience refresh timing. Events such as purchase, expiry, birthday, milestone, top-up, first visit and abandoned cart.

**Known correction pending (do not draw the wrong version)**

- **updateCampaign accepts only name, isPaused, scheduledFor and content.** Why: Trigger, send window, caps and blackout cannot be edited after creation; the scheduling screen has no write for most of its fields. *(source: contracts/satellite/marketing-crm.yaml#updateCampaign; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Channel | select | — | Email · SMS · Whatsapp · Push · In app · Post | `listMessageTemplates` ?channel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Trigger event**: From the event catalogue with its precise state (ticket scanned, not just sold). *(source: DI-561; contracts/satellite/marketing-crm.yaml#/components/schemas/CampaignTrigger)*
- **Send window and blackout**: Hours and dates nothing promotional sends (e.g. national days set by the venue). *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/CreateCampaignRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save campaign (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Schedule summary**: Plain-language summary ("Every Thursday 10:00 GST to Gold members, max 1 a week") with conflicts listed. *(source: screens/P08-venue-back-office.yaml#BO-769)*

**Data it reads**: `listMessageTemplates` (onLoad, Compose across channels)

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The schedule trigger rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the schedule trigger rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No schedule trigger rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the schedule trigger rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `content` amended on a campaign that is no longer in `draft` (`statusDoesNotPermit`). (CampaignStateProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trigger: Birthday - 7 days before - 10:00 GST - once a year
```

#### Permissions

- `listMessageTemplates` → `MARKETING_VIEW` (read) · staff
- `updateCampaign` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.3 | The system should support email templates for e-ticket purchase confirmation supporting dynamic parameters. The email templates should be configurable per site, per event | Ticketing Sales | CONTRACTED | `listMessageTemplates` |
| 2.6.26 | It is expected that confirmation email can be generated including the number of tickets, the cost, the order number. | Ticketing Sales | CONTRACTED | `listMessageTemplates` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-769` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-769`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 10: Works in Schedule & Trigger Rules → Configure when and under what conditions a campaign executes. Support immediate, scheduled, recurring, event-triggered and API/webhook execution. Configure timezone, send windows, blackout dates …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-769?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save campaign, Cancel.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-770` Campaign Approval Workflow

**Enforce configurable review and publishing governance. Support creator, reviewer, approver and publisher stages with role, department, threshold and business-unit rules. Route content, offer, budget, legal, brand and data-privacy approvals independently where required. Capture comments, requested changes, resubmission, delegation, escalation and segregation-of- duties checks. Lock the approved version and audit every decision and subsequent change. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block C · task VM-BO-770 |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/campaign-approval-workflow-bo-770` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the campaign approval workflow that approveCampaignWorkflow writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Multi-level approval for promotions and campaigns by threshold (discount, budget, margin, free-product value, duration), sequential or parallel, with delegation and escalation.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Thresholds and approval modes are strings (campaignBudget, financialExposure, sequentialApproval). (CHG-SBO-005)
- No read operation: the screen declares only approveCampaignWorkflow and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **thresholds and stages**: Threshold rows routing to stages. *(source: contracts/satellite/promotions.yaml#approveCampaignWorkflow)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve campaign workflow (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The campaign approval workflow list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the campaign approval workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No campaign approval workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the campaign approval workflow are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  when: discount over 30% or budget over AED 100,000
  route:
  - Marketing director
  - CFO
```

#### Permissions

- `approveCampaignWorkflow` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-770` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-770`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 12: Works in Campaign Approval Workflow → Enforce configurable review and publishing governance. Support creator, reviewer, approver and publisher stages with role, department, threshold and business-unit rules. Route content, offer, budget …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-770?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve campaign workflow, Cancel.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-771` Budget, Goals & Forecast

**Plan campaign investment and expected commercial results. Capture total and channel budgets, expected revenue, conversion, CPA, margin, break-even and strategic goals. Estimate provider cost, offer cost, reward liability and capacity implications by channel and audience. Compare forecast, actual and committed spend and flag variance or overspend risk. Support approval thresholds, finance integration and controlled adjustment with reason and audit. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-BO-771 |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `MARKETING_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/engagement-support/budget-goals-forecast-bo-771` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Campaign budget, goals and forecast, sent for approval before the campaign runs.

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

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The budget goals forecast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the budget goals forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No budget goals forecast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the budget goals forecast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. (ApprovalStateProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds MARKETING_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_REQUEST for createApprovalRequest. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#createApprovalRequest)*
- **createApprovalRequest answers 409**: Show it as something the person can act on, not a failure: An open request already exists for this subject. Two approvals for one refund is how a refund gets paid twice. `refusedReason` is `openRequestExists` and `requestId` names the open request, so the caller can point at it rather than raise another. A draft is not an open request. *(source: contracts/spine/approvals.yaml#createApprovalRequest)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getCampaign (CampaignDetail):
- name: Refund above AED 500 - Abu Dhabi
  kind: standard
  scheduledFor: 31/12/2026 23:59
  sendTimeMode: fixed
- name: Group discount approval
  kind: standard
  scheduledFor: 15/10/2026 00:00
  sendTimeMode: optimised
```

#### Permissions

- `createApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `getCampaign` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.59 | Complimentary entitlement redemption | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.64 | Employees shall submit requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 1.2.65 | Managers shall approve requests from mobile app. | Ticketing Catalogue | CONTRACTED | `createApprovalRequest` |
| 11.1.51 | Draft Approval Requests - System shall support saving approval requests in draft status. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 11.1.63 | API-Based Approval Processing - System shall expose approval workflows through APIs. | Approval Workflows & Governance | CONTRACTED | `createApprovalRequest` |
| 22.1.20 | Campaign Audit Trail | Marketing & CRM | CONTRACTED | `getCampaign` |
| 22.4.20 | Newsletter Audit Trail | Marketing & CRM | CONTRACTED | `getCampaign` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Campaign tracking shows click-through, conversion and revenue attribution per campaign, with configurable success criteria (e.g. 80% conversion target). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-383)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-771` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-771`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 14: Works in Budget, Goals & Forecast → Plan campaign investment and expected commercial results. Capture total and channel budgets, expected revenue, conversion, CPA, margin, break-even and strategic goals. Estimate provider cost, offer …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-771?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create approval request, Cancel.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-772` A/B & AI Optimization

**Test campaign alternatives and apply AI recommendations safely. Configure A/B or multivariate variants for subject, content, creative, offer, channel and send time. Define audience split, sample size, duration, success metric, statistical confidence and winner rule. Show AI recommendations, expected uplift, confidence, factors and constraints and require human approval. Prevent conflicting tests and preserve assignments, results, model/version and decisions for audit. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-BO-772 |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `campaignId` (navigation), `insightId` (navigation) |
| Route | `/engagement-support/a-b-ai-optimization-bo-772` |

**What the spec says about it.** **Guests who checked out without an account receive marketing only if they ticked the checkout opt-in (unticked by default, source checkout); nothing is sent without it (decided 2 October 2026 by Chinmay, DEC-275; CHG-CSA-025).** Replaces "not targeted until the consent question is answered".

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** A/B and AI optimisation for campaigns: variants for subject, content, creative, offer, channel and send time; split, sample size, duration, success metric and winner rule; AI recommendations and drafted variants. Day one uses rule playbooks and a typical send hour per channel; send time per guest after three touches. The one thing to get right: AI drafts and recommends; applying a winner or a change is a person's action (campaigns L2).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May guests who checked out without an account receive marketing?** → Guests who checked out without an account receive marketing only if they ticked the checkout opt-in (unticked by default, source checkout); nothing is sent without it. Replaces the drawn 'not targeted until the consent question is answered'. *(decided by Chinmay, 2026-10-02; DEC-275 / CHG-NOTE-001)*

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

**Detail panel** (detail panel): One record, read-only.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **recommendations**: Recommendation, expected uplift as a range, evidence, stage and Based on; accept applies through updateCampaign by a person. *(source: contracts/satellite/ai.yaml#listMarketingRecommendations / ADR-0050 / ADR-0051 (AI functions review 30 Sep §4 Marketing))*

**Data it reads**: `listMarketingRecommendations` (onLoad, AI recommendations on this campaign or journey, with …)

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The optimization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the optimization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No optimization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the optimization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and …; 409 The move is not allowed from the insight's state.; 409 `content` amended on a campaign that is no longer in `draft` (`statusDoesNotPermit`). (CampaignStateProblem); 422 A setting the answer cannot do without is missing (29 … |

#### Edge cases to draw

- **A guest who checked out without an account**: Targeted only if they ticked the checkout opt-in (unticked by default, recorded with source checkout); nothing is sent without it. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-001))*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recommendation:
  text: Send the Eid offer at 19:00 instead of 10:00
  uplift: +2 to +5 pts open rate
  basedOn: typical evening hour for email in UAE; 4 weeks of your sends
  stage: Learning
```

#### Permissions

- `getCampaignPerformance` → `MARKETING_VIEW` (read) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `listMarketingRecommendations` → `AI_USE` (operate) · staff
- `decideAiInsight` → `AI_USE` (operate) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest
- `updateCampaign` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

26 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.4.15 | Open & Click Tracking | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.4.16 | Conversion Tracking | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.4.17 | Revenue Attribution | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.4.18 | Newsletter Analytics Dashboard | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.14.16 | Attribution Framework | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.14.19 | Campaign Revenue Attribution | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| … 14 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-772` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-772`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 16: Works in A/B & AI Optimization → Test campaign alternatives and apply AI recommendations safely. Configure A/B or multivariate variants for subject, content, creative, offer, channel and send time. Define audience split, sample …
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-772?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-773` Attribution & Audit

**Measure influenced outcomes and preserve a complete campaign record. Provide first, last, linear, position-based and configurable multi-touch attribution across channels. Attribute ticket, membership, loyalty, wallet, reservation and other revenue using defined windows and identity rules. Display delivery funnel, conversion, revenue, ROI, profitability, channel contribution and unattributed outcomes. Record creation, edits, approvals, execution, pauses, variants, results, exports and user/AI actions. Configuration Scope of Work / Version 1.0 23 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 24 Board 5 - Marketing Automation & Customer Journeys Figure 5. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 25**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-773 |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `campaignId` (navigation) |
| Route | `/engagement-support/attribution-audit-bo-773` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): recordTouchPoint is a service-audience operation (touches are recorded by services), not a staff action (design-notes correction customer-marketing BO-773).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** What campaigns influenced and the full record of each campaign. Attribution across channels with defined windows; the venue's attribution window is a venue setting (proposed 7 days). Delivery funnel, conversion, revenue, unattributed outcomes, and an audit of every creation, edit, approval and send.

**Fixed on main** (the package already carries these; draw what it says): recordTouchPoint (service audience) is declared on this staff screen. (CHG-WIR-005).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What attribution window does the client want (default proposed 7 days)?** → Drawn default accepted: 7 days, shown on every revenue figure. *(decided by Chinmay, 2026-10-02; DEC-280 / CHG-NOTE-002)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Funnel**: Sent, delivered, opened, clicked, bounced, complained, unsubscribed, attributed orders and revenue, with the window shown ("attributed over 7 days"). *(source: contracts/satellite/marketing-crm.yaml#getCampaignPerformance; R094)*
- **Model choice**: First, last, linear or position-based is a view over recorded touches; the platform records touches and does not pick a model. *(source: contracts/satellite/marketing-crm.yaml#recordTouchPoint)*

**Where the user goes next**

- → `BO-764` Campaign Command Center: *Back to Campaign Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attribution audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attribution audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attribution audit yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attribution audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
performance:
  sent: 8240
  delivered: 8102
  opened: 4410
  clicked: 1210
  orders: 255
  revenue: AED 42
  600.0: null
  window: 7 days
```

#### Permissions

- `getCampaignPerformance` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.4.15 | Open & Click Tracking | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.4.16 | Conversion Tracking | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.4.17 | Revenue Attribution | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.4.18 | Newsletter Analytics Dashboard | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.14.16 | Attribution Framework | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |
| 22.14.19 | Campaign Revenue Attribution | Marketing & CRM | CONTRACTED | `getCampaignPerformance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Campaign tracking shows click-through, conversion and revenue attribution per campaign, with configurable success criteria (e.g. 80% conversion target). *(client request · MoM 20 Aug 2026, 4.6 Marketing Automation — Campaigns, Offers & Visual Journey Builder · DI-383)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-773` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS73 Marketing CRM Configuration Reference v1.0 Board 4.dc.html#bo-773`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 4
- Flow F247 *Marketing CRM Configuration Reference v1.0 board 4: Campaign Command Center*, step 18: Works in Attribution & Audit → Measure influenced outcomes and preserve a complete campaign record. Provide first, last, linear, position-based and configurable multi-touch attribution across channels. Attribute ticket …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-773?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-764`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveCampaignWorkflow": {"method":"PUT","path":"/campaign-workflow","contract":"promotions","summary":"Campaign Approval Workflow Designer","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CampaignApprovalWorkflowDesignerInput","responds":"CampaignApprovalWorkflowDesignerView"},
"createApprovalRequest": {"method":"POST","path":"/approval-requests","contract":"approvals","summary":"Raise a request","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateApprovalRequest","responds":"ApprovalRequest"},
"createCampaign": {"method":"POST","path":"/campaigns","contract":"marketing-crm","summary":"Create a campaign","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCampaignRequest","responds":"Campaign"},
"decideAiInsight": {"method":"POST","path":"/insights/{insightId}/decide","contract":"ai","summary":"Review, accept, reject or mark an insight actioned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiInsight"},
"getCampaign": {"method":"GET","path":"/campaigns/{campaignId}","contract":"marketing-crm","summary":"Read a campaign with performance","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CampaignDetail"},
"getCampaignPerformance": {"method":"GET","path":"/campaigns/{campaignId}/performance","contract":"marketing-crm","summary":"Delivery and engagement","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CampaignPerformance"},
"launchCampaign": {"method":"POST","path":"/campaigns/{campaignId}/launch","contract":"marketing-crm","summary":"Launch or schedule a campaign","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listCampaignCalendarTimeline": {"method":"GET","path":"/campaign-calendar-timeline","contract":"promotions","summary":"Campaign Calendar & Timeline","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"attraction","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"promotionFamily","in":"query","required":false},{"name":"view","in":"query","required":false}],"requestBody":null,"responds":"CampaignCalendarTimelineView"},
"listCampaigns": {"method":"GET","path":"/campaigns","contract":"marketing-crm","summary":"List campaigns","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMarketingRecommendations": {"method":"GET","path":"/marketing-recommendations","contract":"ai","summary":"Recommendations on marketing campaigns and journeys","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"targetKind","in":"query","required":true},{"name":"targetRef","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMessageTemplates": {"method":"GET","path":"/message-templates","contract":"marketing-crm","summary":"List message templates","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"proposeMarketingContent": {"method":"POST","path":"/ai/content-drafts","contract":"ai","summary":"Draft marketing content for a person to edit and apply","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"testSendCampaign": {"method":"POST","path":"/campaigns/{campaignId}/test-send","contract":"marketing-crm","summary":"Send a test to named recipients","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateCampaign": {"method":"PATCH","path":"/campaigns/{campaignId}","contract":"marketing-crm","summary":"Amend, pause or resume a campaign","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Campaign"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMarketingRecommendation": {"type":"object","x-ticvai-persistence":"none — read from ai.insight (kind marketingRecommendation)","description":"One recommendation on a campaign or journey (22.1.16, 22.3.17), decided through `decideAiInsight` and applied by a person in marketing-crm.","required":["insightId","targetKind","targetRef","recommendation","status"],"properties":{"insightId":{"type":"string","format":"uuid","description":"The `ai.insight` row; `decideAiInsight` takes it."},"targetKind":{"type":"string","enum":["campaign","journey"]},"targetRef":{"type":"string"},"recommendation":{"type":"string","enum":["changeSegment","changeChannel","changeTiming","changeOffer","changeContent","addStep","removeStep","reorderSteps","startJourneyFromTemplate"]},"parameters":{"type":"object","additionalProperties":true,"nullable":true,"description":"What to change to, e.g. the channel, the send hour, the step to drop."},"expectedImpact":{"type":"object","nullable":true,"properties":{"metric":{"type":"string"},"low":{"type":"number"},"high":{"type":"number"}},"description":"A range on the named metric (conversion, open rate, revenue), never a single number (design 5.6)."},"rationale":{"type":"string"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"priority":{"type":"string","enum":["low","medium","high","critical"]},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"]},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"detectedAt":{"type":"string","format":"date-time"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"Campaign": {"x-ticvai-persistence":"marketing.campaign","allOf":[{"$ref":"#/components/schemas/CreateCampaignRequest"},{"type":"object","required":["id","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetSpent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"},"status":{"$ref":"#/components/schemas/CampaignStatus"},"isPaused":{"type":"boolean"},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"launchedAt":{"type":"string","format":"date-time","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"sentCount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"**How many messages went out**, counted from `marketing.message_dispatch` at read time rather than kept as a counter on the campaign row, so it cannot drift from the dispatch records it summarises. Test sends are not dispatches of the campaign and are not counted.\n"}}}]},
"CampaignApprovalWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is promotions.coupon_campaign at 6%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Campaign Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"discount":{"type":"number","description":"Discount %"},"campaignBudget":{"type":"string","description":"Campaign budget"},"margin":{"type":"number","description":"Margin"},"promotionType":{"type":"string","description":"Promotion type"},"venue":{"type":"string","description":"Venue"},"partner":{"type":"string","description":"Partner"},"channel":{"type":"string","description":"Channel"},"freeProductValue":{"type":"string","description":"Free-product value"},"campaignDuration":{"type":"string","format":"date-time","description":"Campaign duration"},"financialExposure":{"type":"string","description":"Financial exposure"},"sequentialApproval":{"type":"string","description":"Sequential approval"},"parallelApproval":{"type":"string","description":"Parallel approval"},"conditionalApproval":{"type":"string","description":"Conditional approval"},"mandatoryApproval":{"type":"string","description":"Mandatory approval"},"optionalReview":{"type":"string","description":"Optional review"},"delegation":{"type":"string","description":"Delegation"},"escalation":{"type":"string","description":"Escalation"}}},
"CampaignApprovalWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"discount":{"type":"number","description":"Discount %"},"campaignBudget":{"type":"string","description":"Campaign budget"},"margin":{"type":"number","description":"Margin"},"promotionType":{"type":"string","description":"Promotion type"},"venue":{"type":"string","description":"Venue"},"partner":{"type":"string","description":"Partner"},"channel":{"type":"string","description":"Channel"},"freeProductValue":{"type":"string","description":"Free-product value"},"campaignDuration":{"type":"string","format":"date-time","description":"Campaign duration"},"financialExposure":{"type":"string","description":"Financial exposure"},"sequentialApproval":{"type":"string","description":"Sequential approval"},"parallelApproval":{"type":"string","description":"Parallel approval"},"conditionalApproval":{"type":"string","description":"Conditional approval"},"mandatoryApproval":{"type":"string","description":"Mandatory approval"},"optionalReview":{"type":"string","description":"Optional review"},"delegation":{"type":"string","description":"Delegation"},"escalation":{"type":"string","description":"Escalation"}}},
"CampaignCalendarTimelineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Campaign Calendar & Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"calendarState":{"type":"string","enum":["active","upcoming","endingSoon","expired","pendingApproval","conflicting","suspended"],"description":"How the calendar marks this promotion."},"promotionId":{"type":"string","description":"Promotion ID"},"promotionName":{"type":"string","description":"Promotion Name"},"startDate":{"type":"string","format":"date-time","description":"Start Date"},"endDate":{"type":"string","format":"date-time","description":"End Date"},"venue":{"type":"string","description":"Venue"},"channel":{"type":"string","description":"Channel"}}},
"CampaignContent": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","required":["templateId"],"properties":{"templateId":{"type":"string","format":"uuid"},"subjectOverride":{"type":"object","additionalProperties":{"type":"string"}},"mergeDefaults":{"type":"object","description":"Fallback values for the template's `mergeFields`, by name, used where a guest has no value.","additionalProperties":{"type":"string"}},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"Offer carried by the campaign. Coupon codes are issued from it."}}},
"CampaignDetail": {"x-ticvai-persistence":"marketing.campaign","allOf":[{"$ref":"#/components/schemas/Campaign"},{"type":"object","properties":{"performance":{"$ref":"#/components/schemas/CampaignPerformance"}}}]},
"CampaignKind": {"type":"string","enum":["oneOff","scheduled","triggered","recurring"]},
"CampaignPerformance": {"x-ticvai-persistence":"none — aggregated from marketing.message_dispatch (isTest false)","type":"object","required":["campaignId","sent","delivered"],"properties":{"campaignId":{"type":"string","format":"uuid"},"sent":{"type":"integer"},"delivered":{"type":"integer"},"opened":{"type":"integer"},"clicked":{"type":"integer"},"bounced":{"type":"integer"},"complained":{"type":"integer"},"unsubscribed":{"type":"integer"},"attributedOrders":{"type":"integer"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributionWindowDays":{"type":"integer","minimum":1,"description":"The window these figures were attributed over, from `VenueSettings.marketing.attributionWindowDays` (proposed default 7, audit R094)."},"variants":{"type":"array","description":"Per variant of an A/B campaign, from `MessageDispatch.campaignVariantId` (29 September, build pass, group G2; 22.1.17). Empty for a single-content campaign.","items":{"type":"object","properties":{"variantId":{"type":"string","format":"uuid"},"label":{"type":"string"},"sent":{"type":"integer"},"opened":{"type":"integer"},"clicked":{"type":"integer"},"attributedOrders":{"type":"integer"},"attributedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isWinner":{"type":"boolean"}}}},"sendTimeOptimisedCount":{"type":"integer","description":"Messages sent at a per-recipient optimised hour rather than the scheduled time."}}},
"CampaignStatus": {"type":"string","enum":["draft","scheduled","sending","paused","completed","stopped","failed"]},
"CampaignTrigger": {"x-ticvai-persistence":"none — embedded in campaign","type":"object","properties":{"event":{"type":"string","enum":["bookingConfirmed","visitCompleted","membershipExpiring","birthday","abandonedCart","firstVisit","inactivity","entitlementExpiring"],"description":"`entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's `expiryNoticeDays` of `validTo`. The notice period is set on the template, so `delayHours` shifts the send within it rather than setting it. An entitlement belonging to a membership is left to `membershipExpiring`, so a member is not told twice."},"delayHours":{"type":"integer"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/SegmentCriterion"}}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"CreateApprovalRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","kind","subjectContract","subjectType","subjectId","scopePath","summary"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"subjectContract":{"type":"string","description":"Which contract owns the thing being approved."},"subjectType":{"type":"string"},"subjectId":{"type":"string","description":"**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"},"scopePath":{"type":"string"},"summary":{"type":"string","maxLength":300,"description":"What the approver sees in their queue before opening it."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"attributes":{"type":"object","additionalProperties":true},"justification":{"type":"string","maxLength":1000},"isDraft":{"type":"boolean","default":false,"description":"True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"}}},
"CreateCampaignRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","kind","channel","segmentId","content"],"properties":{"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/CampaignKind"},"channel":{"$ref":"#/components/schemas/MessageChannel"},"venueId":{"type":"string","format":"uuid"},"segmentId":{"type":"string","format":"uuid"},"content":{"$ref":"#/components/schemas/CampaignContent"},"trigger":{"$ref":"#/components/schemas/CampaignTrigger"},"scheduledFor":{"type":"string","format":"date-time"},"consentPurpose":{"allOf":[{"$ref":"#/components/schemas/ConsentPurpose"}],"default":"marketing"},"sendWindow":{"type":"object","description":"Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n","properties":{"startTime":{"type":"string"},"endTime":{"type":"string"},"timeZone":{"type":"string"}}},"sendTimeMode":{"type":"string","enum":["fixed","optimised"],"default":"fixed","description":"`optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). `fixed` is the behaviour before. Falls back to `scheduledFor` per recipient where there is no suggestion or AI is off."},"optimiseChannel":{"type":"boolean","default":false,"description":"With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). Off keeps `channel`."},"variants":{"type":"array","maxItems":5,"nullable":true,"description":"**A/B (or up to five-way) content and subject variants** (29 September, build pass, group G2; 22.1.17, BO-772). Each is a subject override and optionally a different template, written by a person or taken from an AI draft (`ai.proposeMarketingContent`, `source` `aiDraft`). Held as rows of `marketing.campaign_variant`. Null or empty is a single-content campaign.","items":{"$ref":"#/components/schemas/MarketingCampaignVariant"}},"abTest":{"type":"object","nullable":true,"description":"How the variants are tested. Required when `variants` has two or more.","properties":{"testPercent":{"type":"integer","minimum":5,"maximum":100,"default":20,"description":"Share of the audience the variants are tested on; 100 splits everyone and picks no winner."},"successMetric":{"type":"string","enum":["openRate","clickRate","conversionRate","attributedRevenue"],"default":"clickRate"},"decideAfterHours":{"type":"integer","minimum":1,"maximum":168,"default":4},"winnerRule":{"type":"string","enum":["automatic","manual"],"default":"automatic"},"minimumSamplePerVariant":{"type":"integer","minimum":1,"default":500,"description":"Below this many sends per variant no winner is declared automatically; a person picks."},"winningVariantId":{"type":"string","format":"uuid","nullable":true,"description":"Set by the automatic rule, or by a person through `updateCampaign`."}}}}},
"MarketingCampaignVariant": {"type":"object","x-ticvai-persistence":"marketing.campaign_variant","description":"One content or subject variant of a campaign, for an A/B test (22.1.17; 29 September, build pass, group G2, from group G1's handoff). Written with its campaign by `createCampaign` and `updateCampaign`.","required":["label"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"campaignId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"marketing.campaign"},"label":{"type":"string","maxLength":20,"description":"A, B, C..."},"subjectOverride":{"type":"object","nullable":true,"description":"Subject line by locale.","additionalProperties":{"type":"string"}},"templateId":{"type":"string","format":"uuid","nullable":true,"description":"A different template for this variant; null uses the campaign's `content.templateId`."},"splitPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Share of the test group; null splits evenly."},"source":{"type":"string","enum":["manual","aiDraft"],"default":"manual"},"aiDecisionRecordId":{"type":"string","nullable":true,"description":"The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`."},"isWinner":{"type":"boolean","default":false,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), the campaign's."}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MessageTemplate": {"x-ticvai-persistence":"marketing.message_template","type":"object","required":["id","code","name","channel","bodies"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"channel":{"$ref":"#/components/schemas/MessageChannel"},"subjects":{"type":"object","description":"Per language. Email only.","additionalProperties":{"type":"string"}},"bodies":{"type":"object","description":"Per language, keyed by ISO 639-1 code.","additionalProperties":{"type":"string"}},"mergeFields":{"type":"array","items":{"type":"string"}},"missingLanguages":{"type":"array","readOnly":true,"description":"Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect.\n","items":{"type":"string"}},"providerTemplateId":{"type":"string","nullable":true,"description":"Required for WhatsApp, where templates are pre-approved by the provider."},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand whose identity the template carries; null for the tenant default."},"ownership":{"type":"string","enum":["platform","crm"],"default":"crm","description":"`platform` = a transactional template owned by the communication service; `crm` = a marketing template owned by CRM (`listSystemTransactionalTemplate`). Content by language and version is in `MessageTemplateVersion`. (decided 29 September, data model for the agreed operations)"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]}
}
```
