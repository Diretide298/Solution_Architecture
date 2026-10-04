# P01-membership-loyalty-value-01 — P01 · Membership, Loyalty & Value

**5 screens · 52 operations · 70 schemas · 14 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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
  `AI_USE, GUEST_MANAGE, GUEST_VIEW, GUEST_VIEW_PII, LOYALTY_REDEEM, MARKETING_MANAGE, MARKETING_VIEW, ORDER_CREATE, ORDER_VIEW, PAYMENT_VIEW, PRICE_VIEW, PRODUCT_VIEW`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
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

### Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale)

A guest finds something to do, picks when and how many, holds capacity, pays, and receives a ticket they can show at the gate, transfer or resell. The same booking engine serves the guest website (P01, WEB-), the guest app (P02, GST-) and, through the same catalogue, cart and order operations, the kiosk (P05), the cashier at the till (P04) and the staff handheld (P06); partners book on credit through the partner portal (P10). Guest surfaces are white-label (venue logo, colours, fonts, card layouts, step indicator style, cart placement) with "Powered by TICVAI" kept; the till and handheld stay TICVAI-branded. The booking runs in a fixed order that the client set on 29 September and confirmed on 30 September: for a dated product, the date first, then the time (hidden until a date), then the tickets (hidden until a time); undated products go straight to the tickets; product-first flows (workshops) pick the product, then the date; seated events with one performance open on the seat map, sections first, zoom into a section, pinch out to compare. Choosing a date, time or session commits nothing; capacity is held only when a quantity is set (a 15-minute basket window, 8 minutes for seats and cabanas, one extension). The guest counters (adult, child, senior, infant, person of determination) belong to the chosen ticket and take its prices, so a basket line is "<ticket> · <guest type> × <n>"; group and school products start from group ticket cards and a typed headcount (minus, plus, and +10 on the app), supervisors free. Help me choose filters the catalogue on the server (never a consent step) with Show everything; consent questions such as "Are you able to swim?" are asked once after the session is picked and never again where the page already asked. Sign-in or the six-digit guest code is asked when the guest leaves Add-ons (or at payment, per venue), only the fields the venue configured; after the code, only the T&Cs tick remains (W1). Payment creates the order first and treats an unknown outcome as "checking with your bank", never a second charge; tickets issue on payment, go to Apple or Google Wallet, and a dynamic-QR event's ticket lives in the app. The guest app is deliberately not a copy of the website (30 September): its structure is Home, Explore, Plan and Tickets tabs with a persistent Buy tickets button, item pages that propose the right product (a restaurant's meal combo that includes admission), ride videos that play with no loader, a visit planner that plans each day at one park from that park's rides, dining and shops only, and in-park walking navigation; the booking flow inside it is functionally identical to the web. Vocabulary in guest copy follows the glossary's recorded exceptions (Booking, Session, QR). source: [F01, F02, F03, F07, F49, F52, F55, F57, F58, F59, MoM 29 Sep 1 (W1-W12), MoM 29 Sep 2, MoM 29 Sep 3, MoM 30 Sep 4.4-4.8, CLIENT-RESPONSE-30SEP 1-6, CLIENT-RESPONSE-REV3-25SEP, REV3-1, REV3-2, REV3-3, REV3-4, REV3-26, DI-1086 …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Booking | An order or reservation as the guest reads it (Booking Confirmation, Group Booking, My bookings). Code says Order or Reservation. | Order (in guest copy), Purchase record, Transaction | docs/glossary.md (Recorded exceptions, Booking, audit R145) |
| Session | A dated, timed performance as the guest reads it (Pick a session, Surf sessions). Staff screens (POS, back office) keep Performance. | Slot, Showtime, Performance (in guest copy) | docs/glossary.md (Recorded exceptions, Session, rev 3 CFG-10); DI-1064 |
| Basket | The guest's unpaid selection with its held capacity (Add to basket, Your basket). Never a paid order. The till and staff screens say Cart. | Cart (in guest copy), Bag, Order (for an unpaid selection) | CLIENT-RESPONSE-REV3-25SEP (Basket, 10) … |
| Ticket | The issued instrument a guest shows at the gate. Product names from the catalogue keep their own words (Day Pass, Annual pass, 2 park ticket); the interface around them says ticket. | Admission, Voucher (for a ticket), Pass (in interface copy) | docs/glossary.md (Ticket) |
| Adult, Child, Senior, Infant, Person of determination | The guest types of a ticket, each with its age or height band shown under it (Child 3-12, Under 1.20 m). A companion of a person of determination is its own free type where the product has one. | Disabled, Handicapped, Kid, Pax | DI-686; screens/P01-guest-web-storefront.yaml#WEB-049 (Passengers notes) … |
| Held for | The countdown on held capacity ("Your seats are held for 7:42"); the release is Release hold. | Lease, Reserved for (a reservation is a different thing), Locked | contracts/spine/orders.yaml#/components/schemas/CartLine (leaseExpiresAt) … |
| Reservation | Booked and not yet paid; holds capacity and expires (My Reservations). Paid tickets are in Tickets or My Tickets. | Booking (for an unpaid hold in lists), Pending order | docs/glossary.md (Reservation); DI-199 |
| Help me choose | The venue's questions whose answers filter the products; Show everything clears them. | Quiz, Wizard, Experience builder, Consent | MoM 29 Sep W4; REV3-11 |
| Info only / Not bookable online | A product listed with full details that cannot be booked online; it shows Contact sales to book with Call sales and Email sales. | Unavailable, Sold out, Coming soon | REV3-14; MoM 29 Sep W3 |
| Guest code | The six-digit code sent to the guest's email or mobile to prove the contact at guest checkout; the copy says six digits. | OTP, PIN, Token, Verification key | DI-1034; MoM 29 Sep W1 |
| How many people | The typed headcount of a group or school booking (number box with minus and plus; +10 on the app), with Supervisors listed separately and free. | Group size (the removed dropdown), Pax | DI-1104; DI-1105; CLIENT-RESPONSE-30SEP 1 |
| Waiting room | The on-sale queue in front of a high-demand performance's sale (WEB-015, GST-046). | Virtual queue (that is the ride queue), Lobby | screens/P01-guest-web-storefront.yaml#WEB-015 notes (ADR-0066) |
| QR | The code a guest shows, in guest copy only (Dynamic QR). Staff screens say Media code. | Barcode, Serial, Media code (in guest copy) | docs/glossary.md (Recorded exceptions, QR, audit R210) |
| Not at this park | The planner's per-day notice that the day's park cannot meet a preference, naming the park that can. | Unavailable, No results | DI-1113 |
| Book this plan | Turns the whole visit plan (tickets, Fast Track, meal combos) into basket lines. | Checkout plan, Buy itinerary | screens/P02-guest-mobile-app.yaml#GST-053 (Book this plan) |

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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-021` | Wallet & Gift Cards | A | 4 | 36 | 6 | 37 | 13 | 6 | guest | review (client-verified) |
| `WEB-022` | Membership Plans | A | 0 | 17 | 6 | 16 | 4 | 0 | guest | review (client-verified) |
| `WEB-023` | Membership Management | A | 3 | 28 | 6 | 6 | 5 | 0 | guest | review (client-verified) |
| `WEB-024` | Devices, Wishlist & Consent | A | 4 | 77 | 6 | 61 | 2 | 4 | guest | review (client-verified) |
| `WEB-043` | Loyalty & Rewards | A | 9 | 51 | 6 | 54 | 2 | 2 | guest | review (client-verified) |

## Thin screens in this batch

**WEB-022 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-021` Wallet & Gift Cards

**See wallet & gift cards for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Membership, Loyalty & Value · wave 1 · needs the `retail` module |
| Block | Block A · ticket #28310 (APP-WEB-WEB-021) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listWalletTransactions` reads the population and `getWallet` reads one of them — list, select, act |
| Offline | **The offline banner shows.** Balances and stored cards already loaded stay visible with their age, cards masked. Storing a card and transferring value need the server. |
| Opens with | `cardCode` (deepLink), `subjectId` (session), `walletId` (navigation) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/membership-loyalty-and-value/wallet-and-gift-cards` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The guest's stored value: wallet balance with its expiry breakdown, transactions, gift cards (balance check by code), game cards, saved cards and auto top-up. Block A. Get right that the guest sees the expiry lots but never chooses which is spent (nearest expiry first), and that top-up and transfer appear only where the venue and the guest's family role allow them.

**Fixed on main** (the package already carries these; draw what it says): Raw "Store payment token" primary button with a form collecting providerId, providerToken, consentPurposeId. (CHG-GST-003); "Every wallet transaction" is bound to retail.yaml in one region and wallet.yaml in another. (CHG-GST-003).

#### Inputs: what the user enters or picks

**Form: Add a card** (modal, opened by *Add a card*; *Save card* calls `storePaymentToken`, *Cancel* sends nothing)

**The gateway's own card form**, hosted by the provider; it returns the token that `storePaymentToken` saves with the guest's consent. No token, provider or consent id is ever a field.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider `providerId` | picker: choose a provider | required | — | — | shows names, sends the id | — | `storePaymentToken` body |
| Provider token `providerToken` | text field | required | — | — | — | — | `storePaymentToken` body |
| Consent purpose `consentPurposeId` | picker: choose a consent purpose | required | — | — | shows names, sends the id | — | `storePaymentToken` body |
| Set default `setDefault` | toggle | optional | off | — | — | — | `storePaymentToken` body |

Errors to draw in the form: 409 The provider cannot hold a stored credential (`tokenisationNotSupported`, `PaymentProvider.supportsTokenisation` false), or the guest has not consented to the … (PaymentProblem)

**Form: Transfer wallet balance** (modal, opened by *Transfer wallet balance*; *Transfer wallet balance* calls `transferWalletBalance`, *Cancel* sends nothing)

**Collects what `transferWalletBalance` sends before it is called.** Required: `amount`. Optional: `toSubjectId`, `toWalletId`, `message`. Dismissing sends nothing; the screen behind is unchanged.

Errors to draw in the form: 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem)

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **gift card code**: Check balance by code (the 16-character code on the card); shows balance, expiry and where it can be used (online, on site or both). *(source: contracts/satellite/wallet.yaml#getGiftCard; DI-533)*
- **auto top-up**: "When my balance drops below AED 50, add AED 200" with the saved card; minimum and maximum per top-up come from the venue's rules. Off by default. *(source: DI-519; DI-517; contracts/satellite/wallet.yaml#setWalletAutoReloadSetting)*
- **transfer**: To a linked family member's wallet, or to another guest only where the venue allows peer-to-peer; amount and optional message. Hidden when the venue toggle is off. *(source: DI-532; DI-536)*

#### Outputs: what the screen shows and produces

**Shown**

**Activity** (card list, from `listWalletTransactions`): Was the generated table 'Every wallet transaction'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)). From `wallet.yaml` `listWalletTransactions`.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Top up, Spend, Refund, Adjustment, Bonus, Expiry… | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Balance after | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**Saved cards** (card list, from `listPaymentTokens`): Was the generated table 'Every payment token'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Method | text | — |
| Masked identifier | text | What a guest sees — the last four digits, the card brand. Enough to choose between two saved cards and not enough to use one. |
| Expires at | 1 Oct 2026 | — |
| Is default | yes / no (icon or chip) | — |

**The gift card** (detail panel, from `getGiftCard`)

| Shows | Format | Notes |
|---|---|---|
| Card code | text | — |
| Kind | text | — |
| Face value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Status | chip: Issued, Active, Partially redeemed, Redeemed, Expired, Blocked | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Activated at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**The game card** (detail panel, from `getGameCard`)

| Shows | Format | Notes |
|---|---|---|
| Card code | text | A pre-printed card keeps the code printed on it. A generated code (a digital card, or a card issued with no printed code) is the venue … |
| Kind | text | — |
| Credits | 1,234 | Bought with money. Buys plays. |
| Bonus credits | 1,234 | From a promotion. Typically non-refundable and spent before paid credits. |
| Points | 1,234 | Won by playing. Buys prizes. |
| Status | chip: Active, Blocked, Expired, Transferred | — |
| Blocked reason | text | — |
| Transferred to card code | text | — |
| Last played at | 1 Oct 2026, 14:30 | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**The wallet** (detail panel, from `getWallet`)

| Shows | Format | Notes |
|---|---|---|
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Credits | list or chips (count when long) | 4.3.5 and 4.3.19. One balance and one bonus balance with one expiry could not express what the requirement asks for — cash, bonus and … |
| Bonus balance | AED 1,234.50 | Promotional value. Typically non-refundable and spent first. |
| Currency | text | — |
| Status | chip: Active, Suspended, Closed | — |
| Home cell name | text | Where the authoritative balance lives. Present when the guest is linked across cells. |
| Expires at | 1 Oct 2026, 14:30 | — |
| Last activity at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add a card (primary button) | `storePaymentToken` POST `/payment-tokens` | inline | PaymentToken | 409 The provider cannot hold a stored credential (`tokenisationNotSupported`, `PaymentProvider.supportsTokenisation` false), or the guest has not consented to the … (PaymentProblem) | opens modal first |
| Transfer wallet balance (secondary button) | `transferWalletBalance` POST `/wallets/{walletId}/transfer` | inline | WalletTransaction | 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **balance**: Total in AED, split into cash and bonus credit, with the expiry lots ("AED 150 expires 31 Dec"); bonus credit is spent first under its own validity. *(source: DI-523; TRACKER 30-September Old rows row 118 (A167))*
- **family**: Each linked child with their allowance ("Omar · AED 200 of AED 500"); a child account sees balance and spending but no Top up. *(source: DI-529; DI-509)*
- **saved cards**: Masked only ("Visa •••• 4242, expires 08/28"); never the full number. *(source: DI-069)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Top up**: Only the payment methods the venue allows online for top-up; a top-up above the venue's approval threshold is not offered online. *(source: DI-517; DI-520)*
- **Save a card**: Through the gateway's card form with the consent to store it; the guest never sees a token. *(source: contracts/spine/orders.yaml#storePaymentToken)*

**Data it reads**: `getWallet` (onLoad, Read a guest wallet); `listWalletTransactions` (onLoad, Wallet transaction history); `listPaymentTokens` (onLoad, Saved cards on this account); `getWalletAutoReloadSetting` (onLoad, Show auto top-up); `getWalletExitBalance` (onLoad, Balance due / refundable at exit)

**Where the user goes next**

- → `WEB-022` Membership Plans: *Membership Plans*
- → `WEB-023` Membership Management: *Membership Management*; carries `orderId`
- → `WEB-024` Devices, Wishlist & Consent: *Devices, Wishlist & Consent*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet gift cards list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet gift cards untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet gift cards yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listWalletTransactions` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Balances and stored cards already loaded stay visible with their age, cards masked. Storing a card and transferring value need the server. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient cash credit, distinct from insufficient balance — a guest with 200 of bonus credit and 10 of cash can transfer 10, and telling them they have 200 … (WalletTransferProblem); 409 Nothing is due or refundable, or the action does not match the balance (`collect` on a wallet in credit), or `waive` by a guest.; 409 The provider cannot hold a stored credential … |

#### Edge cases to draw

- **Wallet settled at exit (resort-style wallets)**: Shows the refundable or due balance at exit and Settle; for venues without exit settlement the block is absent. *(source: screens/P01-guest-web-storefront.yaml#WEB-021 apis (getWalletExitBalance, settleWalletAtExit))*

#### Consistency with other screens

- Match `GST-011`: Same balance, lots and family layout; the app adds wristband and NFC.
- Match `WEB-012`: The wallet tender at payment shows the same balance figure.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
balance: AED 420 (cash AED 350, bonus AED 70 expires 31 Dec)
giftCard: GC-7Q4M-2KX9-PL3A · AED 250 · online and on site
family:
- Omar · AED 200 of AED 500
- Layla · AED 150 of AED 500
savedCard: Visa •••• 4242
```

#### Permissions

- `getWallet` → `WALLET_VIEW` (read) · staff, guest
- `listWalletTransactions` → `WALLET_VIEW` (read) · staff, guest
- `getGiftCard` → `WALLET_VIEW` (read) · staff, guest
- `getGameCard` → no permission · guest
- `listPaymentTokens` → `ORDER_VIEW` (read) · staff, guest
- `storePaymentToken` → `ORDER_CREATE` (operate) · staff, guest
- `transferWalletBalance` → `WALLET_OPERATE` (operate) · staff, guest
- `getWalletAutoReloadSetting` → `WALLET_VIEW` (read) · staff, guest
- `setWalletAutoReloadSetting` → `WALLET_OPERATE` (operate) · staff, guest
- `getWalletExitBalance` → `WALLET_VIEW` (read) · staff, guest
- `settleWalletAtExit` → `WALLET_OPERATE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

37 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.9 | Digital Wallet - System shall provide a digital wallet. | Guest Mobile App & Branding | CONTRACTED | `getWallet` |
| 1.1.105 | Stored value card management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.108 | Balance enquiry | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.111 | Expiry management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 2.6.48 | System shall provide one unified wallet experience across website, mobile app, POS, kiosk, and membership channels. The wallet shall show stored value, vouchers, loyalty points, membership benefits … | Ticketing Sales | CONTRACTED | `getWallet` |
| 2.13.34 | Digital Wallet Integration | Ticketing Sales | CONTRACTED | `getWallet` |
| 4.3.7 | The system should allow guests to use their digital wallet to make online and in-app purchases (through API integrations), buy tickets of all type or purchase any service within venue such as retail … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.8 | The system should provide a digital wallet that allows: - multiple channels for payments, including but not limited to the Mobile app and wearable (which is linked to the digital wallet). - multiple … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.13 | The system should allow guests to make in-store and attraction payments using digital wallets via contactless methods as RFID, NFC and QR-code. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.20 | The system should enable usage of wallet by other systems through integration. All functionalities of the wallet such as credit redemption, balance check and wallet funding should be available … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.22 | Support cashless stored-value balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.23 | Support gift card balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| … 25 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)*
- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*
- Balance can move between linked family/group wallets in either direction (parent to child, child to parent); a venue-controlled toggle, not always enabled. *(agreed · MoM 27 Aug 2026, 4.8 Shared wallet transfer · DI-532)*
- Guests can create family-member profiles themselves and set spending limits directly from their own guest account, in addition to venue-side configuration. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-530)*
- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)*
- Consumption is fully automatic FEFO (nearest expiry first). Guests see their balance and the expiry breakdown per top-up lot in their profile but cannot choose which lot is drawn down; no lot picker at payment. *(agreed · MoM 27 Aug 2026, 4.6 Stored Value, Credit Consumption & FEFO Logic · DI-523)*
- Guests must be able to configure auto-reload and recurring funding schedules themselves in the guest web/app, not only venue admins in the back office. *(agreed · MoM 27 Aug 2026, 4.5 Funding / 5. Key Decisions · DI-519)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)*
- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)*
- Referral rewards may be credited as currency/points directly into the guest's wallet (like Swiggy), in addition to discount vouchers — a business-configurable option. *(agreed · MoM 25 Aug 2026, 4.7 Entitlements & Access Control; 5. Key Decisions · DI-460)*
- A combo product can bundle admission with stored-value credit the guest draws down on F&B or retail purchases (wallet mechanics in a dedicated session). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-459)*
- Wallet balance is shared across a linked family — a parent's top-up can be drawn down by a linked child's wristband without a separate top-up. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 4.5 Loyalty, Membership & Wallet · DI-374)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-021` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Wallet & gift cards' (and 'Payment methods')*. Differences: Rows with toast actions; no transaction list, no gift-card balance lookup. Auto top-up is a prototype addition with no YAML operation. Saved payment tokens are a separate pane.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409, 412, 422).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add a card, Transfer wallet balance.
- [ ] Every transition is wired: `WEB-022`, `WEB-023`, `WEB-024`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 13 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-022` Membership Plans

**Membership Plans — the screen a person opens when they need to deal with membership plans.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Membership, Loyalty & Value · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #28147 (APP-WEB-WEB-022) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getProduct` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `productId` (WEB-001) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/membership-loyalty-and-value/membership-plans` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired 24 August**: getMyMemberships, listGuestMemberships. **The web surface drew the screen and could not fetch what it shows** — the app had these and the browser did not, and there is no reason a membership or a bundle should need an app.

**Known gaps.** The staff-shaped membership list; the guest's own are `getMyMemberships`.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The membership and annual pass plans on sale, compared side by side, and the guest's own plan if they hold one. Block A. In the prototype plans are sold through a booking flow (Annual pass / membership), so this page is a comparison that hands off to that flow.

**Fixed on main** (the package already carries these; draw what it says): Filter fields "Venue id", "Kind" and "Is sellable" and a raw product table. (CHG-GST-003); Both getMyMemberships and listGuestMemberships are declared. (CHG-GST-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Include lapsed | toggle | on | — | `getMyMemberships` ?includeLapsed |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Membership plans** (card list, from `listProducts`): Membership products only, for the guest's venue. The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every product'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Media | list or chips (count when long) | The product's own photos and video (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each … |

**The plan** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |

**Your membership** (detail panel, from `getMyMemberships`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Tier | text | — |
| Status | chip: Active, Frozen, Suspended, Expired, Cancelled | Derived from the entitlement, not held here. This schema is a view assembled from the entitlement, the product that granted it and the … |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Frozen days | 1,234 | Days lost to a freeze and added back to `validTo`. Shown because a guest who paused a pass will check the maths, and a validity date that … |
| Benefits | list or chips (count when long) | 5.4.31. From the product's entitlement template. |
| Renews on | 1 Oct 2026 | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **plan card**: Name, price per year (or month), validity by dates, the benefits as a short list (free entry, F&B discount, guest passes, Fast Track), blockout days named ("Not valid on public holidays"). *(source: DI-138; DI-452; DI-201)*
- **current plan**: The guest's plan is marked "Your plan" with its expiry; upgrade shows only inside the venue's upgrade window. *(source: DI-467; contracts/spine/catalogue.yaml#getMyMemberships)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Choose a plan**: Opens the membership booking flow with a quantity stepper once selected (a family buying two), profile capture of each member, and auto-renewal with card-on-file consent. *(source: DI-980; DI-448; DI-138)*

**Data it reads**: `listProducts` (onLoad, List products); `getProduct` (onLoad, Read a product); `getMyMemberships` (onLoad, A guest's own memberships, benefits and history Only when …)

**Where the user goes next**

- → `WEB-021` Wallet & Gift Cards: *Wallet & Gift Cards*
- → `WEB-023` Membership Management: *Membership Management*
- → `WEB-024` Devices, Wishlist & Consent: *Devices, Wishlist & Consent*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership plans list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership plans untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership plans yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: the plans are the venue's membership products, with no filter a guest sets. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 … |

#### Consistency with other screens

- Match `GST-015`: Same plans and benefits wording on the app's Memberships.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plans:
- name: Summit Peaks Annual Pass
  price: AED 1,295 / year
  benefits:
  - Unlimited entry
  - 10% off food
  - 2 guest passes
- name: Kids Club Membership
  price: AED 149 / month
  benefits:
  - Unlimited weekday play
  - Free socks
```

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getMyMemberships` → `PRODUCT_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.26 | Membership Wallet - System shall provide membership wallets. | Guest Mobile App & Branding | CONTRACTED | `getMyMemberships` |
| 19.2.27 | Membership Benefits Display - System shall display membership benefits. | Guest Mobile App & Branding | CONTRACTED | `getMyMemberships` |
| 19.2.28 | Membership History - System shall display membership history. | Guest Mobile App & Branding | CONTRACTED | `getMyMemberships` |
| 1.1.103 | Membership benefit management | Ticketing Catalogue | CONTRACTED | `getMyMemberships` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Season and membership packages show a quantity stepper once selected. *(client request · design review 23 Sep 2026, Cart 12. No quantity field for the selected ticket · DI-980)*
- UX reference: House of Wisdom (Sharjah library) meeting-room/"pod" booking and tiered membership plans — a simple duration-based booking flow without fixed performances/time slots — to be reviewed by Chinmay/Aishwarya. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 6. Open Items · DI-506)*
- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-022` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Summit Peaks → 'Annual pass / membership' flow; Kids Club → 'Membership pass'; Account → Membership → 'Other plans — Compare'*. Differences: Plans are sold as a booking flow, not a plans page; the account 'Compare' action is a toast.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `WEB-021`, `WEB-023`, `WEB-024`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-023` Membership Management

**Work with membership management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Membership, Loyalty & Value · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #28295 (APP-WEB-WEB-023) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listGuestMemberships` reads the population and `getMyMemberships` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `subjectId` (session), `orderId` (deepLink), `caseId` (navigation), `statementId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/membership-loyalty-and-value/membership-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Wired 24 August**: getMyMemberships, listGuestMemberships. **The web surface drew the screen and could not fetch what it shows** — the app had these and the browser did not, and there is no reason a membership or a bundle should need an app. **Rev 3 (decided 29 September, rev 3 DG-2, no contract change).** The billing statement shows the decline states: a **soft decline** offers *Retry now* (`retryMyDunningPayment`) and *Use another card*; a **hard decline** offers another card only; **declined again** shows the next retry date; then **paid**.

**Known gaps.** The staff-shaped membership list; the guest's own are `getMyMemberships`. No use on Membership Management; moving a membership to a family member is a different operation.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Manage the membership the guest holds: card, benefits, linked members, billing statements and the declined-renewal recovery. Block A. The decline states decided on 29 September are the core of the design.

**Fixed on main** (the package already carries these; draw what it says): "Transfer order tickets" is the primary action on Membership Management. (CHG-GST-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listBillingStatements`. | `listBillingStatements` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listBillingStatements`. | `listBillingStatements` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include lapsed | toggle | on | — | `getMyMemberships` ?includeLapsed |
| Order | picker: choose an order | — | — | `listInstalmentPlans` ?orderId |
| Status | radio group | — | Active · Completed · In arrears · Cancelled | `listInstalmentPlans` ?status |

**Form: Retry the payment** (modal, opened by *Retry the payment*; *Retry my dunning payment* calls `retryMyDunningPayment`, *Cancel* sends nothing)

**Collects what `retryMyDunningPayment` sends before it is called.** Nothing in the body is required. Optional: `paymentTokenId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Payment token `paymentTokenId` | picker: choose a payment token | optional | — | — | shows names, sends the id | A saved card other than the one that failed: the id of one of the guest's own `PaymentToken` rows (`payments.token`, stored through `storePaymentToken`), not a `payments.method` … | `retryMyDunningPayment` body |

Carried, not typed: `caseId`

Errors to draw in the form: 409 The case is already resolved, or the decline is hard and no other card was given.; 422 The payment was declined again.

#### Outputs: what the screen shows and produces

**Shown**

**Statements** (card list, from `listBillingStatements`): Was the generated table 'Every billing statement'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Lines | list or chips (count when long) | — |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Is tax invoice | yes / no (icon or chip) | Always false, and stated rather than assumed. UAE e-invoicing is Peppol five-corner with the FTA as the fifth corner, PINT AE XML and 51 … |

**Payments that need you** (card list, from `listMyPaymentIssues`): Was the generated table 'Every dunning case'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Order | text | The order whose renewal failed. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| State | chip: Scheduled, In progress, Exhausted, Recovered, Resolved manually | BL-100. `exhausted` and `recovered` are both endings and only one of them is a failure. |
| Decline class | chip: Soft, Hard, Unknown | From the most recent attempt. A case that begins `soft` and turns `hard` stops immediately rather than finishing its schedule — the card … |
| Attempts made | 1,234 | — |
| Next attempt at | 1 Oct 2026, 14:30 | Null where the case has ended or the decline is hard. A scheduled time on a case nothing will act on is the field that makes a queue … |
| First failed at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolution | chip: Paid by other means, Card replaced, Write off, Cancelled by guest | — |
| Resolution note | text | What `resolveDunningCase` was told, which had nowhere to land until now. The enum above tells `writeOff` from `cardReplaced`; which … |

**The selected billing statement** (detail panel, from `getBillingStatement`)

| Shows | Format | Notes |
|---|---|---|
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Lines | list or chips (count when long) | — |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Is tax invoice | yes / no (icon or chip) | Always false, and stated rather than assumed. UAE e-invoicing is Peppol five-corner with the FTA as the fifth corner, PINT AE XML and 51 … |

**Your membership** (detail panel, from `getMyMemberships`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Tier | text | — |
| Status | chip: Active, Frozen, Suspended, Expired, Cancelled | Derived from the entitlement, not held here. This schema is a view assembled from the entitlement, the product that granted it and the … |
| Valid from | 1 Oct 2026 | — |
| Valid to | 1 Oct 2026 | — |
| Frozen days | 1,234 | Days lost to a freeze and added back to `validTo`. Shown because a guest who paused a pass will check the maths, and a validity date that … |
| Benefits | list or chips (count when long) | 5.4.31. From the product's entitlement template. |
| Renews on | 1 Oct 2026 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry the payment (secondary button) | `retryMyDunningPayment` POST `/dunning-cases/{caseId}/retry` | RetryDunningPaymentRequest | DunningCase | 409 The case is already resolved, or the decline is hard and no other card was given.; 422 The payment was declined again. | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **membership card**: Member name and photo, membership ID, validity, tier, QR for entry; linked members listed (view only). *(source: DI-201)*
- **billing statement**: Line by line, with VAT, invoice number and member savings; send as PDF or CSV. States: soft decline (Retry now + Use another card), hard decline (Use another card only), declined again (Use another card + the next automatic retry date), paid ("Your membership continues"). *(source: DI-1036; REV3 DG-2; AUDIT-29SEP (Account and services))*
- **instalments**: Where the plan allows, the instalment schedule with paid and upcoming instalments. *(source: screens/P01-guest-web-storefront.yaml#WEB-023 apis (listInstalmentPlans))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Retry now / Use another card**: Retries the declined renewal on the same or a saved card; success shows paid, failure the next state. *(source: contracts/satellite/payments.yaml#retryMyDunningPayment; DI-1036)*
- **Upgrade, suspend, cancel**: Each offered only within the venue's timing windows (e.g. upgrade only in the final two months); cancel confirms what is lost and when. *(source: DI-467)*

**Data it reads**: `listBillingStatements` (onLoad, Membership billing statements); `listMyPaymentIssues` (onLoad, Declined renewals waiting on the guest); `getMyMemberships` (onLoad, A guest's own memberships, benefits and history); `listInstalmentPlans` (onLoad, Instalment plans and schedule)

**Where the user goes next**

- → `WEB-021` Wallet & Gift Cards: *Wallet & Gift Cards*
- → `WEB-022` Membership Plans: *Membership Plans*; carries `productId`
- → `WEB-024` Devices, Wishlist & Consent: *Devices, Wishlist & Consent*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Membership and its benefits |
| Error (`?state=error`) | Could not load. Cancellation and renewal are both blocked |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to and the membership are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The case is already resolved, or the decline is hard and no other card was given.; 409 The order already has a plan, or is already paid in full.; 422 The order or product does not qualify under the instalment policy, or the count or frequency is outside it, or the first instalment was declined.; 422 The payment was declined again. |

#### Consistency with other screens

- Match `GST-015`: The app shows the same decline states and statement.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
member: Ahmed Al Mansoori, SP-AP-0042317, valid to 30 Sep 2027
statement: 1 Oct 2026 · Annual pass renewal AED 1,295 (incl. VAT AED 61.67) · Declined (soft)
```

#### Permissions

- `listBillingStatements` → `ORDER_VIEW` (read) · guest, staff
- `getBillingStatement` → `ORDER_VIEW` (read) · guest, staff
- `listMyPaymentIssues` → no permission · guest
- `retryMyDunningPayment` → no permission · guest
- `getMyMemberships` → `PRODUCT_VIEW` (read) · staff, guest
- `listInstalmentPlans` → `PAYMENT_VIEW` (read) · staff, guest
- `createInstalmentPlan` → `ORDER_CREATE` (operate) · staff, guest, service

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.14.23 | System shall provide detailed membership billing statements, payment history, renewal history, taxes, discounts, credits, and downloadable PDF statements accessible through customer self-service … | Ticketing Sales | CONTRACTED | `getBillingStatement` |
| 19.2.26 | Membership Wallet - System shall provide membership wallets. | Guest Mobile App & Branding | CONTRACTED | `getMyMemberships` |
| 19.2.27 | Membership Benefits Display - System shall display membership benefits. | Guest Mobile App & Branding | CONTRACTED | `getMyMemberships` |
| 19.2.28 | Membership History - System shall display membership history. | Guest Mobile App & Branding | CONTRACTED | `getMyMemberships` |
| 1.1.103 | Membership benefit management | Ticketing Catalogue | CONTRACTED | `getMyMemberships` |
| 4.2.17 | The system shall support recurring and subscription-based payments for memberships, annual passes, installment plans, wallet auto-top-ups, and auto-renewal products. | Bundles and Promotions | CONTRACTED | `createInstalmentPlan` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Account → Membership → Billing statement shows a line-by-line statement with states: soft decline (Retry now + Use another card), hard decline (Use another card only), declined again (Use another card + next automatic retry date), paid ("Your membership continues"). Use another card lists saved cards. *(agreed · design review 29 Sep 2026, 2. Billing statement and payment retry (WEB-023) · DI-1036)*
- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)*
- Membership/pass tickets: seasonal, monthly or annual classes with renewal/auto-renewal using a tokenised card-on-file billed ahead of expiry, subject to the guest's consent to terms and conditions. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-448)*
- Membership screen: membership ID, validity, entitlements (free entry, F&B offers, etc.), linked members (view), membership card, renewal and history. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-201)*
- Membership / season pass is defined by start/end date rather than quantity, requires customer profile capture at purchase, and supports renew, upgrade, cancel and extend workflows. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-138)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-023` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Membership' → 'Billing statement — View'*. Differences: Billing and dunning retry are well covered. Prototype adds membership transfer to a family member and guest passes; YAML's transferOrderTickets on this screen has no visible use.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry the payment.
- [ ] Every transition is wired: `WEB-021`, `WEB-022`, `WEB-024`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-024` Devices, Wishlist & Consent

**Your devices, security, cookie choices and data rights.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Membership, Loyalty & Value · wave 1 · needs the `marketing` module |
| Block | Block A · ticket #28812 (APP-WEB-WEB-024) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act |
| Offline | **Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a device signed out offline is still signed in. |
| Opens with | `deviceId` (deepLink), `itemId` (deepLink), `subjectId` (session), `enrolmentId` (navigation), `methodId` (navigation) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/membership-loyalty-and-value/devices-wishlist-consent` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Renamed 31 August** from *Loyalty & Rewards*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Rev 3 (decided 29 September).** **Security (GAP-D1):** the devices list and signing out a lost device are here (`listGuestDevices`, `revokeGuestDevice`, already declared). **Face Pass stays mobile-only** (GST-069) until the facial-reader vendor SDK is named and supports web capture; viewing and withdrawing an enrolment stay here. **Two-step verification (GAP-B1, per venue):** enrolment appears only when a venue of the tenant enabled it. **One implementation, several ids (GAP-D3):** WEB-009 and WEB-024 are built as one account area; both ids are kept. **The Face Pass enrolmentId comes from the guest's passes (listMyEntitlements, Entitlement.facePassEnrolmentId), bound 4 October 2026** (CHG-FXS-003)

**Known gaps.** **`getWaiverStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The web account's devices, security, Face Pass status, cookie choices, consent and data rights, built as one implementation with WEB-009 (GAP-D3). From this process's angle it is where a signed-in guest reviews consent and cookie decisions, downloads their data and asks for erasure, all with the same honesty as GST-066. Withdrawing must be one step, and erasure must be explained before it is offered.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- getWaiverStatus returns an inline response with no named schema. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): Purpose still reads "See loyalty & rewards for this venue". (CHG-SGU-017); "Signed-in devices" with "Sign out this device" is bound to listGuestDevices / revokeGuestDevice, which are push-notification registrations. (CHG-SGU-017); Action-bar buttons "Add to wishlist", "Register guest device", "Record consent" and "Grant delegation" sit on the security and privacy pane. (CHG-SGU-017).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| What we may send you | repeatable rows | optional | — | — | — | One row per configured purpose (`listConsentPurposes`), its channels as toggles, its plain-language description and the notice version in force; the current position from `getGuestConsents` (Given … | `ConsentState.purposes` |
| Consent toggle | repeatable rows | optional | — | — | — | Per purpose and channel; recorded at once on change, append-only. | `ConsentState.purposes` |
| Whose Face Pass | select field | — | — | — | — | **Who is this for** (decided 28 September, audit R205): the signed-in guest and each child linked to them (`heldByThisGuest` with `delegationKind` `familyMember` or `primaryHolder`), so a parent sees … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getWaiverStatus` ?productId |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `getCookieConsentRuntime` ?channel |
| Brand | picker: choose a brand | — | — | `getCookieConsentRuntime` ?brandId |
| Language | text field | — | max length 10 | `getCookieConsentRuntime` ?language |
| Channel | select | — | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | `listPublishedTrackingTechnologies` ?channel |
| Category | radio group | — | Strictly necessary · Functional · Analytics · Personalisation · Marketing | `listPublishedTrackingTechnologies` ?category |
| State | radio group | Usable now | Usable now · Upcoming · Expired · All | `listMyEntitlements` ?state |
| Include shared | toggle | on | — | `listMyEntitlements` ?includeShared |

**Sent by *Get a copy of my data*** (`exportSubjectData`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Format `format` | segmented control | optional | Json | Json · Csv · Pdf | — | — | `exportSubjectData` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Cookie preferences**: Categories strictly necessary (always on, not a toggle, with its description), functional, analytics, personalisation and marketing (all off until chosen). "Reject non-essential" is always one click. A change is a new decision row, never an edit. *(source: contracts/satellite/marketing-crm.yaml#recordDeviceConsent; contracts/satellite/marketing-crm.yaml#/components/schemas/CookieCategory; contracts/satellite/marketing-crm.yaml#listCookieBannerPreference)*
- **Whose Face Pass**: The signed-in guest and each linked child they hold as guardian; a parent sees and withdraws a child's enrolment. Enrolment itself stays mobile-only (GST-069). *(source: R205; DI-1077)*
- **Data copy format**: JSON, CSV or PDF; PDF is the default for a person, the others for portability. *(source: contracts/spine/identity.yaml#exportSubjectData)*

#### Outputs: what the screen shows and produces

**Shown**

**Every guest device** (data table, from `listGuestDevices`)

| Shows | Format | Notes |
|---|---|---|
| Platform | chip: Ios, Android, Web | — |
| Token fingerprint | text | Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support … |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |

**Every delegated access** (data table, from `listDelegations`)

| Shows | Format | Notes |
|---|---|---|
| Permission | text | From the permission enum. `*` permitted on DENY only. |
| Over object ref | text | Where the authority is over a thing rather than a scope — a wallet, an entitlement, a booking. |
| Delegation kind | chip: Primary holder, Family member, Group leader, Attendee, Corporate admin, Corporate … | What kind of relationship this expresses, for display and for reporting. The mechanism does not branch on it — a family member and a group … |
| Quota | 1,234 | 2.14.15 and 4.3.11. How many the holder may assign. |
| Is revocable by subject | yes / no (icon or chip) | Whether the person it is over can end it. A guest who linked a family member should be able to unlink them; a corporate member should not … |
| Effect | chip: ALLOW, DENY | — |

**Purposes and notices** (card list, from `listConsentPurposes`): The configured purposes with their plain-language description, channels and the notice version in force.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Display name | text | — |
| Description | text | — |
| Channels | list or chips (count when long) | — |
| Notice version | text | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. |
| Is required for service | yes / no (icon or chip) | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. |
| Expires after months | 1,234 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Passes with a face** (card list, from `listMyEntitlements`): Only passes with a facePassEnrolmentId; selecting one reads it.

| Shows | Format | Notes |
|---|---|---|
| Product | the name it points at, never the id | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Face pass enrolment | the name it points at, never the id | The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. |

**The selected guest device** (detail panel, from `listGuestDevices`)

| Shows | Format | Notes |
|---|---|---|
| Platform | chip: Ios, Android, Web | — |
| Token fingerprint | text | Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support … |
| Token ref | text | A vault reference to the push token, written by the server from `registerGuestDevice.token` — the same pattern as … |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |
| Revoked at | 1 Oct 2026, 14:30 | — |

**The face pass enrolment** (detail panel, from `getFacePassEnrolment`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Entitlement | the name it points at, never the id | The `Entitlement.id`, a UUIDv7 (`pii.subject_biometric.entitlement_id`). |
| Kind | chip: Face pass, Face tag | BL-106, CF-35. Two different legal postures, not two settings on one record. |
| Retention anchor | chip: Entitlement validity, Ticket validity, Operating day close | BL-106. Derived from `kind`, never sent. |
| Source | chip: Guest app, Ticket counter, Annual pass counter, Entry gate | `entryGate` is valid for `faceTag` only, and 3.2.43's omission of it from Face Pass is deliberate: an enduring enrolment is a considered … |
| Captured at | 1 Oct 2026, 14:30 | — |
| Consent purpose | the name it points at, never the id | — |
| Consent given at | 1 Oct 2026, 14:30 | — |
| Guardian subject | the name it points at, never the id | Where the subject is a minor (3.2.12). |
| Is active | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | Bounded by whatever `retentionAnchor` names, and a face outliving it is a biometric held for no stated purpose. |

**The consent state** (detail panel, from `getGuestConsents`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Purposes | list or chips (count when long) | — |

**Waiver status** (detail panel, from `getWaiverStatus`): Shows `isSatisfied`, `missingFormIds`, `expiringWithinDays` from `getWaiverStatus`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Is satisfied | yes / no (icon or chip) | — |
| Missing forms | list or chips (count when long) | — |
| Expiring within days | 1,234 | — |

**The wishlist** (detail panel, from `getWishlist`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Items | list or chips (count when long) | — |

**Two-step verification** (card list, from `listMfaMethods`): **Offered only when at least one venue of the tenant has guest two-step verification on** (`VenueSettings.identity.guestTwoStep.enabled`); otherwise the section is not shown. Enrolment is on the guest's account (enrol, verify, remove); the code is then asked only when signing in or acting at a venue that has it on.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**Notifications on my devices** (card list, from `listGuestDevices`): Push registrations (`listGuestDevices`). "Stop notifications on this device" (`revokeGuestDevice`) stops notifications; it does not sign a lost device out. No guest operation lists or ends other sessions yet (CHG-SGU-024).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Platform | chip: Ios, Android, Web | — |
| Token fingerprint | text | Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support … |
| Token ref | text | A vault reference to the push token, written by the server from `registerGuestDevice.token` — the same pattern as … |
| App version | text | — |
| Os version | text | — |
| Device model | text | — |
| Locale | text | — |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |
| Revoked at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Stop notifications on this device (destructive button) | `revokeGuestDevice` DELETE `/guests/{subjectId}/devices/{deviceId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Delete my account (destructive button) | `deleteGuestAccount` DELETE `/auth/guest/account` | — | inline | 409 Open orders or an unexpired entitlement exist. Deleting an account with a valid ticket in it strands the guest at a gate. | — |
| Get a copy of my data (secondary button) | `exportSubjectData` POST `/guests/{subjectId}/data-export` | inline | inline | — | — |
| Revoke face pass (destructive button) | `revokeFacePass` DELETE `/face-pass/enrolments/{enrolmentId}` | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Cookie technologies**: Per category, the approved technologies with name, provider, purpose, expiry in days, and first or third party. Detected, blocked and retired entries never appear. *(source: contracts/satellite/marketing-crm.yaml#listPublishedTrackingTechnologies)*
- **Consent state**: Same rows and states as WEB-020 (Given, Withdrawn, Not asked, Needs renewing). *(source: contracts/satellite/marketing-crm.yaml#getGuestConsents)*
- **Waiver status**: Whether the guest's tickets need a waiver still unsigned, which one, and those expiring soon, with Sign now. *(source: contracts/satellite/marketing-crm.yaml#getWaiverStatus)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Withdraw Face Pass**: The confirmation says the face template is destroyed, not flagged, and that the pass survives so the guest enters another way. After confirming it cannot be undone except by enrolling again in the app. *(source: contracts/spine/access.yaml#revokeFacePass)*
- **Get a copy of my data**: Raises a data request and shows its reference and estimated completion date; the file arrives by the notification the venue configured. *(source: contracts/spine/identity.yaml#exportSubjectData)*
- **Delete my account**: Explains first: personal details are erased; bookings and payments stay in the venue's financial records under an anonymous reference; the request is completed by an estimated date. Then a typed confirmation. Raises an erasure request; it is not an instant delete. *(source: contracts/spine/identity.yaml#deleteGuestAccount; DI-379)*

**Data it reads**: `getWishlist` (onLoad, Read a guest's saved items); `listGuestDevices` (onLoad, A guest's registered devices); `getGuestConsents` (onLoad, What this guest has consented to); `getWaiverStatus` (onLoad, Which waivers are signed and which are due); `listDelegations` (onLoad, Who may act for this guest); `listMfaMethods` (onLoad, The guest's enrolled second-factor methods); `getCookieConsentRuntime` (onLoad, Preference centre: categories and the current decision); `listPublishedTrackingTechnologies` (onLoad, Each cookie's name, provider, purpose, expiry and party); `getDeviceConsentHistory` (onLoad, My cookie decisions so far); `listConsentPurposes` (onLoad, The purposes the consent rows show); `listMyEntitlements` (onLoad, The guest's passes, each with its facePassEnrolmentId for …)

**Where the user goes next**

- → `WEB-021` Wallet & Gift Cards: *Wallet & Gift Cards*
- → `WEB-022` Membership Plans: *Membership Plans*
- → `WEB-023` Membership Management: *Membership Management*
- → `GST-037` Offers & Promotions: *Offers are shown against what they hold*

**What opens over it**

- confirmDialog *Stop notifications on this device*: **Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.
- confirmDialog *Delete my account*: **Names what `deleteGuestAccount` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.
- confirmDialog *Revoke face pass*: **Names what `revokeFacePass` changes and what it leaves alone**, in the consequence rather than the verb. A devices wishlist consent this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Points and rewards |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | No points yet — explains how they accrue |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `GUEST_VIEW`, which `getGuestConsents` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_MANAGE` for `revokeFacePass`; `GUEST_VIEW_PII` for … |
| Offline (`?state=offline`) | **Nothing here is offered offline, and the banner says so.** An erasure request or a device change queued and never sent is worse than one that could not be made — the legal clock starts when the platform receives it, and a device signed out offline is still signed in. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 No published banner design with this id for the channel, or a category the design does not offer; 400 Notice version unknown, or the purpose is not configured; 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135); 409 Open orders or an unexpired entitlement exist. Deleting an account with a valid ticket in it strands the guest at a gate. |

#### Edge cases to draw

- **The guest signed in on a shared browser**: Cookie history from before sign-in now belongs to the guest (claimed); the device history read answers 404 for a claimed key, so show the guest's own consents instead. *(source: contracts/satellite/marketing-crm.yaml#getDeviceConsentHistory)*

#### Consistency with other screens

- Match `GST-066`: Same data-request wording, same erasure explanation, same statuses.
- Match `GST-073`: The app's devices and security screen uses the same device rows and the same "Sign out this device" wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
devices:
- iPhone 15 - Coastal Aqua app - last active today 09:12
- Chrome on Windows - last active 28 Sep 2026
dataRequest:
  reference: DR-2026-00412
  kind: Copy of my data
  raised: 1 Oct 2026
  due: 31 Oct 2026
  status: In progress
cookies:
  analytics: false
  marketing: false
  functional: true
```

#### Permissions

- `getWishlist` → no permission · guest
- `listGuestDevices` → no permission · guest
- `recordConsent` → no permission · guest, staff
- `revokeGuestDevice` → no permission · guest
- `deleteGuestAccount` → no permission · guest
- `exportSubjectData` → `GUEST_VIEW_PII` (operate) · staff, guest
- `getFacePassEnrolment` → `GUEST_VIEW` (read) · staff, guest
- `getGuestConsents` → `GUEST_VIEW` (read) · staff, guest
- `getWaiverStatus` → `GUEST_VIEW` (read) · staff, guest, device
- `listDelegations` → `GUEST_VIEW` (read) · staff, guest
- `revokeFacePass` → `GUEST_MANAGE` (configure) · staff, guest
- `listMfaMethods` → no permission · staff, partner, guest
- `enrolMfaMethod` → no permission · staff, partner, guest
- `verifyMfaEnrolment` → no permission · staff, partner, guest
- `removeMfaMethod` → no permission · staff, partner, guest
- `getCookieConsentRuntime` → no permission · anonymous, guest
- `listPublishedTrackingTechnologies` → no permission · anonymous, guest
- `getDeviceConsentHistory` → no permission · anonymous, guest
- `recordDeviceConsent` → no permission · anonymous, guest
- `listConsentPurposes` → `GUEST_VIEW` (read) · staff, guest
- `listMyEntitlements` → `ORDER_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `GUEST_VIEW`, which `getGuestConsents` requires to show this screen, and names that permission (the screen's other reads need `ORDER_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `GUEST_MANAGE` for `revokeFacePass`; `GUEST_VIEW_PII` for …

#### Requirements it meets

61 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.9 | The system should allow the guest to explicitly opt in to receive any information from venue or its partners. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 5.3.18 | Maintain auditable consent records for Email, SMS, WhatsApp, Push Notifications, Marketing Communications, Privacy Policies, Terms & Conditions, and GDPR compliance. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 7.3.9 | Store and manage customer consent preferences for email, SMS, WhatsApp, push notifications and third-party marketing. Record consent status, source, timestamp, IP address and revocation history. … | F&B POS | CONTRACTED | `recordConsent` |
| 22.2.18 | Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.4.5 | Subscription Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.1 | Consent Management Framework | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.2 | Marketing Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.3 | Channel-Specific Consent | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.4 | Consent Capture Workflows | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.9 | Data Processing Consent | Marketing & CRM | CONTRACTED | `recordConsent` |
| 7.3.10 | Allow authorized users to export customer data in PDF, Excel, CSV or JSON formats. Support anonymization, soft deletion and hard deletion workflows according to configured privacy policies. | F&B POS | CONTRACTED | `exportSubjectData` |
| 7.4.1 | Looking for a customer is quick and simple based on multiple filtering or search criteria. | F&B POS | CONTRACTED | `exportSubjectData` |
| … 49 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Cookie banner*, set in `CMS-026` Cookie Banner & Preference Center Designer:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Brand (`cookieBanner.brandId`) | shows names, sends the id | — | Null for the corporate design every brand inherits. |
| Inherits from (`cookieBanner.inheritsFromId`) | shows names, sends the id | — | — |
| Cookie banner channel (`cookieBanner.channel`) | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | — |
| Logo (`cookieBanner.logoAssetId`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | — |
| Cookie banner title (`cookieBanner.title`) | English and Arabic (Arabic right to left) | — | — |
| Body (`cookieBanner.body`) | English and Arabic (Arabic right to left) | — | — |
| Position (`cookieBanner.position`) | Top · Bottom · Popup · Modal | — | — |
| Buttons: action (`cookieBanner.buttons[].action`) | Accept all · Reject non essential · Manage preferences · Save preferences · Do not sell or share | — | — |
| Buttons: label (`cookieBanner.buttons[].label`) | English and Arabic (Arabic right to left) | — | — |
| Reject is one click (`cookieBanner.rejectIsOneClick`) | — | on | Must be true. |
| Links: label (`cookieBanner.links[].label`) | English and Arabic (Arabic right to left) | — | — |
| Links: policy kind (`cookieBanner.links[].policyKind`) | Privacy · Cookie · Terms and conditions | — | — |
| Categories (`cookieBanner.categories`) | at least 1 | — | — |
| Categories: category (`cookieBanner.categories[].category`) | Strictly necessary · Functional · Analytics · Personalisation · Marketing | — | — |
| Categories: description (`cookieBanner.categories[].description`) | English and Arabic (Arabic right to left) | — | — |
| Categories: default on (`cookieBanner.categories[].defaultOn`) | True only for `strictlyNecessary`, which is always active. | — | True only for `strictlyNecessary`, which is always active. |
| Cookie banner languages (`cookieBanner.languages`) | at least 1 | — | Every language the storefront serves; Arabic renders right to left. |
| Regulatory regimes (`cookieBanner.regulatoryRegimes`) | Gdpr · E privacy · Ccpa cpra · Lgpd · Uae pdpl · Saudi pdpl | — | 2.6.60 (29 September, build). The laws this design is published to satisfy, so compliance is stated rather than assumed. |
| Record ip address (`cookieBanner.recordIpAddress`) | — | off | 2.6.55, "if legally permitted" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. |

Also set there, as content the tenant writes: theme, buttons, links.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-024` · status **review** · provenance client-verified
- Prototype (rev 3 (pointer moved to the 30 September build, CHG-R1S-015), verified 2026-09-28, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Security' (devices), 'Face Pass', 'Data & privacy', 'Newsletters' (devices that get notifications)*. Differences: Spread across four panes rather than one screen; wishlist is its own view (WEB-009). Security pane includes passkeys and two-step verification, which the YAML does not have for guests. YAML purpose text still says 'See loyalty & rewards' (stale).
- Flow F53 *A guest earns, sees and spends loyalty*, step 2: They see rewards and manage their devices. → **Consent sits here deliberately.** A rewards screen is where a guest is most willing to opt in, and CF-160 keeps the merge from ever widening it.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0010 *Cross-Jurisdiction Entitlements* (`docs/adr/0010-cross-jurisdiction-entitlements.md`)
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (77 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Stop notifications on this device, Delete my account, Get a copy of my data, Revoke face pass.
- [ ] Every transition is wired: `WEB-021`, `WEB-022`, `WEB-023`, `GST-037`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-043` Loyalty & Rewards

**Points, tier, and what the next one needs.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Membership, Loyalty & Value · wave 1 · needs the `marketing` module |
| Block | Block A · ticket #28804 (APP-WEB-WEB-043) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listLoyaltyProgrammes` reads the population and `getLoyaltyPosition` reads one of them — list, select, act |
| Offline | **The offline banner shows.** The last known balance stays with its age, and **points earned since are not shown** — and that is said. Redeeming and referring need the connection. |
| Opens with | `subjectId` (session), `customerId` (session) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/loyalty-and-rewards` |

**What the spec says about it.** **P01 Board 3 drew *Membership* with nothing behind it.** `getLoyaltyPosition` and `listLoyaltyProgrammes` were app-only — **the surface a guest checks their points on between visits is the web one.** **`evaluatePromotions` removed 27 September 2026 (audit root R292).** It evaluates promotions against a cart — `EvaluatePromotionsRequest` requires `venueId`, `channel` and at least one line — and this screen arrives with no parameter and holds no cart. Offers apply on WEB-005 and WEB-010, which keep the call.

**Known gaps.** **`getLoyaltyPosition` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The web loyalty page, the surface a guest checks points on between visits. Same position card as GST-036, plus redeem and referral. It sits in the "At the venue" section of the prototype.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Same shape and permission issues as GST-036 (getLoyaltyPosition shape, listLoyaltyProgrammes MARKETING_VIEW, rewards and badges unwired). (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The "Create referral" modal asks the guest for id, referrerSubjectId, code, status, qualifying action, reward ids and expiry. (CHG-SGU-017).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Same programme-configuration question as GST-036.** → Drawn default stands (answer: "Default / recommended accepted"): Same sample tiers. *(decided by Chinmay, 2026-10-02; DEC-027 / CHG-NOTE-002)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `getLoyaltyPosition` ?programmeId |
| Status | select | — | Draft · Scheduled · Live · Paused · Expired · Ended | `listPromotions` ?status |
| Active at | date and time picker | — | — | `listPromotions` ?activeAt |
| Programme | picker: choose a programme | — | — | `listRewards` ?programmeId |
| Programme | picker: choose a programme | — | — | `listLeaderboard` ?programmeId |
| Window | segmented control | Month | Week · Month · Season | `listLeaderboard` ?window |

**Form: Invite a friend** (confirmDialog, opened by *Invite a friend*; *Invite a friend* calls `createReferral`, *Cancel* sends nothing)

One tap: the code that comes back is shown with Share. Code, status, qualifying action, rewards and expiry are set by the platform; the guest types nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Referrer subject `referrerSubjectId` | picker: choose a referrer subject | required | — | — | shows names, sends the id | — | `createReferral` body |
| Qualifying action `qualifyingAction` | segmented control | optional | — | First purchase · First visit · Membership purchase | — | — | `createReferral` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createReferral` body |

**Form: Redeem** (modal, opened by *Redeem*; *Redeem* calls `redeemLoyaltyPoints`, *Cancel* sends nothing)

The reward chosen from the list and its points; the guest is the caller, so no subject or programme is asked.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `redeemLoyaltyPoints` body |
| Programme `programmeId` | picker: choose a programme | required | — | — | shows names, sends the id | — | `redeemLoyaltyPoints` body |
| Points `points` | number field | required | — | — | — | — | `redeemLoyaltyPoints` body |
| Reward `rewardId` | picker: choose a reward | optional | — | — | shows names, sends the id | — | `redeemLoyaltyPoints` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | Where points are being used against a sale rather than for a catalogue reward. | `redeemLoyaltyPoints` body |

Errors to draw in the form: 409 The balance does not cover `points` (`insufficientPoints`). Nothing is held. (LoyaltyRefusedProblem)

**Form: Choose my name** (modal, opened by *Choose my name*; *Choose my name* calls `setLeaderboardNickname`, *Cancel* sends nothing)

The nickname shown on the leaderboard.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Nickname `nickname` | text field | required | — | min length 2; max length 24; pattern `^[\p{L}\p{N}][\p{L}\p{N} _.-]{0,22}[\p{L}\p{N}]$` | — | — | `setLeaderboardNickname` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Redeem**: Pick a reward; the confirmation shows the points it costs and the balance after. Points cannot be split between programmes. Refused with a clear reason when the tier does not qualify or the balance is short. *(source: contracts/satellite/marketing-crm.yaml#redeemLoyaltyPoints; contracts/satellite/marketing-crm.yaml#/components/schemas/LoyaltyRefusedProblem)*

#### Outputs: what the screen shows and produces

**Shown**

**Every loyalty programme** (data table, from `listLoyaltyProgrammes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Unique per tenant (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused … |
| Name | text | — |
| Points expire after months | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**Every promotion** (data table, from `listPromotions`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Discount | grouped details | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |

**Loyalty & Rewards** (card list)

**Detail** (detail panel)

**Rewards** (card list, from `listRewards`): What points can be turned into, with the points each needs; Redeem on a reward the guest can afford.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Loyalty program | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Type | text | — |
| Product | the name it points at, never the id | — |
| Points cost | 1,234.5 | — |
| Discount value | 1,234.5 | — |
| Validity days | 1,234 | — |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**My badges** (card list, from `listCustomerBadges`): Status badges the guest holds (DI-392).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Customer | the name it points at, never the id | — |
| Badge | the name it points at, never the id | — |
| Challenge | the name it points at, never the id | — |
| Source type | text | — |
| Source reference | the name it points at, never the id | — |
| Awarded at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Status | text | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Leaderboard** (card list, from `listLeaderboard`): Standings by nickname; the guest sets theirs with Choose my name.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Rank | 1,234 | — |
| Nickname | text | Always present, and never their real name. The guest's chosen `leaderboardNickname` where they have set one, and otherwise a generated … |
| Points | 1,234 | — |
| Is me | yes / no (icon or chip) | How a client highlights the caller's own row without learning who anybody else is. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Loyalty position** (detail panel, from `getLoyaltyPosition`): Shows `subjectId`, `programmeId`, `pointsBalance`, `pointsPending`, `tier`, `nextTier`, `pointsToNextTier`, `expiringPoints`, `expiringAt` from `getLoyaltyPosition`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Programme | the name it points at, never the id | — |
| Points balance | 1,234 | — |
| Points pending | 1,234 | Earned and not yet cleared — a purchase inside the refund window. Summed at read from the guest's `marketing.loyalty_points` accruals whose … |
| Tier | text | — |
| Next tier | text | The name of the next `MarketingProgrammeTier` by `rank` above the guest's current tier, resolved at read. |
| Points to next tier | 1,234 | — |
| Expiring points | 1,234 | — |
| Expiring at | 1 Oct 2026, 14:30 | Points that lapse unannounced are a complaint. The date is returned so the interface can warn before it happens. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Invite a friend (primary button) | `createReferral` POST `/referrals` | Referral | Referral | — | opens confirmDialog first |
| Redeem (secondary button) | `redeemLoyaltyPoints` POST `/loyalty/redemptions` | inline | LoyaltyPosition | 409 The balance does not cover `points` (`insufficientPoints`). Nothing is held. (LoyaltyRefusedProblem) | opens modal first |
| Choose my name (secondary button) | `setLeaderboardNickname` PUT `/loyalty/leaderboard-nickname` | inline | LoyaltyPosition | — | opens modal first |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Position card**: Same as GST-036. *(source: contracts/satellite/marketing-crm.yaml#getLoyaltyPosition)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Get my referral code**: Same as GST-036; the guest never fills in ids, status or reward ids. *(source: contracts/satellite/marketing-crm.yaml#createReferral)*

**Data it reads**: `getLoyaltyPosition` (onLoad, A guest's points, tier and what is within reach); `listLoyaltyProgrammes` (onLoad, List loyalty programmes); `listPromotions` (onLoad, List promotions); `decideRecommendations` (onLoad, Recommendation slot (homepage / loyalty placement …); `listRewards` (onLoad, What points can be turned into); `listCustomerBadges` (onLoad, Badges the guest holds); `listLeaderboard` (onLoad, Standings, by nickname)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** The last known balance stays with its age, and **points earned since are not shown** — and that is said. Redeeming and referring need the connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The balance does not cover `points` (`insufficientPoints`). Nothing is held. (LoyaltyRefusedProblem) |

#### Consistency with other screens

- Match `GST-036`: Same card and wording.
- Match `WEB-017`: The account tile links here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
position:
  tier: Gold
  points: 6120
  pending: 0
  toNext: 3880 to Platinum
  expiring: none
redemption: Cabana upgrade - 2,500 points - balance after 3,620
```

#### Permissions

- `getLoyaltyPosition` → no permission · guest
- `listLoyaltyProgrammes` → `MARKETING_VIEW` (read) · staff, guest
- `listPromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `createReferral` → `MARKETING_MANAGE` (configure) · staff, guest
- `redeemLoyaltyPoints` → `LOYALTY_REDEEM` (operate) · staff, guest
- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous
- `recordRecommendationEvents` → `AI_USE` (operate) · staff, guest, anonymous
- `listRewards` → `MARKETING_VIEW` (read) · staff, guest
- `listCustomerBadges` → `MARKETING_VIEW` (read) · staff, guest
- `listLeaderboard` → no permission · guest
- `setLeaderboardNickname` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

54 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.41 | Loyalty Wallet - System shall support loyalty point storage. | Guest Mobile App & Branding | CONTRACTED | `getLoyaltyPosition` |
| 19.2.43 | Loyalty Balance - System shall display loyalty balances. | Guest Mobile App & Branding | CONTRACTED | `getLoyaltyPosition` |
| 1.1.56 | Loyalty point entitlement management | Ticketing Catalogue | CONTRACTED | `getLoyaltyPosition` |
| 5.4.4 | The system should support loyalty point system for balance enquiry operation which would capture the point balances in the guest profile and make them available to print in the receipt. | F&B & Guest Management | CONTRACTED | `getLoyaltyPosition` |
| 5.4.19 | Display balances, earning and redemption history. | F&B & Guest Management | CONTRACTED | `getLoyaltyPosition` |
| 5.4.30 | Maintain loyalty transaction history. | F&B & Guest Management | CONTRACTED | `getLoyaltyPosition` |
| 5.4.1 | The system should have the ability to integrate and exchange client information with a loyalty point system which will manage the loyalty points credited on to the loyalty account as per the … | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |
| 5.4.8 | Loyalty program data can be shared with a third party partner thanks to an API. For example, venue has an agreement with the airplane company Etihad allowing Etihad loyalty program members to spend … | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |
| 5.4.29 | Expose APIs for loyalty integrations. | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |
| 3.6.12 | The system should be able to manage all promotions in Backoffice application, where the positioning of the promotions fits in with the mechanics of the booking platform. In this way the Shop Cart is … | Admission and Access | CONTRACTED | `listPromotions` |
| 19.2.44 | Points Redemption - System shall support loyalty redemption. | Guest Mobile App & Branding | CONTRACTED | `redeemLoyaltyPoints` |
| 19.2.45 | Rewards Catalog - System shall provide rewards catalog access. | Guest Mobile App & Branding | CONTRACTED | `redeemLoyaltyPoints` |
| … 42 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Gamification shows badges/status tiers (e.g. Explorer, Adventurer, Legend) earned by spend or engagement thresholds, feeding the loyalty tier structure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-392)*
- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)*

Also apply: 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-043` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Summit Peaks → header 'At the venue' → Loyalty*. Differences: Placed inside the in-venue section; referral code appears under Account → Groups & invitations (YAML createReferral is here).
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (51 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Invite a friend, Redeem, Choose my name.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | body text on the background |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-009` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-009` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-009` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-009` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-009` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-009` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-009` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-009` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-009` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001`, `ADM-424` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Decided for every guest screen:** **No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; CHG-CSA-035). ***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 `powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036). **Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, scale, slide, blur or none, default rise): every customisation option of the approved wireframe (Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040). **Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template (`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).

**Never configurable:** A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P01 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P01 as a whole** (23: 3 open, 20 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- **A174** Cross-check the six previously-scoped wallet types against Allam's documentation and deliver the three wireframe flows (ticketing, F&B, retail) plus the revised B2C flow *(Chinmay Parab / Pradnya Yeram / Allam · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker)*
- … 9 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P01 Guest Web

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Qossai is dissatisfied with the current B2C guest platform build and wants a separate vision session; references: the "Little Explorer" site and Six Flags. Six Flags cues: single-page flow. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-736)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- A multi-language toggle switches the entire site's content. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-120)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- All sites are fully mobile-responsive; e.g. the desktop calendar view collapses into a mobile-optimized layout. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-113)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**26 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createInstalmentPlan": {"method":"POST","path":"/instalment-plans","contract":"payments","summary":"Split an order's payment into scheduled instalments on a stored card","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PayInstalmentPlan"},
"createReferral": {"method":"POST","path":"/referrals","contract":"marketing-crm","summary":"Issue a referral code","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Referral","responds":"Referral"},
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"deleteGuestAccount": {"method":"DELETE","path":"/auth/guest/account","contract":"identity","summary":"Self-service account deletion","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"enrolMfaMethod": {"method":"POST","path":"/auth/mfa/methods","contract":"identity","summary":"Enrol an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaEnrolment"},
"exportSubjectData": {"method":"POST","path":"/guests/{subjectId}/data-export","contract":"identity","summary":"Everything the platform holds about one guest","permission":"GUEST_VIEW_PII","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getBillingStatement": {"method":"GET","path":"/billing-statements/{statementId}","contract":"orders","summary":"One statement, with its lines","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"statementId","in":"path","required":true},{"name":"format","in":"query","required":null},{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"BillingStatement"},
"getCookieConsentRuntime": {"method":"GET","path":"/storefront/cookie-consent","contract":"marketing-crm","summary":"What the page must show and what it may load","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"channel","in":"query","required":true},{"name":"brandId","in":"query","required":false},{"name":"language","in":"query","required":false},{"name":"X-Consent-Key","in":"header","required":false}],"requestBody":null,"responds":"CookieConsentRuntime"},
"getDeviceConsentHistory": {"method":"GET","path":"/consent/device/history","contract":"marketing-crm","summary":"A visitor's own cookie decisions, oldest first","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"X-Consent-Key","in":"header","required":true},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getFacePassEnrolment": {"method":"GET","path":"/face-pass/enrolments/{enrolmentId}","contract":"access","summary":"Whether a pass has a face registered, and when","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FacePassEnrolment"},
"getGameCard": {"method":"GET","path":"/game-cards/{cardCode}","contract":"games","summary":"Read a card's balances","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameCard"},
"getGiftCard": {"method":"GET","path":"/gift-cards/{cardCode}","contract":"wallet","summary":"Check a gift card balance","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GiftCard"},
"getGuestConsents": {"method":"GET","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Read a guest's consent state","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConsentState"},
"getLoyaltyPosition": {"method":"GET","path":"/loyalty/position","contract":"marketing-crm","summary":"A guest's points, tier and what is within reach","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"programmeId","in":"query","required":true}],"requestBody":null,"responds":null},
"getMyMemberships": {"method":"GET","path":"/guests/me/memberships","contract":"catalogue","summary":"A guest's own memberships, benefits and history","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"includeLapsed","in":"query","required":null}],"requestBody":null,"responds":"GuestMembership"},
"getProduct": {"method":"GET","path":"/products/{productId}","contract":"catalogue","summary":"Read a product","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Product"},
"getWaiverStatus": {"method":"GET","path":"/guests/{subjectId}/waiver-status","contract":"marketing-crm","summary":"Whether this guest may be issued a ticket that requires a waiver","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":null}],"requestBody":null,"responds":null},
"getWallet": {"method":"GET","path":"/wallets/{subjectId}","contract":"wallet","summary":"Read a guest wallet","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"getWalletAutoReloadSetting": {"method":"GET","path":"/wallets/{walletId}/auto-reload","contract":"wallet","summary":"A wallet's own auto top-up, if the holder set one","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WalletAutoReloadSetting"},
"getWalletExitBalance": {"method":"GET","path":"/wallets/{walletId}/exit-balance","contract":"wallet","summary":"What the holder owes or is owed on leaving","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WalletExitBalance"},
"getWishlist": {"method":"GET","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Read a guest's saved items","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[],"requestBody":null,"responds":"Wishlist"},
"listBillingStatements": {"method":"GET","path":"/billing-statements","contract":"orders","summary":"What was charged, when, and against which agreement","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentPurposes": {"method":"GET","path":"/consent-purposes","contract":"marketing-crm","summary":"Configured consent purposes","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomerBadges": {"method":"GET","path":"/customers/{customerId}/badges","contract":"marketing-crm","summary":"Badges a guest holds","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"customerId","in":"path","required":true},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDelegations": {"method":"GET","path":"/guests/{subjectId}/delegations","contract":"identity","summary":"Who may act for this guest, and for whom they may act","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuestDevices": {"method":"GET","path":"/guests/{subjectId}/devices","contract":"marketing-crm","summary":"A guest's registered devices","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInstalmentPlans": {"method":"GET","path":"/instalment-plans","contract":"payments","summary":"Instalment plans and their schedules","permission":"PAYMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orderId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLeaderboard": {"method":"GET","path":"/loyalty/leaderboard","contract":"marketing-crm","summary":"Standings, by nickname","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"programmeId","in":"query","required":true},{"name":"window","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLoyaltyProgrammes": {"method":"GET","path":"/loyalty/programmes","contract":"marketing-crm","summary":"List loyalty programmes","permission":"MARKETING_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listMyEntitlements": {"method":"GET","path":"/guests/me/entitlements","contract":"access","summary":"Every ticket, pass and membership this guest holds","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"state","in":"query","required":null},{"name":"includeShared","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyPaymentIssues": {"method":"GET","path":"/guests/me/payment-issues","contract":"payments","summary":"A guest's own failed recurring payments","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPaymentTokens": {"method":"GET","path":"/payment-tokens","contract":"orders","summary":"A guest's saved payment methods","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromotions": {"method":"GET","path":"/promotions","contract":"promotions","summary":"List promotions","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedTrackingTechnologies": {"method":"GET","path":"/storefront/cookie-consent/technologies","contract":"marketing-crm","summary":"The approved cookie registry, as the preference centre shows it","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"channel","in":"query","required":true},{"name":"category","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRewards": {"method":"GET","path":"/loyalty/rewards","contract":"marketing-crm","summary":"What points can be turned into","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWalletTransactions": {"method":"GET","path":"/wallets/{subjectId}/transactions","contract":"wallet","summary":"Wallet transaction history","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordConsent": {"method":"POST","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Record a consent decision","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordConsentRequest","responds":"ConsentState"},
"recordDeviceConsent": {"method":"POST","path":"/consent/device","contract":"marketing-crm","summary":"Record a visitor's cookie decision, before anyone is known","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordDeviceConsentRequest","responds":"DeviceConsent"},
"recordRecommendationEvents": {"method":"POST","path":"/recommendations/events","contract":"ai","summary":"Report what happened to recommended items","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"redeemLoyaltyPoints": {"method":"POST","path":"/loyalty/redemptions","contract":"marketing-crm","summary":"Spend points","permission":"LOYALTY_REDEEM","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LoyaltyPosition"},
"removeMfaMethod": {"method":"DELETE","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Remove an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"retryMyDunningPayment": {"method":"POST","path":"/dunning-cases/{caseId}/retry","contract":"payments","summary":"Retry a declined membership payment now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"caseId","in":"path","required":true}],"requestBody":"RetryDunningPaymentRequest","responds":"DunningCase"},
"revokeFacePass": {"method":"DELETE","path":"/face-pass/enrolments/{enrolmentId}","contract":"access","summary":"Remove a facial profile","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"revokeGuestDevice": {"method":"DELETE","path":"/guests/{subjectId}/devices/{deviceId}","contract":"marketing-crm","summary":"Revoke a device registration","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setLeaderboardNickname": {"method":"PUT","path":"/loyalty/leaderboard-nickname","contract":"marketing-crm","summary":"Choose the name shown on the board","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LoyaltyPosition"},
"setWalletAutoReloadSetting": {"method":"PUT","path":"/wallets/{walletId}/auto-reload","contract":"wallet","summary":"Top the wallet up automatically from a stored card when it runs low","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletAutoReloadSetting","responds":"WalletAutoReloadSetting"},
"settleWalletAtExit": {"method":"POST","path":"/wallets/{walletId}/exit-settlement","contract":"wallet","summary":"Settle a short balance, or refund a credit, when the holder leaves","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletExitSettlement"},
"storePaymentToken": {"method":"POST","path":"/payment-tokens","contract":"orders","summary":"Save a payment method for future use","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentToken"},
"transferWalletBalance": {"method":"POST","path":"/wallets/{walletId}/transfer","contract":"wallet","summary":"Send balance to another guest","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletTransaction"},
"verifyMfaEnrolment": {"method":"POST","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Complete enrolment","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaMethod"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiRecommendationItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList","description":"One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).","required":["trackingId","rank"],"properties":{"trackingId":{"type":"string","format":"uuid","description":"Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."},"couponRef":{"type":"string","nullable":true,"description":"For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."},"rewardId":{"type":"string","format":"uuid","nullable":true,"description":"For `reward`, a marketing-crm loyalty reward the guest can redeem."},"challengeId":{"type":"string","format":"uuid","nullable":true,"description":"For `challenge`, a marketing-crm challenge the guest can join."},"kind":{"type":"string","enum":["upsell","crossSell","upgrade","bundle","addOn","membership","nextBestOffer","offer","reward","challenge"]},"rank":{"type":"integer","minimum":1},"priceRef":{"type":"string","nullable":true,"description":"The Pricing reference the channel resolves to a price. AI never computes a price."},"reasonTemplateKey":{"type":"string","nullable":true,"description":"The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."},"reasonText":{"type":"string","nullable":true,"description":"The rendered template in the session locale, where the channel shows reasons."},"confidenceBand":{"type":"string","enum":["high","medium","low"],"description":"Design 5.6: a band, never a bare percentage."},"score":{"type":"number","nullable":true,"description":"Normalised score. **Returned to staff callers only**; a guest response omits it."}}},
"AiRecommendationResult": {"type":"object","x-ticvai-persistence":"none — written as ai.rec_decision after the response","description":"The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.","required":["decisionId","mode","items","expiresAt"],"properties":{"decisionId":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"]},"items":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationItem"}},"expiresAt":{"type":"string","format":"date-time"}}},
"BillingStatement": {"x-ticvai-persistence":"none — computed from orders.payment and payments.dunning_case","type":"object","description":"2.14.19-2.14.23, 5.7.96, BL-100. **What a guest was charged over a period, and deliberately not a tax document.**\n**Computed rather than stored**, because a statement assembled at read time cannot disagree with the ledger it describes. A stored statement is a second source of truth about money, and the package already has one of those.\n","required":["id","periodStart","periodEnd","total","isTaxInvoice"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","readOnly":true},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/BillingStatementLine"}},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"pdfUrl":{"type":"string","format":"uri","nullable":true,"readOnly":true,"description":"Set when `getBillingStatement` is called with `format=pdf`; a short-lived link. The PDF is a statement, not a tax invoice; the tax invoices for its charges are linked per line."},"isTaxInvoice":{"type":"boolean","default":false,"readOnly":true,"description":"**Always false, and stated rather than assumed.** UAE e-invoicing is Peppol five-corner with the FTA as the fifth corner, PINT AE XML and 51 mandatory fields; **CF-133 is open on it and AED 50m+ businesses must appoint an accredited service provider by 30 October 2026.** A statement that implied it was a tax invoice would be wrong in the one direction that has a regulator at the end of it.\n"}}},
"BillingStatementLine": {"type":"object","description":"BL-100. **One charge, refund or failed attempt.** Failures are lines rather than omissions — a statement showing only what succeeded cannot explain why a pass lapsed.\n","required":["occurredAt","kind","amount"],"properties":{"occurredAt":{"type":"string","format":"date-time"},"kind":{"type":"string","enum":["charge","refund","failedAttempt","adjustment"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"description":{"type":"string"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxRate":{"type":"number","nullable":true,"description":"2.14.23. The VAT rate the charge was posted with; `amount` is the gross."},"taxInvoiceId":{"type":"string","format":"uuid","nullable":true,"description":"The finance tax invoice issued for this charge, where one was (`issueTaxInvoice`); the guest downloads it with `getTaxDocumentRendition`."},"declineClass":{"type":"string","nullable":true,"description":"**Present on `failedAttempt` only**, and it is what turns *\"your payment failed\"* into something a guest can act on: a soft decline means try again, a hard one means the card needs replacing.\n"}}},
"BiometricKind": {"type":"string","description":"BL-106, CF-35. **Two different legal postures, not two settings on one record.** 3.2.44 describes a temporary facial model taken at a counter or a gate and deleted when the ticket expires; 3.2.43 describes an enduring Face Pass enrolled deliberately on three surfaces. **Storing both as one record with a date makes the stricter rule depend on a field nobody enforces**, which is what BL-106 was raised to stop.\n`facePass` — enduring, explicit consent, revocable by the guest, anchored to the validity of the entitlement it belongs to.\n`faceTag` — same-visit, **consent still explicit and still recorded**, anchored to the ticket and purged at close of the operating day. **PDPL Article 4 is a closed list of exceptions with no legitimate-interests basis**, so a short life does not remove the need for consent — it only shortens what the consent is for.\n","enum":["facePass","faceTag"]},
"BiometricRetentionAnchor": {"type":"string","readOnly":true,"description":"BL-106, ADR-0047. **What the expiry is measured from, derived from the kind rather than chosen.** A retention period a person can type is a retention period somebody will type wrongly; the anchor follows the kind, and the kind follows how the biometric was taken.\n`entitlementValidity` — `facePass`. The face cannot outlive the pass it was enrolled for.\n`ticketValidity` — `faceTag` against a dated ticket.\n`operatingDayClose` — `faceTag` where the ticket has no end of its own, plus `VenueSettings.biometrics.faceTagPurgeMinutesAfterClose`.\n","enum":["entitlementValidity","ticketValidity","operatingDayClose"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentPurposeConfig": {"x-ticvai-persistence":"marketing.consent_purpose + marketing.consent_purpose_channel","type":"object","required":["purpose","channels","noticeVersion","isRequiredForService"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"displayName":{"type":"string"},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","description":"Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"},"isRequiredForService":{"type":"boolean","description":"True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"},"expiresAfterMonths":{"type":"integer","nullable":true}}},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"CookieBannerPreferenceCenterDesignerView": {"type":"object","x-ticvai-persistence":"marketing.cookie_banner_design","description":"One version of a cookie banner and preference-centre design (pack 17.1.6).","required":["channel","position","languages","rejectIsOneClick","categories"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"Null for the corporate design every brand inherits."},"inheritsFromId":{"type":"string","format":"uuid","nullable":true},"channel":{"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"]},"logoAssetId":{"type":"string","format":"uuid","nullable":true},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"position":{"type":"string","enum":["top","bottom","popup","modal"]},"themeId":{"type":"string","nullable":true,"description":"The white-label theme it takes colours and fonts from."},"buttons":{"type":"array","items":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["acceptAll","rejectNonEssential","managePreferences","savePreferences","doNotSellOrShare"]},"label":{"$ref":"#/components/schemas/LocalisedText"}}}},"rejectIsOneClick":{"type":"boolean","default":true,"description":"Must be true."},"links":{"type":"array","items":{"type":"object","required":["label","policyKind"],"properties":{"label":{"$ref":"#/components/schemas/LocalisedText"},"policyKind":{"type":"string","enum":["privacy","cookie","termsAndConditions"]}}}},"categories":{"type":"array","minItems":1,"items":{"type":"object","required":["category","defaultOn"],"properties":{"category":{"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"]},"description":{"$ref":"#/components/schemas/LocalisedText"},"defaultOn":{"type":"boolean","description":"True only for `strictlyNecessary`, which is always active."}}}},"languages":{"type":"array","minItems":1,"items":{"type":"string","maxLength":10},"description":"Every language the storefront serves; Arabic renders right to left."},"regulatoryRegimes":{"type":"array","items":{"type":"string","enum":["gdpr","ePrivacy","ccpaCpra","lgpd","uaePdpl","saudiPdpl"]},"description":"2.6.60 (29 September, build). **The laws this design is published to satisfy**, so compliance is stated rather than assumed. The strictest posture (opt-in, one-click reject, every non-essential category off) already meets GDPR/ePrivacy, LGPD and both PDPLs; `ccpaCpra` adds the \"Do not sell or share\" button (`doNotSellOrShare`) and honours a Global Privacy Control signal as that opt-out."},"recordIpAddress":{"type":"boolean","default":false,"description":"2.6.55, \"if legally permitted\" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. Off by default."},"noticeVersion":{"type":"string","readOnly":true,"description":"Moves with the cookie policy (white-label `setPolicy`, kind `cookie`)."},"version":{"type":"integer","minimum":1,"readOnly":true},"status":{"type":"string","enum":["draft","published","superseded"],"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CookieCategory": {"type":"string","enum":["strictlyNecessary","functional","analytics","personalisation","marketing"],"description":"2.6.53. The five categories the banner design (`CookieBannerPreferenceCenterDesignerView.categories`) offers; the matrix's \"preference\" category is `personalisation` (British spelling, as `ConsentPurpose`)."},
"CookieConsentChannel": {"type":"string","enum":["b2cWebsite","customerPortal","mobileApp","embeddedCheckout","whiteLabelSite","partnerMicrosite"],"description":"The six governed surfaces, as the registry and the banner design name them (pack 17.1.5-17.1.6)."},
"CookieConsentRuntime": {"type":"object","x-ticvai-persistence":"none — assembled at read time from marketing.cookie_banner_design, marketing.tracking_technology and marketing.device_consent","description":"What `getCookieConsentRuntime` gives the storefront tag loader and the app SDK gate (2.6.52, 2.6.58).","required":["banner","noticeVersion","requiresDecision","allowedTechnologies","consentModeSignals"],"properties":{"banner":{"$ref":"#/components/schemas/CookieBannerPreferenceCenterDesignerView"},"noticeVersion":{"type":"string"},"requiresDecision":{"type":"boolean","description":"True with no decision, an expired one, or one given against a superseded notice."},"decision":{"allOf":[{"$ref":"#/components/schemas/DeviceConsent"}],"nullable":true,"description":"The latest decision for the presented key; null without a key."},"allowedTechnologies":{"type":"array","description":"Per category, the approved technologies it unlocks. Anything not listed never loads.","items":{"type":"object","required":["category","technologies"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"granted":{"type":"boolean","description":"Whether the presented decision grants it; always true for `strictlyNecessary`."},"technologies":{"type":"array","items":{"type":"object","required":["name","provider"],"properties":{"name":{"type":"string"},"provider":{"type":"string"},"technologyType":{"type":"string"}}}}}}},"consentModeSignals":{"type":"object","description":"**The decision in Google consent-mode terms** (2.6.65), so Analytics and Tag Manager are told, not left to guess. `denied` wherever no decision grants the category.","properties":{"adStorage":{"type":"string","enum":["granted","denied"]},"adUserData":{"type":"string","enum":["granted","denied"]},"adPersonalization":{"type":"string","enum":["granted","denied"]},"analyticsStorage":{"type":"string","enum":["granted","denied"]},"functionalityStorage":{"type":"string","enum":["granted","denied"]},"personalizationStorage":{"type":"string","enum":["granted","denied"]},"securityStorage":{"type":"string","enum":["granted"]}}}}},
"CreatePromotionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","discount","validFrom"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$"},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"allOf":[{"$ref":"#/components/schemas/StackingMode"}],"default":"bestOnly"},"stackingGroup":{"type":"string","maxLength":64},"precedence":{"type":"integer","default":0,"description":"Higher evaluates first where several could apply."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptions":{"type":"integer","nullable":true},"maxRedemptionsPerGuest":{"type":"integer","nullable":true},"budgetCap":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Total discount value after which the promotion stops automatically. **Enforced at checkout**, where an order whose discount would take the total past the cap does not receive the promotion (decided 28 September, audit R101)."},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) this promotion belongs to; null for a promotion run on its own. The directory, calendar and campaign budget screens group by it. (DM5, 29 September: data model for the agreed operations)"},"recommendable":{"type":"boolean","default":false,"description":"**May the recommendation engine show this offer to a guest** (8.6.30 to 8.6.36; 29 September, build pass, group G2, from group G1's handoff). False keeps a promotion to the basket, where `evaluatePromotions` applies it as before. True makes a live promotion a candidate item of kind `offer` in `ai.decideRecommendations` for the guests its conditions and `recommendableSegmentIds` admit: while it is live, `promotions.recommendationStrategyPublished` (kind `offers`) keeps the engine's candidate cache current, and it leaves the cache when it is paused, ends or expires. **The engine shows the offer; the discount is still computed here at the basket**, never by ai."},"recommendableSegmentIds":{"type":"array","nullable":true,"description":"The marketing-crm segments the offer may be recommended to; null means every guest its own conditions admit.","items":{"type":"string","format":"uuid"}}}},
"DeclineClass": {"type":"string","description":"BL-100. **Whether a failed charge may be tried again at all**, and the distinction is a merchant-account risk rather than a courtesy.\n`soft` — insufficient funds, a temporary hold, an issuer timeout. **Worth another attempt on another day**, and the whole reason a dunning schedule exists.\n`hard` — closed account, stolen card, do-not-honour, invalid number. **Never retried.** A hard decline put on a timetable is how a merchant ID gets flagged by the scheme, and the venue finds out when its acquirer calls.\n`unknown` — the provider gave no usable code. **Treated as `hard`**, because guessing `soft` optimises for one more attempt and risks the thing that cannot be undone.\n","enum":["soft","hard","unknown"]},
"DelegatedAccess": {"x-ticvai-persistence":"identity.delegated_access","type":"object","required":["id","permission","scopePath","effect"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid","nullable":true},"roleId":{"type":"string","format":"uuid","nullable":true},"permission":{"type":"string","description":"From the permission enum. `*` permitted on DENY only."},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"CF-132, CL-05. **A grant held by a guest rather than a staff principal.**\nSection 5.5 asks for portfolios — a primary holder assigning entitlements, transfer between linked accounts, shared wallets with individual tracking — and it appears ten times across ten sections. **Every one of those reduces to the same question: who may act on whose behalf, over what, and until when.**\n**That is a grant, not a household table.** A primary holder assigning an entitlement is a grant. A group leader holding tickets for twelve is a grant. A corporate account enrolling members is a grant with a quota. **A shared wallet with individual tracking is a grant over a balance, and the transaction log already records who spent.**\n**A household table would answer one of those four.**\n"},"overSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"Whose behalf. **Null for a staff grant, which is the existing behaviour** — every grant written before 18 August means exactly what it meant before.\n"},"overObjectRef":{"type":"string","nullable":true,"description":"**Where the authority is over a thing rather than a scope** — a wallet, an entitlement, a booking. `scopePath` answers *where*; this answers *what*, and a guest's authority is almost always over a specific object rather than a branch of the tree.\n"},"delegationKind":{"type":"string","nullable":true,"enum":["primaryHolder","familyMember","groupLeader","attendee","corporateAdmin","corporateMember","carer"],"description":"**What kind of relationship this expresses**, for display and for reporting. The mechanism does not branch on it — a family member and a group attendee are the same grant with different words around them, which is the point.\n"},"quota":{"type":"integer","nullable":true,"description":"2.14.15 and 4.3.11. **How many the holder may assign.** A corporate account with fifty allocations and a family with four are the same structure with different numbers.\n"},"isRevocableBySubject":{"type":"boolean","default":true,"description":"**Whether the person it is over can end it.** A guest who linked a family member should be able to unlink them; a corporate member should not be able to revoke their employer's oversight — and **a delegation nobody can end is a delegation somebody will regret.**\n"},"scopePath":{"type":"string"},"effect":{"type":"string","enum":["ALLOW","DENY"]},"permissionId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from `identity.user_access`, 20 September, when that table was collapsed into this one.** `permission` above is free text; this names a row in `identity.permission`, the catalogue wired the same day. A grant that names a catalogue row can be checked against the keys the contracts actually enforce — which is the whole point of a catalogue that reported *154 on operations, 35 in roles.yaml, 0 shared*.\nNullable because a role grant carries no permission at all.\n"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Taken from `identity.user_access`. This table recorded `revokedBy` and not when, so it could say who revoked a grant and not whether it was before or after the thing somebody is asking about.\n"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"DeviceConsent": {"type":"object","x-ticvai-persistence":"marketing.device_consent + marketing.device_consent_category","description":"**One cookie decision by a visitor nobody has identified yet** (BL-073 §4b, decided 29 September). Append-only: a change of mind is a new row. Keyed for the visitor by `consentKey`, which the platform mints; the categories are child rows. The IP address and user agent, where recorded at all, are in `pii.consent_identifier` (`ConsentCaptureIdentifier`), never here.","required":["consentKey","channel","action","categories","noticeVersion","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"consentKey":{"type":"string","maxLength":64,"readOnly":true,"description":"**Opaque, minted by us, not a device fingerprint.** It answers 2.6.55's \"user identifier/session ID\" and is the join key `claimDeviceConsent` needs. Shared by all the tenant's domains (2.6.62), never across tenants."},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"brandId":{"type":"string","format":"uuid","nullable":true},"bannerDesignId":{"type":"string","format":"uuid","nullable":true,"description":"The published `CookieBannerPreferenceCenterDesignerView` version the visitor was shown."},"action":{"$ref":"#/components/schemas/DeviceConsentAction"},"categories":{"type":"array","minItems":1,"description":"Every category of the design, with the decision this row gives it.","items":{"type":"object","required":["category","decision"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"decision":{"type":"string","enum":["granted","declined"]}}}},"noticeVersion":{"type":"string","description":"The cookie notice version decided against (white-label `setPolicy`, kind `cookie`)."},"language":{"type":"string","maxLength":10,"nullable":true},"globalPrivacyControl":{"type":"boolean","default":false,"description":"The browser sent a Global Privacy Control signal; honoured as a CCPA/CPRA opt-out of sale and sharing."},"source":{"$ref":"#/components/schemas/ConsentSource"},"country":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true,"readOnly":true,"description":"The edge's geolocation of the request, for the geographic statistics (2.6.63). The address is not kept here."},"decidedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A device consent expires and a subject consent does not.** Set from the tenant's device-consent term; after it the banner asks again."},"claimedBySubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Set once, by `claimDeviceConsent`. Never cleared."},"claimedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), tenant-scoped: a decision with no subject still belongs to one tenant."}}},
"DeviceConsentAction": {"type":"string","enum":["acceptAll","rejectNonEssential","savePreferences","withdraw","doNotSellOrShare"],"description":"What the visitor pressed. `doNotSellOrShare` is the CCPA/CPRA opt-out link, shown where the design's `regulatoryRegimes` include `ccpaCpra`."},
"Discount": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","required":["kind"],"properties":{"kind":{"$ref":"#/components/schemas/DiscountKind"},"percentage":{"type":"number","minimum":0,"maximum":100},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fixedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"buyQuantity":{"type":"integer","minimum":1},"getQuantity":{"type":"integer","minimum":1},"getDiscountPercentage":{"type":"number","minimum":0,"maximum":100,"description":"100 makes the free items actually free; lower values give a partial discount."},"tiers":{"type":"array","description":"For `tieredPercentage` — more units, larger discount.","items":{"type":"object","required":["minQuantity","percentage"],"properties":{"minQuantity":{"type":"integer","minimum":1},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"maxDiscountAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Cap on a percentage discount. Prevents an unbounded discount on a large basket."},"rewardVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (createPromotion; the builders setGiftFreeProduct and setBuyGetBogo were retired in r2, CHG-CLN-001). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"},"maxApplicationsPerBasket":{"type":"integer","minimum":1,"nullable":true,"description":"How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (createPromotion; setFixedPriceOffer was retired in r2, CHG-CLN-001). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"}}},
"DunningCase": {"x-ticvai-persistence":"payments.dunning_case","type":"object","description":"BL-100. **One recurring charge being chased**, and the row a venue works from.\n","required":["id","state","attemptsMade","firstFailedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"orderId":{"type":"string","description":"The order whose renewal failed."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"state":{"$ref":"#/components/schemas/DunningState"},"declineClass":{"allOf":[{"$ref":"#/components/schemas/DeclineClass"}],"description":"**From the most recent attempt.** A case that begins `soft` and turns `hard` stops immediately rather than finishing its schedule — the card changed underneath it.\n"},"attemptsMade":{"type":"integer"},"nextAttemptAt":{"type":"string","format":"date-time","nullable":true,"description":"**Null where the case has ended or the decline is hard.** A scheduled time on a case nothing will act on is the field that makes a queue untrustworthy.\n"},"firstFailedAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true},"resolution":{"type":"string","nullable":true,"enum":["paidByOtherMeans","cardReplaced","writeOff","cancelledByGuest",null]},"resolutionNote":{"type":"string","nullable":true,"maxLength":500,"description":"**What `resolveDunningCase` was told, which had nowhere to land until now.** The enum above tells `writeOff` from `cardReplaced`; **which invoice, whose phone call and on what authority is the sentence beside it**, and the operation's own reasoning — that these reasons must be told apart afterwards — only works if the sentence survives.\n**Same shape as `marketing.case.resolution_note`**, which is a RAG source for exactly this reason: a resolution note is the most useful free text a support record holds.\n"},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who closed it.** A write-off with no name against it is the one resolution nobody can follow up, and it is also the one that moves money.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Written at `venue` scope.\n"}}},
"DunningState": {"type":"string","enum":["scheduled","inProgress","exhausted","recovered","resolvedManually"],"description":"BL-100. **`exhausted` and `recovered` are both endings and only one of them is a failure.** A schedule with a single terminal state cannot tell a venue whether dunning is working, which is the only question a venue asks of it.\n"},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). **Null for an entitlement an invitation issued** (`invitationId`; 4 October 2026, CHG-FXC-007)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"firstEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232; CHG-CSP-030). A replayed earlier scan moves it back."},"timeBoundUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Where the template is time-bound, when its window closes**: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 October 2026, Chinmay, BO-159; DEC-232; CHG-CSP-030). Null until the first scan and on an entitlement with no time bound. A scan after it is denied (`timeBoundWindowElapsed`); it never extends `validTo`, and the earlier of the two wins."},"lifecycleLabel":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"**The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\", and BO-336/DI-670: \"Reserved maps to Pending fulfilment\"; DEC-266; CHG-CSP-033). Computed on read from `status` (orders `EntitlementStatus`), `suspendedReason`, `cancellationKind`, `issuedVia` and an active identity lock; the mapping is in `states/entitlement-status.yaml`. It is what BO-334, BO-336 and the ticket status transition matrix (`AccessTicketStatusTransition`) show; logic still reads `status`."},"cancellationKind":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","enum":["voided","refunded","performanceCancelled","superseded"],"description":"**Which act cancelled the entitlement**, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one r1 value `cancelled` (DEC-266; CHG-CSP-033). Written with the cancelling transition: `voidEntitlement`, `createRefund`, `cancelPerformance`, or a reissue that supersedes it (`supersedesEntitlementId` on the new one). Null unless `cancelled`."},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"},"invitationId":{"type":"string","format":"uuid","nullable":true,"description":"**The invitation that issued it** (4 October 2026, CHG-FXC-007): `orders.issueInvitation` issues the entitlement without an order, because an invitation never enters the order path. Exactly one of `orderId` and `invitationId` is set."}}},
"FacePassEnrolment": {"type":"object","x-ticvai-persistence":"pii.subject_biometric","description":"3.2.43. **Metadata about a facial profile. Never the profile.**\n","required":["id","kind","subjectId","entitlementId","source","capturedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid"},"entitlementId":{"type":"string","format":"uuid","description":"The `Entitlement.id`, a UUIDv7 (`pii.subject_biometric.entitlement_id`)."},"kind":{"$ref":"#/components/schemas/BiometricKind"},"retentionAnchor":{"allOf":[{"$ref":"#/components/schemas/BiometricRetentionAnchor"}],"x-ticvai-derived":"onWrite","description":"BL-106. **Derived from `kind`, never sent.** `facePass` anchors to the entitlement, `faceTag` to the ticket or to the close of the operating day.\n"},"source":{"type":"string","enum":["guestApp","ticketCounter","annualPassCounter","entryGate"],"description":"**`entryGate` is valid for `faceTag` only**, and 3.2.43's omission of it from Face Pass is deliberate: an enduring enrolment is a considered act with consent attached, not something done in a queue. 3.2.44 puts a Face Tag at a gate precisely because it dies the same day.\n**A self-service kiosk enrolment reads `ticketCounter` here** (an on-site enrolment) so the r1 values stand; the precise channel is `enrolmentChannel` (DEC-236; CHG-CSP-021).\n"},"enrolmentChannel":{"type":"string","readOnly":true,"enum":["guestApp","ticketCounter","annualPassCounter","selfServiceKiosk","entryGate"],"description":"**Where the face was actually captured** (decided 2 October 2026, Chinmay, BO-186; DEC-236; CHG-CSP-021): `source` with `selfServiceKiosk` told apart. `entryGate` for a Face Tag only.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The venue's consent form the capture was consented on, and its version below (DEC-128; CHG-CSP-018)."},"consentFormVersion":{"type":"integer","nullable":true,"readOnly":true},"capturedAt":{"type":"string","format":"date-time"},"consentPurposeId":{"type":"string","format":"uuid"},"consentGivenAt":{"type":"string","format":"date-time"},"guardianSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"Where the subject is a minor (3.2.12)."},"isActive":{"type":"boolean","readOnly":true},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**Bounded by whatever `retentionAnchor` names**, and a face outliving it is a biometric held for no stated purpose.\n**Settled 20 September by ADR-0047**, which CF-64 had been carrying since 6 August: a `facePass` cannot outlive its entitlement and a `faceTag` does not survive the close of the operating day. **These are ceilings rather than defaults** — they cannot be configured upward, because a retention that a tenant can extend without limit is the breach ADR-0047 gave the platform a ceiling to prevent.\n"}}},
"GameCard": {"x-ticvai-persistence":"games.card","type":"object","required":["cardCode","venueId","credits","bonusCredits","points","status","issuedAt"],"properties":{"cardCode":{"type":"string","description":"**A pre-printed card keeps the code printed on it. A generated code** (a digital card, or a card issued with no printed code) **is the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of that sequence, so a card issued offline takes its code at once. Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"credits":{"type":"integer","description":"Bought with money. Buys plays."},"bonusCredits":{"type":"integer","description":"From a promotion. Typically non-refundable and spent before paid credits.\n"},"points":{"type":"integer","description":"Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"},"status":{"type":"string","enum":["active","blocked","expired","transferred"]},"blockedReason":{"type":"string","nullable":true},"transferredToCardCode":{"type":"string","nullable":true},"lastPlayedAt":{"type":"string","format":"date-time","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**The card's own id** (4 October 2026, CHG-FXC-006): the `{cardId}` of `setGameCardLifecycle`, which had no column to match, and the `id` of the Wallet view `wallet.loadGameCredits` and `wallet.adjustGameCard` return for a card with no wallet."},"walletId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Where the card's credits are held** (4 October 2026, CHG-FXC-006). Set when the card is registered to a guest who has a wallet: credits loaded to it are wallet credit lots. Null for an anonymous card, whose credits are held on the card row itself (`credits`, `bonusCredits`)."}}},
"GiftCard": {"x-ticvai-persistence":"wallet.gift_card","type":"object","required":["cardCode","faceValue","balance","status","issuedAt"],"properties":{"cardCode":{"type":"string"},"kind":{"type":"string"},"faceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["issued","active","partiallyRedeemed","redeemed","expired","blocked"]},"blockedReason":{"type":"string","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},
"GuestDevice": {"type":"object","x-ticvai-persistence":"marketing.guest_device","required":["id","subjectId","platform","status","registeredAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"platform":{"type":"string","enum":["ios","android","web"]},"tokenFingerprint":{"type":"string","description":"Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"},"tokenRef":{"type":"string","writeOnly":true,"description":"**A vault reference to the push token**, written by the server from `registerGuestDevice.token` — the same pattern as `PaymentProvider.credentialRef`. Never the token and never returned; the sender resolves it at send time. Without it a registered device could not be sent to.\n"},"appVersion":{"type":"string","nullable":true},"osVersion":{"type":"string","nullable":true},"deviceModel":{"type":"string","nullable":true},"locale":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","revoked","failed"]},"failureCount":{"type":"integer","description":"Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"},"registeredAt":{"type":"string","format":"date-time"},"lastSeenAt":{"type":"string","format":"date-time","nullable":true},"revokedAt":{"type":"string","format":"date-time","nullable":true}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuestMembership": {"type":"object","description":"19.2.26 to 19.2.28. **A view, not a table** — assembled from the entitlement, the product that granted it and the order that bought it.\n","required":["entitlementId","productId","name","status"],"properties":{"entitlementId":{"type":"string","format":"uuid","description":"The `access.Entitlement.id` this membership is — a UUIDv7, like every entitlement id."},"productId":{"type":"string","format":"uuid"},"name":{"type":"string"},"tier":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","frozen","suspended","expired","cancelled"],"description":"**Derived from the entitlement, not held here.** This schema is a view assembled from the entitlement, the product that granted it and the order that bought it — the lifecycle lives in `states/entitlement-status.yaml` and `frozen` is what `freezeEntitlement` sets.\nNo state model of its own, deliberately: **two models over one lifecycle drift.**\n"},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date"},"frozenDays":{"type":"integer","description":"Days lost to a freeze and added back to `validTo`. **Shown because a guest who paused a pass will check the maths**, and a validity date that moved without explanation is a support call.\n"},"benefits":{"type":"array","description":"5.4.31. From the product's entitlement template. **Traceable to what grants them**, so a gate can honour what the app promised.\n","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"value":{"type":"string","nullable":true}}}},"renewsOn":{"type":"string","format":"date","nullable":true},"previousTerms":{"type":"array","description":"Prior terms, including lapsed ones.","items":{"type":"object","properties":{"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date"},"endedBecause":{"type":"string","enum":["expired","renewed","cancelled","upgraded"]}}}}}},
"GuestPromotion": {"x-ticvai-persistence":"none — guest projection of promotions.promotion","type":"object","description":"**What a guest may see of a promotion.** `Promotion` carries the commercial internals (`budgetCap`, `maxRedemptions`, `redemptionCount`, `discountGiven`, `precedence`, `stackingGroup`), and `listPromotions` and `getPromotion` are guest-audience. A guest caller receives this shape instead. `additionalProperties: false` is the point: a server that adds an internal field to it fails validation instead of publishing the field.\n","additionalProperties":false,"required":["id","code","name","discount","validFrom"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"$ref":"#/components/schemas/StackingMode"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptionsPerGuest":{"type":"integer","nullable":true}}},
"LeaderboardEntry": {"x-ticvai-persistence":"none — computed from marketing.loyalty_position","type":"object","description":"22.6. **One row of a leaderboard, and deliberately not enough to identify anybody.** There is no `subjectId` here and that is the whole design: a nickname beside a resolvable identifier protects nothing.\n","required":["rank","nickname","points"],"properties":{"rank":{"type":"integer","minimum":1},"nickname":{"type":"string","description":"**Always present, and never their real name.** The guest's chosen `leaderboardNickname` where they have set one, and otherwise a generated `Player-4821`.\n**Not nullable, because a rank with no name is a hole on the board.** The first cut of this returned null and left second place reading as a dash, which tells somebody they do not count every time they look — and being on the board is the whole point of the board.\n**Generated from the loyalty position's own id**, not from the subject id and not from a counter: it is stable across months, so the same guest is the same `Player-N` and can be congratulated by it, and it carries nothing — no rank, no join date, and no sequence anybody can count backwards from to learn how many guests a programme has.\n"},"points":{"type":"integer"},"isMe":{"type":"boolean","default":false,"description":"**How a client highlights the caller's own row without learning who anybody else is.** The alternative — returning identifiers and letting the client match — is the disclosure this schema exists to avoid.\n"}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"LoyaltyProgramme": {"x-ticvai-persistence":"marketing.loyalty_programme + marketing.points_earning_rule + marketing.programme_tier","type":"object","required":["id","code","name","earnRules","tiers"],"properties":{"tiers":{"type":"array","description":"**Rows of `marketing.programme_tier`**, the same shape `MarketingProgrammeTier` has — one definition of a tier, not a second copy that cannot round-trip. `loyaltyProgrammeId` and `id` are the server's on create.\n","items":{"$ref":"#/components/schemas/MarketingProgrammeTier"}},"id":{"readOnly":true,"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused with `409 duplicate-code`.\n"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"pointsLiabilityAccountId":{"type":"string","format":"uuid","description":"Points post here on accrual. They are a liability from the moment they are earned, not from the moment they are spent.\n"},"earnRules":{"type":"array","items":{"type":"object","required":["trigger","points"],"properties":{"trigger":{"type":"string","enum":["perCurrencyUnit","perVisit","perProduct","onSignup","onBirthday","onReview"]},"points":{"type":"number"},"productKinds":{"type":"array","description":"Limits a `perProduct` or `perCurrencyUnit` rule to these kinds. Empty means every kind.","items":{"$ref":"../spine/catalogue.yaml#/components/schemas/ProductKind"}},"multiplier":{"type":"number"}}}},"pointsExpireAfterMonths":{"type":"integer","nullable":true},"isActive":{"type":"boolean"}}},
"MarketingCustomerBadge": {"type":"object","x-ticvai-persistence":"marketing.customer_badge","description":"**Taken from the backend workbook, 20 September.** Stores badges actually awarded to customers and the source that generated each award.","required":["customerId","badgeId","awardedAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"customerId":{"type":"string","format":"uuid"},"badgeId":{"type":"string","format":"uuid"},"challengeId":{"type":"string","format":"uuid","nullable":true},"sourceType":{"type":"string","maxLength":30,"nullable":true},"sourceReferenceId":{"type":"string","format":"uuid","nullable":true},"awardedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","maxLength":20}}},
"MarketingProgrammeTier": {"type":"object","x-ticvai-persistence":"marketing.programme_tier","description":"**The tier definition decision 8 promised and nobody built.** `marketing.loyalty_position` carried `tierCode`, `tierName` and `pointsToNextTier` as denormalised strings and a number, with no table saying what tiers exist or what each one requires — so `pointsToNextTier` was computed from a threshold that lived nowhere.\n**Not named `marketing.loyalty_tier`**: that name is recorded in `schema-history.json` as renamed to `marketing.points_earning_rule` on 20 September, and a rename record that contradicts the schema is worse than a longer name. Not named `marketing.tier` either, because `subscription.tier_allowance` is a SaaS plan's tier and one bare `tier` in a package with two tier concepts is how `plan_id` came to point at `subscription.plan`.\n**The denormalised copy on the position stays.** A till rendering *Gold* beside a balance must not join, and must certainly not cross a cell boundary to print a word. This table is the source of truth and those columns are its cache.\n","required":["loyaltyProgrammeId","code","name","rank"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"loyaltyProgrammeId":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":120},"rank":{"type":"integer","description":"**Order, not threshold.** Two tiers can share a qualifying rule and still have an order, and sorting by points breaks the moment a tier is granted rather than earned.\n"},"minLifetimePoints":{"type":"integer","nullable":true,"description":"What reaching this tier requires. **`pointsToNextTier` on the position is this minus the guest's lifetime points**, and until now it was this minus nothing.\n"},"retainLifetimePoints":{"type":"integer","nullable":true,"description":"What keeping it requires, per review period. **Usually lower than reaching it**, and a scheme that cannot express the difference either never demotes or demotes on the day a guest stops earning.\n"},"validityMonths":{"type":"integer","nullable":true,"description":"Null means the tier does not lapse on its own."},"benefits":{"type":"array","description":"What the tier gives, as the guest reads it. Text shown, not rules enforced.","items":{"type":"string"}},"earnMultiplier":{"type":"number","nullable":true,"description":"Applied to every earn rule while the guest holds this tier. Null means 1."},"isActive":{"type":"boolean","default":true}}},
"MarketingReward": {"type":"object","x-ticvai-persistence":"marketing.reward","description":"**Taken from the backend workbook, 20 September.** Defines a loyalty reward that can be issued to eligible customers.","required":["loyaltyProgramId","code","name","type","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"loyaltyProgramId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"type":{"type":"string","maxLength":30},"productId":{"type":"string","format":"uuid","nullable":true},"pointsCost":{"type":"number","nullable":true},"discountValue":{"type":"number","nullable":true},"validityDays":{"type":"integer","nullable":true},"isActive":{"type":"boolean"}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MfaEnrolment": {"x-ticvai-persistence":"none — transient","type":"object","required":["methodId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"methodId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"secret":{"type":"string","nullable":true,"description":"TOTP shared secret. Returned once, at enrolment, and never again."},"qrCodeUri":{"type":"string","nullable":true},"recoveryCodes":{"type":"array","description":"Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n","items":{"type":"string"}},"expiresAt":{"type":"string","format":"date-time"}}},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PayInstalment": {"type":"object","description":"One scheduled charge in an instalment plan.","required":["sequence","dueDate","amount","status"],"properties":{"sequence":{"type":"integer","minimum":1},"dueDate":{"type":"string","format":"date"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["scheduled","paid","failed","waived","cancelled"]},"paymentId":{"type":"string","format":"uuid","nullable":true},"dunningCaseId":{"type":"string","format":"uuid","nullable":true},"attemptedAt":{"type":"string","format":"date-time","nullable":true}}},
"PayInstalmentPlan": {"type":"object","x-ticvai-persistence":"payments.instalment_plan + payments.instalment","description":"4.2.17. A schedule of charges for one order, independent of the product's term.","required":["id","orderId","frequency","status","total","instalments"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"frequency":{"type":"string","enum":["monthly","quarterly","custom"]},"paymentTokenId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["active","completed","inArrears","cancelled"]},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"paidToDate":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nextDueDate":{"type":"string","format":"date","nullable":true},"instalments":{"type":"array","items":{"$ref":"#/components/schemas/PayInstalment"}},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the order was sold at."}}},
"PaymentToken": {"type":"object","x-ticvai-persistence":"payments.token","description":"BL-116. **A stored credential, held by the provider and referenced here.** The platform never sees a card number, which is what keeps PCI scope where it belongs.\n**A token is provider-scoped.** A card tokenised with one gateway does not work with another, so a routing change does not silently move a guest's saved card — it means asking them again, and the model should make that visible rather than surprising.\n","required":["id","subjectId","providerId","token","isDefault"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid"},"token":{"type":"string","format":"password","writeOnly":true,"description":"**Write-only, never returned.** The provider's reference to a credential it holds. Required on the stored row; absent from every response.\n"},"method":{"type":"string"},"maskedIdentifier":{"type":"string","description":"What a guest sees — the last four digits, the card brand. **Enough to choose between two saved cards and not enough to use one.**\n"},"expiresAt":{"type":"string","format":"date","nullable":true},"isDefault":{"type":"boolean"},"consentPurposeId":{"type":"string","format":"uuid","nullable":true,"description":"**Storing a card for future use is a purpose a guest consents to**, separate from the payment they are making now. A token taken without it is a card kept on a guest's behalf that they never agreed to.\n"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"Promotion": {"x-ticvai-persistence":"promotions.promotion","allOf":[{"$ref":"#/components/schemas/CreatePromotionRequest"},{"type":"object","required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/PromotionStatus"},"isPaused":{"type":"boolean"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Starts at 1 and goes up by one on every saved change. The version the directory, the audit history (`promotions.promotion_audit`) and the channel publication monitor (`promotions.promotion_channel_publication`) name. (DM5, 29 September: data model for the agreed operations)"}}}]},
"PromotionConditions": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","description":"All conditions must hold. An empty object matches everything.","properties":{"variantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productKinds":{"type":"array","items":{"type":"string"}},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minQuantity":{"type":"integer","minimum":1},"minBasketValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channels":{"type":"array","description":"Empty or absent matches every channel.","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"purchaseGate":{"type":"boolean","default":false,"description":"BL-037. **`evaluatePromotions` gates a price and nothing gated a sale.** A non-member could buy a member-only product at the member price refused, which is a discount failure rather than an eligibility one.\nTrue makes these conditions a **precondition of purchase**: fail them and the line cannot be added, not merely charged more. **Evaluated at add-to-cart**, because a guest told at payment has already entered a card.\n"},"paymentMethod":{"type":"array","nullable":true,"description":"BL-113. **Card-issuer and payment-type promotions** — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible.\n**Evaluated at payment, not at cart**, which is the awkward part: the discount appears after the tender is chosen, and the basket total must be allowed to move at that point.\n","items":{"type":"string"}},"issuerBins":{"type":"array","nullable":true,"description":"Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. **The bank supplies these and they change**, so they are data rather than configuration.\n","items":{"type":"string"}},"componentRedemption":{"type":"string","nullable":true,"enum":["allTogether","independently","sequenced"],"description":"BL-112. **Per-component redemption inside a bundle was unstated.** A park-plus-lunch bundle where lunch may be used another day behaves differently from one where both must be used on the same visit, and **the difference is revenue recognition, not just convenience.**\n"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"membershipTierIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresCoupon":{"type":"boolean","default":false},"firstPurchaseOnly":{"type":"boolean","default":false},"performanceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"advanceDaysMin":{"type":"integer","description":"Early-bird — booked at least this many days ahead."},"advanceDaysMax":{"type":"integer","description":"Last-minute — booked no more than this many days ahead."},"eligibilityRuleIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own) that must also hold. **Deprecated in r2** (CHG-CLN-001): setEligibilityRule, which saved library rules, was retired (BC-017), so no operation creates one; send the conditions inline. Rules already saved still apply. Each is evaluated with its own `effect`. (DM5, 29 September: data model for the agreed operations)"}}},
"PromotionStatus": {"type":"string","enum":["draft","scheduled","live","paused","expired","ended"]},
"PublishedTrackingTechnology": {"type":"object","x-ticvai-persistence":"none — the approved rows of marketing.tracking_technology, guest-facing fields only","description":"One approved technology as the preference centre shows it (2.6.54).","required":["name","provider","category","isThirdParty"],"properties":{"name":{"type":"string"},"provider":{"type":"string"},"category":{"$ref":"#/components/schemas/CookieCategory"},"technologyType":{"type":"string"},"purpose":{"type":"string","nullable":true},"durationDays":{"type":"integer","nullable":true,"description":"Null for session storage."},"isThirdParty":{"type":"boolean"},"privacyInformation":{"type":"string","nullable":true}}},
"RecordConsentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["purpose","decision","noticeVersion","source","recordedAt"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","description":"Omit to apply to every channel the purpose covers.","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string"},"source":{"$ref":"#/components/schemas/ConsentSource"},"recordedAt":{"type":"string","format":"date-time"}}},
"RecordDeviceConsentRequest": {"type":"object","x-ticvai-persistence":"none — request only","description":"What the banner or preference centre sends to `recordDeviceConsent`.","required":["channel","action","noticeVersion","decidedAt"],"properties":{"consentKey":{"type":"string","maxLength":64,"nullable":true,"description":"The key the browser or app already holds; omitted on a first decision, and one is minted."},"channel":{"$ref":"#/components/schemas/CookieConsentChannel"},"brandId":{"type":"string","format":"uuid","nullable":true},"bannerDesignId":{"type":"string","format":"uuid","nullable":true},"action":{"$ref":"#/components/schemas/DeviceConsentAction"},"categories":{"type":"array","description":"Required for `savePreferences`; ignored for the other actions, which decide every category themselves.","items":{"type":"object","required":["category","decision"],"properties":{"category":{"$ref":"#/components/schemas/CookieCategory"},"decision":{"type":"string","enum":["granted","declined"]}}}},"noticeVersion":{"type":"string"},"language":{"type":"string","maxLength":10,"nullable":true},"globalPrivacyControl":{"type":"boolean","default":false},"source":{"$ref":"#/components/schemas/ConsentSource"},"decidedAt":{"type":"string","format":"date-time"}}},
"Referral": {"type":"object","x-ticvai-persistence":"marketing.referral","description":"BL-034. **No referrer, no reward, nothing anywhere.**\n**The reward fires on the referee's qualifying act, not on the sign-up**, because a referral that pays on registration pays for accounts rather than for guests.\n","required":["id","referrerSubjectId","code","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"referrerSubjectId":{"type":"string","format":"uuid"},"refereeSubjectId":{"readOnly":true,"type":"string","format":"uuid","nullable":true},"code":{"readOnly":true,"type":"string"},"status":{"readOnly":true,"type":"string","enum":["issued","registered","qualified","rewarded","expired","void"]},"qualifyingAction":{"type":"string","enum":["firstPurchase","firstVisit","membershipPurchase"]},"referrerRewardId":{"readOnly":true,"type":"string","format":"uuid","nullable":true},"refereeRewardId":{"readOnly":true,"type":"string","format":"uuid","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"RetryDunningPaymentRequest": {"type":"object","description":"Request only.","properties":{"paymentTokenId":{"type":"string","format":"uuid","nullable":true,"description":"A saved card other than the one that failed: the id of one of the guest's own `PaymentToken` rows (`payments.token`, stored through `storePaymentToken`), **not** a `payments.method` id, which names a kind of method in the catalogue rather than a card. Required after a hard decline.\n"}}},
"StackingMode": {"type":"string","description":"How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket.\n","enum":["exclusive","stackable","bestOnly","stackWithGroup"]},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletAutoReloadSetting": {"type":"object","x-ticvai-persistence":"wallet.auto_reload_setting","description":"4.2.17, 4.3.28. Also the `setWalletAutoReloadSetting` body. One per wallet; the holder's own setting within the venue's `WalletFundingRules.autoReload`.","required":["enabled"],"properties":{"walletId":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","readOnly":true},"enabled":{"type":"boolean"},"thresholdAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reloadAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"paymentTokenId":{"type":"string","format":"uuid","nullable":true},"maximumPerDay":{"type":"integer","minimum":1,"nullable":true},"status":{"type":"string","readOnly":true,"enum":["active","suspendedAfterDecline","disabledByVenue"]},"lastReloadAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the wallet's venue scope."}}},
"WalletExitBalance": {"type":"object","x-ticvai-persistence":"none — computed from wallet.wallet, wallet.credit_lot and held offline transactions","required":["walletId","balance","amountDue","refundable"],"properties":{"walletId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"pendingOfflineAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amountDue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nonRefundableCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"waiveAllowedUpTo":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"asAt":{"type":"string","format":"date-time"}}},
"WalletExitSettlement": {"type":"object","x-ticvai-persistence":"wallet.exit_settlement","description":"4.3.4. One settlement of a wallet at exit.","required":["id","walletId","action","amount","settledAt"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"action":{"type":"string","enum":["collect","refund","waive"]},"method":{"type":"string","nullable":true,"enum":["card","cash","storedCard","originalPayment"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceBefore":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"paymentId":{"type":"string","format":"uuid","nullable":true},"refundId":{"type":"string","format":"uuid","nullable":true},"walletTransactionId":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"settledByPrincipalId":{"type":"string","format":"uuid","nullable":true},"settledAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]},
"Wishlist": {"type":"object","required":["subjectId","items"],"x-ticvai-persistence":"none — wrapper. The items are the table, keyed by subject","properties":{"subjectId":{"type":"string","format":"uuid"},"items":{"type":"array","x-ticvai-persistence":"marketing.wishlist_item","items":{"type":"object","required":["id","variantId","addedAt","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string"},"performanceId":{"type":"string","format":"uuid","nullable":true},"performanceStartsAt":{"type":"string","format":"date-time","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money","description":"The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"},"unavailableReason":{"type":"string","nullable":true},"note":{"type":"string","nullable":true},"addedAt":{"type":"string","format":"date-time"}}}}}}
}
```
