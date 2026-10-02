# P01-booking-selection-01 — P01 · Booking & Selection

**7 screens · 31 operations · 64 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `AI_USE, ORDER_CREATE, ORDER_VIEW, PRICE_VIEW, PRODUCT_VIEW, RESOURCE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-005` | Ticket Type Selection | A | 2 | 71 | 6 | 27 | 31 | 6 | guest | review (client-verified) |
| `WEB-006` | Date & Performance Selection | A | 40 | 19 | 6 | 17 | 32 | 6 | guest | review (client-verified) |
| `WEB-007` | Interactive Seat Selection | A | 8 | 39 | 6 | 30 | 22 | 6 | guest | review (client-verified) |
| `WEB-008` | Add-ons & Upsell | A | 19 | 22 | 5 | 47 | 16 | 0 | guest | review (client-verified) |
| `WEB-009` | Wishlist | A | 0 | 15 | 5 | 1 | 2 | 0 | guest | review (client-verified) |
| `WEB-047` | Map Booking — Cabanas & Spots | A | 24 | 38 | 6 | 5 | 4 | 6 | guest | notStarted (client-verified) |
| `WEB-048` | Book a Space by the Hour | A | 23 | 40 | 6 | 25 | 7 | 0 | guest | notStarted (client-verified) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-005` Ticket Type Selection

**Choose which ticket and how many.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Booking & Selection · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18013 (APP-WEB-WEB-005) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listProductVariants` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `productId` (WEB-004), `venueId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/booking-and-selection/ticket-type-selection` |

**What the spec says about it.** **Rev 3 (decided 29 September).** **Order (REV3-2):** in the dated flow the guest picks the date, then the time (WEB-006), then tickets here: tickets stay hidden until a time is picked and Continue stays off until both are chosen, per `BookingFlowConfig.performanceReveal` (`dateTimeTicket` default, `allAtOnce` shows all). The two steps may render as one staged page. This screen may also render as a side panel on WEB-002 and WEB-004 (23SEP-5). **Sign-in (REV3-3):** with `signInAt` `afterAddOns` (default) the sign-in or guest code is asked when the guest leaves Add-ons (WEB-008), or on Continue here when the booking has no add-ons step; `atPayment` asks at WEB-012. The basket is kept either way. **Filters:** categories (REV3-16), experience and level (REV3-19). **Info-only** products show their label and open details (REV3-14). **Help me choose** (REV3-11) is a region and a pop-up of this step, not a screen of its own: the prototype draws it as a dialog over the booking step with a banner under the products. **Quick tour** (REV3-20). **Cart (REV3-10):** `cartLayout` may be `floatingIcon`, a round basket button with the count that opens the cart; the cart stays on the right in Arabic unless `cartSideInRtl` is `mirror`. Card layout, size and density are enums (DG-6). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). **The step order comes from the published booking …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The ticket counters: which ticket and how many of each guest type. Block A. In the dated flow it is the last stage of one staged step (date, then time, then tickets) and in the prototype it is the same page; on a listing it opens as a side panel. Get right the pricing model the client corrected on 30 September: the guest counters belong to the chosen ticket and take its prices, so a multi-park ticket with three adults is ONE basket line.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Supervisors (free, one per N guests) and a water-park group choosing a session are not in the contract. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The action bar has a primary "Evaluate promotions" button and a modal that collects venueId, channel and lines. (CHG-GST-003); A raw "Every product variant" table (id, sku, axisValues, isActive) and a selected-variant detail panel. (CHG-GST-003); The prototype's Read more panel on the multi-park flow still prices guests at single-park rates (Adult AED 325, Infant AED 475). (CHG-SGU-020).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How many supervisors are free per group, and is it per group ticket?** → Drawn default accepted: A separate free guest type, up to 1 per 10 guests. *(decided by Chinmay, 2026-10-02; DEC-115 / CHG-NOTE-007)*
- **Is each group card's minimum set per group ticket?** → Drawn default accepted: Each group ticket carries its own minimum, default 10. *(decided by Chinmay, 2026-10-02; DEC-116 / CHG-NOTE-007)*
- **Is the swim vest an add-on product and the splash and river pass a separate product?** → Drawn default accepted: The vest is an add-on; the splash and river pass is its own product filtered by the swim answer. *(decided by Chinmay, 2026-10-02; DEC-117 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Choose your experience | picker: choose a category | optional | — | — | shows names, sends the id | Each option carries its one-line `ProductCategory.description`. Narrows `listProducts?categoryId=`. | `listProducts` ?categoryId |
| Select level | text field | optional | — | max length 120 | — | Beginner to expert, from the products' `segmentTags` `level/<code>` (`listProducts?segmentTag=`). **Reset** clears both filters. | `listProducts` ?segmentTag |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Product | picker: choose a product | — | — | `getPublishedBookingFlow` ?productId |
| Product category | picker: choose a product category | — | — | `getPublishedBookingFlow` ?productCategoryId |
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `getPublishedBookingFlow` ?flowTypeKey |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **ticket choice**: Ticket cards first (e.g. 1 park, 2 park, 3 park ticket), then the guest counters for the chosen ticket. Before a ticket (or, in a session product, a session) is chosen the counter area shows the hint "Choose a ticket above, then set how many of each guest." and no counters. *(source: DI-1106; CLIENT-RESPONSE-30SEP 2; sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html (waitText))*
- **guest counters (Adult, Child, Senior, Infant, Person of determination)**: Each counter is a variant of the chosen ticket and is priced from it (listProductVariants), so child and senior scale from the chosen ticket and infant stays free where the ticket says so. Steppers start at 0, minus disabled at 0, plus disabled at the purchase limit with the reason ("Up to 6 tickets per booking"). Each row has an (i) with who it is for and what it includes (up to 300 characters) when cardInfo is on. *(source: DI-1106; DI-464; DI-172; REV3 23SEP-6)*
- **group headcount (Group and school booking)**: Group products start from group ticket cards (School group, Corporate group, Tour operator group, Community group), each with a per-person price and its minimum group size. Then "How many people" is a number box the guest can type into (e.g. 45) with minus and plus; there is no Group size dropdown. Supervisors are a separate, free row ("One free for every 10 guests"). Values below the card's minimum are refused inline ("School groups start at 10 guests"). *(source: DI-1104; DI-1105; DI-1114; DI-1116; CLIENT-RESPONSE-30SEP 1)*
- **experience and level filters**: "Choose your experience" and "Select level" dropdowns where the venue uses them (surf, lessons, swim, sauna; beginner to expert), each option with its one-line description, and Reset. They narrow the products, they are not answers stored on the booking. *(source: REV3-19)*
- **promotion code**: Not entered here. The guest enters codes in the basket (WEB-010); this step only shows near-miss offers ("Add one more child for the family rate") from the promotion evaluation. *(source: screens/P01-guest-web-storefront.yaml#WEB-005 wireframe.prototype.differences; F01 step 5)*

#### Outputs: what the screen shows and produces

**Shown**

**Booking at** (banner): The venue this booking is for, with **Change location**. Reuses the venue choice of WEB-001 (audit R267). On a switch the selection is cleared, except lines whose product shares a `familyKey` with a product at the new venue, which move to it; times and prices refresh. Shown only when `BookingFlowConfig.locationSwitcher` is on.

**Ticket categories** (card list, from `listProductCategories`): `ticketCategories` `categoryThenSubcategory` (default): category tiles, then that category's tickets (`listProducts?categoryId=`); `flatList`: every ticket at once.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Code | text | Taken from their category tables, 20 September. Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a … |
| Name localised | grouped details | — |
| Kind | chip: Category, Brand, Collection, Season, Department | — |
| Parent | the name it points at, never the id | One tree, not four. A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each … |
| Display order | 1,234 | — |
| Image | the image or video | — |
| Description | in the reader's language | The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September … |
| Booking flow | the name it points at, never the id | The booking flow for every product filed here that names none of its own (decided 29 September, W12, BO-115). |
| Is active | yes / no (icon or chip) | Deactivated rather than deleted. A category with a season behind it still names the products sold under it, and removing it rewrites last … |
| Children | list or chips (count when long) | Empty on a leaf. |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Code | text | Taken from their category tables, 20 September. Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a … |
| Name localised | grouped details | — |
| Kind | chip: Category, Brand, Collection, Season, Department | — |
| Parent | the name it points at, never the id | One tree, not four. A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each … |
| Display order | 1,234 | — |
| Image | the image or video | — |

**Help me choose** (banner, from `getPublishedGuidedChoice`): The venue's published Help me choose, if any (404 = none, and nothing shows). `mode` `button`: a button on this step; `popupOnArrival`: the pop-up also opens once on the first arrival (a seen flag on the device only); `showBanner`: a dark banner under the products (*Choose from the experiences above or let us help you decide*). Opens the Help me choose pop-up. **29 September (W4): the answers …

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | UUIDv7. |
| Venue | the name it points at, never the id | From the path of `createGuidedChoice`. |
| Name | text | Staff-facing name, e.g. "Water park day planner". |
| Mode | chip: Button, Popup on arrival, Off | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on … |
| Show banner | yes / no (icon or chip) | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Behaviour | chip: Filter, Recommend | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything | yes / no (icon or chip) | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Questions | list or chips (count when long) | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| ID | the name it points at, never the id | UUIDv7. The row's own key. |
| Title | in the reader's language | — |
| Kind | chip: Choice, Yes no, Age, Level, Certification | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. |
| Sort order | 1,234 | — |
| Answers | list or chips (count when long) | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). |
| ID | the name it points at, never the id | UUIDv7. The row's own key. |
| Title | in the reader's language | — |
| Body | in the reader's language | The one-liner under the title, at most 140 characters in each language. |
| Icon | text | An icon name from the guest app's icon set. |
| Badge | in the reader's language | Optional, e.g. "Best value". |
| Sort order | 1,234 | — |
| Target | grouped details | Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list. |

**Card list** (card list, from `listProductVariants`): Each row is a variant with a stepper. Price updates live. Each row shows `ProductVariant.description` (who it is for, what it includes) behind the (i) when `BookingFlowConfig.cardInfo` is on (23SEP-6), its display tags when `ticketTags` is on (23SEP-3) and its own photo (23SEP-4). In the dated flow the rows stay hidden until a time is picked (`performanceReveal` `dateTimeTicket`, REV3-2)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| SKU | text | — |
| Axis values | grouped details | — |
| Name | text | Taken from their variant tables, 20 September. `axisValues` gives `{size: L}` and no string a guest can read. |
| Barcode | text | Taken from their variant tables, 20 September. `catalogue.alternative_code` is a partner's own code for a variant and requires `partnerId` … |
| Is default | yes / no (icon or chip) | Taken from their variant tables. Which variant a product page opens on. |
| Is active | yes / no (icon or chip) | False when retired. Retired variants are never deleted — orders reference them. |
| Description | in the reader's language | Who this ticket type is for and what it includes, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Banner** (banner, from `evaluatePromotions`): Shows near-miss offers — "add one more for the family rate". Uses the rejected list, which exists precisely so this can be said Promotions are evaluated by themselves on every change (`evaluatePromotions`); a guest never fills a promotions form (F01 step 4, GFIX-3).

| Shows | Format | Notes |
|---|---|---|
| Total discount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Lines | list or chips (count when long) | — |
| Line | text | — |
| Original price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discounted price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | — |
| Applied | list or chips (count when long) | — |
| Promotion | the name it points at, never the id | — |
| Promotion code | text | — |
| Promotion name | text | — |
| Discount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Coupon code | text | — |
| Rejected | list or chips (count when long) | Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount. |
| Promotion code | text | — |
| Promotion name | text | — |
| Reason | chip: Conditions not met, Superseded by better offer, Exclusive promotion applied … | — |
| Detail | text | — |

**Booking steps** (progress indicator, from `getPublishedBookingFlow`): The steps of the published flow in their `sortOrder`, this one (tickets) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back. Drawn in the venue's `BookingFlowSettings.stepIndicator` style; `embedMode` and `singleEventPage` come from the same published settings (CMS-016) (CHG-SGU-022).

| Shows | Format | Notes |
|---|---|---|
| Steps | list or chips (count when long) | Every step of the type, in the venue's order. Filled from the type when left out on create. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Quick tour (icon button) | navigation or local | — | — | — | — |
| Show everything (secondary button) | `listProducts` GET `/products` | — | Product (paged) | 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 403 Authenticated but not permitted at the requested scope | — |
| Continue (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **running total and basket line preview**: One line per ticket per guest type, written "<ticket> · <guest type> × <n> = AED <total>", e.g. "2 park ticket · Adult × 3 = AED 1,425". Never a ticket line plus a separate guest line. AED with a thousands separator and no decimals for whole amounts. *(source: DI-1106; CLIENT-RESPONSE-30SEP 2)*
- **session tickets**: For a session product the panel title names the session ("Tickets for Intermediate surf · 19:30") with its own guest types (Surfer at the session price, Junior surfer 10-15 with a paying adult, Spectator AED 35). Choosing the session adds nothing to the basket; a line appears only when a quantity is set. *(source: DI-1107; CLIENT-RESPONSE-30SEP 3; MoM 29 Sep W5)*
- **group estimate**: The enquiry panel reads "<group ticket> · Guests × <n>" with the per-person price and the estimate; supervisors are listed with "Free". A group booking is a request (requestGroupBooking with the group ticket and the headcount), so the button says Send request, not Pay. *(source: DI-1105; screens/P01-guest-web-storefront.yaml#WEB-005 notes (30 September))*
- **step indicator**: The published flow's steps in their order with this one highlighted, drawn in the venue's style (Bars, Dots, Counter "Step 2 of 4", Step names). A step the flow turned off is not drawn and is skipped. *(source: DI-1093; MoM 30 Sep 4.6; screens/P01-guest-web-storefront.yaml#WEB-005 (progressIndicator))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Continue**: Off until a ticket and at least one guest are set (and, in the dated flow, a date and time). Goes to Add-ons (WEB-008) when the flow has an Extras step; otherwise to sign-in or the guest code (WEB-016) when signInAt is afterAddOns and the guest is anonymous; otherwise the basket. The basket is kept through sign-in. *(source: REV3-2; REV3-3; F01 branch at step 4)*
- **Help me choose**: Pop-up of one to four questions, three answers each; the answers filter the products in place (behaviour filter) or end on one result card (behaviour recommend). Show everything clears it. A swimmer answer pre-fills the swim consent, which the guest still confirms once. *(source: MoM 29 Sep W4; contracts/satellite/white-label.yaml#/components/schemas/GuidedChoice; REV3-26)*
- **Change location (Booking at bar)**: Shown only when locationSwitcher is on. Switching venue clears the selection except lines whose product shares a familyKey at the new venue, which move; times and prices refresh. Confirm first when it would clear lines ("Changing to Mirdif clears 2 tickets"). *(source: REV3-18; DI-1058)*

**Data it reads**: `listProductVariants` (onLoad, List generated variants); `listProductCategories` (onLoad, Category tiles and the experience filter, with descriptions); `listProducts` (onLoad, The tickets of a category or level (`categoryId` …); `getPublishedGuidedChoice` (onLoad, The venue's published Help me choose (404 = none)); `getPublishedBookingFlow` (onLoad, The published booking flow for this product: which steps it …)

**Where the user goes next**

- → `WEB-006` Date & Performance Selection: *Change date or time (the dated flow picks them first)*; carries `eventId`
- → `WEB-007` Interactive Seat Selection: *Interactive Seat Selection*; carries `eventId`
- → `WEB-008` Add-ons & Upsell: *Add-ons & Upsell*
- → `WEB-010` Shopping Cart: *Shopping Cart*; carries `code`, `lineId`
- → `WEB-016` Login / Register: *Continue, when sign-in is asked after add-ons and this booking has no add-ons step*; carries `cartId`
- → `WEB-006` Date & Performance Selection: *Workshop chosen, then date and time (product-first flow)*; carries `productId`

**What opens over it**

- modal *Help me choose (the button, the banner, or once on first arrival when the mode …*: **One or two questions, three answers each** (title, one-liner, icon, optional badge), from the published `GuidedChoice`. The answer to the last question opens its target through a result card: a product (this step with that product), a product category (its tiles), an event (WEB-006) or a module. …
- modal *First booking visit on this device, or Quick tour*: **Four coach marks** over date, time, tickets and basket, with Back, Next and End tour. Shown once per device (the flag is kept on the device only) and replayable from Quick tour; only when `BookingFlowConfig.quickTour` is on (decided 29 September, rev 3 REV3-20).

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket type selection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket type selection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket type selection yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listProductVariants` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 Validation failed |

#### Edge cases to draw

- **Water park swim answer**: "All of us" keeps the full ride list at standard prices; "Some of us" changes the ride notes and shows a "Swim vests needed" counter; "None of us" switches the tickets to the splash and river pass (Adult AED 175, Junior AED 135, Child AED 125, Senior AED 135) and removes slides from the ride notes. The swim pop-up is not shown again where the question is on the page. *(source: DI-1108; CLIENT-RESPONSE-30SEP 4; DI-1118)*
- **An info-only product is chosen**: Its details open with "Contact sales to book"; it can never reach the basket (the server refuses it with 409). *(source: REV3-14)*
- **The guest raises a quantity past what is left**: The plus button stops at the remaining count with "Only 4 left for 19:30"; the line is refused rather than added and removed later. *(source: contracts/spine/orders.yaml#addCartLine ("Refused rather than added where capacity has gone"))*

#### Consistency with other screens

- Match `GST-008`: Same pricing model, same one-line-per-ticket rule, same group headcount box. The app adds a +10 button to the headcount stepper; the web does not.
- Match `WEB-006`: In the dated flow this is the third stage of the same staged page; the time hint and this hint use the same component.
- Match `KSK-004`: The kiosk counters follow the same ticket-then-guest-type rule and the same purchase limits.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
flow: Summit Peaks, Multi-park combo, Friday
tickets:
- name: 1 park ticket
  price: AED 325
- name: 2 park ticket
  price: AED 475
  sub: Valid 6 days
  badge: Popular
counters: Adult × 3 (AED 475 each), Child × 0, Senior × 0, Infant × 0 (free)
basketLine: 2 park ticket · Adult × 3 = AED 1,425
groupCards:
- name: School group
  sub: Ages 5-18 · minimum 10
  price: AED 145 per person
  note: One teacher free for every 10 students
- name: Corporate group
  sub: Adults · minimum 15
  price: AED 225 per person
- name: Tour operator group
  sub: Any age · minimum 20
  price: AED 195 per person
- name: Community group
  sub: Charities and clubs · minimum 10
  price: AED 125 per person
groupEstimate: School group · Guests × 45 = AED 6,525; Supervisors × 4 Free
```

#### Permissions

- `evaluatePromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getPublishedGuidedChoice` → no permission · guest
- `getPublishedBookingFlow` → no permission · guest, staff

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

27 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.11 | - Discounts | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.12 | - Dynamic promotions | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.6.13 | - Coupons | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 2.8.5 | The system should allow call center agents to apply promotions, discounts, up-sales and offers configured in the system. Application of discount coupons via a code supplied (on the phone) by the … | Ticketing Sales | CONTRACTED | `evaluatePromotions` |
| 3.5.9 | System shall automatically present bundle offers based on configurable conditions such as number of tickets purchased, guest type, loyalty tier, membership status, sales channel, season, location, or … | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.16 | The system should allow creation of promotion on a bundle: “buy x, get x free”, or “buy a ticket and a catalogue and get 10% off or get AED 10 discount” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.17 | The system should allow creation of added value: “Buy for more than 200 AED and get a free pencil” | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.32 | Discounts can be under conditions (dynamic discounts): - early birds, - subject to volume (buy one get one, 4 for 3 …), - subject to the type of tickets or - subject to the customer segment. | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 3.6.34 | Cart-level promotions & bundle logic (e.g., “Buy 4 Pay 3”, multi-park family packs) applied automatically at checkout, without new SKUs | Admission and Access | CONTRACTED | `evaluatePromotions` |
| 4.1.7 | The system should be able to accept promotions linked with admission tickets and/or vouchers. | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.9 | The system should be able to apply BOGO based promotion offers based on purchased product types and/or product count | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| 4.1.10 | The system should be able to allow: - Buy X product and get X product for free. - Buy X product and get Y product for free. - Buy N number of products and Get X product for free. - Buy N number of … | Bundles and Promotions | CONTRACTED | `evaluatePromotions` |
| … 15 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- The water-park swim answer changes the offer: All of us = full ride list at standard prices; Some of us = ride notes change and a "Swim vests needed" counter appears; None of us = tickets switch to a cheaper splash and river pass, slides removed from ride notes. The swim pop-up is not shown where the question is on the page. *(client request · design review 30 Sep 2026, 4. Swim ability and height gate: the answer changed nothing · DI-1108)*
- Picking a surf session adds nothing to the cart. Then "Tickets for Intermediate surf · 19:30" shows Surfer (session price), Junior surfer 10–15 and Spectator (AED 35); items reach the cart only when a quantity is set. Before a session: "Choose a session above to see its tickets and prices." *(client request · design review 30 Sep 2026, 3. Surfing session added to the cart straight away · DI-1107)*
- Guest counters take their price from the chosen park ticket and produce one line, e.g. "2 park ticket · Adult × 3 = AED 1,425" (no separate Adult × 3 line). Child and senior prices scale from the chosen ticket; infants free. *(client request · design review 30 Sep 2026, 2. Multi-park ticket adds an extra adult line · DI-1106)*
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)*
- Each Adult / Child / Senior / Infant row has an (i) button showing who the ticket is for and what it includes (up to 300 characters). Setting "Extra info on cards", default on. *(agreed · design review 29 Sep 2026, Tickets 6. Extra information for each ticket in the ticket section · DI-1028)*
- Clicking a ticket opens the Adult / Child / Senior / Infant counters in a side panel on the same listing or details screen (no separate "Select Tickets" step); the panel is open by default on the listing and Book goes straight into the booking. *(agreed · design review 29 Sep 2026, Tickets 5. Clicking Dated Day Pass should show the tickets on the same screen · DI-1027)*
- Read more opens with the ticket's video or photo, and every ticket in a listing has its own photo (product media: images and videos, one primary). *(agreed · design review 29 Sep 2026, Tickets 4. Video or image should show · DI-1026)*
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)*
- Museum workshops: after Help me choose, the guest selects the workshop first, then date/time; only relevant products are shown. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W8 Workshops (museum) · DI-1010)*
- Surf sessions follow the time-selection pattern: products (beginner, intermediate...) appear only after a time slot is chosen. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W5 Surf sessions · DI-1007)*
- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)*
- Experience venues list each experience directly (e.g. author talk, calligraphy workshop, story hour, rooftop reading night), each with its own date, time and tickets; no category step. *(client request · rev 3 design review 25 Sep 2026, 12. Experience flow: show the product directly, not the ticket category · DI-999)*
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)*
- Season and membership packages show a quantity stepper once selected. *(client request · design review 23 Sep 2026, Cart 12. No quantity field for the selected ticket · DI-980)*
- Add-ons appear only on the Add-ons / Extras step, never in the ticket panels. Each add-on appears once (no duplicates such as 'Large locker' on two steps). *(client request · design review 23 Sep 2026, Cart 11. Show add-ons only on the Add-ons / Extras page · DI-979)*
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)*
- Reference details: sibling/multi-buy discount shown with a struck-through original price; workshop add-ons inline with theme/cuisine sub-selection feeding time-slot availability; a package builder for bundled experiences. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-586)*
- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)*
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Packages bundle any combination of ticket-type components with package-level pricing (e.g. admission + F&B item + retail item, or admission + show); F&B or retail is not required. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-435)*
- Decision: ticket types are browsed in-page, not across multiple pages; "View all ticket types" expands additional categories in place. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-427)*
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)*
- Minimum/maximum sellable quantity per customer (e.g. a promotional bundle requiring at least two) must be enforced at selection. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-172)*
- Some clients (e.g. museums with 5-6 standard configurations) start by asking the number of guests, which narrows the calendar to dates/times with sufficient availability. *(client request · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-117)*

Also apply: 7 for P01 · Booking & Selection, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A120** Build the product creation wizard with four paths (from scratch · save as reusable template · clone · file upload using a standard tenant data-collection template) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'product creation wizard')*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker · keyword 'ticket type')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| … 36 more | | | `WHITE-LABEL.md` |

Also set there, as content the tenant writes: venue overrides: settings.

*Booking flows: steps, their order and per-flow settings*, set in `CMS-102` Site Builder, `CMS-103` Booking Flows:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

Also set there, as content the tenant writes: settings.

*Help me choose*, set in `CMS-101` Help Me Choose:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Help me choose name (`guidedChoices.name`) | max length 80 | — | Staff-facing name, e.g. "Water park day planner". |
| Help me choose mode (`guidedChoices.mode`) | Button · Popup on arrival · Off | Button | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on … |
| Show banner (`guidedChoices.showBanner`) | — | on | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Help me choose behaviour (`guidedChoices.behaviour`) | Filter · Recommend | Filter | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything (`guidedChoices.showEverything`) | — | on | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Help me choose questions (`guidedChoices.questions`) | at least 1; at most 4 | — | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| Questions: title (`guidedChoices.questions[].title`) | English and Arabic (Arabic right to left) | — | — |
| Questions: kind (`guidedChoices.questions[].kind`) | Choice · Yes no · Age · Level · Certification | Choice | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. |
| Questions: sort order (`guidedChoices.questions[].sortOrder`) | min 0 | — | — |
| Questions: answers (`guidedChoices.questions[].answers`) | at least 2; at most 4 | — | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). |
| Answers: title (`guidedChoices.questions[].answers[].title`) | English and Arabic (Arabic right to left) | — | — |
| Answers: body (`guidedChoices.questions[].answers[].body`) | The one-liner under the title, at most 140 characters in each language. | — | The one-liner under the title, at most 140 characters in each language. |
| Answers: icon (`guidedChoices.questions[].answers[].icon`) | max length 40 | — | An icon name from the guest app's icon set. |
| Answers: badge (`guidedChoices.questions[].answers[].badge`) | At most 24 characters in each language. | — | Optional, e.g. "Best value". |
| Answers: sort order (`guidedChoices.questions[].answers[].sortOrder`) | min 0 | — | — |

Also set there, as content the tenant writes: answers: target, answers: filter, answers: consent prefill, answers: result.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-005` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Engine controls → Theme park → Multi-park combo → Book → Fri → 2 park ticket → three adults (the counters take the 2 park ticket's price; one cart line)*. Differences: Ticket choice is on the same step as date and time and comes last: 'Date → time → ticket' (Config 'Performance reveal', Rev 3 item 2), whereas YAML goes WEB-005 → WEB-006. Prototype adds category → subcategory browsing, info-only (not bookable) products, 'Help me choose' questions, location switcher ('Booking at' bar), quick tour. Promo codes are entered in the cart, not on this step (YAML keeps evaluatePromotions here). 30 September: the guest counters take their price from the ticket chosen …
- Flow F01 *Guest buys a ticket online*, step 4: Chooses ticket types and quantities → Sees a running total that already reflects any applicable promotion. The tickets appear once a time is picked and Continue stays off until both are chosen (decided 29 September, rev 3 REV3-2)
- Flow F01 branch at step 4 (recoverable): when The guest is not signed in and leaves the ticket step (or Add-ons, where the booking has one), With the published flow's `settings.signInAt` `afterAddOns` (the default; read with `getPublishedBookingFlow`, W12) the guest is asked to sign in, or for a guest code when guest checkout is on …
- Flow F01 branch at step 4 (recoverable): when The guest checks out as a guest (guest checkout on for the venue), The pop-up asks only `BookingFlowSettings.guestContactFields` (email, and name or mobile where configured), then the six-digit code. After the code nothing is asked again: the cart goes to WEB-012 …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (71 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Quick tour, Show everything, Continue.
- [ ] Every transition is wired: `WEB-006`, `WEB-007`, `WEB-008`, `WEB-010`, `WEB-016`, `WEB-006`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 31 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-006` Date & Performance Selection

**Pick a date and time that has capacity.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Booking & Selection · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17870 (APP-WEB-WEB-006) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (compact density): `getAvailability` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `performanceId` (navigation), `cartId` (navigation), `eventId` (WEB-004), `venueId` (session) |
| Route | `/booking-and-selection/date-and-session-selection` |

**What the spec says about it.** Availability is read live and never cached beyond a few seconds. A guest selecting a session that filled while they were reading is a worse outcome than a slightly slower screen. **Wired 24 August from review**: acquireInventoryHold. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe. **Rev 3 (decided 29 September).** **Date → time → ticket (REV3-2):** this step now comes before the ticket choice (WEB-005); the time sits right after the date and stays hidden until a date is picked, and tickets stay hidden until a time is picked (`BookingFlowConfig.performanceReveal`, default `dateTimeTicket`; `allAtOnce` shows everything). **Times (REV3-1):** compact tiles paged `timesPerPage` at a time, with Morning / Afternoon / Evening chips and counts (`dayPartFilter`, boundaries per venue, default before 12:00, 12:00-17:00, from 17:00, venue time zone). **Seated events (REV3-4, REV3-7):** `seatEventDateMode` `inlineStep` keeps this step before the seat map; `popupOnSeatMap` asks the date and time in a pop-up over WEB-007 instead. **This step is skipped when the event has exactly one on-sale performance.** For a seated event this step and WEB-007 may render as one page (date, time, show — plus language and format for cinema — and the seat map). **Language (REV3-17)**, **experience and level with a four-day calendar (REV3-19)**, **Booking at (REV3-18)**, **Quick tour (REV3-20)**. **Consent questions (REV3-26)** pop up once after the session or date is picked; the …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Pick a date and then a time that has capacity. Block A. It comes BEFORE the tickets in every dated flow (date, then time, then tickets), and in the prototype the three stages are one staged page where each stage stays hidden until the previous one is chosen. Get right that choosing a time or session commits nothing: capacity is held only when a quantity is set.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The 30 September swim answer is three options for the party (All of us, Some of us, None of us) changing the products and prices, while REV3-26 models swim as a Yes/No consent per person or per booking. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The primary action is labelled "Acquire inventory hold" with a modal collecting variantId, quantity, seatIds. (CHG-GST-003); "Check booking eligibility" is a secondary button with a modal collecting productIds and party. (CHG-GST-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the swim question a party-level three-way answer (filter) or a per-person consent, or both?** → Drawn default accepted: Draw the on-page three-way question (All, Some, None of us) as the filter, and record the consent once per booking from it; no second pop-up. *(decided by Chinmay, 2026-10-02; DEC-118 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Part of the day | select field | — | — | — | — | Morning, Afternoon and Evening chips, each with its count of times, split in the venue time zone at `BookingFlowConfig.dayPartBoundaries` (`afternoonStartsAt` default 12:00, `eveningStartsAt` default … | — |
| Tour language | select field | — | — | — | — | EN, AR, FR, DE, ZH, RU; sends `?language=` so only performances in that language are listed. Each time shows `Performance.language`, and for cinema also `Performance.format` (2D, 3D, subtitled). | — |
| Next 7 days | date picker | — | — | — | — | **Date strip of the next `BookingFlowSettings.dateStripDays` days** (default 7, 3-31) with a calendar icon for the full month (M17-08). Surf-style layout: four days side by side, each time with … | — |
|  | date picker | — | — | — | — | Sold-out dates disabled with a reason on hover, not hidden | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `getAvailability` ?performanceId |
| Channel capacity | picker: choose a channel capacity | — | — | `getAvailability` ?channelCapacityId |
| Event | picker: choose an event | — | — | `getAvailability` ?eventId |
| From | date and time picker | — | — | `getAvailability` ?from |
| To | date and time picker | — | Exclusive; at most 31 days after `from`. | `getAvailability` ?to |
| From | date and time picker | — | — | `listPerformances` ?from |
| To | date and time picker | — | — | `listPerformances` ?to |
| Category | picker: choose a category | — | — | `listPerformances` ?categoryId |
| Language | text field | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | `listPerformances` ?language |
| Product | picker: choose a product | — | — | `getPublishedBookingFlow` ?productId |
| Product category | picker: choose a product category | — | — | `getPublishedBookingFlow` ?productCategoryId |
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `getPublishedBookingFlow` ?flowTypeKey |

**Form: Once, on leaving selection, when a chosen product has an eligibility rule** (drawer, opened by *Once, on leaving selection, when a chosen product has an eligibility rule*; *Continue* calls `checkBookingEligibility`, *Back* sends nothing)

**The party's age and height, asked once per person** (DI-1037; REV3 DG-3) for the products that set a rule, then checked with `checkBookingEligibility`. A person who does not meet a rule is named with the product, and the guest changes the selection; never a button, and never a form of product ids.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Products `productIds` | list of values (chips) | required | — | at least 1 | — | — | `checkBookingEligibility` body |
| Party `party` | repeatable rows | required | — | at least 1 | — | — | `checkBookingEligibility` body |
| Age band `party[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `checkBookingEligibility` body |
| Age years `party[].ageYears` | number field | optional | — | — | — | — | `checkBookingEligibility` body |
| Height band index `party[].heightBandIndex` | number field | optional | — | — | — | Which band of the rule's `heightBandsCm`, counting from 0. | `checkBookingEligibility` body |
| Guardian signed `party[].guardianSigned` | toggle | optional | off | — | — | — | `checkBookingEligibility` body |

**Form: Once, after the session or date is picked, when the cart has consent questions** (modal, opened by *Once, after the session or date is picked, when the cart has consent questions*; *Next* calls `recordConsentAnswers`, *Back* sends nothing)

**The venue's consent questions for this booking**, e.g. *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*: one or several, in the order `Cart.consentQuestions` gives (the booking flow's `BookingFlowConfig.consentQuestionIds` and every cart product's `consentQuestionIds`, each question once). A question asked **per person** is asked for each member of the party; one asked **per booking** once. Themed as the prototype's pop-up (Yes / No, Next). Next sends the answers to `recordConsentAnswers`, which stores each as a consent record (question version, answer, who answered, when). **A blocking answer** (e.g. *No* to the swim question) marks the lines it blocks …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Cart `cartId` | picker: choose a cart | required | — | — | shows names, sends the id | The cart the answers are given for. `checkoutCart` binds them to its order. | `recordConsentAnswers` body |
| Answers `answers` | repeatable rows | required | — | at least 1; at most 200 | — | — | `recordConsentAnswers` body |
| Question `answers[].questionId` | picker: choose a question | required | — | — | shows names, sends the id | — | `recordConsentAnswers` body |
| Question version `answers[].questionVersion` | number field | required | — | min 1 | — | The version the guest was shown, from `Cart.consentQuestions`. | `recordConsentAnswers` body |
| Answer `answers[].answer` | segmented control | required | — | Yes · No | — | — | `recordConsentAnswers` body |
| Cart line `answers[].cartLineId` | picker: choose a cart line | optional | — | — | shows names, sends the id | For a `perPerson` question, the line the person is on. | `recordConsentAnswers` body |
| Person index `answers[].personIndex` | number field | optional | — | min 0 | — | For a `perPerson` question, the person's row in that line's `eligibilityDeclaration`, counting from 0. | `recordConsentAnswers` body |
| Person name `answers[].personName` | text field | optional | — | max length 120 | — | — | `recordConsentAnswers` body |
| Person subject `answers[].personSubjectId` | picker: choose a person subject | optional | — | — | shows names, sends the id | Where the person is a known guest, such as the booker or a family member. | `recordConsentAnswers` body |
| Source `source` | select | required | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | — | `checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents` … | `recordConsentAnswers` body |
| Answered at `answeredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordConsentAnswers` body |

Errors to draw in the form: 409 The question has changed since the cart was read (`questionVersionSuperseded`); the client re-reads the cart and asks the current version. (ConsentAnswerProblem); 422 A `perPerson` question answered without a person (`personRequired`), a question this cart does not ask (`questionNotAsked`), or a retired one … (ConsentAnswerProblem)

**Sent by *Continue*** (`addCartLine`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **date**: A strip of the next dateStripDays days (default 7) with a calendar icon for the full month. Days with no performance or sold out online are disabled with the reason, not hidden. Days outside the channel's sales window are disabled ("Online booking closes the day before" for a next-day-minimum product). *(source: DI-920; DI-583; screens/P01-guest-web-storefront.yaml#WEB-006 (datePicker notes))*
- **time**: Hidden until a date is picked, with the hint "Choose a date to see times". Up to 8 times as large tiles; more than 8 as compact tiles paged timesPerPage at a time (default 24) with Earlier and Later, and Morning, Afternoon, Evening chips with counts (venue time zone, default split at 12:00 and 17:00). Tapping a selected chip again shows all times. Sold-out times are greyed, not removed. *(source: REV3-1; REV3-2; DI-1041)*
- **tour language**: For guided tours the order is date, then language, then time slot; only tours in that language are listed. Languages are shown in their own script (English, العربية, Français, Deutsch, 中文, Русский). Cinema times show language and format (2D, 3D, subtitled). *(source: REV3-17; MoM 29 Sep W11; DI-1057)*
- **party ages and heights**: Asked once, on leaving selection, only for products with an age or height rule: each person declares an age band and a height band. A person who does not qualify is flagged "Can't take part, too short" with Remove this guest or Choose another activity; Continue stays off until everyone qualifies. Height bands already chosen on a water-park day pass are the check and are not asked again. *(source: DI-1037; REV3 DG-3; DI-1000)*

#### Outputs: what the screen shows and produces

**Shown**

**Booking at** (banner): The venue this booking is for, with **Change location** (audit R267 venue choice). On a switch the selection clears unless products share a `familyKey`; times and prices refresh. Only when `BookingFlowConfig.locationSwitcher` is on.

**Card list** (card list): Session times with remaining counts. Availability is per channel — a session showing sold out here may still have counter allocation, which is correct behaviour and not a defect. **More than 8 times show as compact tiles**, `BookingFlowConfig.timesPerPage` at a time (8, 12, 24 or all; default 24) with Earlier and Later; sold-out times greyed, not hidden. Times stay hidden until a date is picked …

**Availability** (data table, from `getAvailability`): From `getAvailability`, now a `PerformanceAvailabilityPage` (a Page of `PerformanceAvailability`, each with `startsAt`): `channelCapacityId`, `performanceId`, `startsAt`, `capacity`, `sold`, `leased`, `remaining`, `byChannel`. The time grid calls it once with `eventId`, `from` and `to` for every performance in the window (decided 29 September, rev 3 REV3-1), not once per tile.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Channel capacity | the name it points at, never the id | — |
| Performance | the name it points at, never the id | The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart. |
| Starts at | 1 Oct 2026, 14:30 | The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's … |
| Capacity | 1,234 | — |
| Sold | 1,234 | — |
| Leased | 1,234 | Held by terminals but not yet sold. |
| Remaining | 1,234 | — |
| By channel | list or chips (count when long) | Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect. |
| Channel | chip: POS, Kiosk, Web, Mobile, B2B, Ota… | — |
| Allocated | 1,234 | — |
| Sold | 1,234 | — |
| Remaining | 1,234 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The performance** (detail panel, from `getPerformance`)

| Shows | Format | Notes |
|---|---|---|
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |

**Booking steps** (progress indicator, from `getPublishedBookingFlow`): The steps of the published flow in their `sortOrder`, this one (date and time) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back. Drawn in the venue's `BookingFlowSettings.stepIndicator` style; `embedMode` and `singleEventPage` come from the same published settings (CMS-016) (CHG-SGU-022).

| Shows | Format | Notes |
|---|---|---|
| Steps | list or chips (count when long) | Every step of the type, in the venue's order. Filled from the type when left out on create. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Continue (primary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | — |
| Quick tour (icon button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **time tile**: Start time in 24-hour venue time (19:30), places left when low ("6 left"), price per person when it differs by time; a surf-style four-day calendar shows sessions stacked by time in each day column with places left and price per surfer. *(source: REV3-19; DI-1041)*
- **hint in place of the next stage**: Until a session is chosen the ticket area says "Choose a session above to see its tickets and prices." Continue is off until date and time are both chosen. *(source: DI-1107; REV3-2)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Choose a time or session**: Reveals that session's tickets (WEB-005 stage). Adds nothing to the basket and holds nothing. If the cart's products ask consent questions they pop up once now, in the venue's theme, unless the page already asked the same question. *(source: DI-1107; F01 step 3; REV3-26; CLIENT-RESPONSE-30SEP 4)*
- **Set a quantity**: addCartLine takes the capacity for the cart's 15-minute window; the basket shows the line and the countdown. Refused with the next available time offered if the session filled meanwhile. *(source: contracts/spine/orders.yaml#addCartLine ("the window is 15 minutes"); F01 branch at step 3)*

**Data it reads**: `getAvailability` (onLoad, Live remaining capacity); `listPerformances` (onLoad, The times of the event for the picked date or range …); `getPublishedBookingFlow` (onLoad, The published booking flow for this product: which steps it …)

**Where the user goes next**

- → `WEB-005` Ticket Type Selection: *Picks a time; the tickets for it appear*; carries `performanceId`
- → `WEB-008` Add-ons & Upsell: *Add-ons & Upsell*
- → `WEB-010` Shopping Cart: *Reviews the cart and may enter a promotion code*; carries `cartId`; calls `getAvailability`
- → `WEB-015` Branded Queue / Waiting Room: *Adds tickets for a performance whose on-sale waiting room is on*; carries `performanceId`; only when `addCartLine` refused `403 admission-required`: this performance's room is on and the page holds no admission token for …; calls `addCartLine`
- → `WEB-007` Interactive Seat Selection: *Selects seats on the map*; carries `eventId`, `performanceId`; calls `getAvailability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The date session selection, read by `getPerformance`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the date session selection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No date session selection yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Empty, no results (`?state=emptyNoResults`) | No time matches the part of the day or the language picked, and the other times are still there. Names the filter and offers to clear it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 409 The question has changed since the cart was read (`questionVersionSuperseded`); the client re-reads the cart and asks the current version. (ConsentAnswerProblem); 422 A `perPerson` question answered without a person (`personRequired`), a question this cart does not … |

#### Edge cases to draw

- **The session sells out between loading and choosing**: "19:30 has just sold out" with the next available time pre-selected; nothing in the basket changes. *(source: F01 branch at step 3)*
- **Online share sold out while the gate still sells**: "Sold out online" on the tile; correct per-channel behaviour, worth showing so it is not reported as a bug. *(source: F01 branch at step 3)*
- **The event has exactly one on-sale performance**: This step is skipped; a seated event opens straight on the seat map. *(source: REV3-4)*
- **The performance has a branded waiting room on**: Adding tickets routes through WEB-015 before the line is taken. *(source: screens/P01-guest-web-storefront.yaml#WEB-006 transitions (ADR-0066))*

#### Consistency with other screens

- Match `GST-007`: Same reveal order, same day-part chips and the same consent pop-up. The app's own setting has times per page default 12 in the v4 build against 24 on the contract; use the contract default until the client says otherwise.
- Match `WEB-007`: For seated events this step and the seat map may render as one page; the time bar on the map is this step's time list.
- Match `KSK-005`: The kiosk's performance picker uses the same tiles and sold-out treatment.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Coastal Aqua (water park), Surf sessions with filters
dates: Fri 2 Oct to Thu 8 Oct, calendar for later
dayParts: Morning 6 · Afternoon 8 · Evening 4
sessions:
- time: 09:00
  name: Beginner surf
  place: Bay 1 · 55 min
  price: AED 295
  left: 12
- time: '19:30'
  name: Intermediate surf
  place: Bay 2 · 55 min
  price: AED 345
  left: 6
- time: '17:00'
  name: Expert barrels
  place: Reef · 55 min
  price: AED 495
  left: 0
tourLanguages:
- English
- العربية
- Français
- Deutsch
- 中文
- Русский
```

#### Permissions

- `checkBookingEligibility` → `PRODUCT_VIEW` (read) · guest, staff
- `getAvailability` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `addCartLine` → no permission · guest, partner, staff
- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `getCart` → no permission · guest, partner, staff
- `recordConsentAnswers` → `ORDER_CREATE` (operate) · guest, staff
- `getPublishedBookingFlow` → no permission · guest, staff

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.74 | System shall support event-driven integrations. | Ticketing Catalogue | CONTRACTED | `getAvailability` |
| 2.1.4 | The system should ensure full integration of all internal sales channels. All associated information (capacity, sales, etc.) must be available to multiple operators simultaneously in real-time. | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.10 | - Event capacity updated in real-time | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.6.14 | - Remaining quantities | Ticketing Sales | CONTRACTED | `getAvailability` |
| 2.7.14 | - Capacity management in real time is expected | Ticketing Sales | CONTRACTED | `getAvailability` |
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- The water-park swim answer changes the offer: All of us = full ride list at standard prices; Some of us = ride notes change and a "Swim vests needed" counter appears; None of us = tickets switch to a cheaper splash and river pass, slides removed from ride notes. The swim pop-up is not shown where the question is on the page. *(client request · design review 30 Sep 2026, 4. Swim ability and height gate: the answer changed nothing · DI-1108)*
- Picking a surf session adds nothing to the cart. Then "Tickets for Intermediate surf · 19:30" shows Surfer (session price), Junior surfer 10–15 and Spectator (AED 35); items reach the cart only when a quantity is set. Before a session: "Choose a session above to see its tickets and prices." *(client request · design review 30 Sep 2026, 3. Surfing session added to the cart straight away · DI-1107)*
- Swim ability is a consent question a venue attaches to a product or flow (e.g. "Are you able to swim?", "Do you hold a scuba certification?", "I accept the risk"), each with its own text and per-person or once-per- booking setting. Shown as a pop-up in the venue's theme after session/date; answers recorded. *(agreed · rev 3 design review 29 Sep 2026, REV3-26 · Built to match your examples: Swim question (water park) · DI-1062)*
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)*
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)*
- The guest picks a tour language (e.g. English, العربية, Français, Deutsch, 中文, Русский) and only tours in that language are listed. Cinema performances show language and format (2D/3D/subtitled) to pick from. *(agreed · rev 3 design review 29 Sep 2026, REV3-17 · 17. Guided tour times based on the tour language · DI-1057)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Theatre has its own auditorium seat map: stage (or screen for cinema) at front, Stalls/Circle/Balcony with curved rows, aisles and Premium/Standard/Economy pricing. Date, time, show (plus language & format for cinema) and the seat map sit on one page. Seats per guest booking default 10 (venue setting); basket lists each seat. *(agreed · rev 3 design review 29 Sep 2026, REV3-7 · 7. Theatre flow should be similar to the stadium flow · DI-1047)*
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)*
- More than eight times show as compact time tiles, paged with Earlier / Later (Times per page 8/12/24/all, default 24), with day-part chips (All, Morning, Afternoon, Evening) showing counts (filter on by default). Day-part boundaries are venue settings, default before 12:00 / 12:00–17:00 / from 17:00. *(agreed · rev 3 design review 29 Sep 2026, REV3-1 · 1. Many performances should resize and page; filter by morning, afternoon, evening · DI-1041)*
- On leaving selection (rides, water slides, kids club), each person declares an age band and height band; toggles only where needed (confident swimmer; guardian signature for 12–15). Per-person "Can't take part: too short, needs an adult" with Remove this guest / Choose another activity; Continue locked until all qualify. *(agreed · design review 29 Sep 2026, 3. Height and age check (WEB-006) · DI-1037)*
- Guided tours/sessions confirmed: date, then language, then time slot. Sessions come from configuration; the slot grid reflows when there are many slots. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W11 Guided tours / sessions · DI-1013)*
- Museum workshops: after Help me choose, the guest selects the workshop first, then date/time; only relevant products are shown. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W8 Workshops (museum) · DI-1010)*
- Surf sessions follow the time-selection pattern: products (beginner, intermediate...) appear only after a time slot is chosen. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W5 Surf sessions · DI-1007)*
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)*
- A venue selling a single event gets a dedicated page with a banner/video and brief description, showing only the near-term available dates (e.g. next 7 days) by default. *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-949)*
- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- Allam (ref. "Little Explorer"): show only a short near-term availability window by default (e.g. next 7 days) with a calendar icon that expands to a full calendar for later dates, instead of the flat 15-day range shown. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-915)*
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)*
- Date-change flow detects conflicts across an existing multi-ticket cart and lets the guest shift the whole booking to a new date in one action. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-587)*
- Allam's UX benchmark (Little Explorer, Dubai): multi-location selector, a horizontal near-term date picker with full-calendar fallback, and tabbed browsing (passes / workshops / packages) on one page rather than multiple screens. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-585)*
- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)*
- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*
- Camping/lesson-based tickets: when buying a multi-lesson package (e.g. ski or snowboard lessons on a regular schedule) the guest selects the specific class dates/performances. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-449)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Kidiya family-pass example showed a dynamic-pricing calendar applied at ticket-type level (prices shown on the calendar per date). *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-430)*
- Platinum List reference: event page with short video + image + description → select tickets → calendar collapsed to a week view, expandable to full month → time-slot selection. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-408)*
- Some clients (e.g. museums with 5-6 standard configurations) start by asking the number of guests, which narrows the calendar to dates/times with sufficient availability. *(client request · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-117)*
- Seat assignment flow is "select time, then select seat", with the two steps on different screens. *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-057)*

Also apply: 7 for P01 · Booking & Selection, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| … 36 more | | | `WHITE-LABEL.md` |

Also set there, as content the tenant writes: venue overrides: settings.

*Booking flows: steps, their order and per-flow settings*, set in `CMS-102` Site Builder, `CMS-103` Booking Flows:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

Also set there, as content the tenant writes: settings.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-006` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Engine controls → Water park → Surf sessions with filters → Book → Intermediate surf 09:00 → able to swim → one surfer (the session's tickets appear once it is …*. Differences: Merged into the ticket step (date first, time revealed after the date, tickets after the time). Prototype adds morning/afternoon/evening filters, times-per-page paging, sold-out greying, per-guest age/height eligibility dialog with 'Remove this guest', and the water-park 'Are you able to swim?' pop-up. YAML's separate hold call (addCartLine / inventory hold) is implicit. 30 September: a session's tickets (Surfer, Junior surfer, Spectator) appear once the session is chosen, and choosing it adds …
- Flow F01 *Guest buys a ticket online*, step 3: Picks a date, then a time → Holds nothing yet: capacity is held when the tickets go into the cart (step 4, `addCartLine`, a 15-minute cart hold), not on a look. Availability is read from a one-second cache (ADR-0065, decided 1 …
- Flow F02 *Guest buys seated tickets*, step 1: Picks a performance → Seated performances route to the map rather than to the cart. Per the published flow's `settings.seatEventDateMode` (`getPublishedBookingFlow`, W12; was `BookingFlowConfig`) the date and time are …
- Flow F01 branch at step 3 (recoverable): when The session sells out between loading the page and selecting it, Selection is refused with the next available session offered. Availability comes from a one-second cache (ADR-0065), and the hold is the guarded decrement, so this is caught here rather than at …
- Flow F01 branch at step 3 (recoverable): when The venue attached consent questions to the flow or to a product in the cart, Asked once, right after the session or date is picked (e.g. *Are you able to swim?*), per person or once per booking as each question says, and recorded as consent records by `recordConsentAnswers`. …
- Flow F01 branch at step 3 (recoverable): when The session shows sold out online while counter allocation remains, Correct behaviour, not a defect. Availability is per channel under channel allocation — web has exhausted its share. Worth stating because it will be raised as a bug.
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0065 *Browse availability is read from a one-second cache; the hold decides* (`docs/adr/0065-on-sale-availability-is-read-from-a-short-cache.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (40), with its required mark, default, format and its error state (400, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-006?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline, emptyNoResults.
- [ ] Every action is wired with its success and its failure: Continue, Quick tour.
- [ ] Every transition is wired: `WEB-005`, `WEB-008`, `WEB-010`, `WEB-015`, `WEB-007`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 32 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-007` Interactive Seat Selection

**Choose specific seats.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Booking & Selection · wave 2 · needs the `seating` module |
| Block | Block A · ticket #18132 (APP-WEB-WEB-007) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (compact density): `getSeatAvailability` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `performanceId` (deepLink), `eventId` (WEB-006), `holdId` (navigation), `venueId` (session) · cold entry: **A link to a performance that has happened.** Offers the next performance of the same event. |
| Route | `/booking-and-selection/seat-map-selection` |

**What the spec says about it.** A map with no geometry falls back to category and best-available selection. Availability returns renderMode: list, and the screen renders groups rather than a plan. Never refuses the seated flow. **Drawn 26 August** — `Seat Board 3.dc.html` frame `seat-3b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **Renamed 31 August** from *Seat Map Selection*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added recommendSeats. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** Date and time on seated events: an inline step before this map, or a pop-up over it, per `BookingFlowConfig.seatEventDateMode` (REV3-4); a single-performance event opens straight here. Time bar with performance switcher (REV3-6, `seatTimeBar`). View-from-your-seat box placed per `seatViewPosition` (REV3-5) and fed by a section photo or the geometry (23SEP-14). Fixture strip and a direct WEB-004 → WEB-007 path (23SEP-16). With WEB-006 this may render as one step (REV3-7). Seat picker defaults to the bowl (`seatPicker` default `bowl`, CFG-6). **The cabana map is no longer this screen:** a cabana, lounger or other spot placed …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Choose seats on the stadium or theatre map. Block A. The client's rule is sections first: the map opens with every section coloured by its price band, a tap zooms into that section on the same map to show its seats, and pinch or scroll out (or Whole map) returns to compare sections. Get right that each tapped seat is held at once and goes into the basket with section, row, seat and price.

**Fixed on main** (the package already carries these; draw what it says): The action bar shows "Create seat hold" as a primary button with a modal collecting id, performanceId, seatIds and ttlSeconds. (CHG-GST-003); The seat hold lasts 8 minutes but the cart's lease window is 15 minutes, and the screens show both as a countdown. (CHG-SGU-020).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Choose seats | seat map | — | — | — | — | **A seat selection screen with no seat map.** `noGeometry` is the state that matters: a map imported from a manifest alone can be sold from a list and not rendered, and the screen has to say which it … | — |
| Time bar | select field | — | — | — | — | Above the map: the chosen performance, the other times of the event to switch to, and **Change date**. Switching releases the seats held for the old performance (`relinquishSeatHold`, the guest's own … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |
| From | date and time picker | — | — | `listPerformances` ?from |
| To | date and time picker | — | — | `listPerformances` ?to |
| Category | picker: choose a category | — | — | `listPerformances` ?categoryId |
| Language | text field | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | `listPerformances` ?language |
| Product | picker: choose a product | — | — | `getPublishedBookingFlow` ?productId |
| Product category | picker: choose a product category | — | — | `getPublishedBookingFlow` ?productCategoryId |
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `getPublishedBookingFlow` ?flowTypeKey |

**Form: Recommend seats** (modal, opened by *Recommend seats*; *Recommend seats* calls `recommendSeats`, *Cancel* sends nothing)

**How many seats, and best available or together.** The party size is the tickets already chosen; the guest only picks the preference, then `recommendSeats` places them.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party size `partySize` | stepper or slider | required | — | min 1; max 50 | — | — | `recommendSeats` body |
| Strategy `strategy` | radio group | required | — | Best available · Best value · Closest to stage · Accessible · Contiguous | — | — | `recommendSeats` body |
| Categorys `categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `recommendSeats` body |
| Max price `maxPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `recommendSeats` body |
| Accessible count `accessibleCount` | number field | optional | 0 | — | — | Wheelchair spaces in the party. Companions are added automatically. | `recommendSeats` body |
| Max options `maxOptions` | number field | optional | 3 | max 10 | — | — | `recommendSeats` body |

Errors to draw in the form: 404 No selection satisfies the constraints

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **section**: Colour-coded by price band with the price on the map itself (no separate tier list). Tap zooms in place, never a modal or a new page. Mixed maps show standing sections ("fan pit") as a block with a quantity stepper instead of seats. *(source: MoM 29 Sep W2; DI-916; DI-950; DI-411)*
- **seat**: Zoomed in, every nearby section shows equal-size dots: available in the section's price colour, taken in grey, picked highlighted. Tap picks and holds; tap again releases. At most maxSeatsPerGuestOrder seats (default 10); the 11th tap says "Up to 10 seats per booking". Zoom in, Zoom out and Whole map buttons sit under the map. *(source: DI-983; DI-982; REV3-7; contracts/satellite/seating.yaml#/components/schemas/CreateSeatHoldRequest)*
- **performance (time bar)**: Above the map when seatTimeBar is on (default): the chosen performance, the event's other times and Change date. Switching shows a confirmation when seats are held ("Changing the show releases your 4 seats") and then releases them. *(source: REV3-6; DI-1046)*

#### Outputs: what the screen shows and produces

**Shown**

**The seat availability** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Totals | grouped details | — |
| By category | list or chips (count when long) | — |
| Seats | list or chips (count when long) | — |

**Banner** (banner): **One countdown: `Cart.expiresAt`** (the earliest lease in the cart), always visible. The 8-minute seat hold and the 15-minute cart lease are never shown as two clocks; a selection that expires silently while a guest enters card details is the worst outcome in this flow (CHG-SGU-020).

**Fixture strip** (card list, from `listPerformances`): The fixture (teams, date, kick-off) as a strip at the top of the seat step, so a single-performance fixture opens straight on the map.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Language | text | The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). |
| Format | text | How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**View from this section** (detail panel, from `getSeatAvailability`): When a section is picked: its photo (`sections[].viewAssetId`) if the venue uploaded one, otherwise a view rendered from the imported geometry (section boundary, stage position, seat positions) — closer sections show a larger stage and fewer rows ahead. Placed per `BookingFlowConfig.seatViewPosition` (bottom default, right, left, top) on wide screens; always below the map on narrow screens.

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| Total | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Sold | 1,234 | — |
| Blocked | 1,234 | — |
| Buffered | 1,234 | — |
| By category | list or chips (count when long) | — |
| Category | the name it points at, never the id | — |
| Available | 1,234 | — |
| Sold | 1,234 | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sections | list or chips (count when long) | The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the … |
| Code | text | — |
| Name | text | — |
| View image | the image or video | As `Section.viewAssetId`. Null means render the view from geometry. |
| Boundary | list or chips (count when long) | As `Section.boundary`. Null when `renderMode` is `list`. |

**Booking steps** (progress indicator, from `getPublishedBookingFlow`): The steps of the published flow in their `sortOrder`, this one (seats) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back. Drawn in the venue's `BookingFlowSettings.stepIndicator` style; `embedMode` and `singleEventPage` come from the same published settings (CMS-016) (CHG-SGU-022).

| Shows | Format | Notes |
|---|---|---|
| Steps | list or chips (count when long) | Every step of the type, in the venue's order. Filled from the type when left out on create. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Recommend seats (secondary button) | `recommendSeats` POST `/performances/{performanceId}/seat-recommendations` | SeatRecommendationRequest | inline | 404 No selection satisfies the constraints | opens modal first |
| Continue to checkout (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **view from this section**: The section's photo if supplied, else a render from the geometry (closer sections see a larger stage and fewer rows ahead). Placed bottom (default), right, left or top on wide screens; always below the map on narrow screens. *(source: REV3 23SEP-14; REV3-5; DI-1030)*
- **hold countdown**: Always visible once a seat is held: "Your seats are held for 7:42". Seats are held 8 minutes by default (extendable to 30 minutes in all); the basket shows the earliest expiry. Turns amber under 2 minutes. *(source: contracts/satellite/seating.yaml#/components/schemas/CreateSeatHoldRequest (ttlSeconds default 480, max 1800); contracts/spine/orders.yaml#/components/schemas/CartLine (leaseExpiresAt); AUDIT-29SEP …)*
- **basket line per seat**: One line per seat with section, row, seat and price, e.g. "Section 101 · Row A, Seat 4 · AED 165" or, at the theatre, "Stalls · Row F, Seat 9". *(source: DI-982; DI-1047)*
- **fixture strip**: The fixture (teams, date, kick-off) as a strip at the top, so a single-performance fixture opens straight on the map. *(source: REV3 23SEP-16)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Best available**: The guest picks a section and a party size and the system proposes seats together (accessible count and maximum price optional); accepting holds them like taps do. Shown as a link above the map, not a primary button. *(source: contracts/satellite/seating.yaml#recommendSeats; DI-410)*
- **Continue**: Off until at least one seat is held; goes to Add-ons, sign-in or the basket as the flow says. *(source: F02 step 2; REV3-3)*

**Data it reads**: `getSeatAvailability` (onLoad, Seat status for a performance); `listPerformances` (onLoad, The event's other times, for the time bar and the date and …); `getPublishedBookingFlow` (onLoad, The published booking flow for this product: which steps it …)

**Where the user goes next**

- → `WEB-005` Ticket Type Selection: *Ticket Type Selection*
- → `WEB-008` Add-ons & Upsell: *Add-ons & Upsell*
- → `WEB-006` Date & Performance Selection: *Date & Performance Selection*; carries `eventId`, `performanceId`
- → `WEB-010` Shopping Cart: *Reviews the cart*; carries `holdId`, `performanceId`

**What opens over it**

- modal *The seat map opens for an event with several performances and …*: **Pick the date and time over the seat map** instead of a separate step: the dates, then that day's times; choosing one loads that performance's seat availability. Closing it keeps the performance already shown (decided 29 September, rev 3 REV3-4).

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The interactive seat selection, read by `getSeatAvailability`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the interactive seat selection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No interactive seat selection yet. Offers Create seat hold (`createSeatHold`). |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Empty, no results (`?state=emptyNoResults`) | The event has no other time to switch to on the time bar; the chosen performance stays. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 One or more seats are no longer available, or the selection breaks a seating rule. (SeatConflictProblem); 409 The hold is no longer active (`holdNotActive`) - converted to an order, already released or expired.; 422 More seats than one booking may take: above `VenueSettings.seating.maxSeatsPerGuestOrder` on a guest channel (decided 29 September, rev 3 REV3-7), or above 10 … (SeatLimitProblem) |

#### Edge cases to draw

- **The map has no geometry (imported from a manifest only)**: The step sells from price categories and best-available groups as a list, saying so; it never shows an empty frame or refuses the seated flow. *(source: contracts/satellite/seating.yaml#/components/schemas/SeatAvailability (renderMode list); screens/P01-guest-web-storefront.yaml#WEB-007 notes)*
- **A seat is taken by someone else between drawing and tapping**: "Seat A4 was just taken" and the dot turns grey; other held seats are kept. *(source: contracts/satellite/seating.yaml#createSeatHold)*
- **The hold expires**: Seats return to the map, the basket lines are removed with a notice, and the guest can pick again. *(source: DI-422)*
- **A seating rule would leave a single empty seat**: The tap is refused with the reason ("Please don't leave a single seat between bookings"). *(source: DI-416)*
- **Date and time asked as a pop-up (seatEventDateMode popupOnSeatMap)**: The map opens with a dialog for date then time; closing it keeps the performance already shown. *(source: REV3-4)*

#### Consistency with other screens

- Match `GST-049`: Same section-first zoom and the same pinch in and out behaviour (agreed 30 September); the app always puts the view box below the map.
- Match `POS-004`: The till uses the same seat statuses and colours; the guest hold and the cashier hold are the same hold kinds.
- Match `WEB-049`: Transport seat selection (RTA layout, step 2 of 3) enters this screen; its map is a coach plan, not a bowl.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Union Arena (stadium), Desert Nights concert, Sat 10 Oct 20:00
priceBands:
- VIP Box AED 650
- Lower Tier AED 245
- Upper Tier AED 165
- Accessible bay AED 130 + companion free
picked:
- Section 101 · Row A, Seat 4 · AED 165
- Section 101 · Row A, Seat 5 · AED 165
theatre: Grand Playhouse, Stalls rows A-K AED 245, Circle A-E AED 165, Balcony A-D AED 95
countdown: Your seats are held for 7:42
```

#### Permissions

- `createSeatHold` → `ORDER_CREATE` (operate) · staff, guest
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `relinquishSeatHold` → `ORDER_CREATE` (operate) · staff, guest
- `getPublishedBookingFlow` → no permission · guest, staff

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

30 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.12 | The system should constantly update the seating arrangement as not to cause any double reservation (i.e. as not for two guests to select the same seat). | Ticketing Catalogue | CONTRACTED | `createSeatHold` |
| 21.5.11 | Mobile Seat Selection | Seat Management & Venue Mapping | CONTRACTED | `createSeatHold` |
| 21.5.12 | Cart Integration | Seat Management & Venue Mapping | CONTRACTED | `createSeatHold` |
| 21.5.21 | Multi-Seat Cart Management | Seat Management & Venue Mapping | CONTRACTED | `createSeatHold` |
| 1.3.15 | Define seating layouts, sections, pricing tiers, and total capacity. | Ticketing Catalogue | CONTRACTED | `getSeatAvailability` |
| 2.6.31 | Selling Event with a seat map, shared inventory with onsite sales. | Ticketing Sales | CONTRACTED | `getSeatAvailability` |
| 21.4.1 | Seat Status Management | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.2 | Seat Availability Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.3 | Seat Hold Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.4 | Seat Reservation Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.4.5 | Seat Sales Tracking | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| 21.5.13 | Real-Time Seat Availability | Seat Management & Venue Mapping | CONTRACTED | `getSeatAvailability` |
| … 18 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- Theatre has its own auditorium seat map: stage (or screen for cinema) at front, Stalls/Circle/Balcony with curved rows, aisles and Premium/Standard/Economy pricing. Date, time, show (plus language & format for cinema) and the seat map sit on one page. Seats per guest booking default 10 (venue setting); basket lists each seat. *(agreed · rev 3 design review 29 Sep 2026, REV3-7 · 7. Theatre flow should be similar to the stadium flow · DI-1047)*
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)*
- The 'view from your seat' box can sit Bottom (default), Right, Left or Top of the seat map (web only); on narrow screens and mobile it is always below the map. Setting "Seat view box". *(agreed · rev 3 design review 29 Sep 2026, REV3-5 · 5. CMS option to show the seat view right, left, top or bottom · DI-1045)*
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)*
- Picking a section shows the view from that section (concert mode shows the stage; closer sections see a larger stage with fewer rows in front). Use the venue's photo for the section when supplied, otherwise render the view from the imported 3D geometry. *(agreed · design review 29 Sep 2026, Seat map 14. Show the view to the stage in the small window · DI-1030)*
- Stadium/theatre seat maps show sections first with colour and price; zooming into a section shows its seats. Pinch-out / scroll-out returns to the full map so other sections can be compared. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W2 Seat maps · DI-1003)*
- Zoomed in, every nearby section shows its seats as equal-size dots: available in the section's price colour, taken in grey, picked seat highlighted. Zoom in, Zoom out and "Whole map" buttons sit under the map. *(client request · design review 23 Sep 2026, Seat map 17. When zoomed in, show the available seats across the map · DI-983)*
- Each picked seat goes into the cart with section, row, seat and price (e.g. "Section 101 · Row A, Seat 4 · AED 165"); tapping the seat again removes it. *(client request · design review 23 Sep 2026, Seat map 15. Selected seats should be added to the cart · DI-982)*
- On 3D venue maps, selecting a section takes the guest straight into that section's seats in one motion by zooming in, not via a separate pop-up, modal or new window. *(agreed · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-950)*
- Allam (ref. Platinum List Dubai): replace the tier-name list (VIP box, lower tier, upper tier) with a full colour-coded visual map of the venue upfront, each zone coloured with its price visible (e.g. gold near the stage, higher price; blue further away, lower), before drilling into the section's 2D/3D seat view. *(agreed · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-916)*
- 3D seat view: a guest booking a seated event (e.g. stadium concert) can preview the view from the selected section in 3D - built in (Three.js in React), no third-party integration; the standard 2D seat map remains the simpler option. *(agreed · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-889)*
- **Open question.** Prototype events: concert seat-map selection modelled on Coca-Cola Arena (like Platinum List); multi-day festival with day/time-slot selection; tiered show tickets (early bird, couple, group-of-4, group-of-6); all share one add-to-cart and checkout flow. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Events) · DI-685)*
- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)*
- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*
- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)*
- Platinum List reference seat step: interactive seat map colour-coded by price tier → seat selection with a live cart hold and countdown timer → checkout via Quick Order / Apple ID / Google ID. *(client request · MoM 21 Aug 2026, 4.1 Reference Walkthrough — Platinum List Seat Selection & Checkout Journey · DI-409)*
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)*
- Movie/cinema ticketing is in scope through the seat management module (e.g. a Kuwait museum's educational cinema: assigned seats, a film, a time slot). *(agreed · MoM 14 Aug 2026, 5. Movie Ticketing · DI-286)*
- Booking steps follow the product type: admission goes straight to quantity; dated products to a date, timed ones on to a time, then quantity; seated products to zone, then seats on a seat map, then quantity by variant (adult, child, concession). *(agreed · MoM 3 Aug 2026, Ticket Flow Variations by Product Type · DI-131)*
- Seat assignment flow is "select time, then select seat", with the two steps on different screens. *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-057)*

Also apply: 7 for P01 · Booking & Selection, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| … 36 more | | | `WHITE-LABEL.md` |

Also set there, as content the tenant writes: venue overrides: settings.

*Booking flows: steps, their order and per-flow settings*, set in `CMS-102` Site Builder, `CMS-103` Booking Flows:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

Also set there, as content the tenant writes: settings.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-007` · status **review** · provenance client-verified · **Drawn by Claude Design on `Seat Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (rev 3 (29 September build), verified 2026-09-29, match exact): `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`, view *Union Arena → 'Flow 1 · Fixed date → zone → seat map' or 'Flow 2 · Choose date & time → seat map'; Grand Playhouse → Flow 1 / Flow 2*
- Derived from `wireframes/reference/Seat Board 3.dc.html`
- Client design-board frames: `Seat Board 3.dc.html#seat-3b`
- Flow F02 *Guest buys seated tickets*, step 2: Selects seats on the map → Seats held with a visible countdown. At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1-50; `422 seat-limit-exceeded`), and the basket …
- Flow F02 branch at step 2 (recoverable): when The map has no geometry, Availability returns renderMode: list and the screen shows category groups and best-available. The seated flow is never refused — a venue that has not supplied a CAD plan can still sell.
- Flow F02 branch at step 2 (recoverable): when A selection would leave an orphan seat, Refused with the reason. Operators want orphan prevention and rarely ask for it by name.
- Flow F02 branch at step 3 (abandonsFlow): when The hold expires while the guest reads the cart, Seats return to the pool and the cart shows what was lost, with one action to re-select. A silent expiry discovered at payment is the worst outcome in this flow.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-007?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline, emptyNoResults.
- [ ] Every action is wired with its success and its failure: Recommend seats, Continue to checkout.
- [ ] Every transition is wired: `WEB-005`, `WEB-008`, `WEB-006`, `WEB-010`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 22 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-008` Add-ons & Upsell

**See add-ons & upsell for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Booking & Selection · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #18204 (APP-WEB-WEB-008) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (compact density): `getUpsellSuggestions` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `cartId` (session), `bundleId` (navigation), `venueId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/booking-and-selection/add-ons-and-upsell` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. Add-ons. Sanket noted on the 20 August review that the screen shows individual add-ons rather than bundles, and it does. **Rewired on that review.** **Corrected 1 October (audit R269):** these notes said `listCatalogueBundles` had gone from this screen then; it never left `apis`, and it is still bound to the *Every bundle* table. It lists the signed catalogue snapshots terminals pull (ADR-0013), not the sellable bundles `promotions.listBundles` returns, so unbinding it is still owed; GST-056, in the same add-ons pair, calls it too, and the two change together. **Rev 3 (decided 29 September).** **Sign-in gate (REV3-3):** with `BookingFlowConfig.signInAt` `afterAddOns` (default), leaving this step asks the guest to sign in, or for a guest code when guest checkout is on (WEB-016); the basket is kept. With `atPayment` the gate is at WEB-012. Floating basket icon and cart side (REV3-10). Every booking-flow setting named here is read from `getTenantConfig` `bookingFlow`, resolved for the venue the guest picked (audit R267): the tenant's values with that venue's `venueOverrides` entry laid over field by field (decided 29 September, rev 3 CFG-11). **The step order comes from the published booking flow** (W12, 29 September): `getPublishedBookingFlow` returns the flow the product (or its category, else the venue default for its kind) uses, with its enabled steps in `sortOrder`; this screen renders when that flow has its step and in the order the flow gives. Flow-level settings …

**From the AI & Intelligence process.** The web Extras step ("Add-ons & Upsell"): the distinct step after ticket selection where up to three upgrades, add-ons and bundles are offered, before sign-in (with "Ask to sign in: After add-ons", the default) and the cart. Block A offers come from the Promotions relationship map through the recommendation slot; Block B swaps in the engine. The one thing to get right: offers must look like helpful extras the guest can ignore, never like a required step, and the add-ons live only here.

**Fixed on main** (the package already carries these; draw what it says): dataTable "Every bundle" bound to listCatalogueBundles (signed terminal snapshots, with publishedBy, contentHash, signatureKeyId columns). (CHG-SGU-016); The suggestion panel binds getUpsellSuggestions, which is not in the screen's apis (decideRecommendations is). (CHG-SGU-016); The WEB-008 to WEB-016 transition (sign-in after add-ons) is missing from navigation. (CHG-SGU-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the swim-vest add-on offered here for non-swimmers (Help me choose answer), and is the splash-and-river pass a separate product?** → Drawn default stands (answer: "Default / recommended accepted"): The vest is an add-on on this step; the splash-and-river pass is its own product (as built). *(decided by Chinmay, 2026-10-02; DEC-015 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getPublishedBookingFlow` ?productId |
| Product category | picker: choose a product category | — | — | `getPublishedBookingFlow` ?productCategoryId |
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `getPublishedBookingFlow` ?flowTypeKey |

**Form: Add cart line** (modal, opened by *Add cart line*; *Add cart line* calls `addCartLine`, *Cancel* sends nothing)

**Collects what `addCartLine` sends before it is called.** Required: `variantId`, `quantity`. Optional: `performanceId`, `seatIds`, `parentLineId`, `attributes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

Errors to draw in the form: 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem)

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **add-on quantity**: -/+ stepper, minimum 0, price multiplies (setting "Quantities on add-ons"); mandatory add-ons attached to a product are pre-selected and cannot be removed here. *(source: DI-1070 / DI-470)*
- **No thanks**: As GST-048 - an explicit decline per card; ignoring is not a decline. *(source: ADR-0052 (AI-D07) / contracts/satellite/ai.yaml#recordRecommendationEvents)*

#### Outputs: what the screen shows and produces

**Shown**

**Suggested for you** (card list, from `decideRecommendations`): The engine's slot (`decideRecommendations`, placement cart, maxItems 3: the client set at most three, DI-959), answered in Block A from the Promotions relationship map (ADR-0052). Each card shows the price from Pricing and the template reason; impressions and clicks go to `recordRecommendationEvents`.

| Shows | Format | Notes |
|---|---|---|
| Product | the name it points at, never the id | The product recommended. Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind` (29 … |
| Kind | chip: Upsell, Cross sell, Upgrade, Bundle, Add on, Membership… | — |
| Price ref | text | The Pricing reference the channel resolves to a price. AI never computes a price. |
| Reason text | text | The rendered template in the session locale, where the channel shows reasons. |
| Rank | 1,234 | — |

**The bundle** (detail panel, from `getBundle`): A bundle the recommendation slot names (`kind` bundle), opened from its card; signed catalogue snapshots (`listCatalogueBundles`) are the tills', not the guest's (R269).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Fixed, Dynamic, Mandatory, Optional, Promotional | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Components | list or chips (count when long) | — |
| Choice groups | list or chips (count when long) | Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups … |
| Allocation | grouped details | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| ID | the name it points at, never the id | — |
| Savings amount | AED 1,234.50 | Sum of component list prices less the bundle price. |
| Savings percentage | 1,234.5 | — |
| Has been sold | yes / no (icon or chip) | True locks components and allocation against amendment. |
| Is active | yes / no (icon or chip) | — |

**Booking steps** (progress indicator, from `getPublishedBookingFlow`): The steps of the published flow in their `sortOrder`, this one (extras) highlighted. A step the flow has turned off is not shown and is skipped by Continue and Back. Drawn in the venue's `BookingFlowSettings.stepIndicator` style; `embedMode` and `singleEventPage` come from the same published settings (CMS-016) (CHG-SGU-022).

| Shows | Format | Notes |
|---|---|---|
| Steps | list or chips (count when long) | Every step of the type, in the venue's order. Filled from the type when left out on create. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add cart line (primary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **offer cards**: Max three, ranked, image + name + price + template reason; bundles show savings with the original struck through (savingsAmount / savingsPercentage from the bundle). Reasons from templates only, in the page language. *(source: DI-959 / DI-586 / contracts/satellite/promotions.yaml#getBundle / ADR-0052 (AI-D09))*
- **booking step indicator**: The Extras step is one step of the venue's published booking flow; when the flow has no Extras step or nothing qualifies, the step disappears from the indicator. *(source: contracts/satellite/white-label.yaml#getPublishedBookingFlow / DI-428)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Continue**: With signInAt afterAddOns (default) opens sign-in (WEB-016), or the guest code when guest checkout is on; the basket is kept. With atPayment goes straight to the cart. *(source: DI-1043 / screens/P01-guest-web-storefront.yaml#WEB-008 (notes, REV3-3))*
- **Add / No thanks**: As GST-048. *(source: contracts/spine/orders.yaml#addCartLine / contracts/satellite/ai.yaml#recordRecommendationEvents)*

**Data it reads**: `decideRecommendations` (onLoad, Fill the cart slot, maxItems 3 (DI-959)); `getPublishedBookingFlow` (onLoad, The published booking flow for this product: which steps it …)

**Where the user goes next**

- → `WEB-005` Ticket Type Selection: *Ticket Type Selection*
- → `WEB-006` Date & Performance Selection: *Date & Performance Selection*; carries `cartId`, `performanceId`
- → `WEB-010` Shopping Cart: *Shopping Cart*; carries `cartId`, `code`, `performanceId`
- → `WEB-016` Login / Register: *Continue — sign in or use a guest code (when sign-in is asked after add-ons)*; carries `cartId`; only when the guest is not signed in

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The add-ons, read by `decideRecommendations`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the add-ons upsell untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No add-ons for this booking: the step is skipped and Continue goes on to sign-in. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem) |

#### Edge cases to draw

- **Recommendation slot times out (200 ms) or recommendations are paused**: Rules answer or no offers; the step renders the venue's configured add-ons for the product and never blocks Continue. *(source: ADR-0052 / contracts/satellite/ai.yaml#pauseAiCapability)*
- **Guest is a member**: No membership offer; F&B or retail add-ons instead. An expiring membership shows a renewal. *(source: DI-960)*
- **Arabic**: Cards mirror; the cart stays on the right by default ("Cart side in Arabic"). *(source: DI-1051)*

#### Consistency with other screens

- Match `GST-048`: Same step, same limits and wording.
- Match `GST-056`: The app's add-ons screen shares the catalogue-bundle binding that must be removed (R269); change both together.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Coastal Aqua
cart: 2 Adult + 2 Child Day Pass, Sat 10 Oct
offers:
- name: Family Day Pass (2+2)
  price: AED 540.00
  was: AED 600.00
  reason: Saves AED 60 for your family
- name: Cabana - Family
  price: AED 350.00
  reason: Shade and seating for up to 6
- name: Lunch combo
  price: AED 45.00 each
  reason: Burger, fries and a drink
  stepper: true
```

#### Permissions

- `addCartLine` → no permission · guest, partner, staff
- `getBundle` → `PRODUCT_VIEW` (read) · staff, guest
- `decideRecommendations` → `AI_USE` (operate) · staff, guest, anonymous
- `recordRecommendationEvents` → `AI_USE` (operate) · staff, guest, anonymous
- `getPublishedBookingFlow` → no permission · guest, staff

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

47 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |
| 19.2.46 | Personalized Offers - System shall provide personalized offers. | Guest Mobile App & Branding | CONTRACTED | `decideRecommendations` |
| 1.1.33 | AI shall recommend suitable ticket products, upgrades, bundles and promotions based on guest profile, behavior and purchase history. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.34 | AI shall recommend upgrades, add-ons and premium experiences during the purchasing journey. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 1.1.35 | AI shall automatically recommend ticket bundles, packages and complementary products to maximize guest value and revenue. | Ticketing Catalogue | CONTRACTED | `decideRecommendations` |
| 2.6.46 | AI shall recommend relevant tickets, memberships, packages, upgrades, add-ons, F&B, retail products, and experiences based on browsing behavior, purchase history, guest profile, selected products … | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 2.13.45 | AI Assisted Recommendations | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 2.14.18 | AI recommends upgrades, renewals and offers. | Ticketing Sales | CONTRACTED | `decideRecommendations` |
| 3.7.9 | System shall generate personalized recommendations for attractions, experiences, memberships, annual passes, F&B products, retail products, upgrades, and add-ons using AI and behavioral analytics. | Admission and Access | CONTRACTED | `decideRecommendations` |
| … 35 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Is the swim vest an add-on product, and is the splash-and-river pass a separate product offered only to non-swimmers? Default built: the swim answer filters products (as Help me choose); the vest is an add-on; the splash-and-river pass is its own product. *(open · Decisions Register 1 Oct 2026, Questions for the client — Guest safety / Swim ability · DI-1118)*
- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)*
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)*
- Add-ons appear only on the Add-ons / Extras step, never in the ticket panels. Each add-on appears once (no duplicates such as 'Large locker' on two steps). *(client request · design review 23 Sep 2026, Cart 11. Show add-ons only on the Add-ons / Extras page · DI-979)*
- "Upgrade your day" (upgrades) stays hidden until a main ticket is in the cart. *(client request · design review 23 Sep 2026, Cart 10. Show upgrades only after the main ticket is in the cart · DI-978)*
- A guest is not repeatedly re-offered something already declined (e.g. a fast pass rejected three times), and an offer ignored online is not re-presented on another channel, e.g. at POS after the guest bought it there. *(agreed · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-962)*
- What a guest is offered depends on context: a member is not offered another membership (F&B or retail add-ons instead); general admission is not offered once VIP/fast pass is selected; an expiring membership prompts a renewal rather than a new product; similar offers are not shown back-to-back (alternate F&B and experience upsells). *(client request · MoM 21 Sep 2026, 4.2 / 4.3 / 4.5 Recommendation Strategy and Decisioning · DI-960)*
- Recommendations stay within business limits, e.g. at most three recommendations shown at checkout and never a product the customer already owns; AI recommendations never override hard business rules or eligibility constraints. *(agreed · MoM 21 Sep 2026, 4.3 Recommendation Strategy — Business Priority, Conflict Suppression & Fallback · DI-959)*
- Upsell/cross-sell offers (e.g. a family pass after 2 adult + 2 child tickets are added) are a distinct "extras" step after main product selection, not inline on the ticket selection page, where guests would miss them. *(agreed · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-951)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*
- Reference details: sibling/multi-buy discount shown with a struck-through original price; workshop add-ons inline with theme/cuisine sub-selection feeding time-slot availability; a package builder for bundled experiences. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-586)*
- Add-ons attached to a main product can be mandatory or optional; cross-sell offers related add-on products, upsell proposes a higher tier (e.g. adult admission → membership). *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-470)*
- Decision: the add-ons step is optional/removable in configuration for products with no add-ons, collapsing the flow to Ticket Selection → Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-428)*
- System-driven upsell/cross-sell prompts, e.g. a yearly membership on top of general admission, or a family bundle when 2 adult + 2 child tickets are in the cart, each with its discount/benefit. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-216)*

Also apply: 7 for P01 · Booking & Selection, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| … 36 more | | | `WHITE-LABEL.md` |

Also set there, as content the tenant writes: venue overrides: settings.

*Booking flows: steps, their order and per-flow settings*, set in `CMS-102` Site Builder, `CMS-103` Booking Flows:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Flow type key (`bookingFlows.flowTypeKey`) | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour … | — | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). |
| Booking flows name (`bookingFlows.name`) | max length 80 | — | Staff-facing, e.g. "Day pass, date first". |
| Is default for type (`bookingFlows.isDefaultForType`) | At most one per venue and type; setting it takes it from the previous default. | off | At most one per venue and type; setting it takes it from the previous default. |
| Booking flows is enabled (`bookingFlows.isEnabled`) | — | on | A disabled flow is kept and not published; products naming it fall back to the default. |
| Steps (`bookingFlows.steps`) | at most 30 | — | Every step of the type, in the venue's order. Filled from the type when left out on create. |
| Steps: step key (`bookingFlows.steps[].stepKey`) | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … |
| Steps: enabled (`bookingFlows.steps[].enabled`) | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | A `required` step cannot be off; the flow saves and `isValid` turns false. |
| Steps: sort order (`bookingFlows.steps[].sortOrder`) | min 0 | — | — |
| Steps: settings (`bookingFlows.steps[].settings`) | A name the type does not give is refused with 400. | — | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. |
| Settings: performance reveal (`bookingFlows.settings.performanceReveal`) | Date time ticket · All at once | Date time ticket | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. |
| Settings: sign in at (`bookingFlows.settings.signInAt`) | After add ons · At payment | After add ons | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). |
| Settings: seat event date mode (`bookingFlows.settings.seatEventDateMode`) | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. |
| Settings: extras step (`bookingFlows.settings.extrasStep`) | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. |
| Settings: quick tour (`bookingFlows.settings.quickTour`) | — | off | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. |
| Settings: consent questions (`bookingFlows.settings.consentQuestionIds`) | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. |

Also set there, as content the tenant writes: settings.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-008` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Book → 'Extras' step (e.g. Summit Peaks → Dated day pass → Continue)*. Differences: Sign-in is asked when leaving Add-ons (Config 'Ask to sign in: After add-ons', Rev 3 item 3), so WEB-008 → WEB-016 is a transition YAML does not have. Add-ons also appear on the payment step (combo) and confirmation (upsells). 28 Sep flow review: all add-ons live here only.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0052 *One recommendation engine; runtime in AI, configuration in Promotions* (`docs/adr/0052-one-recommendation-engine.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-008?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add cart line.
- [ ] Every transition is wired: `WEB-005`, `WEB-006`, `WEB-010`, `WEB-016`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 16 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-009` Wishlist

**Find the right one quickly, and act on it without opening it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Booking & Selection · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #18224 (APP-WEB-WEB-009) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (compact density): `getWishlist` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `itemId` (deepLink), `subjectId` (session) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/booking-and-selection/wishlist` |

**What the spec says about it.** Withdrawn products stay in the list marked unavailable. A guest who saved something and finds it silently gone assumes the feature is broken. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Wishlist. **Device operations removed** — Sanket flagged that no device management appears on this screen, and he was right. **Rewired on the 20 August review.** **Rev 3 (decided 29 September, rev 3 GAP-D3).** Built as one implementation with WEB-024 (the account's devices, wishlist and consent); both ids are kept.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The guest's wishlist on the web: products, and specific dates, saved to book later, including F&B and retail items to buy on site. It is built as one implementation with WEB-024 (account) and keeps both ids. The one thing to get right: nothing silently disappears. A withdrawn product stays on the list marked as no longer available, because a guest who finds a saved item gone assumes the feature is broken.

**Fixed on main** (the package already carries these; draw what it says): The "Add to wishlist" modal on this screen asks the guest to supply a variantId (and optionally a performanceId). (CHG-SGU-017).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a wishlist entry for a performance that has passed stay, or should the platform drop it, and should a guest be told when a saved date is about to sell out?** → Drawn default stands (answer: "Default / recommended accepted"): Keep it under "Past dates" (no deletion); no sell-out alert until a journey for it is configured. *(decided by Chinmay, 2026-10-02; DEC-022 / CHG-NOTE-002)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Saving an item (heart on a product or date card)**: Saving happens on the product and date screens (WEB-005, WEB-006), not by typing on this screen. The entry key is the variant plus the performance. The same product for two different dates is two entries; a save with no date is a third, date-less entry for the product generally. Saving twice is one entry, so a double tap never inflates the count. *(source: contracts/satellite/marketing-crm.yaml#addToWishlist; R149)*
- **Note**: Optional free text the guest keeps for themselves ("for Omar's birthday"). Shown under the item, editable only by removing and saving again (there is no update operation). *(source: contracts/satellite/marketing-crm.yaml#addToWishlist)*

#### Outputs: what the screen shows and produces

**Shown**

**The wishlist** (detail panel, from `getWishlist`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Items | list or chips (count when long) | — |

**Removed. Undo** (toast, from `addToWishlist`): The 5-second Undo after Remove; re-saves the same entry.

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Variant | the name it points at, never the id | — |
| Product name | text | — |
| Performance | the name it points at, never the id | — |
| Performance starts at | 1 Oct 2026, 14:30 | — |
| Price | AED 1,234.50 | The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the … |
| Image | the image or video | — |
| Is available | yes / no (icon or chip) | False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and … |
| Unavailable reason | text | — |
| Note | text | — |
| Added at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Browse (secondary button) | navigation or local | — | — | — | — |
| Remove from wishlist (destructive button) | `removeFromWishlist` DELETE `/guests/{subjectId}/wishlist/{itemId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Each saved item**: Photo, product name, ticket type, the saved date and time or "Any date", and the current price from the catalogue in AED. Items whose product was withdrawn come back with isAvailable false: show them greyed with "No longer available" and offer only Remove, never Book. *(source: contracts/satellite/marketing-crm.yaml#getWishlist)*
- **Order of the list**: Dated items soonest first, then "Any date" items, then unavailable items last. Group F&B and retail items to buy on site under their own heading, because they are bought at the venue, not online. *(source: designer default; DI-202)*
- **Header count**: The count of saved items in the account menu equals the list length. Idempotent saves keep it honest. *(source: contracts/satellite/marketing-crm.yaml#addToWishlist)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Book**: Opens ticket selection (WEB-005) or the date step (WEB-006) with the product, and the date where one was saved, pre-selected. If that date has sold out, the date step opens with the date shown as sold out rather than silently moving to another date. *(source: screens/P01-guest-web-storefront.yaml#WEB-009)*
- **Remove**: Removes the one entry (removeFromWishlist). No confirmation dialog for a single item. Show an Undo toast for 5 seconds; Undo re-saves the same variant and date, which is idempotent. *(source: contracts/satellite/marketing-crm.yaml#removeFromWishlist; designer default)*

**Data it reads**: `getWishlist` (onLoad, Read a guest's saved items)

**Where the user goes next**

- → `WEB-005` Ticket Type Selection: *Ticket Type Selection*
- → `WEB-006` Date & Performance Selection: *Date & Performance Selection*; carries `performanceId`

**What opens over it**

- confirmDialog *Remove from wishlist*: **Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A wishlist this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Saved items load |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | Nothing saved — explains what the list is for |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |

#### Edge cases to draw

- **The saved date is in the past**: Shown under "Past dates" with "This date has passed" and a Book another date action that opens the date step for the product. The contract only flags withdrawn products, so this state is read from the performance date on the client. *(source: contracts/satellite/marketing-crm.yaml#getWishlist)*
- **Guest not signed in**: Sign in and come back here. The wishlist is the guest's own and has no anonymous version. *(source: screens/P01-guest-web-storefront.yaml#WEB-009)*
- **Offline or the connection drops**: The list already loaded stays, marked with its age. Remove and Book wait for the connection and say so. *(source: screens/P01-guest-web-storefront.yaml#WEB-009)*

#### Consistency with other screens

- Match `GST-020`: Same list, same item card, same "No longer available" treatment, same wording "Wishlist".
- Match `WEB-024`: One implementation with two ids (GAP-D3); the account's wishlist pane is this screen.
- Match `BO-757`: A saved item is a behavioural signal segments read (wishlist-based audiences); the guest never sees that wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
items:
- Coastal Aqua Day Pass - Adult, Sat 17 Oct 2026, AED 295.00
- Kids Club Explorer Pass - Child (any date), AED 120.00
- Tidewater Museum Pearl Diving Heritage Tour, Fri 23 Oct 2026 14:30, AED 85.00 (No longer available)
- On site - Karak chai and luqaimat, AED 18.00
noteExample: For Omar's birthday
```

#### Permissions

- `getWishlist` → no permission · guest
- `addToWishlist` → no permission · guest
- `removeFromWishlist` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.44 | System shall allow guests to save tickets, memberships, events, packages, add-ons, F&B items, retail products, and experiences to a wishlist for future purchase. Wishlist items shall remain linked to … | Ticketing Sales | CONTRACTED | `addToWishlist` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Duplicate screens become one implementation covering several screen IDs (mobile Transfer + Delivery & Sharing; web Wishlist / Devices & Consent; Help Centre + Help & Accessibility as one Help view with FAQ, cases, policies, accessibility tabs). Ticket-selection functions belong on GST-008. Web gets a Group Booking view. *(agreed · design review 29 Sep 2026, GAP-D3 · D. Duplicate screens merged; group booking on web · DI-1078)*
- Add bookings to Apple/Google/Outlook calendar with reminders; wishlist of F&B and retail items to buy later on-site. *(client request · MoM 10 Aug 2026, 4.3 B2C Guest App — End-to-End Booking Journey · DI-202)*

Also apply: 7 for P01 · Booking & Selection, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-009` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Discover → 'Wishlist' link (discoverLinks)*. Differences: No 'withdrawn product stays marked unavailable' state (YAML note). Prototype adds 'Restore removed' and live queue times.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-009?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Browse, Remove from wishlist.
- [ ] Every transition is wired: `WEB-005`, `WEB-006`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-047` Map Booking — Cabanas & Spots

**Pick a specific cabana, lounger or other spot on the venue map and hold it while you book.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Booking & Selection · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20736 (APP-WEB-WEB-047) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `getMapResourceAvailability` reads the population of spots and a tap holds one of them — list (as a map), select, act |
| Offline | **The offline banner shows.** The map and the spots already loaded stay on screen with their age, never shown as free now. Holding a spot and adding it to the basket need the connection — a cabana held offline is a cabana two people think they have. |
| Opens with | `mapId` (WEB-004), `productId` (WEB-004), `cartId` (session), `venueId` (session), `holdId` (navigation) · cold entry: **A link to a map that is no longer published, or a day that has passed,** says which and offers today on the current map. Nothing is held on arrival. |
| Route | `/booking-and-selection/map-booking` |

**What the spec says about it.** **New 29 September** (decided 29 September, rev 3 REV3-15 and GAP-C2). **Cabana maps work like the stadium seat map:** the venue's map is ingested with its cabanas, loungers and other bookable spots (number, zone, capacity, price band), and the guest picks a specific one on the map and buys it. This supersedes audit R073 (c) (*cabanas stay staff-booked*) for resources placed on an ingested map. **Tables on the map are non-dining spots sold like cabanas** (decided 29 September by the user); a restaurant table stays the F&B reservation flow (WEB-036 / GST-070). The map comes from `getVenueMap` (its `resources`: label, kind, zone, capacity, price band, boundary) and the status of every spot for the chosen day from one `getMapResourceAvailability` call, joined on `resourceId`; held, booked and unavailable spots are greyed. Tapping a free spot calls `createResourceHold` and starts the *Remaining time* counter from the hold's `expiresAt` (8 minutes, extendable to 30 in all, audit R169); Add to basket sends `addCartLine` with the spot's price-band `variantId` and the `resourceHoldId`, e.g. *Cabana B09 · Large cabana · Beach, AED 1,855*. Picking another spot releases the first hold (`relinquishResourceHold`). **29 September (W6).** Map booking of cabanas stays **optional per flow**: the venue picks *Cabana: pick on map* (WEB-047) or *Cabana: by size* (capacity) as its booking flow (CMS-103), and the resource selection policy (`guestMayChoose`, REV3-15) decides whether the guest chooses the unit. Same venue-map back end as F&B and locations.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The guest picks a specific cabana, lounger, beach table or other spot on the venue's ingested map, like a stadium seat: numbered spots by zone, free ones tappable, held/booked ones greyed, a list alternative, and a remaining-time counter once a spot is held. The one thing to get right: the hold countdown is always visible and the spot is released (and the guest told) when it runs out.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should cabana categories (premium, VIP, luxury, private, family, couples) be a filter on the map?** → Drawn default accepted: Show category as a filter chip row above the zones when the venue sets categories. *(decided by Chinmay, 2026-10-02; DEC-143 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date | date picker | — | — | — | — | Sends `from`/`to` (the venue's opening for the day, or a slot) to `getMapResourceAvailability`. | — |
| Who is coming | number field | — | — | — | — | `partySize`; a spot smaller than the party is refused `422 party-exceeds-capacity`. | — |
| Area | text field | optional | — | max length 80 | — | Beach, Tower, Riverside, Splash zone… from the placed resources' zones. | `PlacedResource.zone` |
| Venue map | repeatable rows | optional | — | — | — | The ingested map with every placed spot drawn at its boundary and numbered (R01-R10, T01-T08, S01-S06, B01-B10 on Coastal Aqua). Free spots are tappable; held, booked and unavailable ones greyed. | `VenueMapDetail.resources` |
| Map | repeatable rows | optional | — | at most 50 | — | **Which map to book on.** `listBookableVenueMaps(venueId, productId)` returns the venue's published maps that carry bookable spots; with one map the screen opens it directly and this choice is not … | `BookableVenueMaps.maps` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | number field | — | — | `getVenueMap` ?version |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, because the draft is unfinished work that must never reach a guest. | `getVenueMap` ?draft |
| Map | picker: choose a map | — | — | `getMapResourceAvailability` ?mapId |
| From | date and time picker | — | — | `getMapResourceAvailability` ?from |
| To | date and time picker | — | — | `getMapResourceAvailability` ?to |
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `getMapResourceAvailability` ?kind |
| Product | picker: choose a product | — | — | `listBookableVenueMaps` ?productId |
| Kind | radio group | — | Cabana · Lounger · Table · Pitch · Other | `listBookableVenueMaps` ?kind |

**Form: Pick another (or tapping a second spot)** (confirmDialog, opened by *Pick another (or tapping a second spot)*; *Release it* calls `relinquishResourceHold`, *Keep it* sends nothing)

**Release the spot you are holding?** It goes back on the map at once and someone else may take it.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Sent by *Add to basket*** (`addCartLine`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Date (and slot)**: Short date strip plus calendar; the day's window is the venue opening, or a slot where the product is slotted. *(source: contracts/satellite/resources.yaml#getMapResourceAvailability / TRACKER Actions row 312)*
- **Who is coming**: Party size stepper (adults and children); spots smaller than the party are shown but not tappable, with "Seats 4". *(source: contracts/satellite/resources.yaml#createResourceHold)*
- **Area / Map**: Zone chips (Beach, Tower, Riverside, Splash zone) filter the map; a map selector only when the venue has more than one bookable map. *(source: contracts/satellite/venue-map.yaml#listBookableVenueMaps)*

#### Outputs: what the screen shows and produces

**Shown**

**Spots** (card list, from `getMapResourceAvailability`): The same spots as a list for the chosen area: number, capacity, price band and price, status. The accessible alternative to the map.

| Shows | Format | Notes |
|---|---|---|
| Map | the name it points at, never the id | — |
| Map version | 1,234 | The published `venue-map` version the placements were read from; the client checks it against the map it cached. |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Totals | grouped details | — |
| Total | 1,234 | — |
| Available | 1,234 | — |
| Held | 1,234 | — |
| Booked | 1,234 | — |
| Unavailable | 1,234 | — |
| Resources | list or chips (count when long) | — |
| Resource | the name it points at, never the id | — |
| Placed resource | the name it points at, never the id | The `venue-map.PlacedResource` it was read from. |
| Label | text | As on the map, e.g. `B09`. |
| Kind | chip: Cabana, Lounger, Locker, Wheelchair, Stroller, Equipment… | BL-135. `locker` was an entitlement kind in `orders` and nothing issued, assigned or released one. |
| Zone | text | — |
| Capacity | 1,234 | — |
| Price band code | text | — |
| Variant | the name it points at, never the id | What the cart line names to buy it. |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Remaining time** (banner, from `getResourceHold`): Counts down from the hold's `expiresAt`, always visible. At zero the spot is released and the guest is told.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Map | the name it points at, never the id | — |
| Resources | list or chips (count when long) | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Party size | 1,234 | — |
| Status | chip: Held, Converted, Released, Expired | — |
| Total price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Held by principal | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Order | the name it points at, never the id | Set when the order converts it. |
| Extension count | 1,234 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**The spot you picked** (detail panel, from `getVenueMap`)

| Shows | Format | Notes |
|---|---|---|
| Label | text | What the guest sees and taps, e.g. `B09`. |
| Kind | chip: Cabana, Lounger, Table, Pitch, Other | A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold … |
| Zone | text | The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`. |
| Capacity | 1,234 | Guests it takes, e.g. 15. |
| Price band code | text | The band it sells in, e.g. `Large`, one of the `priceBands` given at import. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add to basket (primary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | — |
| Keep it longer (secondary button) | `extendResourceHold` POST `/resource-holds/{holdId}/extend` | — | ResourceHold | 409 Already expired or converted, or the extension limit is reached. `refusedReason` says which. (ResourceHoldExtendProblem) | — |
| Pick another (secondary button) | `relinquishResourceHold` DELETE `/resource-holds/{holdId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens confirmDialog first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Map**: Spots drawn at their boundaries and numbered by zone (R01-R10, T01-T08, S01-S06, B01-B10); free in the brand colour, held or booked greyed and marked, unavailable struck; the selected spot outlined. Map on the first screen, not behind a button. *(source: DI-1055 / contracts/satellite/venue-map.yaml#getVenueMap)*
- **Spot card**: "Cabana B09 - Large cabana - Beach - seats 6 - AED 1,855" with amenities where the product carries them. *(source: DI-1055 / DI-687)*
- **Remaining time**: Banner counting down from the hold's expiry; at zero, "Your hold on B09 has ended" and the spot frees. *(source: contracts/satellite/resources.yaml#getResourceHold / DI-1055)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tap a free spot**: Places a hold for the window and starts the counter; tapping a second spot asks to release the first. *(source: contracts/satellite/resources.yaml#createResourceHold / F52 step 2)*
- **Keep it longer**: Extends the hold where allowed; disabled when the maximum extensions are used, with the reason. *(source: contracts/satellite/resources.yaml#extendResourceHold)*
- **Add to basket**: Adds the spot's price band and the hold to the cart; continue to add-ons (towels, rentals) or checkout. *(source: contracts/spine/orders.yaml#addCartLine)*

**Data it reads**: `getVenueMap` (onLoad, The map with its placed spots (label, kind, zone, capacity …); `getMapResourceAvailability` (onLoad, Every spot's status for the day in one call); `getResourceHold` (onInterval, The hold's countdown With the guest session the device …); `listBookableVenueMaps` (onLoad, Find the venue's published map with bookable spots (with …)

**Where the user goes next**

- → `WEB-010` Shopping Cart: *Go to checkout*; carries `cartId`; only when a spot is held and added; calls `addCartLine`
- → `WEB-008` Add-ons & Upsell: *Continue to add-ons (rentals, towels)*; carries `cartId`
- → `WEB-004` Attraction Details: *Back to the product*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue map and the status of every spot for the day, read together. |
| Error (`?state=error`) | Could not load the map or the spots. Names which read failed; nothing is held. |
| Empty, first run (`?state=emptyFirstRun`) | **No bookable spots are placed on this map yet.** Says so and offers the venue's other ways to book, rather than an empty map. |
| Empty, no results (`?state=emptyNoResults`) | Every spot in this area is taken for the day. Names the area and offers another area or day. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** The map and the spots already loaded stay on screen with their age, never shown as free now. Holding a spot and adding it to the basket need the connection — a cabana held offline is a cabana two people think they have. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already expired or converted, or the extension limit is reached. `refusedReason` says which. (ResourceHoldExtendProblem); 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 409 Taken for some of the window, held by someone else, not placed on the published map, or marked not bookable. (ResourceConflictProblem); 422 The booked window is … |

#### Edge cases to draw

- **Spot taken between seeing and tapping**: "B09 was just taken - pick another" and the map refreshes; no silent failure. *(source: contracts/satellite/resources.yaml#createResourceHold)*
- **Offline**: Loaded map stays with its age and nothing shows as free now; holding needs the connection. *(source: screens/P01-guest-web-storefront.yaml#WEB-047)*
- **Venue does not use map booking**: The screen is not offered; the product books without a map (configurable per operator). *(source: DI-1008)*

#### Consistency with other screens

- Match `GST-074`: Same map, numbering, colours and countdown on the app.
- Match `BO-096`: A booked spot appears on the resource calendar with setup, teardown and cleaning bands.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
map: Coastal Aqua beach map
spots:
- spot: B09
  kind: Large cabana
  zone: Beach
  seats: 6
  price: AED 1,855
  status: Free
- spot: T03
  kind: Tower cabana
  zone: Tower
  seats: 4
  price: AED 1,250
  status: Booked
- spot: R07
  kind: Lounger pair
  zone: Riverside
  seats: 2
  price: AED 220
  status: Held
hold:
  spot: B09
  remaining: 09:42
```

#### Permissions

- `getVenueMap` → `VENUE_MAP_VIEW` (read) · staff, guest
- `getMapResourceAvailability` → `RESOURCE_VIEW` (read) · staff, guest
- `createResourceHold` → `ORDER_CREATE` (operate) · staff, guest
- `getResourceHold` → `ORDER_VIEW` (read) · staff, guest
- `extendResourceHold` → `ORDER_CREATE` (operate) · staff, guest
- `relinquishResourceHold` → `ORDER_CREATE` (operate) · staff, guest
- `addCartLine` → no permission · guest, partner, staff
- `listBookableVenueMaps` → `VENUE_MAP_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.55 | Interactive Venue Map - System shall provide interactive venue maps. | Guest Mobile App & Branding | CONTRACTED | `getVenueMap` |
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The table/cabana screen becomes map-based booking: a venue map can carry cabanas, loungers, tables (beach or event tables) and other bookable resources, sold like cabanas. Dining tables stay F&B table reservations. *(agreed · design review 29 Sep 2026, GAP-C2 · C. Wave 2: Reserve a Table or Cabana (waitlist, notify) · DI-1076)*
- Cabanas are picked on the venue's ingested map, like stadium seats: numbered cabanas by zone (e.g. R01–R10, T01–T08, S01–S06, B01–B10) showing guests seated, sold-out greyed and marked. Tapping one adds it (e.g. "Cabana B09 · Large cabana · Beach, AED 1,855") and starts a remaining-time counter. Map on the first screen. *(agreed · rev 3 design review 29 Sep 2026, REV3-15 · 15. Book the product from the map (e.g. pick an available cabana) · DI-1055)*
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)*
- **Open question.** Cabanas: category (premium, VIP, luxury, private, family, couples), date/time, guest count, amenity details. Activities: desert-safari packages (buy-one-get-one, evening, Bedouin-style), pickup point, add-ons (stroller), duration packages (2-hour/4-hour). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Cabanas, Activities) · DI-687)*

Also apply: 7 for P01 · Booking & Selection, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-047` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Coastal Aqua → 'Cabana & locker rentals' → cabana map ('Remaining time' counter)*
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add to basket, Keep it longer, Pick another.
- [ ] Every transition is wired: `WEB-010`, `WEB-008`, `WEB-004`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-048` Book a Space by the Hour

**Book a meeting room or other space for a start time and a length; the price is the room rate for that length.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Booking & Selection · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20706 (APP-WEB-WEB-048) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | multiStepForm (compact density): A staged booking — date, start time, length, room type, attendees, add-ons — ending in one `addCartLine`; the prototype draws it as one step revealing each choice in turn |
| Offline | **The offline banner shows.** Rooms and times already loaded stay on screen with their age. Picking a start time and adding the booking need the connection — a room held offline is a room two people think they have. |
| Opens with | `productId` (WEB-004), `cartId` (session) · cold entry: Resolves the venue from the site and lists its room types; nothing is booked on arrival. |
| Route | `/booking-and-selection/space-by-the-hour` |

**What the spec says about it.** **New 29 September** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). A staged booking: date → start time → length (1 hour, 2 hours, half day, full day) → room type (focus pod, majlis, boardroom, auditorium) → attendees → add-ons (coffee break, working lunch, AV technician). **A room type is a product with `requiresTimeWindow`; a length is one of its variants** (the `length` axis, each value with `durationMinutes`), priced on its own, so the price is the variant's — the room rate for that length. The guest never names a room: `addCartLine` carries `bookedWindow` {startsAt, endsAt}, `endsAt` being the start plus the length, and `allocateResources` picks the room at checkout (26 August minute). Add-ons are lines with `parentLineId`. `422 windowLengthMismatch`, `windowRequired` and `windowNotAllowed` are programming errors; `409 windowUnavailable` says the time filled and offers the next free start. **29 September (W9).** Availability is checked against date, start time and length together (`listProductStartTimes` with `variantId` = length); changing any of the three re-checks every room, and a busy room shows *free from*. Starts every 15 minutes where the venue sets `stepMinutes` 15.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Book a meeting room or other space by the hour (House of Pages). Block A. A staged booking: date, start time, length, room type, attendees, add-ons. The guest picks a room type, never a specific room; availability is checked on date, start and length together.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No wireframe frame yet (status notStarted), though the prototype covers it. (CHG-SGU-026)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Select a date | date picker | — | — | — | — | — | — |
| Start time | select field | — | — | — | — | The start times at which a room of the chosen type is free for the chosen length (`listProductStartTimes` with `productId`, `variantId` = the length, `date`; hourly, 08:00-20:00 in the prototype) … | — |
| How long | select field | — | — | — | — | 1 hour, 2 hours, half day (4 h), full day (8 h): the room type's `length` variants, each priced on its own (the prototype shows *Save 10%* and *Save 15%*). | — |
| Attendees | number field | — | — | — | — | For the visitor list at reception; a room type smaller than the party is not offered. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Sent by *Add to basket*** (`addCartLine`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **start time**: Starts every 15 minutes where the venue sets it, between the venue's hours; each shows how many rooms of the type are left. Changing date, start or length re-checks every room; a busy room type says "free from 11:15". *(source: MoM 29 Sep W9; DI-1011; screens/P01-guest-web-storefront.yaml#WEB-048 notes)*
- **how long**: 1 hour, 2 hours, half day (4 h), full day (8 h), each priced on its own with the saving shown (Save 10%, Save 15%). *(source: REV3-13; screens/P01-guest-web-storefront.yaml#WEB-048 (selectField How long))*
- **attendees**: A number; room types smaller than the party are not offered. *(source: screens/P01-guest-web-storefront.yaml#WEB-048 (numberField Attendees))*

#### Outputs: what the screen shows and produces

**Shown**

**Choose a room** (card list, from `listProducts`): Room types (focus pod, majlis room, boardroom, auditorium) with capacity, description, badge and the price for the chosen length.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Family key | text | The same product at another location (decided 29 September, rev 3 REV3-18). Optional. |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Code schema | text | 7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. `Product.code` existed and nothing required a format, so a venue with three thousand … |

**Add to the booking** (card list, from `listProducts`): Coffee break, working lunch, AV technician: add-on lines with `parentLineId`.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Family key | text | The same product at another location (decided 29 September, rev 3 REV3-18). Optional. |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Code schema | text | 7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. `Product.code` existed and nothing required a format, so a venue with three thousand … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add to basket (primary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **cleaning buffer**: Not shown as a separate slot; it shapes availability. Fixed buffer after each booking (e.g. 15 minutes) or N cleanings a day placed by the system. *(source: MoM 29 Sep W10; DI-1012)*
- **basket line**: "Boardroom · Tue 6 Oct 10:00-12:00 · 2 hours · AED 600" with add-ons under it. *(source: DI-1053)*

**Data it reads**: `listProducts` (onLoad, Room types sold by the hour (`requiresTimeWindow`) and …); `listProductVariants` (onLoad, The lengths of a room type, each with its price)

**Where the user goes next**

- → `WEB-010` Shopping Cart: *Add to basket, then review the cart*; carries `cartId`; only when date, start time, length and room type chosen; calls `addCartLine`
- → `WEB-004` Attraction Details: *Back to the product*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The room types and their lengths for this venue. |
| Error (`?state=error`) | Could not load. Names which read failed; nothing is booked. |
| Empty, first run (`?state=emptyFirstRun`) | **This venue sells no space by the hour yet.** Says so rather than an empty list. |
| Empty, no results (`?state=emptyNoResults`) | No room of the type is free at that time for that length. Offers the next free start time. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Rooms and times already loaded stay on screen with their age. Picking a start time and adding the booking need the connection — a room held offline is a room two people think they have. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed` … |

#### Edge cases to draw

- **The time fills while the guest is choosing**: "10:00 has just been taken" with the next free start offered. *(source: screens/P01-guest-web-storefront.yaml#WEB-048 notes (409 windowUnavailable))*

#### Consistency with other screens

- Match `GST-075`: Same staged order and the same "free from" wording on the app.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: House of Pages (library and rooms), Sharjah
roomTypes:
- Focus pod · 1-2 people
- Majlis room · up to 8
- Boardroom · up to 12
- Auditorium · up to 80
lengths:
- 1 hour AED 300
- 2 hours AED 540 (Save 10%)
- Half day AED 1,020 (Save 15%)
- Full day
addOns:
- Coffee break AED 35 pp
- Working lunch AED 85 pp
- AV technician AED 250
```

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductStartTimes` → `RESOURCE_VIEW` (read) · staff, guest
- `addCartLine` → no permission · guest, partner, staff

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Meeting rooms by the hour are in scope: date → start time → length (1 hour, 2 hours, half day, full day) → room (focus pod, majlis room, boardroom, auditorium) → attendees → add-ons (coffee break, working lunch, AV technician). Price = room rate × length; the cart line shows the booked time window. *(agreed · rev 3 design review 29 Sep 2026, REV3-13 · 13. House of Wisdom: meeting room flow · DI-1053)*
- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)*
- Meeting-room availability is checked against date + start time + duration together; changing any of the three re-checks all rooms. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W9 Meeting rooms · DI-1011)*
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- UX reference: House of Wisdom (Sharjah library) meeting-room/"pod" booking and tiered membership plans — a simple duration-based booking flow without fixed performances/time slots — to be reviewed by Chinmay/Aishwarya. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 6. Open Items · DI-506)*
- A bookable resource such as a meeting room can be priced per hour: total price is calculated from the booked duration and the room is blocked for that window so no other guest can book it. *(client request · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A · DI-503)*
- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*

Also apply: 7 for P01 · Booking & Selection, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-048` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *House of Pages → 'Meeting room by the hour'*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add to basket.
- [ ] Every transition is wired: `WEB-010`, `WEB-004`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 7 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
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
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
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

### In P01 · Booking & Selection

- The prototype validated five booking-flow types (dated, multi-park, combo, annual pass, membership) and their skeleton screens; these flows are the basis for the real white-label builder. *(agreed · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-989)*
- Each ticket type gets its own flow: open-dated (no calendar step, straight to guest category/quantity, valid e.g. 30-60 days), dated (date, then product), dated-with-time (date, time, product) and seated (date, time, seat selection). *(client request · MoM 18 Sep 2026, 4.13 Guest Website UX Review — Ticket Type Flows & Seat Map Selection · DI-948)*
- **Open question.** Movies: language/screen type (e.g. English, Dolby Atmos), cinema and showtime, seats, concession add-ons. Theme park: ticket-type list, guest categories (adult/child/senior/infant/people of determination with companion), per-ticket guest-name capture driven by quantity. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Movies, Theme park) · DI-686)*
- Decision: the B2C checkout shows a clear, visible step indicator — Ticket Selection → Add-ons → My Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-426)*
- Reference checkouts: Six Flags-style (product → quantity/name capture → cart summary → login/guest checkout with dual OTP validation) and Platinum List (event → date → colour-coded interactive seat map → seats → one-page checkout via Quick Order/Apple/Google, as few as four clicks, optional post-purchase profile prompt). *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-398)*
- **Open question.** Two selection patterns: (a) event, date, time, see availability, then product; (b) product, quantity, date, then only time slots with enough capacity. How many customization scenarios to support needs deeper UI exploration. *(open · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-118)*
- Navigation depends on ticket type: admission has no date/time and goes straight to quantity/cart; dated asks date only; timed asks date then time; seated asks date, then time, then seat. *(agreed · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-116)*

**114 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"addToWishlist": {"method":"POST","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Save an item","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wishlist"},
"checkBookingEligibility": {"method":"POST","path":"/eligibility-checks","contract":"catalogue","summary":"Can this party take part","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EligibilityCheckRequest","responds":"EligibilityCheckResult"},
"createResourceHold": {"method":"POST","path":"/resource-holds","contract":"resources","summary":"Hold a specific resource picked on the map","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateResourceHoldRequest","responds":"ResourceHold"},
"createSeatHold": {"method":"POST","path":"/seat-holds","contract":"seating","summary":"Hold specific seats","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateSeatHoldRequest","responds":"SeatHold"},
"decideRecommendations": {"method":"POST","path":"/recommendations/decide","contract":"ai","summary":"Fill a recommendation slot","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRecommendationResult"},
"evaluatePromotions": {"method":"POST","path":"/promotions/evaluate","contract":"promotions","summary":"Evaluate promotions against a cart","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EvaluatePromotionsRequest","responds":"PromotionEvaluation"},
"extendResourceHold": {"method":"POST","path":"/resource-holds/{holdId}/extend","contract":"resources","summary":"Extend a resource hold","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceHold"},
"getAvailability": {"method":"GET","path":"/availability","contract":"catalogue","summary":"Live remaining capacity","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":"channelCapacityId","in":"query","required":null},{"name":"eventId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceAvailabilityPage"},
"getBundle": {"method":"GET","path":"/bundles/{bundleId}","contract":"promotions","summary":"Read a bundle with components and allocation","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Bundle"},
"getCart": {"method":"GET","path":"/carts/{cartId}","contract":"orders","summary":"The cart, priced and checked, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getMapResourceAvailability": {"method":"GET","path":"/resource-availability","contract":"resources","summary":"Every bookable resource on a venue map, free or taken, in one call","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mapId","in":"query","required":true},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"MapResourceAvailability"},
"getPerformance": {"method":"GET","path":"/performances/{performanceId}","contract":"catalogue","summary":"Read a performance","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Performance"},
"getPublishedBookingFlow": {"method":"GET","path":"/venues/{venueId}/booking-flow","contract":"white-label","summary":"The published booking flow a product or category books through","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":false},{"name":"productCategoryId","in":"query","required":false},{"name":"flowTypeKey","in":"query","required":false}],"requestBody":null,"responds":"BookingFlow"},
"getPublishedGuidedChoice": {"method":"GET","path":"/venues/{venueId}/guided-choice","contract":"white-label","summary":"The venue's published Help me choose","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuidedChoice"},
"getResourceHold": {"method":"GET","path":"/resource-holds/{holdId}","contract":"resources","summary":"Read a resource hold","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceHold"},
"getSeatAvailability": {"method":"GET","path":"/performances/{performanceId}/seat-availability","contract":"seating","summary":"Seat status for a performance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"availableOnly","in":"query","required":null},{"name":"mode","in":"query","required":null}],"requestBody":null,"responds":"SeatAvailability"},
"getVenueMap": {"method":"GET","path":"/venue-maps/{mapId}","contract":"venue-map","summary":"A map with its points and paths","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null},{"name":"draft","in":"query","required":null}],"requestBody":null,"responds":"VenueMapDetail"},
"getWishlist": {"method":"GET","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Read a guest's saved items","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[],"requestBody":null,"responds":"Wishlist"},
"listBookableVenueMaps": {"method":"GET","path":"/bookable-venue-maps","contract":"venue-map","summary":"The published maps of a venue that carry bookable spots","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"productId","in":"query","required":false},{"name":"kind","in":"query","required":false}],"requestBody":null,"responds":"BookableVenueMaps"},
"listPerformances": {"method":"GET","path":"/events/{eventId}/performances","contract":"catalogue","summary":"List performances of an event","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"language","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductCategories": {"method":"GET","path":"/product-categories","contract":"catalogue","summary":"The merchandise hierarchy — categories, brands, collections","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductCategoryNode"},
"listProductStartTimes": {"method":"GET","path":"/resource-start-times","contract":"resources","summary":"Start times a space sold by the hour can be booked at, for one length on one day","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":true},{"name":"variantId","in":"query","required":true},{"name":"date","in":"query","required":true},{"name":"stepMinutes","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVariants": {"method":"GET","path":"/products/{productId}/variants","contract":"catalogue","summary":"List generated variants","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recommendSeats": {"method":"POST","path":"/performances/{performanceId}/seat-recommendations","contract":"seating","summary":"Recommend seats for a party","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRequest","responds":null},
"recordConsentAnswers": {"method":"POST","path":"/consent-answers","contract":"marketing-crm","summary":"Answer the consent questions a booking asks","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordConsentAnswersRequest","responds":null},
"recordRecommendationEvents": {"method":"POST","path":"/recommendations/events","contract":"ai","summary":"Report what happened to recommended items","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"relinquishResourceHold": {"method":"DELETE","path":"/resource-holds/{holdId}","contract":"resources","summary":"Give up a resource hold","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"relinquishSeatHold": {"method":"DELETE","path":"/seat-holds/{holdId}","contract":"seating","summary":"Release a hold","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"removeFromWishlist": {"method":"DELETE","path":"/guests/{subjectId}/wishlist/{itemId}","contract":"marketing-crm","summary":"Remove a saved item","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"AiRecommendationItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList","description":"One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).","required":["trackingId","rank"],"properties":{"trackingId":{"type":"string","format":"uuid","description":"Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."},"productId":{"type":"string","format":"uuid","nullable":true,"description":"The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."},"couponRef":{"type":"string","nullable":true,"description":"For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."},"rewardId":{"type":"string","format":"uuid","nullable":true,"description":"For `reward`, a marketing-crm loyalty reward the guest can redeem."},"challengeId":{"type":"string","format":"uuid","nullable":true,"description":"For `challenge`, a marketing-crm challenge the guest can join."},"kind":{"type":"string","enum":["upsell","crossSell","upgrade","bundle","addOn","membership","nextBestOffer","offer","reward","challenge"]},"rank":{"type":"integer","minimum":1},"priceRef":{"type":"string","nullable":true,"description":"The Pricing reference the channel resolves to a price. AI never computes a price."},"reasonTemplateKey":{"type":"string","nullable":true,"description":"The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."},"reasonText":{"type":"string","nullable":true,"description":"The rendered template in the session locale, where the channel shows reasons."},"confidenceBand":{"type":"string","enum":["high","medium","low"],"description":"Design 5.6: a band, never a bare percentage."},"score":{"type":"number","nullable":true,"description":"Normalised score. **Returned to staff callers only**; a guest response omits it."}}},
"AiRecommendationResult": {"type":"object","x-ticvai-persistence":"none — written as ai.rec_decision after the response","description":"The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.","required":["decisionId","mode","items","expiresAt"],"properties":{"decisionId":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["productPage","cart","checkout","postPurchase","preVisit","inVenue","posBasket","kioskBasket","fnbMenu","retailBasket","seatUpgrade","membership","email","homepage","loyalty"]},"mode":{"type":"string","enum":["personalised","contextual","rulesOnly","fallback"]},"items":{"type":"array","items":{"$ref":"#/components/schemas/AiRecommendationItem"}},"expiresAt":{"type":"string","format":"date-time"}}},
"BookableVenueMapRef": {"type":"object","description":"One published map with bookable spots on it: enough to pick it and call `getVenueMap` (with `publishedVersion`) and `resources.getMapResourceAvailability`.\n","required":["mapId","name","kind","publishedVersion","placedResourceCount"],"properties":{"mapId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"publishedVersion":{"type":"integer","description":"The `VenueMap.publishedVersion` a guest is served; send it to `getVenueMap` as `version`."},"placedResourceCount":{"type":"integer","minimum":1,"description":"Placed resources on the published version."},"kinds":{"type":"array","description":"The kinds of spot on this map, e.g. `[cabana, lounger]`, for the picker's chips.","items":{"type":"string","enum":["cabana","lounger","table","pitch","other"]}}}},
"BookableVenueMaps": {"type":"object","description":"What `listBookableVenueMaps` returns: the published maps of one venue that carry bookable spots (decided 29 September, readiness close-out). **Bounded by the venue**: a venue has a handful of maps, so the list is capped at 50 rather than paged.\n","required":["venueId","maps"],"properties":{"venueId":{"type":"string","format":"uuid"},"maps":{"type":"array","maxItems":50,"items":{"$ref":"#/components/schemas/BookableVenueMapRef"}}}},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"BookingConsentRecord": {"type":"object","x-ticvai-persistence":"marketing.booking_consent_record","description":"**One answer to one consent question, as given** (decided 29 September, rev 3 REV3-26). Append-only: a changed answer is a new record and this one gets `supersededAt`. Distinct from `ConsentRecord`, which is a guest's standing decision about a data-processing purpose; this is an answer given for a booking.\n","required":["id","questionId","questionVersion","questionKind","answer","scope","source","answeredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"questionId":{"type":"string","format":"uuid"},"questionVersion":{"type":"integer","minimum":1},"questionKind":{"$ref":"#/components/schemas/ConsentQuestionKind"},"answer":{"type":"string","enum":["yes","no"]},"scope":{"type":"string","enum":["perPerson","perBooking"]},"blocksBooking":{"type":"boolean","readOnly":true,"description":"The answer is the question's `blockingAnswer` at that version."},"cartId":{"type":"string","format":"uuid","nullable":true},"cartLineId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Set by `orders.checkoutCart` when the cart becomes an order."},"orderLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"personIndex":{"type":"integer","minimum":0,"nullable":true},"personName":{"type":"string","maxLength":120,"nullable":true},"personSubjectId":{"type":"string","format":"uuid","nullable":true},"answeredBySubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest who answered, from the session. Null for an anonymous cart."},"answeredByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The staff member who answered on the guest's behalf."},"source":{"$ref":"#/components/schemas/ConsentSource"},"answeredAt":{"type":"string","format":"date-time"},"supersededAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"Bundle": {"x-ticvai-persistence":"promotions.bundle + promotions.bundle_component","allOf":[{"$ref":"#/components/schemas/CreateBundleRequest"},{"type":"object","required":["id","savingsAmount","isActive","hasBeenSold"],"properties":{"id":{"type":"string","format":"uuid"},"savingsAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum of component list prices less the bundle price."},"savingsPercentage":{"type":"number"},"hasBeenSold":{"type":"boolean","description":"True locks components and allocation against amendment."},"isActive":{"type":"boolean"}}}]},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConsentQuestionKind": {"type":"string","description":"What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue set them.","enum":["swim","scuba","risk","custom"]},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"CreateBundleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","kind","price","components","allocation"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/BundleKind"},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"components":{"type":"array","minItems":0,"items":{"$ref":"#/components/schemas/BundleComponent"}},"choiceGroups":{"type":"array","description":"Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups the guest chooses from. **The bundle price does not move with the choice** (ADR-0019).\n","items":{"$ref":"#/components/schemas/BundleChoiceGroup"}},"allocation":{"type":"object","required":["method","components"],"properties":{"method":{"allOf":[{"$ref":"#/components/schemas/AllocationMethod"}],"default":"proRataListPrice","description":"Proportional to list price by default. The rounding remainder in the currency's minor unit goes to the first component (decided 28 September, audit R101).\n"},"components":{"type":"array","items":{"$ref":"#/components/schemas/AllocationComponent"}}}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) the bundle is sold under. (DM5, 29 September: data model for the agreed operations)"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The bundle owner (Bundle Definition & Setup). (DM5, 29 September: data model for the agreed operations)"},"category":{"type":"string","maxLength":100,"nullable":true,"description":"The bundle category the setup screen files it under. (DM5, 29 September: data model for the agreed operations)"},"isStandaloneProduct":{"type":"boolean","default":true,"description":"Whether the bundle appears as a product in its own right, or only as an offer on another product. (DM5, 29 September: data model for the agreed operations)"},"isRecommendedAtCheckout":{"type":"boolean","default":false,"description":"Whether checkout recommends the bundle. (DM5, 29 September: data model for the agreed operations)"},"requiredVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"Products that must already be in the basket for the bundle to be sold (the setup screen's \"requires another product\"). (DM5, 29 September: data model for the agreed operations)"}}},
"CreateResourceHoldRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","mapId","resourceIds","from","to"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7, as a seat hold's."},"mapId":{"type":"string","format":"uuid","description":"The published venue map the guest picked from."},"resourceIds":{"type":"array","minItems":1,"maxItems":10,"description":"Placed resources on that map, e.g. two adjoining loungers. All or none are held.","items":{"type":"string","format":"uuid"}},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"partySize":{"type":"integer","minimum":1,"nullable":true,"description":"Checked against each resource's `capacity`; above it the hold is refused `422`."},"ttlSeconds":{"type":"integer","minimum":60,"maximum":1800,"default":480,"description":"8 minutes by default, 30 in all with extensions (audit R169), as a seat hold."},"subjectId":{"type":"string","format":"uuid","nullable":true}}},
"CreateSeatHoldRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","performanceId","seatIds"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","minItems":1,"maxItems":50,"description":"50 is the ceiling of the venue setting, not the limit a caller gets. On a guest channel the limit is `VenueSettings.seating.maxSeatsPerGuestOrder` (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); on a staff channel it stays 10 per sale (audit R080 (c)), as POS-002 shows. Either is refused with `422` `seat-limit-exceeded`.\n","items":{"type":"string"}},"ttlSeconds":{"type":"integer","minimum":60,"maximum":1800,"default":480,"description":"**8 minutes by default, extendable to 30 in all** (decided 28 September, audit R169). Left out, the hold lasts 480 seconds. No hold, first grant or extended, outlives 1800 seconds from its creation.\n"},"subjectId":{"type":"string","format":"uuid"}}},
"EligibilityCheckRequest": {"type":"object","description":"Request only.","required":["productIds","party"],"properties":{"productIds":{"type":"array","minItems":1,"items":{"type":"string"}},"party":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/EligibilityDeclaration"}}}},
"EligibilityCheckResult": {"type":"object","x-ticvai-persistence":"none — computed per request","required":["eligible"],"properties":{"eligible":{"type":"boolean"},"guests":{"type":"array","items":{"type":"object","properties":{"index":{"type":"integer"},"eligible":{"type":"boolean"},"reasons":{"type":"array","items":{"type":"string","enum":["tooYoung","tooOld","tooShort","tooTall","needsAdult","needsGuardianSignature","needsSwimmer"]}}}}},"waiverRequired":{"type":"boolean"}}},
"EligibilityDeclaration": {"type":"object","description":"What a guest declares about one member of the party. Declared, not measured.","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true,"description":"Which band of the rule's `heightBandsCm`, counting from 0."},"confidentSwimmer":{"type":"boolean","nullable":true,"deprecated":true,"description":"Superseded by the consent record for the product's swim consent question (decided 29 September, rev 3 REV3-26); see `ProductEligibilityRule.swimAbility`."},"guardianSigned":{"type":"boolean","default":false}}},
"EvaluatePromotionsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","channel","lines"],"properties":{"venueId":{"type":"string","format":"uuid"},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"description":"Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"},"subjectId":{"type":"string","format":"uuid"},"membershipTierId":{"type":"string","format":"uuid"},"couponCodes":{"type":"array","items":{"type":"string"}},"evaluateAt":{"type":"string","format":"date-time","description":"For back-office testing of a rule before publishing."},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one `promotions.promotion_evaluation_trace` row for it. (decided 29 September, writers pass)"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["lineId","variantId","quantity","unitPrice"],"properties":{"lineId":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuidedChoice": {"x-ticvai-persistence":"whitelabel.guided_choice + whitelabel.guided_choice_question + whitelabel.guided_choice_answer","type":"object","description":"**Help me choose (decided 29 September, rev 3 REV3-11).** A venue's short set of questions that ends on a result card opening the booking flow, product, category or event that fits. Each question has a few answers with a title, a one-line body, an icon and an optional badge; **the answer the guest picks on the last question decides the result**, and each earlier answer carries a target too, so a one-question setting still ends on a result. Venue configuration, never hard-coded: set up in Venue Management, off unless the venue publishes one.\n**Two sources, one review.** `manual` is written by staff; `aiSuggested` is proposed by the `ai` service from the venue's uploaded products (a suggestion, reviewed and published by a person, never auto-published). Both arrive as `draft`.\n**Help me choose filters the catalogue (decided 29 September, W4).** With `behaviour` `filter`, the default, each answer's `filter` narrows the products the guest sees (web, mobile and kiosk alike, through catalogue `listProducts` and `searchCatalogue` `guidedAnswerIds`), with a \"Show everything\" link; `recommend` keeps the rev 3 result card from the last answer's `target`. **It is never a consent step**: an answer may pre-fill a REV3-26 consent question (`consentPrefill`), which the guest still confirms, so the question is not asked twice and the consent stays explicit.\n","required":["id","venueId","name","mode","questions","status","source"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createGuidedChoice`."},"name":{"type":"string","maxLength":80,"description":"Staff-facing name, e.g. \"Water park day planner\". Not shown to guests."},"mode":{"type":"string","enum":["button","popupOnArrival","off"],"default":"button","description":"**How the guest reaches it (rev 3 REV3-11).** `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on the device only); `off` keeps a published choice configured but not shown.\n"},"showBanner":{"type":"boolean","default":true,"description":"The dark banner under the products (\"Choose from the experiences above or let us help you decide\") with a Help me choose button. Ignored when `mode` is `off`."},"behaviour":{"type":"string","enum":["filter","recommend"],"default":"filter","description":"**`filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4).** With `filter`, every answer needs a `filter` and `target` is optional; with `recommend`, every answer on the last question needs a `target`. `publishGuidedChoice` refuses the other case with 422.\n"},"showEverything":{"type":"boolean","default":true,"description":"The \"Show everything\" link under a filtered list, which clears the answers (W4)."},"questions":{"type":"array","minItems":1,"maxItems":4,"description":"**One to four questions** (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). Shown in `sortOrder`.\n","items":{"type":"object","required":["title","sortOrder","answers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"kind":{"type":"string","enum":["choice","yesNo","age","level","certification"],"default":"choice","description":"**What the question asks (decided 29 September, W4).** `choice` free answers; `yesNo` two answers (e.g. \"Can everyone swim?\"); `age` answers carrying an age range; `level` answers carrying a level tag; `certification` answers saying whether the guest holds a certificate (e.g. a diving licence). The kind decides which `filter` fields its answers use.\n"},"sortOrder":{"type":"integer","minimum":0},"answers":{"type":"array","minItems":2,"maxItems":4,"description":"Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11).","items":{"type":"object","required":["title","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The one-liner under the title, at most 140 characters in each language."},"icon":{"type":"string","maxLength":40,"nullable":true,"description":"An icon name from the guest app's icon set."},"badge":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Optional, e.g. \"Best value\". At most 24 characters in each language."},"sortOrder":{"type":"integer","minimum":0},"target":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceTarget"}],"nullable":true,"description":"Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list."},"filter":{"type":"object","nullable":true,"description":"**What this answer keeps in the list (decided 29 September, W4).** Every field set must hold; answers to different questions are combined with AND. Required with `behaviour` `filter`. The server applies it (catalogue `guidedAnswerIds`), so web, mobile and kiosk show the same list.\n","properties":{"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"segmentTags":{"type":"array","description":"Catalogue `Product.segmentTags`, e.g. a level tag.","items":{"type":"string"}},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true,"description":"With `minAgeYears`, checked against each product's age rule (catalogue `ProductEligibilityRule`)."},"requiresSwimmer":{"type":"boolean","nullable":true,"description":"False hides products whose eligibility needs a swimmer; true keeps only those."},"certificationCode":{"type":"string","nullable":true,"maxLength":40,"description":"Keeps products that need this certificate, or with `holdsCertification` false, hides them."},"holdsCertification":{"type":"boolean","nullable":true}}},"consentPrefill":{"type":"object","nullable":true,"description":"**Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4).** The guest still ticks it at the consent step; nothing is recorded as consent until they do.\n","required":["consentQuestionId","answer"],"properties":{"consentQuestionId":{"type":"string","format":"uuid"},"answer":{"type":"boolean"}}},"result":{"type":"object","nullable":true,"description":"The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image.","properties":{"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"imageAssetRef":{"type":"string","format":"uuid","nullable":true}}}}}}}}},"status":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceStatus"}],"readOnly":true},"source":{"type":"string","enum":["manual","aiSuggested"],"readOnly":true,"description":"`manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). Kept after a person edits a suggestion, so a report can say how many AI proposals were published."},"suggestionRef":{"type":"string","nullable":true,"readOnly":true,"description":"For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"publishedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The person who published it. Never a service."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuidedChoiceStatus": {"type":"string","description":"**Draft until a person publishes it (decided 29 September, rev 3 REV3-11).** Guests see only a `published` choice. An AI-proposed choice arrives as `draft` and is never published by the system. Moves as `states/guided-choice.yaml` says: `publishGuidedChoice` and `unpublishGuidedChoice`, and a publish returns the venue's previously published choice to `draft`.\n","enum":["draft","published"],"default":"draft"},
"GuidedChoiceTarget": {"x-ticvai-persistence":"none — embedded","type":"object","description":"**What an answer opens (decided 29 September, rev 3 REV3-11).** A product (its kind picks the booking flow), a product category (its tickets, as `ticketCategories` shows them), an event, or a module such as `membership`. Each id must belong to the choice's venue and be on sale or enabled when the choice is published, or `publishGuidedChoice` refuses it.\n","required":["kind"],"properties":{"kind":{"type":"string","enum":["product","productCategory","event","module","bookingFlow"]},"productId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `product`. A catalogue `Product`."},"productCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `productCategory`. A catalogue `ProductCategory`."},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `event`."},"moduleKey":{"allOf":[{"$ref":"#/components/schemas/ModuleKey"}],"nullable":true,"description":"Required when `kind` is `module`. The module must be enabled."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `bookingFlow` (decided 29 September, W12; BUILD-YOUR-EXPERIENCE \"each answer points to one booking flow\"). One of the venue's enabled `BookingFlow`s."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MapResourceAvailability": {"x-ticvai-persistence":"none — computed from placed resources, bookings, holds and blocks","type":"object","description":"What `getMapResourceAvailability` returns: **every placed resource on one map, for one window, in one answer** (rev 3 REV3-15).\n","required":["mapId","mapVersion","from","to","resources"],"properties":{"mapId":{"type":"string","format":"uuid"},"mapVersion":{"type":"integer","description":"The published `venue-map` version the placements were read from; the client checks it against the map it cached."},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"booked":{"type":"integer"},"unavailable":{"type":"integer"}}},"resources":{"type":"array","items":{"type":"object","required":["resourceId","label","status"],"properties":{"resourceId":{"type":"string","format":"uuid"},"placedResourceId":{"type":"string","format":"uuid","description":"The `venue-map.PlacedResource` it was read from."},"label":{"type":"string","description":"As on the map, e.g. `B09`."},"kind":{"$ref":"#/components/schemas/ResourceKind"},"zone":{"type":"string"},"capacity":{"type":"integer"},"priceBandCode":{"type":"string"},"variantId":{"type":"string","format":"uuid","description":"What the cart line names to buy it."},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","held","booked","unavailable"],"description":"`unavailable` covers maintenance, a blackout, a block and a placement marked not bookable; the map greys all of them the same way.\n"}}}}}},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"PerformanceAvailability": {"type":"object","x-ticvai-persistence":"none — computed on read from catalogue.channel_capacity and live leases","description":"Remaining capacity of one channel capacity of one performance (rev 3 REV3-1).","required":["channelCapacityId","performanceId","capacity","sold","leased","remaining"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid","description":"The performance this channel capacity belongs to (`ChannelCapacity.performanceId`), so rows for several performances can be told apart."},"startsAt":{"type":"string","format":"date-time","readOnly":true,"description":"The performance's start, so a time tile and its day part (morning, afternoon, evening, split at the venue's `BookingFlowConfig.dayPartBoundaries`) come from this one call (rev 3 REV3-1)."},"capacity":{"type":"integer"},"sold":{"type":"integer"},"leased":{"type":"integer","description":"Held by terminals but not yet sold."},"remaining":{"type":"integer"},"byChannel":{"type":"array","description":"Per-channel position. A guest seeing sold out online while units remain at the counter is correct behaviour, not a defect.\n","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"allocated":{"type":"integer"},"sold":{"type":"integer"},"remaining":{"type":"integer"}}}}}},
"PerformanceAvailabilityPage": {"x-ticvai-persistence":"none — computed on read","description":"The `getAvailability` answer (named 29 September, rev 3 REV3-1).","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Page"},{"type":"object","properties":{"items":{"type":"array","items":{"$ref":"#/components/schemas/PerformanceAvailability"}}}}]},
"PlacedResource": {"type":"object","x-ticvai-persistence":"venuemap.placed_resource","description":"**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n","required":["id","mapId","resourceId","label","kind","zone","capacity","priceBandCode","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes it."},"resourceId":{"type":"string","format":"uuid","x-ticvai-references":"resources.Resource","description":"The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"},"label":{"type":"string","maxLength":40,"x-ticvai-unique":"map","description":"What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"},"kind":{"type":"string","enum":["cabana","lounger","table","pitch","other"],"description":"A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."},"zone":{"type":"string","maxLength":80,"description":"The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."},"capacity":{"type":"integer","minimum":1,"maximum":500,"description":"Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."},"priceBandCode":{"type":"string","maxLength":40,"description":"The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"},"variantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"catalogue.ProductVariant","description":"Resolved from the price band. What a cart line for this resource names."},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates of its label anchor, as on `VenuePoint`.","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"boundary":{"type":"array","nullable":true,"description":"The shape drawn, as a polygon in drawing coordinates. Null for a pin.","items":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}}},"isBookable":{"type":"boolean","default":true,"description":"False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductCategory": {"type":"object","x-ticvai-persistence":"catalogue.product_category","description":"Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n","required":["id","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"code":{"type":"string","maxLength":64,"nullable":true,"x-ticvai-unique":"tenant","description":"**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"kind":{"type":"string","enum":["category","brand","collection","season","department"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"},"scopePath":{"type":"string","readOnly":true,"description":"Set by the server from the venue the caller acts at; not sent."},"displayOrder":{"type":"integer","default":100},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"},"isActive":{"type":"boolean","default":true,"description":"**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"}}},
"ProductCategoryNode": {"x-ticvai-persistence":"none — projection over catalogue.product_category","description":"**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n","allOf":[{"$ref":"#/components/schemas/ProductCategory"},{"type":"object","required":["children"],"properties":{"children":{"type":"array","description":"Empty on a leaf.","items":{"$ref":"#/components/schemas/ProductCategoryNode"}}}}]},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProductStartTime": {"x-ticvai-persistence":"none — computed on read","type":"object","description":"One start time a room type can be booked at for the chosen length (rev 3 REV3-13).","required":["startsAt","endsAt","freeCount"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"`startsAt` plus the variant's `durationMinutes`; the cart line's `bookedWindow.endsAt`."},"freeCount":{"type":"integer","minimum":1,"description":"Resources of the room type free for the whole window. Only times with at least one are returned."}}},
"ProductVariant": {"x-ticvai-persistence":"catalogue.variant","type":"object","required":["id","productId","sku","axisValues","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"axisValues":{"type":"object","additionalProperties":{"type":"string"}},"name":{"type":"string","maxLength":150,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"},"isDefault":{"type":"boolean","default":false,"description":"Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"},"isActive":{"type":"boolean","description":"False when retired. Retired variants are never deleted — orders reference them."},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"}}},
"PromotionEvaluation": {"x-ticvai-persistence":"none — computed","type":"object","required":["totalDiscount","lines","applied","rejected"],"properties":{"totalDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","required":["lineId","originalPrice","discountedPrice","discount"],"properties":{"lineId":{"type":"string"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"applied":{"type":"array","items":{"type":"object","required":["promotionId","promotionCode","discount"],"properties":{"promotionId":{"type":"string","format":"uuid"},"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"couponCode":{"type":"string","nullable":true}}}},"rejected":{"type":"array","description":"Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n","items":{"type":"object","required":["promotionCode","reason"],"properties":{"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"reason":{"type":"string","enum":["conditionsNotMet","supersededByBetterOffer","exclusivePromotionApplied","redemptionLimitReached","budgetExhausted","outsideValidPeriod","wrongChannel","membershipRequired","couponRequired"]},"detail":{"type":"string"}}}}}},
"RecordConsentAnswersRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["cartId","answers","source","answeredAt"],"properties":{"cartId":{"type":"string","format":"uuid","description":"The cart the answers are given for. `checkoutCart` binds them to its order."},"answers":{"type":"array","minItems":1,"maxItems":200,"items":{"type":"object","required":["questionId","questionVersion","answer"],"properties":{"questionId":{"type":"string","format":"uuid"},"questionVersion":{"type":"integer","minimum":1,"description":"The version the guest was shown, from `Cart.consentQuestions`."},"answer":{"type":"string","enum":["yes","no"]},"cartLineId":{"type":"string","format":"uuid","nullable":true,"description":"For a `perPerson` question, the line the person is on."},"personIndex":{"type":"integer","minimum":0,"nullable":true,"description":"For a `perPerson` question, the person's row in that line's `eligibilityDeclaration`, counting from 0."},"personName":{"type":"string","maxLength":120,"nullable":true},"personSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"Where the person is a known guest, such as the booker or a family member."}}}},"source":{"$ref":"#/components/schemas/ConsentSource"},"answeredAt":{"type":"string","format":"date-time"}}},
"ResourceHold": {"x-ticvai-persistence":"resources.resource_hold","type":"object","description":"**A guest's pick on the map, held while they pay** (decided 29 September, rev 3 REV3-15). The resource counterpart of `seating.SeatHold`: named resources, short-lived, converted by the order rather than released. States in `states/resource-hold.yaml`.\n","required":["id","mapId","resourceIds","from","to","status","createdAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"mapId":{"type":"string","format":"uuid"},"resourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"partySize":{"type":"integer","nullable":true},"status":{"type":"string","enum":["held","converted","released","expired"]},"totalPrice":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"heldByPrincipalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"Set when the order converts it."},"extensionCount":{"type":"integer","default":0},"createdAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","description":"The partition key (ADR-0005), written at `venue` scope."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"SeatAvailability": {"x-ticvai-persistence":"none — computed from seat, hold and block","type":"object","required":["performanceId","seatMapId","renderMode","totals","seats"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"renderMode":{"type":"string","enum":["graphical","list"],"description":"The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"buffered":{"type":"integer"}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"available":{"type":"integer"},"sold":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"sections":{"type":"array","description":"The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n","items":{"type":"object","required":["code","name"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"description":"As `Section.viewAssetId`. Null means render the view from geometry."},"boundary":{"type":"array","nullable":true,"items":{"$ref":"#/components/schemas/Point"},"description":"As `Section.boundary`. Null when `renderMode` is `list`."}}}},"seats":{"type":"array","items":{"type":"object","required":["seatId","status"],"properties":{"seatId":{"type":"string"},"status":{"$ref":"#/components/schemas/SeatStatus"},"categoryId":{"type":"string","format":"uuid","nullable":true},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`, as on `Seat`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true,"description":"The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."}}}}}},
"SeatHold": {"x-ticvai-persistence":"seating.seat_hold","type":"object","required":["id","performanceId","seatIds","status","createdAt","expiresAt"],"properties":{"id":{"type":"string"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","items":{"type":"string"}},"bufferedSeatIds":{"type":"array","items":{"type":"string"},"description":"Neighbours implicitly held by a seating rule."},"status":{"type":"string","enum":["held","converted","released","expired"]},"totalPrice":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"heldByPrincipalId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"extensionCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SeatRecommendation": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatIds","totalPrice","isContiguous","rank"],"properties":{"seatIds":{"type":"array","items":{"type":"string"}},"displayLabels":{"type":"array","items":{"type":"string"}},"totalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryId":{"type":"string","format":"uuid"},"isContiguous":{"type":"boolean"},"rank":{"type":"integer","description":"Best first."},"rationale":{"type":"string","description":"Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"}}},
"SeatRecommendationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["partySize","strategy"],"properties":{"partySize":{"type":"integer","minimum":1,"maximum":50},"strategy":{"$ref":"#/components/schemas/SeatRecommendationStrategy"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maxPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accessibleCount":{"type":"integer","default":0,"description":"Wheelchair spaces in the party. Companions are added automatically."},"maxOptions":{"type":"integer","default":3,"maximum":10}}},
"SeatRecommendationStrategy": {"type":"string","enum":["bestAvailable","bestValue","closestToStage","accessible","contiguous"]},
"SeatStatus": {"type":"string","enum":["available","held","sold","blocked","buffered","unavailable"]},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"}}},
"VenueMapDetail": {"type":"object","description":"19.2.55. **The whole map in one call**, so a client caches it and filters locally.","properties":{"version":{"type":"integer","nullable":true,"readOnly":true,"description":"**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"},"map":{"$ref":"#/components/schemas/VenueMap"},"points":{"type":"array","items":{"$ref":"#/components/schemas/VenuePoint"}},"paths":{"type":"array","items":{"$ref":"#/components/schemas/VenuePath"}},"resources":{"type":"array","description":"The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n","items":{"$ref":"#/components/schemas/PlacedResource"}}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenuePoint": {"type":"object","x-ticvai-persistence":"venuemap.point","description":"19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n","required":["id","mapId","kind","name","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the point."},"kind":{"type":"string","enum":["ride","attraction","show","restaurant","cafe","shop","kiosk","toilet","babyCare","prayerRoom","firstAid","atm","lockers","entrance","exit","emergencyExit","assemblyPoint","parking","guestServices","smokingArea","waterFountain","chargingPoint","photoSpot","junction","other"],"description":"**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"},"name":{"type":"string","x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"},"nameLocalised":{"type":"object","nullable":true,"additionalProperties":{"type":"string"}},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"},"productId":{"type":"string","format":"uuid","nullable":true,"description":"For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"},"isStepFree":{"type":"boolean","default":true,"description":"Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"},"openingHours":{"type":"string","nullable":true},"iconRef":{"type":"string","nullable":true},"isActive":{"type":"boolean","default":true},"isNavigable":{"type":"boolean","default":true,"description":"Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"},"isDestination":{"type":"boolean","default":true,"description":"**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"},"description":{"type":"object","nullable":true,"additionalProperties":{"type":"string","maxLength":1000},"description":"**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"},"media":{"type":"array","maxItems":12,"description":"**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n","items":{"type":"object","required":["assetId","kind"],"properties":{"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.media_asset"},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false},"altText":{"type":"string","nullable":true,"maxLength":200}}}},"featuredOffer":{"type":"object","nullable":true,"required":["kind","id"],"description":"**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n","properties":{"kind":{"type":"string","enum":["product","bundle"]},"id":{"type":"string","format":"uuid","description":"The `catalogue.product` id or the `promotions.bundle` id, by `kind`."},"label":{"type":"string","nullable":true,"maxLength":40,"description":"The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."}}},"typicalDurationMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":600,"description":"**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"},"interestTags":{"type":"array","maxItems":12,"description":"**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n","items":{"type":"string","enum":["thrill","family","kids","water","animals","shows","culture","shopping","dining","relaxing","photo","adventure","sport","nightlife","indoor"]}},"cuisineTags":{"type":"array","maxItems":8,"description":"**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n","items":{"type":"string","maxLength":30}},"retailTags":{"type":"array","maxItems":8,"description":"**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n","items":{"type":"string","maxLength":30}}}},
"Wishlist": {"type":"object","required":["subjectId","items"],"x-ticvai-persistence":"none — wrapper. The items are the table, keyed by subject","properties":{"subjectId":{"type":"string","format":"uuid"},"items":{"type":"array","x-ticvai-persistence":"marketing.wishlist_item","items":{"type":"object","required":["id","variantId","addedAt","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string"},"performanceId":{"type":"string","format":"uuid","nullable":true},"performanceStartsAt":{"type":"string","format":"date-time","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money","description":"The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"},"unavailableReason":{"type":"string","nullable":true},"note":{"type":"string","nullable":true},"addedAt":{"type":"string","format":"date-time"}}}}}}
}
```
