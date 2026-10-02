# P02-engagement-support-01 — P02 · Engagement & Support (1 of 2)

**10 screens · 34 operations · 80 schemas · 4 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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
  `AI_USE, CASE_MANAGE, GUEST_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **11 of these operations work offline**: getTenantAppStatus, getVisitPlan, getWaitTimes, listCatalogueBundles, listMyNotifications, listProducts, listPublishedContentPages, listPublishedFaqs
  — and the rest do not. A surface that looks the same online and off is lying.
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

### White Label & CMS

A tenant (one operator, one or many venues) brands and arranges its own guest surfaces, the guest web (P01), the guest app (P02) and the kiosk (P05), from the Venue CMS (P13, a section of the Venue Management app), and TICVAI platform staff can do the same from the console (P09 ADM-016..018) only under a time-boxed grant into the tenant. Everything is configuration over a fixed structure: the guest flow, the page structure and the components are TICVAI's and stay the same for every tenant; the tenant chooses graphics, colours, fonts, which modules and tabs appear, the order of homepage sections and booking steps within allowed limits, copy in each language, and its domain. It never adds components. Work happens in ONE working draft per tenant; nothing a guest sees changes until a person with TENANT_PUBLISH publishes the draft as an immutable version (with a note), and a rollback is restore into the draft, review the diff, then publish, never one click. Three things are deliberately outside the draft and take effect at once: the live app status (maintenance, minimum app version, contact, sold out or closed), a venue's Help me choose publish, and policies (each save is a new version). Build-time parts (app icons, native splash, custom font files, wallet and payment integrations) reach guests only with a new store build, which the client publishes under its own Apple and Google accounts (CMS-104). Staff surfaces (POS, scanner, staff app, kitchen display) never take tenant branding; every guest surface carries the "Powered by TICVAI" credit, a toggle that is on by default (decided 2 October 2026, CHG-NOTE-009; DI-297 amended). Arabic is a first-class layout: enabling `ar` requires an Arabic font, the whole layout mirrors (numbers, times, codes and logos do not), and every authored text is a per-language value. The step-based Site Builder (CMS-102) walks a new tenant through seven steps from a venue-type preset so that a logo, four colours and a publish are enough for a working site in about 30 minutes; every step opens the full screen for its details. Vocabulary below; the element-by-element model follows; inputToOutput at the end gives worked examples.
*(source: contracts/satellite/white-label.yaml#/info; DI-223; DI-285; DI-111; DI-297; DI-296; DI-298; DI-997; DI-998; DI-1014; R139; R073; F22 step 5; F22 step 6; docs/architecture/rtl-and-theming.md)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Draft | The tenant's one working configuration. Every Save writes it; guests never see it. | Staging, Unsaved, Pending | contracts/satellite/white-label.yaml#/info |
| Publish | Make the draft the live version guests read, with a note. Needs TENANT_PUBLISH. | Go live, Deploy, Push, Save and publish | contracts/satellite/white-label.yaml#publishTenantConfig |
| Save | Write to the draft. Never publishes. | Apply, Update live | contracts/satellite/white-label.yaml#/info |
| Version | An immutable published snapshot, numbered, with who published it and the note. | Release, Revision, Backup | contracts/satellite/white-label.yaml#/components/schemas/ConfigVersion |
| Restore into draft | Copy an old version back into the draft. Publishes nothing. | Roll back, Revert, Undo | R139 |
| Live now | The changes that bypass the draft and apply at once (maintenance, availability, minimum app version, contact, Help me choose publish, policies). | Instant publish | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Needs an app update | A build-time change (app icon, native splash, uploaded font, wallet or payment integration) that reaches app users only with a new store build. | Rebuild required, Build-time, Pending release | contracts/satellite/white-label.yaml#/components/schemas/ChangeScope |
| Theme | The tenant's colours, corner radius, surfaces and buttons. | Skin, Template, Style sheet | contracts/satellite/white-label.yaml#/components/schemas/Theme |
| Booking flow | The ordered steps a guest goes through to book one kind of product at one venue. | Checkout flow, Journey, Funnel, Wizard | contracts/satellite/white-label.yaml#/components/schemas/BookingFlow |
| Step | One stage of a booking flow (Date, Time, Tickets, Extras, Payment...). Marked Required, Optional or Conditional. | Page, Stage, Screen | contracts/satellite/white-label.yaml#/components/schemas/BookingFlowStepKey |
| Help me choose | The venue's short set of questions that filters the products shown. Never a consent step. | Quiz, Experience builder, Wizard, Recommender | DI-1005 |
| Module | A licensed product area a tenant switches on for guests (Dining, Shop, Map...). Off means hidden, not greyed. | Plugin, App, Feature | contracts/satellite/white-label.yaml#setModuleEnablement |
| Feature | A finer switch inside the guest app (guest checkout, AI concierge, Apple Wallet...). | Module, Add-on | contracts/satellite/white-label.yaml#setFeatureToggles |
| Buy tickets | The persistent button in the guest app that opens GST-003, and its label. | Book now, Shop, Purchase | DI-1081 |
| Powered by TICVAI | The platform credit on every guest surface; a toggle, on by default, off only where the venue's licence allows. | Built by TICVAI, Made by TICVAI | DI-297 / decided 2 October 2026 by Chinmay (CHG-NOTE-009) |
| Site Builder | The seven-step guided set-up (CMS-102). | Wizard, Onboarding, Setup assistant | DI-997 |
| Venue override | A booking setting one venue sets differently from the tenant; everything else is inherited. | Exception, Custom setting | DI-1063 |
| Sold out today / Closed | The two availability signals guests see; sold out means come another day, closed means the venue is not open. | Unavailable, Error | R073 |
| Maintenance | The tenant-branded page shown while the guest web and app are switched off, with when they are expected back. | Down, Outage, Offline | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Domain | The web address the tenant's guests use; Verify proves the tenant controls it before a certificate is issued. | URL, Site address, DNS | contracts/satellite/white-label.yaml#claimCustomDomain |

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
| `GST-030` | In-Venue Notifications | A | 3 | 12 | 5 | 0 | 4 | 0 | guest | notStarted (client-verified) |
| `GST-031` | AI Concierge – Home | A | 8 | 23 | 5 | 35 | 3 | 0 | guest | notStarted (designed) |
| `GST-032` | AI Concierge – Chat | A | 38 | 26 | 6 | 34 | 3 | 0 | guest | notStarted (designed) |
| `GST-033` | AI Concierge – Contextual Help | A | 7 | 20 | 5 | 18 | 0 | 0 | guest | notStarted (designed) |
| `GST-035` | Feedback & Ratings | A | 28 | 20 | 4 | 82 | 2 | 0 | guest | notStarted (client-verified) |
| `GST-040` | Help & Support | A | 8 | 31 | 6 | 0 | 3 | 0 | guest | notStarted (client-verified) |
| `GST-051` | Plan | A | 26 | 0 | 7 | 7 | 8 | 1 | guest | notStarted (client-verified) |
| `GST-052` | Suggested Itineraries | A | 17 | 28 | 6 | 3 | 2 | 1 | guest | notStarted (designed) |
| `GST-053` | Your Plan | A | 15 | 91 | 7 | 9 | 8 | 1 | guest | notStarted (client-verified) |
| `GST-054` | AI Planner | A | 9 | 71 | 7 | 29 | 4 | 1 | guest | notStarted (client-verified) |

## Thin screens in this batch

**GST-030, GST-052 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `GST-030` In-Venue Notifications

**Work with in-venue notifications for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `fnb` module |
| Block | Block A · ticket #18153 (APP-MOB-GST-030) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | configEditor (comfortable density): `listMyNotifications` reads the feed (decided 29 September, rev 3 GAP-C1); the location-session claim stays a form on the same screen, so the pattern is kept until the screen is redrawn |
| Offline | **The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late. |
| Opens with | `subjectId` (session) |
| Route | `/general/in-venue-notifications` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Back in the first release** (decided 29 September, rev 3 GAP-C1): the notifications feed is needed in the first release, which reverses audit R242's deferral of this screen. The `deferred` block is removed and the screen returns to `wave: 2`, where it sat before R242. Queue calls and order status still also show on the queue and order screens, which poll. **In the first release (rev 3 GAP-C1, 29 September; DI-1075)**, superseding the R242 deferral (CHG-SGU-017).

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The app's in-venue notifications feed, the same as WEB-046 and better delivered (native push). It is also the place a guest finds a call they missed while the app was closed.

**Fixed on main** (the package already carries these; draw what it says): Same claimLocationSession attach as WEB-046. (CHG-SGU-017); The prototype note still says deferred (R242). (CHG-SGU-017).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unread only | toggle | optional | off | — | — | Sends `?unreadOnly=` to `listMyNotifications`. | `listMyNotifications` ?unreadOnly |

**Sent by *Mark all as read*** (`markMyNotificationsRead`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Ids `ids` | list of values (chips) | optional | — | at most 200 | — | — | `markMyNotificationsRead` body |
| All `all` | toggle | optional | off | — | — | — | `markMyNotificationsRead` body |

#### Outputs: what the screen shows and produces

**Shown**

**Notifications** (card list, from `listMyNotifications`): **Newest first, unread ones marked.** Each card shows the kind, title, body and when it was queued; tapping one opens its `deepLink` (an order, a queue ticket, a booking) and marks it read. `unreadCount` is the badge on the tab. Sends `?venueId=` for the venue the guest picked.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | text | — |
| Kind | chip: Queue call, Order ready, Booking change, Venue alert, Offer, Other | — |
| Title | in the reader's language | — |
| Body | in the reader's language | — |
| Venue | the name it points at, never the id | — |
| Deep link | text | Where tapping the notification leads in the app (an order, a queue ticket, a booking). |
| Queued at | 1 Oct 2026, 14:30 | — |
| Read | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Unread count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Mark all as read (primary button) | `markMyNotificationsRead` POST `/me/notifications/read` | inline | inline | — | works offline |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Feed**: Same cards and rules as WEB-046; the tab bar shows the unread count. *(source: contracts/satellite/marketing-crm.yaml#listMyNotifications)*

**Data it reads**: `listMyNotifications` (onLoad, The guest's notification feed, newest first: queue calls …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-031` AI Concierge – Home: *AI Concierge – Home*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The notification feed. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the in-venue notifications untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No notifications yet.** Queue calls, order updates and venue notices appear here as the venue sends them. |
| Offline (`?state=offline`) | **The offline banner shows.** Notices already received stay listed. New queue calls and order updates arrive once the connection is back, and the banner is the warning that they may be late. |
| Empty, no results (`?state=emptyNoResults`) | **No unread notifications.** Names the Unread only filter and offers to show all; the read ones are still there. |

#### Edge cases to draw

- **Push permission denied on the device**: A one-line banner explains that queue calls will only show when the app is open, with Open settings. *(source: contracts/satellite/marketing-crm.yaml#registerGuestDevice)*
- **Offline**: Notices already received stay listed; new ones arrive when the connection returns, and the banner warns they may be late. *(source: screens/P02-guest-mobile-app.yaml#GST-030)*

#### Consistency with other screens

- Match `WEB-046`: Same feed.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
notifications:
- kind: Queue
  title: 'Your turn: Pearl Diver ride'
  time: just now
- kind: Booking
  title: Your cabana moved to Cabana 12
  time: 3h ago
```

#### Permissions

- `listMyNotifications` → no permission · guest
- `markMyNotificationsRead` → no permission · guest

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Virtual queue join flow with a persistent status notification (e.g. "in queue, 25 minutes"). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1090)*
- The in-venue notifications feed is needed in the first release on web and mobile (R242 deferral reversed). *(agreed · design review 29 Sep 2026, GAP-C1 · C. Wave 2: In-Venue Notifications · DI-1075)*
- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-030` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *DEFERRED (R242), still in the prototype: Account → All screens → Wave 2 → In-venue notifications; At-venue tab → Alerts*. Differences: The YAML defers this (no in-app notification feed in the first release), but the prototype still shows a feed and an Alerts tab, so the client will expect it.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-030?state=<state>`: loading, error, emptyFirstRun, offline, emptyNoResults.
- [ ] Every action is wired with its success and its failure: Mark all as read.
- [ ] Every transition is wired: `GST-001`, `GST-031`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-031` AI Concierge – Home

**Ask, and be answered or handed to a person.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `ai` module |
| Block | Block A · ticket #18172 (APP-MOB-GST-031) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (comfortable density): The conversation and its state (thinking, answered, handed to a person) are the content; the menu is only a shortcut (design-notes correction ai, CHG-SGU-016) |
| Offline | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Opens with | `conversationId` (deepLink), `outletId` (deepLink), `messageId` (navigation) · cold entry: A guest opening a notification about their own conversation (an agent replied, a handover was picked up): it opens that conversation, or says it was closed. |
| Route | `/general/ai-concierge-home` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **Cross-surface parity, 31 August**: added createAiConversation, handoverToAgent, requestSuggestion. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations. **Rev 3 (decided 29 September).** The concierge shows as mascot art when `BookingFlowConfig.conciergeMascot` is on (default), otherwise a plain button (CFG-5).

**From the AI & Intelligence process.** Sahli's home in the guest app: where a guest starts a conversation, sees earlier ones and finds quick help. It is the app rendering of WEB-044 and must behave identically. It is entered from the app home (GST-001) and opens the chat (GST-032). The one thing to get right: it is a concierge, not an F&B screen - the menu read it currently declares is a shortcut at most.

**Fixed on main** (the package already carries these; draw what it says): requiresModule is fnb. (CHG-SGU-016); purpose reads "The screen this app sits on. Everything else is entered from here and returns to it." (CHG-SGU-016); The only read is getGuestMenu, drawn as the screen's record; no list of the guest's conversations. (CHG-SGU-016); requestSuggestion is offered to the guest with kind prepPlan. (CHG-SGU-016); recordAnswerFeedback and sendConversationMessage missing (both on WEB-044). (CHG-SGU-016); entryState.coldEntry says "A conversation link an agent opens from a notification". (CHG-SGU-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is Sahli a tab of the app's bottom bar, or reached from home and the floating button only?** → Drawn default stands (answer: "Default / recommended accepted"): Floating button on every screen plus an entry on home, as the web prototype; no dedicated tab. *(decided by Chinmay, 2026-10-02; DEC-011 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Your question | text field | optional | — | — | — | The ask box under the conversation (typed, or a starter chip). Sending opens the conversation on the first message. | `AiMessage.content` |
| Message to the agent | text area | optional | — | — | — | Replaces the ask box once a person has taken the conversation; the transcript stays above. | `ConversationMessage.body` |

**Sent by *Hand over to a person*** (`handoverToAgent`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Guest requested · Assistant refused · Assistant failed · Out of scope · Negative sentiment · Complex intent · Payment issue | — | — | `handoverToAgent` body |
| Summary `summary` | text field | optional | — | — | — | The assistant's own summary of what the guest wants, so the agent opens with context rather than reading a transcript while somebody waits. | `handoverToAgent` body |
| Preferred queue `preferredQueueId` | picker: choose a preferred queue | optional | — | — | shows names, sends the id | — | `handoverToAgent` body |

**Sent by *Helpful / Not helpful*** (`recordAnswerFeedback`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rating `rating` | segmented control | required | — | Helpful · Not helpful | — | — | `recordAnswerFeedback` body |
| Reason `reason` | select | optional | — | Wrong · Outdated · Incomplete · Not grounded · Unsafe · Other | — | — | `recordAnswerFeedback` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `recordAnswerFeedback` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **question / starter chips**: A prominent "Ask Sahli" input and 4-6 starter chips from guestCapabilityScope (opening hours, wait times, what suits my kids, parking, food near me). Tapping a chip opens GST-032 with the question sent. Voice input is not specified; do not draw it. *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicy (guestCapabilityScope) / DI-207)*
- **module, locale**: Never asked. The conversation opens silently on the first question with the guest module and the app locale. *(source: contracts/satellite/ai.yaml#createAiConversation)*

#### Outputs: what the screen shows and produces

**Shown**

**Ask Sahli** (assistant panel, from `sendAiMessage`): **The conversation is the content.** The question shows at once and the answer streams with its sources; on 503 (every provider failed) "Sahli can't answer right now" with Hand over to a person and Try again. The conversation is opened silently (`createAiConversation`) on the first message, its scope taken from the session; the guest never picks a module.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Role | chip: User, Assistant, System | — |
| Content | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Kind | chip: Document, Product, Entitlement, Report, Record | — |
| ID | text | — |
| Title | text | — |
| Collection | the name it points at, never the id | — |
| Excerpt | text | — |
| Relevance | 1,234.5 | — |
| Confidence | 1,234.5 | 8.1.5, 8.3.67. Nullable on purpose — a provider that does not report confidence must yield null rather than an invented number, and an … |
| Rationale | text | 8.3.68, 8.3.69. |
| Proposed action | grouped details | Present where the answer suggests a change. A draft, never applied here. |
| ID | the name it points at, never the id | — |
| Interaction | the name it points at, never the id | — |
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |
| Payload | grouped details | The request body a person would submit, ready to review. Open on purpose: its shape is the request body of `targetOperation` in … |

**Earlier conversations** (card list, from `listAiConversations`): The signed-in guest's own conversations, newest first, the first question as the title; no principal, scope or module columns.

| Shows | Format | Notes |
|---|---|---|
| Started at | 1 Oct 2026, 14:30 | — |
| Last message at | 1 Oct 2026, 14:30 | — |
| Message count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Hand over to a person (secondary button) | `handoverToAgent` POST `/conversations/{conversationId}/handover` | inline | Conversation | 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem) | — |
| Helpful / Not helpful (secondary button) | `recordAnswerFeedback` POST `/messages/{messageId}/feedback` | inline | AiAnswerFeedback | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Order food (secondary button) | `getGuestMenu` GET `/outlets/{outletId}/guest-menu` | — | GuestMenu | 404 No menu in force at that time. | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **earlier conversations**: The guest's own conversations, newest first (first question as title, relative date); empty state "Ask Sahli anything about your visit". *(source: contracts/satellite/ai.yaml#listAiConversations / screens/P02-guest-mobile-app.yaml#GST-031 (guest app return FINDINGS.md))*
- **wait-time and upsell suggestions**: Where the home shows a suggestion (a short wait now, an add-on), it carries the "Based on" line and, where the estimate is a range, the range. A guest never sees a confidence number. *(source: contracts/satellite/ai.yaml#requestSuggestion / ADR-0051)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Ask / tap a starter chip**: Opens GST-032 with the question sent and the answer streaming. *(source: screens/P02-guest-mobile-app.yaml#GST-031 (navigation.transitions))*
- **Hand over to a person**: Same as WEB-044 - one tap, reason guestRequested, Sahli's summary, queue position and wait shown; 409 offers a case. *(source: contracts/satellite/marketing-crm.yaml#handoverToAgent)*
- **Order food (optional shortcut)**: Opens the outlet's menu in force (getGuestMenu); shows "Menu until 11:00" from inForceUntil. *(source: contracts/satellite/fnb.yaml#getGuestMenu)*

**Data it reads**: `createAiConversation` (background, Opened silently on the first message; the scope comes from …); `requestSuggestion` (background, From the conversation only, kinds waitTime and upsell …); `listAiConversations` (onLoad, The guest's own earlier conversations)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-032` AI Concierge – Chat: *AI Concierge – Chat*; carries `conversationId`, `messageId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The concierge home: earlier conversations (`listAiConversations`) and the ask box. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the concierge home untouched. |
| Empty, first run (`?state=emptyFirstRun`) | "Ask Sahli anything about your visit": no earlier conversations; the first question opens one. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem); 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem); 422 The guard model blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Edge cases to draw

- **AI unavailable, paused or not licensed**: The screen never shows an error page: it offers Hand over to a person and the venue's help topics. With AI not licensed the Sahli entry is hidden from the tab bar and home. *(source: contracts/satellite/ai.yaml#pauseAiCapability / screens/P02-guest-mobile-app.yaml#GST-031 (notes))*
- **Cold entry from a notification link to a closed conversation**: Opens the transcript read-only with "This conversation was closed" and a button to start a new one. *(source: screens/P02-guest-mobile-app.yaml#GST-031 (entryState.coldEntry))*
- **Offline**: Earlier conversations stay readable; Ask is disabled with "You're offline". *(source: screens/P02-guest-mobile-app.yaml#GST-031 (states.offline))*

#### Consistency with other screens

- Match `WEB-044`: Same component set, same mascot setting (Concierge mascot, default on), same handover and feedback.
- Match `GST-032`: The chat itself; GST-031 only starts and lists conversations.
- Match `GST-033`: Contextual help opens the same conversation component pre-filled with the context of the screen it was opened from.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Coastal Aqua
starterChips:
- What time do you close today?
- Shortest wait right now?
- Rides for a 6-year-old
- Where can we eat near the wave pool?
- Parking
earlierConversations:
- title: Is the lazy river open in the evening?
  when: Yesterday
- title: هل يمكنني استرداد التذكرة؟
  when: 12 Sep
```

#### Permissions

- `getGuestMenu` → no permission · guest, staff
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `handoverToAgent` → no permission · guest
- `requestSuggestion` → `AI_USE` (operate) · staff, guest
- `listAiConversations` → `AI_USE` (operate) · staff, guest
- `recordAnswerFeedback` → `AI_USE` (operate) · staff, guest
- `sendConversationMessage` → `CASE_MANAGE` (configure) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

35 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.9 | APIs shall support menu retrieval, order creation, order status, kitchen status, inventory updates and promotions. | Developer & API Management | CONTRACTED | `getGuestMenu` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| … 23 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The concierge (Sahli) shows as mascot art or as a plain button; setting "Concierge mascot", default on. *(agreed · design review 29 Sep 2026, CFG-5 · Sahli mascot (on/off) · DI-1069)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Concierge mascot (`bookingFlow.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |
| Settings: concierge mascot (`bookingFlow.venueOverrides[].settings.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-031` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-031?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Hand over to a person, Helpful / Not helpful, Order food.
- [ ] Every transition is wired: `GST-001`, `GST-032`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-032` AI Concierge – Chat

**Talk to Sahli: the answers, and a person when Sahli cannot help.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #18197 (APP-MOB-GST-032) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (comfortable density): `getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Opens with | `cartId` (session), `conversationId` (deepLink), `orderId` (deepLink), `messageId` (navigation) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. **A guest opening an order link weeks later.** Shows the … |
| Route | `/general/ai-concierge-chat` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. The chat design itself was deferred to the AI workshop (DI-195); this screen keeps the operations it needs until then (CHG-SGU-020).

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The AI concierge chat: answers about tickets, food, shops, timings and the guest's own bookings, grounded in the venue's data, with a hand-over to a person. Block A (wave 2). Shown as mascot art (Sahli) or a plain button per the venue.

**Fixed on main** (the package already carries these; draw what it says): "Create guest F&B order" is the primary action with a form exposing id, lines, quotedTotal, recordedAt. (CHG-GST-003); Purpose "Add ai concierge – chat for this venue" and no prototype frame. (CHG-SGU-020).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the concierge chat design settled after the AI workshop?** → Drawn default accepted: Draw the chat with grounded answers and hand-over; leave billing out of the guest UI. *(decided by Chinmay, 2026-10-02; DEC-109 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

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

**Form: Checkout cart** (modal, opened by *Checkout cart*; *Checkout cart* calls `checkoutCart`, *Cancel* sends nothing)

**Collects what `checkoutCart` sends before it is called.** Nothing in the body is required. Optional: `subjectId`, `attendees`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | The guest the order is for. A guest caller may name only themselves (`guestAuth` never widens to another subject); omitted, the cart's own `subjectId` is used. | `checkoutCart` body |
| Charge currency `chargeCurrency` | text field | optional | — | pattern `^[A-Z]{3}$`; A currency the venue does not take is refused 400 `currency-not-chargeable`. | — | The currency the guest selected to pay in (decided 2 October 2026, Chinmay; CHG-FIN-001). | `checkoutCart` body |
| Marketing consents `marketingConsents` | repeatable rows | optional | — | — | — | Marketing opt-ins given at checkout (29 September, M18-15). Shown unticked beside the terms; one entry per channel and purpose the guest ticked. | `checkoutCart` body |
| Channel `marketingConsents[].channel` | radio group | required | — | Email · SMS · Whatsapp · Push | — | — | `checkoutCart` body |
| Purpose `marketingConsents[].purpose` | text field | required | — | max length 60 | — | The consent purpose code (marketing ConsentPurpose), for example `marketing`. | `checkoutCart` body |
| Granted `marketingConsents[].granted` | toggle | required | — | True only when the guest ticked it. | — | True only when the guest ticked it. Never pre-ticked. | `checkoutCart` body |
| Notice version `marketingConsents[].noticeVersion` | text field | optional | — | max length 40 | — | The version of the consent notice shown. | `checkoutCart` body |
| Attendees `attendees` | repeatable rows | optional | — | — | — | The named holder for each cart line that needs one. Becomes `CreateOrderLine.holderName` on the order's matching line. | `checkoutCart` body |
| Line `attendees[].lineId` | picker: choose a line | required | — | — | shows names, sends the id | A `CartLine.id` in this cart. | `checkoutCart` body |
| Holder name `attendees[].holderName` | text field | required | — | — | — | — | `checkoutCart` body |

Errors to draw in the form: 400 `chargeCurrency` is not one the venue takes (problem type `currency-not-chargeable`, CHG-FIN-001).; 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest checkout with no confirmed one-time code … (CartProblem); 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 422 A required consent question is unanswered (`consentRequired`), or an answer blocks the booking (`consentAnswerBlocks`), with the lines in `lineIds` (decided 29 … (CartProblem)

**Form: Send AI message** (modal, opened by *Send AI message*; *Send AI message* calls `sendAiMessage`, *Cancel* sends nothing)

**Collects what `sendAiMessage` sends before it is called.** Required: `content`. Optional: `collectionIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Content `content` | text area | required | — | min length 1; max length 8000 | — | — | `sendAiMessage` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Restrict retrieval to named collections. Absent means every collection the principal may read. | `sendAiMessage` body |

Errors to draw in the form: 422 The guard model blocked the message or the reply (`guard-refused`, CHG-CSA-003).

**Form: Send conversation message** (modal, opened by *Send conversation message*; *Send conversation message* calls `sendConversationMessage`, *Cancel* sends nothing)

**Collects what `sendConversationMessage` sends before it is called.** Required: `body`. Optional: `attachments`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | text area | required | — | max length 4000 | — | — | `sendConversationMessage` body |
| Attachments `attachments` | repeatable rows | optional | — | — | — | — | `sendConversationMessage` body |
| Asset `attachments[].assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `sendConversationMessage` body |
| Kind `attachments[].kind` | select | optional | — | Image · Video · Document · Ticket · QR · Payment link | — | — | `sendConversationMessage` body |

**Form: Handover to agent** (modal, opened by *Handover to agent*; *Handover to agent* calls `handoverToAgent`, *Cancel* sends nothing)

**Collects what `handoverToAgent` sends before it is called.** Required: `reason`. Optional: `summary`, `preferredQueueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Guest requested · Assistant refused · Assistant failed · Out of scope · Negative sentiment · Complex intent · Payment issue | — | — | `handoverToAgent` body |
| Summary `summary` | text field | optional | — | — | — | The assistant's own summary of what the guest wants, so the agent opens with context rather than reading a transcript while somebody waits. | `handoverToAgent` body |
| Preferred queue `preferredQueueId` | picker: choose a preferred queue | optional | — | — | shows names, sends the id | — | `handoverToAgent` body |

Errors to draw in the form: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem)

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **message**: Free text in English or Arabic; suggested questions as chips ("What's open now?", "Where is my booking?"). *(source: DI-207; DI-388)*

#### Outputs: what the screen shows and produces

**Shown**

**The guest order status** (detail panel, from `getGuestOrderStatus`)

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Is ready for collection | yes / no (icon or chip) | — |
| Lines | list or chips (count when long) | Per-line status. A guest waiting on one dish should see which. |

**The cart** (detail panel, from `getCart`)

| Shows | Format | Notes |
|---|---|---|
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Status | chip: Active, Expiring, Expired, Abandoned, Checked out | — |
| Lines | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | Re-evaluated on every read. A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became … |
| Expires at | 1 Oct 2026, 14:30 | The earliest lease expiry in the cart, or the cart's own window where it holds none. |
| Extensions used | 1,234 | — |
| Max extensions | 1,234 | — |

**Order to confirm** (card list, from `createGuestFnbOrder`): An order the concierge proposes is a card in the conversation: items, total and Confirm, which places it (`createGuestFnbOrder`). No raw form.

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | Short and readable. It gets called out across a counter. |
| Fulfilment | chip: Collect, Deliver to location, Table service, Deliver to address | How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is … |
| Delivery label | text | Where it is going, as a runner would read it. |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Collection point | text | — |
| Table label | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add cart line (secondary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | opens modal first |
| Checkout cart (secondary button) | `checkoutCart` POST `/carts/{cartId}/checkout` | inline | Order | 400 `chargeCurrency` is not one the venue takes (problem type `currency-not-chargeable`, CHG-FIN-001).; 403 The contact the tickets would go to is not proven — an unverified session (`sessionNotVerified`), or a guest … | emits `order.created`; opens modal first |
| Send AI message (secondary button) | `sendAiMessage` POST `/conversations/{conversationId}/messages` | inline | AiMessage | 422 The guard model blocked the message or the reply (`guard-refused`, CHG-CSA-003). | opens modal first |
| Send conversation message (secondary button) | `sendConversationMessage` POST `/conversations/{conversationId}/messages` | inline | ConversationMessage | — | opens modal first |
| Handover to agent (secondary button) | `handoverToAgent` POST `/conversations/{conversationId}/handover` | inline | Conversation | 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem) | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **answer**: Short answers with cards the guest can act on (a product to book, a food order to track, a map pin); "Was this helpful?" on each answer. *(source: DI-207; screens/P02-guest-mobile-app.yaml#GST-032 apis (recordAnswerFeedback))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Talk to a person**: Hands the conversation to an agent with a summary; the guest sees "Connecting you to our team". *(source: contracts/satellite/marketing-crm.yaml#handoverToAgent)*

**Data it reads**: `getGuestOrderStatus` (onLoad, Track an order Only when signed in (decided 2 October 2026 …); `getCart` (onLoad, The cart, priced and checked, right now With the guest …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `GST-033` AI Concierge – Contextual Help: *AI Concierge – Contextual Help*; carries `conversationId`, `messageId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The concierge chat, read by `getGuestOrderStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the concierge chat untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No concierge chat yet. Offers Create guest F&B order (`createGuestFnbOrder`). |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Empty, no results (`?state=emptyNoResults`) | Nothing the concierge found matches the question; it says so in the conversation and offers to hand over to a person. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `chargeCurrency` is not one the venue takes (problem type `currency-not-chargeable`, CHG-FIN-001).; 409 A lease expired between the last read and checkout (`leaseExpired`), or a resource hold did (`resourceHoldInvalid`, rev 3 REV3-15). (CartProblem); 409 An item became unavailable, the quoted total no longer matches, the location session expired, or the outlet stopped taking orders.; 409 No … |

#### Edge cases to draw

- **The venue has no AI or the guest's scope excludes a request**: Says what it cannot do and offers the manual route (book from Buy tickets, help centre), never an error. *(source: screens/P02-guest-mobile-app.yaml#GST-032 notes (degrades to the manual planner); DI-1069)*
- **Offline**: Unavailable with the reason; past conversations readable. *(source: screens/P02-guest-mobile-app.yaml#GST-032 states.offline)*

#### Consistency with other screens

- Match `GST-033`: Contextual help opens the same conversation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
guest: Is the Lazy River open today?
answer: Yes, until 18:00. The wait is about 5 minutes. Want directions?
```

#### Permissions

- `createGuestFnbOrder` → no permission · guest
- `getGuestOrderStatus` → no permission · guest
- `getCart` → no permission · guest, partner, staff
- `addCartLine` → no permission · guest, partner, staff
- `checkoutCart` → no permission · guest, partner
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `sendConversationMessage` → `CASE_MANAGE` (configure) · staff, guest
- `handoverToAgent` → no permission · guest
- `recordAnswerFeedback` → `AI_USE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

34 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.47 | Mobile Food Ordering - System shall support mobile food ordering. | Guest Mobile App & Branding | CONTRACTED | `createGuestFnbOrder` |
| 2.9.2 | The system should provide a service to enable the dynamic composition of the shop cart. The system must provide back all the information in real time, such as the performance availabilities of an … | Ticketing Sales | CONTRACTED | `getCart` |
| 2.9.5 | The system should highlight conflicting times at different attractions when trying to purchase tickets in the same time-slot for one guest. For example, if a ticket for Golf 1 to 2 pm has been added … | Ticketing Sales | CONTRACTED | `getCart` |
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |
| 19.2.10 | Ticket Purchase - System shall support ticket purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.23 | Membership Purchase - System shall support membership purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.24 | Membership Renewal - System shall support membership renewals. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 19.2.53 | Product Purchases - System shall support merchandise purchases. | Guest Mobile App & Branding | CONTRACTED | `checkoutCart` |
| 1.1.98 | Membership renewals | Ticketing Catalogue | CONTRACTED | `checkoutCart` |
| … 22 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI chat box answers guided/predefined queries (booking status, rescheduling) and logs guest conversation history across channels (WhatsApp, web, Instagram, Facebook) with per-channel conversion attribution. *(client request · MoM 20 Aug 2026, 4.8 AI Chat Box, Routing/Queue & Case Management · DI-388)*
- AI concierge answers natural-language guest questions (ticketing, F&B, retail, venue info, timings) grounded in the venue's configured data. *(client request · MoM 10 Aug 2026, 4.6 AI Functions, Lost & Found, Reviews, Loyalty · DI-207)*
- **Open question.** AI concierge chat design is deferred until a dedicated AI workshop settles the technical approach (third-party LLM with PII masking) and the token/billing model. *(open · MoM 10 Aug 2026, 4.2 AI Concierge Chat — Open Item · DI-195)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-032` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (38), with its required mark, default, format and its error state (400, 402, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-032?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline, emptyNoResults.
- [ ] Every action is wired with its success and its failure: Add cart line, Checkout cart, Send AI message, Send conversation message, Handover to agent.
- [ ] Every transition is wired: `GST-001`, `GST-033`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-033` AI Concierge – Contextual Help

**Answer a question without needing a person.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `ai` module |
| Block | Block A · ticket #18092 (APP-MOB-GST-033) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (comfortable density): A conversation sheet: the question, the answer and its state are the content; nothing is configured or saved here (CHG-SGU-016) |
| Offline | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Opens with | `conversationId` (deepLink), `messageId` (navigation) · cold entry: A guest opening a notification about their own conversation: it opens the conversation, or says it was closed. |
| Route | `/general/ai-concierge-contextual-help` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. **createPayment removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted. **Cross-platform navigation removed 24 August**: BO-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**From the AI & Intelligence process.** Contextual help: Sahli opened from inside another screen (a product, the cart, a booking) with that screen's context, so the guest can ask "can I cancel this?" or "is this suitable for my 4-year-old?" without retyping what they are looking at. It is a bottom sheet over the current screen, not a form. The one thing to get right: the guest must never lose the screen they came from; closing the sheet returns them exactly where they were.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No way to pass the screen context (product, booking, cart) to the assistant. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): pattern configEditor / template form, states "The saved concierge contextual help", emptyFirstRun "No concierge contextual help … (CHG-SGU-016); Only sendAiMessage is declared. (CHG-SGU-016); "Collection ids" multiSelect on the guest form. (CHG-SGU-016); The prototype match is to "Account → All screens → Wave 2 → AI concierge – contextual help" (a catalogue view, not a drawn screen), marked … (CHG-SGU-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **On which screens does contextual help appear (product detail, cart, booking detail, ride detail)?** → Drawn default stands (answer: "Default / recommended accepted"): Product/attraction detail, cart and booking detail, as a small "Ask Sahli about this" link. *(decided by Chinmay, 2026-10-02; DEC-012 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Your question | text field | optional | — | — | — | The ask box under the conversation (typed, or a starter chip). Sending opens the conversation on the first message. | `AiMessage.content` |

**Sent by *Hand over to a person*** (`handoverToAgent`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Guest requested · Assistant refused · Assistant failed · Out of scope · Negative sentiment · Complex intent · Payment issue | — | — | `handoverToAgent` body |
| Summary `summary` | text field | optional | — | — | — | The assistant's own summary of what the guest wants, so the agent opens with context rather than reading a transcript while somebody waits. | `handoverToAgent` body |
| Preferred queue `preferredQueueId` | picker: choose a preferred queue | optional | — | — | shows names, sends the id | — | `handoverToAgent` body |

**Sent by *Helpful / Not helpful*** (`recordAnswerFeedback`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Rating `rating` | segmented control | required | — | Helpful · Not helpful | — | — | `recordAnswerFeedback` body |
| Reason `reason` | select | optional | — | Wrong · Outdated · Incomplete · Not grounded · Unsafe · Other | — | — | `recordAnswerFeedback` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `recordAnswerFeedback` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **question**: Opens with 2-3 context chips written for the source screen (on a ticket: "Can I change the date?", "What's included?"; in the cart: "Can I get a refund?"), then a free-text box. Up to 8,000 characters. *(source: contracts/satellite/ai.yaml#sendAiMessage / DI-207)*

#### Outputs: what the screen shows and produces

**Shown**

**Ask about this** (assistant panel, from `sendAiMessage`): A conversation sheet over the screen the guest is on (product, booking or cart). Opened silently with `createAiConversation` on the first question; knowledge collections are the venue's, never chosen by the guest.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Role | chip: User, Assistant, System | — |
| Content | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Kind | chip: Document, Product, Entitlement, Report, Record | — |
| ID | text | — |
| Title | text | — |
| Collection | the name it points at, never the id | — |
| Excerpt | text | — |
| Relevance | 1,234.5 | — |
| Confidence | 1,234.5 | 8.1.5, 8.3.67. Nullable on purpose — a provider that does not report confidence must yield null rather than an invented number, and an … |
| Rationale | text | 8.3.68, 8.3.69. |
| Proposed action | grouped details | Present where the answer suggests a change. A draft, never applied here. |
| ID | the name it points at, never the id | — |
| Interaction | the name it points at, never the id | — |
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |
| Payload | grouped details | The request body a person would submit, ready to review. Open on purpose: its shape is the request body of `targetOperation` in … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Hand over to a person (secondary button) | `handoverToAgent` POST `/conversations/{conversationId}/handover` | inline | Conversation | 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem) | — |
| Helpful / Not helpful (secondary button) | `recordAnswerFeedback` POST `/messages/{messageId}/feedback` | inline | AiAnswerFeedback | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **answer**: Same bubble, citations and feedback as WEB-044/GST-031. An answer about a policy cites the policy document (e.g. "Cancellation policy - Family Day Pass"). *(source: contracts/satellite/ai.yaml#/components/schemas/AiMessage)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Ask**: Opens a conversation on first send (silently) and answers in the sheet; "Continue in chat" moves it to GST-032. *(source: contracts/satellite/ai.yaml#createAiConversation / contracts/satellite/ai.yaml#sendAiMessage)*
- **Hand over to a person**: As WEB-044; the handover summary includes what the guest was looking at. *(source: contracts/satellite/marketing-crm.yaml#handoverToAgent)*

**Data it reads**: `createAiConversation` (background, Opened silently on the first question; the scope comes from …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Sahli is thinking: a typing indicator under the question. |
| Error (`?state=error`) | Sahli can't answer right now (every provider failed): Hand over to a person and Try again. |
| Empty, first run (`?state=emptyFirstRun`) | No question yet: the sheet opens with the ask box and two starter questions about the screen behind it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** The assistant needs the connection; conversations already loaded stay readable. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 No agent available. Returns the reason and offers a case, rather than queuing a guest for somebody who is not there. (HandoverRefusedProblem); 422 The guard model blocked the message or the reply (`guard-refused`, CHG-CSA-003). |

#### Edge cases to draw

- **The question needs a change Sahli cannot make (e.g. refund this order)**: Sahli explains the policy and links to the screen that does it (manage booking) or hands over; it never performs the change (AI is read-only on the transactional core). *(source: ADR-0020 / screens/P01-guest-web-storefront.yaml#WEB-044 (notes))*
- **AI unavailable**: The sheet shows the venue's help topics for that screen and Hand over to a person; never an error page. *(source: screens/P02-guest-mobile-app.yaml#GST-033 (notes - degrades rather than errors))*

#### Consistency with other screens

- Match `GST-031`: Same conversation component; the conversation started here appears in the guest's earlier conversations.
- Match `WEB-044`: The web equivalent is the Ask Sahli panel opened from a page; same context chips.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
openedFrom: Family Day Pass / تذكرة اليوم العائلي - Coastal Aqua, Sat 10 Oct
chips:
- Can I change the date?
- Is it suitable for under-3s?
- What's included?
answer: You can change the date once, up to 24 hours before your visit, from My bookings. Children under 3 enter
  free and don't need a ticket.
sources:
- Date change policy
- Child admission
```

#### Permissions

- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `handoverToAgent` → no permission · guest
- `recordAnswerFeedback` → `AI_USE` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 8.4.1 | System shall provide a conversational AI assistant across all platform modules. | Unified Operations Dashboard | CONTRACTED | `createAiConversation` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-033` · status **notStarted** · provenance designed · Corrected 2 October 2026 (CHG-SGU-016): the prototype view is a catalogue entry ("Account → All screens → Wave 2"), not a client-drawn layout, so the frame is treated as designed, not client-verified.
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → AI concierge – contextual help*
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-033?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Hand over to a person, Helpful / Not helpful.
- [ ] Every transition is wired: `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-035` Feedback & Ratings

**Tell the venue how the visit went, answer a survey it sent, or report a problem.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #18222 (APP-MOB-GST-035) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`submitReview`, `raiseMyCase`) and no read of a population — it is settings, not a list |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `formId` (deepLink) |
| Route | `/general/feedback-and-ratings` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The app's feedback and ratings, the same as WEB-026, plus "Report a problem", which raises a case. A survey link from a post-visit or post-scan message opens here.

**Fixed on main** (the package already carries these; draw what it says): The form is raw SubmitReviewRequest text fields, as on WEB-026. (CHG-SGU-017); No survey operation, as on WEB-026. (CHG-SGU-017).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Which visit | text field | optional | — | — | — | Chosen from the guest's recent orders ("Coastal Aqua - Sat 26 Sep 2026"); never typed. | `SubmitReviewRequest.relatedOrderId` |
| Your rating | stepper or slider | optional | — | min 1; max 5 | — | 1 to 5 stars; required. | `SubmitReviewRequest.rating` |
| What stood out | multi-select chips | optional | — | Exhibitions · Staff · Cleanliness · Food · Value; no duplicates | — | The venue's closed aspect set (Cleanliness, Staff, Food, Queues); multi-select, optional. | `SubmitReviewRequest.aspects` |
| Your comments | text area | optional | — | max length 5000 | — | Optional, any language. Id, subject, venue and time are set by the platform. | `SubmitReviewRequest.body` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | number field | — | min 1 | `getForm` ?version |
| Since | date picker | — | — | `listMyOrders` ?since |

**Form: Raise my case** (modal, opened by *Raise my case*; *Raise my case* calls `raiseMyCase`, *Cancel* sends nothing)

**Collects what `raiseMyCase` sends before it is called.** Required: `id`, `kind`, `summary`, `recordedAt`. Optional: `detail`, `venueId`, `orderRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Created on the device, so a retry after a dropped connection carries the same id and is the same case. | `raiseMyCase` body |
| Kind `kind` | select | required | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `raiseMyCase` body |
| Summary `summary` | text field | required | — | max length 200 | — | Lands in `Case.subject` — the case's one-line title. | `raiseMyCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time when the guest raised it. The server stamps `syncedAt` on arrival; both are kept (naming-and-style 5.2), because the SLA clock starts at `recordedAt`, not at the … | `raiseMyCase` body |
| Detail `detail` | text field | optional | — | — | — | Required, and not empty, when `kind` is `other` (decided 28 September, audit R222); a 400 otherwise. | `raiseMyCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `raiseMyCase` body |
| Order ref `orderRef` | text field | optional | — | — | — | — | `raiseMyCase` body |

Errors to draw in the form: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema

**Sent by *Submit review*** (`submitReview`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `submitReview` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `submitReview` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `submitReview` body |
| Related order `relatedOrderId` | text field | optional | — | — | — | — | `submitReview` body |
| Rating `rating` | stepper or slider | required | — | min 1; max 5 | — | — | `submitReview` body |
| Body `body` | text area | optional | — | max length 5000 | — | — | `submitReview` body |
| Aspects `aspects` | multi-select chips | optional | — | Exhibitions · Staff · Cleanliness · Food · Value; no duplicates | — | Aspect chips — the closed set the description always named. | `submitReview` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `submitReview` body |

**Sent by *Send survey*** (`submitForm`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Form `formId` | picker: choose a form | required | — | — | shows names, sends the id | — | `submitForm` body |
| Form version `formVersion` | number field | required | — | — | — | The version, not the form. 2.15.13 requires the exact accepted version retained, and a submission pointing at a form that has since changed is a submission proving nothing. | `submitForm` body |
| Subject `subjectId` | picker: choose a subject | required | — | — | shows names, sends the id | — | `submitForm` body |
| On behalf of subject `onBehalfOfSubjectId` | picker: choose an on behalf of subject | optional | — | — | shows names, sends the id | A guardian signing for a minor, or a group leader for an attendee. | `submitForm` body |
| Answers `answers` | key and value settings | optional | — | — | — | One entry per answered `FormField`, keyed by its `key`. The value's type follows the field's `type`: a string for text, long text, date, phone, email, select and `file` (the asset … | `submitForm` body |
| Signature image `signatureAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `submitForm` body |
| Submitted at `submittedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the acceptance — `submitForm` is offline-capable, and the time a waiver was signed is the evidence, not the time it synced. | `submitForm` body |
| Captured at channel `capturedAtChannel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `submitForm` body |
| Ip address `ipAddress` | text field | optional | — | — | — | — | `submitForm` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Rating, aspects, comments, visit**: Same rules as WEB-026. *(source: contracts/satellite/marketing-crm.yaml#submitReview)*
- **Report a problem**: Opens the case form with the topic preset to Complaint and the visit attached; the guest can change the topic. *(source: contracts/satellite/marketing-crm.yaml#raiseMyCase)*

#### Outputs: what the screen shows and produces

**Shown**

**Survey** (detail panel, from `getForm`): A triggered survey link (post-visit, post-scan, case closure) opens here with its formId; answered with `submitForm` (DI-391).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Kind | chip: Waiver, Survey, Data capture, Consent form, Incident report, Registration | — |
| Consent purposes | list or chips (count when long) | What a `consentForm` consents to (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form … |
| Fields | list or chips (count when long) | — |
| Key | text | — |
| Label | text | — |
| Label localised | grouped details | — |
| Type | chip: Text, Long text, Number, Date, Select, Multi select… | — |
| Options | list or chips (count when long) | — |
| Is required | yes / no (icon or chip) | — |
| Is personal data | yes / no (icon or chip) | Marked at the field, because retention is decided at the field. A survey answer and a medical condition on the same form have different … |
| Consent purpose | the name it points at, never the id | — |
| Show when | grouped details | — |
| Field | text | — |
| Equals | text | — |
| Requires signature | yes / no (icon or chip) | What makes it a waiver. And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it. |
| Signature kind | chip: Drawn, Typed, Checkbox, None | — |
| Score scale | chip: Nps, Csat, Ces, Likert5, Likert7, Stars | What makes it a survey. Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's. |
| Applies to products | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit review (primary button) | `submitReview` POST `/reviews` | SubmitReviewRequest | Review | — | — |
| Raise my case (secondary button) | `raiseMyCase` POST `/my/cases` | inline | Case | 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema | opens modal first |
| Send survey (secondary button) | `submitForm` POST `/form-submissions` | FormSubmission | FormSubmission | — | works offline |

**Data it reads**: `getForm` (onLoad, A triggered survey opened from its link); `listMyOrders` (onLoad, The recent visits a review can be about)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved feedback ratings. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the feedback ratings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No feedback ratings configured. The form opens empty and `submitReview` saves the first one; it says what the platform does in the meantime. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema |

#### Edge cases to draw

- **Offline**: The rating waits for the connection and the button says so. A rating is not queued silently. *(source: screens/P02-guest-mobile-app.yaml#GST-035)*

#### Consistency with other screens

- Match `WEB-026`: Same form and confirmation wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
visit: Tidewater Museum - Fri 25 Sep 2026
rating: 5
aspects:
- Staff
- Exhibits
comment: Our guide Aisha was wonderful with the children.
```

#### Permissions

- `submitReview` → no permission · guest
- `raiseMyCase` → no permission · guest
- `getForm` → `GUEST_VIEW` (read) · staff, guest
- `submitForm` → `GUEST_VIEW` (read) · staff, guest
- `listMyOrders` → no permission · guest

#### Requirements it meets

82 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.71 | Feedback Management - System shall support guest feedback. | Guest Mobile App & Branding | CONTRACTED | `submitReview` |
| 6.1.46 | The system should be able to report on the captured customer satisfaction feedback (based on number of stars or smiley faces, etc.) and report this monthly by attraction /location. | Retail POS | CONTRACTED | `submitReview` |
| 22.5.1 | Review Collection | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.2 | Multi-Channel Review Capture | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.14 | CRM Integration | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.15 | Loyalty Integration | Marketing & CRM | CONTRACTED | `submitReview` |
| 22.5.16 | Membership Integration | Marketing & CRM | CONTRACTED | `submitReview` |
| 2.1.13 | The system should provide the ability to capture configurable survey data. e.g. nationality, residency, guest type (individual, group, ...) in the POS and self-service kiosks. The survey should be … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.5.3 | The system should collect demographic data about guests and transfer to Guest 360 (CRM) through API integration. The data to be collected should be configurable. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.7.22 | It is expected to have the Reseller collecting the Guest information to be filled in online in order for FE to retrieve them. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.7.28 | The Guest information collected by the Market place are available for FE who can use it for future marketing campaigns. | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| 2.8.6 | The system should be able to prompt call center agents for entry of market sampling questions, several customizable data points and demographic data collection capabilities, e.g. country code, first … | Ticketing Sales | CONTRACTED | data `FormDefinition` |
| … 70 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Surveys trigger at configurable points: post-purchase, post-visit, post-ticket-scan, membership renewal and case closure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-391)*
- Example site showed a live integration with a government satisfaction-survey ("happiness meter") service. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-112)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-035` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 3 → Feedback & ratings*

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-035?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Submit review, Raise my case, Send survey.
- [ ] Every transition is wired: `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-040` Help & Support

**Answer a question without needing a person.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 2 · needs the `marketing` module |
| Block | Block A · ticket #18174 (APP-MOB-GST-040) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | commandCentre (comfortable density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |
| Opens with | `caseId` (deepLink) · cold entry: A case opened from a notification or the list. **Optional** — the ordinary way in is to raise a new one, not to open an old one. |
| Route | `/general/help-and-support` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Guest case operations wired 24 August.** **No case operation was guest-callable** — a guest could raise nothing and read nothing, and `check-screens` refused the staff-permissioned ones on a guest surface. `listMyCases`, `raiseMyCase` and `replyToMyCase` are scoped to the caller rather than filtered by a subject parameter. **Rev 3 (decided 29 September).** The Help screen shows app status and a public *What's new* (GAP-B2).

**Known gaps.** Replaced by `listPublishedFaqs`, the guest read of the same data. Replaced by `listPublishedContentPages`, the guest read of the same data.

**From the White Label & CMS process.** Help in the app: FAQ, My cases, Policies, Accessibility, app status and What's new, the same content as WEB-045. Raising a case is disabled offline with how to reach staff instead.

**Fixed on main** (the package already carries these; draw what it says): The layout is a metric dashboard (FAQ count, page count, case count tiles) and emptyNoAccess cites TENANT_CONFIGURE. (CHG-GST-004); No guest-readable policy operation. (CHG-GST-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category code | text field | — | — | `listPublishedContentPages` ?categoryCode |
| Slug | text field | — | pattern `^[a-z0-9-]+$` | `listPublishedContentPages` ?slug |
| Kind | radio group | — | Privacy · Terms and conditions · Refund · Cookie · Accessibility | `listPublishedPolicies` ?kind |

**Form: Raise my case** (modal, opened by *Raise my case*; *Raise my case* calls `raiseMyCase`, *Cancel* sends nothing)

**Collects what `raiseMyCase` sends before it is called.** Required: `id`, `kind`, `summary`, `recordedAt`. Optional: `detail`, `venueId`, `orderRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Created on the device, so a retry after a dropped connection carries the same id and is the same case. | `raiseMyCase` body |
| Kind `kind` | select | required | — | Lost property · Complaint · Question · Accessibility · Refund request · Other; Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.; A case raised as `other` must carry a non-empty `detail` … | — | What the guest says the case is about, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. | `raiseMyCase` body |
| Summary `summary` | text field | required | — | max length 200 | — | Lands in `Case.subject` — the case's one-line title. | `raiseMyCase` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time when the guest raised it. The server stamps `syncedAt` on arrival; both are kept (naming-and-style 5.2), because the SLA clock starts at `recordedAt`, not at the … | `raiseMyCase` body |
| Detail `detail` | text field | optional | — | — | — | Required, and not empty, when `kind` is `other` (decided 28 September, audit R222); a 400 otherwise. | `raiseMyCase` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `raiseMyCase` body |
| Order ref `orderRef` | text field | optional | — | — | — | — | `raiseMyCase` body |

Errors to draw in the form: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema

**Form: Reply to my case** (modal, opened by *Reply to my case*; *Reply to my case* calls `replyToMyCase`, *Cancel* sends nothing)

**Collects what `replyToMyCase` sends before it is called.** Required: `message`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Message `message` | text area | required | — | min length 1; max length 10000 | — | — | `replyToMyCase` body |

#### Outputs: what the screen shows and produces

**Shown**

**Questions and answers** (card list, from `listPublishedFaqs`): Categories in their order, each opening to its questions. Was the generated table 'Every faq category'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | in the reader's language | — |
| Entries | list or chips (count when long) | — |

**Help pages** (card list, from `listPublishedContentPages`): The live help pages; the accessibility ones open GST-057.

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Icon | the image or video | — |

**Policies** (card list, from `listPublishedPolicies`): The current terms, privacy, refund, cookie and accessibility policies.

| Shows | Format | Notes |
|---|---|---|
| Title | text | — |
| Version | text | The version a consent records (a guest who consented to version 3 consented to version 3). |
| Effective from | 1 Oct 2026 | — |

**My cases** (card list, from `listMyCases`): Only when signed in: the cases this guest raised, newest first.

| Shows | Format | Notes |
|---|---|---|
| Case number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Subject | text | The case's one-line title, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps … |
| Status | chip: Open, In progress, Awaiting guest, Escalated, Resolved, Closed | — |
| Recorded at | 1 Oct 2026, 14:30 | Device time the case was raised — the start of the SLA clock. |

**What's new** (card list, from `getTenantAppStatus`): Public, localised release notes from `getTenantAppStatus` `whatsNew`, newest first, at most 10; the staff-only `recentChanges` stays staff only.

| Shows | Format | Notes |
|---|---|---|
| Is published | yes / no (icon or chip) | True once any version has been published. |
| Published version | text | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Draft version | text | Staff only. |
| Has unpublished changes | yes / no (icon or chip) | Staff only. The working draft differs from the current version's `snapshot`. |
| Active module count | 1,234 | Staff only. `ModuleEnablement` rows with `isEnabled` true. |
| Licensed module count | 1,234 | Staff only. `ModuleEnablement` rows with `isLicensed` true. |
| Active page count | 1,234 | Staff only. Content pages that are `published` and enabled. |
| Is in maintenance | yes / no (icon or chip) | — |
| Maintenance message | in the reader's language | — |
| Expected back at | 1 Oct 2026, 14:30 | — |
| Minimum app version | grouped details | The oldest guest app build still allowed to run (decided 28 September, audit R073). |
| Ios | text | — |
| Android | text | — |
| Contact | grouped details | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided … |
| Phone | +971 50 123 4567 | — |
| Email | email, tap to write | — |
| Whatsapp | text | — |
| Address | in the reader's language | — |
| Opening hours | in the reader's language | Prose, as the guest reads it. The bookable hours are the catalogue's. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Raise my case (primary button) | `raiseMyCase` POST `/my/cases` | inline | Case | 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema | opens modal first |
| Reply to my case (secondary button) | `replyToMyCase` POST `/my/cases/{caseId}/messages` | inline | CaseDetail | — | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Tabs**: FAQ, My cases (signed in only), Policies, Accessibility; What's new under the app status line. *(source: DI-1078; DI-1073)*

**Data it reads**: `listPublishedFaqs` (onLoad, The published FAQs, readable before sign-in (GFIX-2)); `listPublishedContentPages` (onLoad, The live help and accessibility pages, readable before …); `listMyCases` (onLoad, The cases this guest raised Only when signed in (decided 2 …); `getTenantAppStatus` (onLoad, App status and the public *What's new*); `listPublishedPolicies` (onLoad, Terms, privacy, refund, cookie and accessibility policies …)

**Where the user goes next**

- → `GST-001` Home: *Home – Default*
- → `WEB-034` Lost & Found: *They report something lost*; carries `caseId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Questions, pages and policies load in place; each list loads on its own. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the help support untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No help support yet. Offers Raise my case (`raiseMyCase`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listPublishedFaqs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Reading help needs no sign-in (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)). **Raising or reading a case needs a signed-in guest**: one who is not signed in is offered sign-in and brought back to this screen; the questions, pages and policies stay readable. |
| Offline (`?state=offline`) | **The offline banner shows.** Help already loaded stays readable, marked with its age. **Raising a case is disabled offline** — it needs the connection (decided 28 September, audit R148) — and the screen says how to reach staff in person instead: the guest services desk, or any member of staff. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `kind` is `other` and `detail` is missing or empty (audit R222), or another field breaks the schema |

#### Consistency with other screens

- Match `WEB-045`: Same content and wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
whatsNew:
- version: 2.4.0
  notes:
    en: Faster ticket wallet and Arabic receipts.
    ar: محفظة تذاكر أسرع وإيصالات باللغة العربية.
```

#### Permissions

- `listPublishedFaqs` → no permission · anonymous, guest, device
- `listPublishedContentPages` → no permission · anonymous, guest, device
- `listMyCases` → no permission · guest
- `raiseMyCase` → no permission · guest
- `replyToMyCase` → no permission · guest
- `getTenantAppStatus` → no permission · device, guest, staff
- `listPublishedPolicies` → no permission · anonymous, guest, device

**A refused user sees:** Reading help needs no sign-in (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-2)). **Raising or reading a case needs a signed-in guest**: one who is not signed in is offered sign-in and brought back to this screen; the questions, pages and policies stay readable.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The guest Help screen shows app status and a public, localised "what's new" (release notes). *(agreed · design review 29 Sep 2026, GAP-B2 · B. Help: app status + recent changes · DI-1073)*
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Availability and maintenance*, set in `CMS-001` Tenant Workspace:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | — |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | — |

Also set there, as content the tenant writes: is in maintenance, minimum app version, contact, contact: whatsapp.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-040` · status **notStarted** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html`, view *Account → All screens → Wave 2 → Help & support*
- Flow F54 *Something goes wrong in the venue*, step 1: They look for an answer first. → **Self-serve before a case.** A support queue full of questions the FAQ answers is a support queue nobody can staff.
- Flow F54 *Something goes wrong in the venue*, step 2: It does not answer, so they raise a case. → **One case mechanism** — a lost item, a bad meal and a refund query are the same object with a different subject.
- Flow F54 branch at step 2 (high): when It is urgent — a child, a medical issue., **Not a case.** The app surfaces how to reach staff physically, and `reportIncident` on the staff side (F69) is what actually happens. **A queue is the wrong response to an emergency.**
- Flow F54 branch at step 2 (medium): when The guest has no connection., **Raising and replying are disabled, not queued** (decided 28 September, audit R148). The screen says the case needs a connection and shows how to reach staff in person — the nearest guest services …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-040?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Raise my case, Reply to my case.
- [ ] Every transition is wired: `GST-001`, `WEB-034`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-051` Plan

**The Plan tab: tell the venue who is coming, when, at what pace and what you like, and get a day-by-day plan.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18216 (APP-MOB-GST-051) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | multiStepForm (comfortable density): The v4 prototype asks six questions one at a time (who, heights, days, pace, likes, food) and ends on *Make my plan* |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `venueId` (session) · cold entry: The Plan tab; a cold arrival is the ordinary case and starts at the first question. |
| Route | `/general/plan-your-adventure-start` |

**What the spec says about it.** Minuted 10 Aug §4.9. Benchmarked against Skidata. Tied to a ticket purchase and saved as a personal visit profile. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1. **Mobile v4 role (MOB-6): the Plan tab root, "Plan".** Inputs: party size, heights (or ages), dates, pace (packed, balanced or relaxed), interests and cuisine. The rules planner (`generateVisitPlan`) runs with no AI. The tab is hidden when the venue turns module `visitPlanner` off. **Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam; agreed by Chinmay).** In a multi-venue tenant each chosen day is at one park, and the planner uses **only the rides, dining and retail that exist at that park**: a cuisine or shop preference is checked against that park's own points, never assumed of every park (only one park has the Indian restaurant, so *Indian* places lunch there on that park's day and nowhere else). Retail and kiosk shops are now planner options alongside F&B (the gap a Softlabs teammate flagged). Contract: venue-map `generateVisitPlan` `dayVenues`, `retailTags` …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Plan tab: six questions (party, children's heights, days, park per day in a multi-park tenant, pace, interests and shops, lunch cuisine) produce a rules-based day-by-day plan (no AI). From the venue-operations angle the plan uses live wait times and ride height rules and only offers what each day's park actually has. The one thing to get right: a preference no chosen park can meet is said, not silently filled.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Screen classified under Virtual Queue for this process (CHG-SGU-025)

**Fixed on main** (the package already carries these; draw what it says): Notes say the planner is out of the first release (R187, wave 4) yet it is in the Block A slice (CHG-SGU-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Adults | number field | — | — | — | — | Age 12 and over, at least 1, at most 8. | — |
| Children | number field | — | — | — | — | Age 3 to 11, 0-8. | — |
| How tall are the children? | select field | — | — | — | — | Per child: under 1.0 m, 1.0-1.2 m, 1.2-1.4 m, 1.4 m and over (or an age where the venue sets age rules). Rides over a child's limit are left out, from `ProductEligibilityRule`. | — |
| Which days are you visiting? | multi select | — | — | — | — | Up to three days; each day gets its own park at a multi-park venue. | — |
| Which park each day? | repeatable rows | optional | — | at most 200 | — | **Only in a multi-venue tenant** (more than one entry in `getTenantAppStatus.venues`); hidden otherwise. One choice per chosen day, defaulting to the venue picked on Home; sent as … | `TenantAppStatus.venues` |
| How busy should each day be? | select field | — | — | — | — | Packed, Balanced or Relaxed. | — |
| What are you most interested in? | multi select | — | — | — | — | Interest tags from the venue's points (`VenuePoint.interestTags`): thrill rides, family rides, shows, water, shopping. | — |
| Any shops you'd like to visit? | multi select | — | — | — | — | **Shown when Shopping is chosen above** (client meeting 30 September, MoM 4.7: retail and kiosk shops join F&B in the planner). Options are the `retailTags` of the shops and retail kiosks of the … | — |
| What would you like for lunch? | select field | — | — | — | — | **Cuisines from the dining points of the chosen parks only** (`VenuePoint.cuisineTags` of restaurants, cafes and food kiosks; client meeting 30 September, MoM 4.7). Lunch is planned at a restaurant … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Sent by *Make my plan*** (`generateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. | `generateVisitPlan` body |
| Day venues `dayVenues` | repeatable rows | optional | — | at most 7; One entry per date that is not at `venueId`; each date of `dates` at most once. | — | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). | `generateVisitPlan` body |
| Date `dayVenues[].date` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateVisitPlan` body |
| Venue `dayVenues[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `generateVisitPlan` body |
| Dates `dates` | list of values (chips) | required | — | at least 1; at most 7 | — | — | `generateVisitPlan` body |
| Party `party` | repeatable rows | required | — | at least 1; at most 20 | — | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. | `generateVisitPlan` body |
| Height cm `party[].heightCm` | number field | optional | — | min 40; max 230 | — | — | `generateVisitPlan` body |
| Age years `party[].ageYears` | number field | optional | — | min 0; max 120 | — | — | `generateVisitPlan` body |
| Pace `pace` | segmented control | optional | Relaxed | Packed · Relaxed | — | — | `generateVisitPlan` body |
| Interest tags `interestTags` | list of values (chips) | optional | — | at most 12 | — | The same closed list as `VenuePoint.interestTags`. | `generateVisitPlan` body |
| Cuisine tags `cuisineTags` | list of values (chips) | optional | — | at most 8 | — | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). | `generateVisitPlan` body |
| Retail tags `retailTags` | list of values (chips) | optional | — | at most 8 | — | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. | `generateVisitPlan` body |
| Must include points `mustIncludePointIds` | multi-picker: choose must include points | optional | — | at most 10 | — | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day. | `generateVisitPlan` body |
| Preset `preset` | select | optional | — | Highlights · Family · Thrill seeker · Water day · Relaxed · Shows and dining | — | A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility. | `generateVisitPlan` body |
| Preset key `presetKey` | text field | optional | — | max length 64; pattern `^[a-z][a-zA-Z0-9]*$`; An unknown key is refused 422 `unknown-preset`. | — | The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan … | `generateVisitPlan` body |
| Start time `startTime` | time picker | optional | — | — | HH:mm, 24-hour | When the party arrives. Null means opening time. | `generateVisitPlan` body |
| Locale `locale` | text field | optional | — | — | — | — | `generateVisitPlan` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Party**: Adults 1-8 (age 12+), children 0-8 (3-11); heights per child in bands (under 1.0 m, 1.0-1.2, 1.2-1.4, 1.4+); the heights step is skipped when no children come. *(source: screens/P02-guest-mobile-app.yaml#GST-051 / contracts/satellite/venue-map.yaml#generateVisitPlan)*
- **Days and park per day**: Up to three days; "Which park each day?" appears only in a multi-venue tenant, one choice per day. *(source: DI-1112)*
- **Pace**: Packed / Balanced / Relaxed as three cards. *(source: DI-1098)*
- **Interests, shops, lunch**: Interest chips from the venue's tags; shops shown only when Shopping is chosen; lunch cuisines list only those served at the chosen parks and name them ("Indian - Summit Peaks only"). *(source: DI-1100 / DI-1113)*

#### Outputs: what the screen shows and produces

**Shown**

**Plan your visit · n of 6** (progress indicator): Six questions; Heights is skipped when no children are coming.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Make my plan (primary button) | `generateVisitPlan` POST `/visit-plans` | VisitPlanRequest | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a … | — |
| Take a ready-made plan (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Not-at-this-park notice**: A chip or day banner "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)." *(source: DI-1113)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Make my plan**: Calls the rules planner and opens Your Plan (GST-053). *(source: contracts/satellite/venue-map.yaml#generateVisitPlan / F49 step 1)*
- **Take a ready-made plan**: Opens Suggested Itineraries (GST-052). *(source: screens/P02-guest-mobile-app.yaml#GST-051)*

**Data it reads**: `getWaitTimes` (onLoad, Wait times across a venue); `listProducts` (onLoad, List products); `getTenantAppStatus` (onLoad, The tenant's active venues, for the park-per-day choice in …)

**Where the user goes next**

- → `GST-053` Your Plan: *Make my plan*; carries `planId`; calls `generateVisitPlan`
- → `GST-052` Suggested Itineraries: *Take a ready-made plan*
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | No plan yet: the first question is shown. Nothing is saved until *Make my plan*. |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Preference not at venue (`?state=preferenceNotAtVenue`) | **A preference no chosen park can meet** (client meeting 30 September, MoM 4.7): a cuisine or shop tag with no matching point at any park of the plan is marked on its chip (*Not at the parks you chose*) before *Make my plan*; the plan is still made without it, never with a restaurant or shop from a park the party is not visiting. Where another park of the tenant has it, the chip says which, and choosing that park for a day brings it in. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a planning duration (`venue-not-plannable`), so … |

#### Edge cases to draw

- **Offline**: Answers kept; Make my plan waits for the connection and says so. *(source: screens/P02-guest-mobile-app.yaml#GST-051)*

#### Consistency with other screens

- Match `GST-022`: Rides in the plan carry the same wait source labels.
- Match `GST-023`: A plan item for a ride with a virtual queue offers "Join virtual queue" on the day.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
answers:
  adults: 2
  children: 2 (1.1 m, 1.3 m)
  days: Fri 16 Oct (Aqua Park), Sat 17 Oct (Summit Peaks)
  pace: Balanced
  interests: Family rides, Water, Shopping
  lunch: Indian - Aqua Park only
```

#### Permissions

- `getWaitTimes` → no permission · guest, public
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `generateVisitPlan` → no permission · guest
- `getTenantAppStatus` → no permission · device, guest, staff

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- The visit planner is tied to a ticket purchase and saved as a personal visit profile; benchmarked against Skidata. *(agreed · MoM 10 Aug 2026, 4.9 · DI-242)*
- Chinmay: share an itinerary with a group via an in-app QR code a friend scans to join, or an invite-to-join. *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-218)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Settings: step indicator (`bookingFlow.venueOverrides[].settings.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | — |

*Availability and maintenance*, set in `CMS-001` Tenant Workspace:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | — |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | — |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | — |

Also set there, as content the tenant writes: is in maintenance, minimum app version, contact, contact: whatsapp.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-051` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Plan tab (Plan your visit · 1 of 6)*
- Flow F49 *A guest plans a day and follows it*, step 1: They answer six questions (party, heights, days, pace, interests, lunch) and choose Make my plan. → **The rules planner, no AI.** A plan per day that leaves out rides over a child's height and plans lunch where the chosen cuisine is served. **Each day uses only its own park's rides, dining and …
- Flow F49 branch at step 1 (recoverable): when Nothing suits the whole party on the chosen day (every ride is over a child's height, or the park is closed)., **Refused with a reason**, naming the answer that ruled everything out, and the answers are kept so changing one costs nothing.
- Flow F49 branch at step 1 (recoverable): when A cuisine or shop the guest chose exists at none of the day's park's points (only one park has the Indian restaurant)., **Said, not faked** (client meeting 30 September, MoM 4.7): the day is planned from that park's own points, `unmatchedPreferences` names the park that has it, and the guest may move the day there by …
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, preferenceNotAtVenue, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Make my plan, Take a ready-made plan.
- [ ] Every transition is wired: `GST-053`, `GST-052`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-052` Suggested Itineraries

**Ready-made day plans for this venue that a guest can take instead of answering questions.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18228 (APP-MOB-GST-052) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | listDetail (comfortable density): `listProducts` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `venueId` (session) · cold entry: Lists the venue's ready-made plans; nothing is needed upstream. |
| Route | `/general/suggested-itineraries` |

**What the spec says about it.** Minuted 10 Aug §4.9. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1. **Mobile v4 role (MOB-6): ready-made day plans per venue** the guest can take; each is rules-built by `generateVisitPlan` from preset inputs, then edited on …

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Ready-made day plans for the venue (Thrill day, Family day, Relaxed day) a guest can take instead of answering the planner's questions. Block A. Since 30 September plans are per venue: each preset belongs to one park and uses only that park's rides, dining and shops.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The presets are bound to listProducts and a raw "Every bundle" table. (CHG-SGU-024)
- No prototype frame (match none). (CHG-SGU-026)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who defines the ready-made plans per venue, and where?** → Drawn default accepted: The venue configures presets as saved planner inputs per park. *(decided by Chinmay, 2026-10-02; DEC-111 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Sent by *Use this plan*** (`generateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. | `generateVisitPlan` body |
| Day venues `dayVenues` | repeatable rows | optional | — | at most 7; One entry per date that is not at `venueId`; each date of `dates` at most once. | — | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). | `generateVisitPlan` body |
| Date `dayVenues[].date` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `generateVisitPlan` body |
| Venue `dayVenues[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `generateVisitPlan` body |
| Dates `dates` | list of values (chips) | required | — | at least 1; at most 7 | — | — | `generateVisitPlan` body |
| Party `party` | repeatable rows | required | — | at least 1; at most 20 | — | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. | `generateVisitPlan` body |
| Height cm `party[].heightCm` | number field | optional | — | min 40; max 230 | — | — | `generateVisitPlan` body |
| Age years `party[].ageYears` | number field | optional | — | min 0; max 120 | — | — | `generateVisitPlan` body |
| Pace `pace` | segmented control | optional | Relaxed | Packed · Relaxed | — | — | `generateVisitPlan` body |
| Interest tags `interestTags` | list of values (chips) | optional | — | at most 12 | — | The same closed list as `VenuePoint.interestTags`. | `generateVisitPlan` body |
| Cuisine tags `cuisineTags` | list of values (chips) | optional | — | at most 8 | — | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). | `generateVisitPlan` body |
| Retail tags `retailTags` | list of values (chips) | optional | — | at most 8 | — | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. | `generateVisitPlan` body |
| Must include points `mustIncludePointIds` | multi-picker: choose must include points | optional | — | at most 10 | — | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day. | `generateVisitPlan` body |
| Preset `preset` | select | optional | — | Highlights · Family · Thrill seeker · Water day · Relaxed · Shows and dining | — | A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility. | `generateVisitPlan` body |
| Preset key `presetKey` | text field | optional | — | max length 64; pattern `^[a-z][a-zA-Z0-9]*$`; An unknown key is refused 422 `unknown-preset`. | — | The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan … | `generateVisitPlan` body |
| Start time `startTime` | time picker | optional | — | — | HH:mm, 24-hour | When the party arrives. Null means opening time. | `generateVisitPlan` body |
| Locale `locale` | text field | optional | — | — | — | — | `generateVisitPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**Ready-made plans** (card list, from `listProducts`): The venue's preset plans (e.g. *Thrill day*, *Family day*, *Relaxed day*), each a set of planner inputs; **Use this plan** runs `generateVisitPlan` with those inputs and the guest's party size and date. Rules-built, not AI: seeded, not learned, on day one.

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

**Every bundle** (data table, from `listCatalogueBundles`): Bundles a preset plan can include (e.g. Fast Track).

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Use this plan (primary button) | `generateVisitPlan` POST `/visit-plans` | VisitPlanRequest | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a … | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **preset card**: Name, the park, a one-line description, pace, the highlights (3 to 4 items), suitable ages or heights, and an estimated price per person. *(source: screens/P02-guest-mobile-app.yaml#GST-052 (Ready-made plans); DI-1112)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Use this plan**: Asks only party size and date (and heights if children), then builds the plan and opens Your Plan (GST-053). *(source: screens/P02-guest-mobile-app.yaml#GST-052 (Ready-made plans notes))*
- **Make my own**: Opens the six questions (GST-051). *(source: screens/P02-guest-mobile-app.yaml#GST-052 transitions)*

**Data it reads**: `listProducts` (onLoad, List products); `listCatalogueBundles` (onLoad, List published bundles)

**Where the user goes next**

- → `GST-053` Your Plan: *Use this plan*; carries `planId`; calls `generateVisitPlan`
- → `GST-051` Plan: *Make my own*
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | The venue has no ready-made plans: says so and offers *Make my own* (GST-051). |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 422 A venue of the plan (`venueId` or a `dayVenues` venue) has no published map, or none of its points carries a planning duration (`venue-not-plannable`), so … |

#### Edge cases to draw

- **A preset includes rides a child is too short for**: The plan leaves them out and says so ("Freefall Tower needs 1.40 m"). *(source: screens/P02-guest-mobile-app.yaml#GST-053 (Left out for your group))*

#### Consistency with other screens

- Match `GST-053`: The preset opens as an ordinary editable plan.
- Match `WEB-050`: The web planner has no presets; it asks the six questions.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
presets:
- name: Thrill day
  park: Summit Peaks
  pace: Packed
  highlights:
  - Freefall Tower
  - Summit Coaster
  - The Drop
  from: AED 410 pp with Fast Track
- name: Family day
  park: Summit Peaks
  pace: Balanced
  highlights:
  - Junior Circuit
  - Sunset Parade
  - Adventure Play Area
- name: Relaxed day
  park: Coastal Aqua
  pace: Relaxed
  highlights:
  - Lazy River
  - Cabana Row
  - Poolside Bar
```

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `generateVisitPlan` → no permission · guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-052` · status **notStarted** · provenance designed · **Drawn by Claude Code on 30 September 2026 in the Mobile App v4 look; not client-verified, awaiting the client's design reviewer.** `provenance: designed` because the accepted vocabulary has no …
- Prototype (Mobile App v4, 29 September 2026, verified —, match none): `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`, view **
- Drawn by: Claude Code, 30 September 2026, drawn in the Mobile App v4 look
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0028 *Seventeen modules, and the data boundary decides where they split* (`docs/adr/0028-service-decomposition.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Use this plan.
- [ ] Every transition is wired: `GST-053`, `GST-051`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-053` Your Plan

**The plan, day by day: swap, remove or add items, undo, add Fast Track, then book the whole plan.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18229 (APP-MOB-GST-053) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getCart` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `planId` (GST-051), `venueId` (session), `itemId` (navigation), `cartId` (session) · cold entry: A saved plan opened from a link or the Plan tab. A plan whose dates have passed says so and offers to plan again; a plan that is not this guest's is refused … |
| Route | `/general/build-your-own-itinerary` |

**What the spec says about it.** Minuted 10 Aug §4.9. **Group sharing agreed** — an in-app QR a friend scans to join the itinerary (Chinmay raised, Qossai confirmed). **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes audit R187, the deferral half of R209 and rev 3 GAP-C3; the `deferred` block is removed and the screen is wave 1. **Mobile v4 role (MOB-6): "Your Plan".** Per-day itinerary with swap, remove, add and undo (`updateVisitPlan` is versioned), add-ons such as Fast Track, and **Book this plan** → GST-041. **Multi-venue intelligence (client meeting 30 September, MoM 4.7, Allam).** Each day tab is one park, and every item on it (rides, dining, and now retail: shops and kiosks) is at that park; a preference the park cannot meet shows as *Not at this park* rather than being filled from another park.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Your Plan, day by day: swap, remove, add, undo, add Fast Track, then Book this plan. Block A. The 30 September rules: each day tab names its park and every item, swap and suggestion comes from that park only; retail shops and kiosks join dining as stops; a preference a park cannot meet is said in a "Not at this park" banner, never filled from another park.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Group sharing (in-app QR, agreed 10 August) is not drawn and no operation backs it. (CHG-SGU-024)

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is plan sharing by QR in the Block A planner?** → Drawn default accepted: Draw a Share button; leave it out of the build until confirmed. *(decided by Chinmay, 2026-10-02; DEC-112 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Day tabs | select field | — | — | — | — | Day 1 · Fri 2 Oct · Summit Peaks … one tab per chosen day; the park is the day's `VisitPlan.days[].venueId` (client meeting 30 September, MoM 4.7). | — |
| Add Fast Track | toggle | — | — | — | — | An add-on from the plan's `addOnSuggestions` (the product GST-048 sells), priced per guest, with the queuing time it saves. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Version | number field | — | min 1 | `getVisitPlan` ?version |

**Sent by *Remove*** (`updateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | — | `updateVisitPlan` body |
| Changes `changes` | repeatable rows | required | — | at least 1; at most 20 | — | — | `updateVisitPlan` body |
| Op `changes[].op` | select | required | — | Swap · Remove · Add · Move · PIN · Accept add on · Decline add on · Revert to | — | — | `updateVisitPlan` body |
| Item `changes[].itemId` | picker: choose an item | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Date `changes[].date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateVisitPlan` body |
| Point `changes[].pointId` | picker: choose a point | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Performance `changes[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Starts at `changes[].startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateVisitPlan` body |
| Version `changes[].version` | number field | optional | — | — | — | For `revertTo`, the earlier version to restore (undo). | `updateVisitPlan` body |

**Sent by *Book this plan*** (`bookVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | The version the guest is looking at. | `bookVisitPlan` body |
| Cart `cartId` | picker: choose a cart | optional | — | — | shows names, sends the id | The guest's open cart. Null creates one. | `bookVisitPlan` body |
| Items `itemIds` | multi-picker: choose items | optional | — | — | — | Only these items. Empty books every bookable item of every day. | `bookVisitPlan` body |
| Include add ons `includeAddOns` | toggle | optional | on | — | — | Also add the add-ons the guest accepted on the plan (`VisitPlanItem.addOnAccepted`). | `bookVisitPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**The day** (timeline, from `getVisitPlan`): Arrive, then each timed item (ride, show, lunch at a restaurant serving the chosen cuisine, a shop or kiosk stop) with its place and zone; Fast Track marked on the rides it covers. **Every item is at the day's park** (`VisitPlanItem.venueId`; client meeting 30 September, MoM 4.7): retail stops (`kind` `shop`: shops and retail kiosks) sit beside meals, both from that park's own points.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Left out for your group** (banner, from `getVisitPlan`): Items left out because of a child's height, with the limit (e.g. *Freefall Tower (needs 1.40 m)*), and a must-see at none of the chosen parks (`notAtVenue`).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Not at this park** (banner, from `getVisitPlan`): **Per day, what the day's park could not offer** (client meeting 30 September, MoM 4.7): e.g. *No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2).* Names the other park from `availableAtVenueIds`, or says no park has it. Lunch that day is at the park's best other restaurant, marked as such. Hidden when every preference is met.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Estimated total** (detail panel, from `getVisitPlan`): Estimated price for the group and days; the guest confirms dates and tickets in the basket.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**The wait time** (detail panel, from `getWaitTimes`): Live waits beside the rides on today's plan.

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Swap (secondary button) | `listVisitPlanAlternatives` GET `/visit-plans/{planId}/items/{itemId}/alternatives` | — | VisitPlanAlternative (paged) | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Remove (destructive button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| + Add something (secondary button) | `listVisitPlanAlternatives` GET `/visit-plans/{planId}/items/{itemId}/alternatives` | — | VisitPlanAlternative (paged) | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Undo changes (secondary button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| Book this plan (primary button) | `bookVisitPlan` POST `/visit-plans/{planId}/booking` | inline | VisitPlanBooking | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not current (`plan-version-conflict`), or the cart is not the caller's or is no longer open … | — |
| Refine with the AI planner (secondary button) | navigation or local | — | — | — | — |
| Change answers (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **day timeline**: Arrive, then timed rides and shows with their zone and walking time, lunch at a restaurant serving the chosen cuisine, shop or kiosk stops; Fast Track marked on the rides it covers; live waits next to today's rides. *(source: DI-1098; DI-1100; screens/P02-guest-mobile-app.yaml#GST-053 (The day))*
- **left out**: Items left out for a child's height with the limit; a must-see none of the chosen parks has. *(source: screens/P02-guest-mobile-app.yaml#GST-053 (Left out for your group))*
- **Not at this park**: Per day, names the cuisine or shop and the park that has it, or says no park has it; lunch is then the park's best other restaurant, marked as such. *(source: DI-1113; screens/P02-guest-mobile-app.yaml#GST-053 (Not at this park))*
- **estimated total**: For the group and days, labelled an estimate; confirmed in the basket. *(source: DI-1098 (associated costing))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Swap / Add / Remove / Undo**: A sheet of candidates that suit everyone, from that day's park; each change a new version, Undo goes back one; arrival and lunch cannot be removed. *(source: screens/P02-guest-mobile-app.yaml#GST-053 layout)*
- **Book this plan**: Tickets, Fast Track and meal combos as basket lines, then the basket (GST-041). *(source: contracts/satellite/venue-map.yaml#bookVisitPlan)*
- **Share**: An in-app QR a friend scans to join the plan. *(source: DI-241; DI-218)*
- **Refine with the AI planner**: Opens the chat (GST-054) when the venue has AI on; its suggestions also stay within the day's park. *(source: DI-1112)*

**Data it reads**: `getCart` (onLoad, The cart, priced and checked, right now With the guest …); `listProducts` (onLoad, List products); `getWaitTimes` (onLoad, Wait times across a venue); `getVisitPlan` (onLoad, The plan: days, timed items and add-on suggestions, at its …)

**Where the user goes next**

- → `GST-041` Checkout Entry: *Book this plan*; carries `cartId`; calls `bookVisitPlan`
- → `GST-054` AI Planner: *Refine with the AI planner*; carries `planId`
- → `GST-051` Plan: *Change answers*
- → `GST-048` Upsell / Cross-Sell: *More add-ons*; carries `cartId`
- → `GST-059` Plan in Progress: *On the day: follow the plan*; carries `planId`
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | No plan yet: offers the questions (GST-051) or a ready-made plan (GST-052). |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Preference not at venue (`?state=preferenceNotAtVenue`) | **A day whose park cannot meet a preference** (client meeting 30 September, MoM 4.7): the day is shown in full with the *Not at this park* banner naming the cuisine or shop and where it is instead; nothing from another park is placed. *Change answers* (GST-051) lets the guest move that day to the park that has it. An empty swap sheet says the day's park has no other option of that kind, not that none exists anywhere. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 409 `baseVersion` is not current (`plan-version-conflict`), or the cart is not the caller's or is no longer open (`cart-not-open`).; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … |

#### Consistency with other screens

- Match `WEB-050`: Same plan rules; the web has no AI chat.
- Match `GST-059`: The same plan followed on the day.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
day1: Day 1 · Fri 2 Oct · Summit Peaks
items:
- 09:30 Arrive · Main Gate
- 09:45 Summit Coaster · Fast Track · 5 min
- 11:00 Sky Swing
- 12:30 Lunch · The Crater Grill (Emirati)
- 14:00 Summit Store
- 16:00 Sunset Parade
banner: No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2).
estimate: Estimated AED 1,840 for 2 adults and 2 children
```

#### Permissions

- `getCart` → no permission · guest, partner, staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getWaitTimes` → no permission · guest, public
- `getVisitPlan` → no permission · guest
- `updateVisitPlan` → no permission · guest
- `listVisitPlanAlternatives` → no permission · guest
- `bookVisitPlan` → no permission · guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.9.2 | The system should provide a service to enable the dynamic composition of the shop cart. The system must provide back all the information in real time, such as the performance availabilities of an … | Ticketing Sales | CONTRACTED | `getCart` |
| 2.9.5 | The system should highlight conflicting times at different attractions when trying to purchase tickets in the same time-slot for one guest. For example, if a ticket for Golf 1 to 2 pm has been added … | Ticketing Sales | CONTRACTED | `getCart` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Retail/kiosk shops are added to the planner's venue-linked options alongside F&B (previously only F&B). *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1100)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- Itinerary planner (Yas Island planner reference): party composition (adults/children with height/age), visit dates, pace (packed/balanced/relaxed) and cuisine preferences feed an auto-generated, swappable multi-day itinerary with associated costing. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1098)*
- Itinerary group sharing: an in-app QR code a friend scans to join the itinerary (Chinmay raised, Qossai confirmed). *(agreed · MoM 10 Aug 2026, 4.9 · DI-241)*
- Chinmay: share an itinerary with a group via an in-app QR code a friend scans to join, or an invite-to-join. *(agreed · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-218)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-053` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Plan tab → the six questions → Make my plan (Your plan)*
- Flow F49 *A guest plans a day and follows it*, step 2: They swap, remove and add items, undo a change and add Fast Track. → **Every change is a new version**, so undo is one step back. Swap candidates suit everyone in the party.
- Flow F49 *A guest plans a day and follows it*, step 4: They choose Book this plan. → The plan and its add-ons become cart lines; the guest confirms dates and tickets in the basket.
- Flow F49 branch at step 4 (recoverable): when An item sold out after the plan was made., The basket is not built for that item; the guest is told which one and offered a swap, and the rest of the plan is kept.
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 409, 410, 422).
- [ ] Every output is drawn (91 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-053?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, preferenceNotAtVenue, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Swap, Remove, + Add something, Undo changes, Book this plan, Refine with the AI planner, Change answers.
- [ ] Every transition is wired: `GST-041`, `GST-054`, `GST-051`, `GST-048`, `GST-059`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `GST-054` AI Planner

**Ask the planner in your own words to change the plan; it refines the rules plan, and the rules plan stays if AI is unavailable.**

| | |
|---|---|
| App · platform | TICVAI Guest · P02 Guest App (mobile) |
| Module | Engagement & Support · wave 1 · needs the `ai` module |
| Block | Block A · ticket #18217 (APP-MOB-GST-054) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest phone app, 390 x 844, in the venue's brand, with the v4 tab bar (Home, Explore, Plan, Tickets) and the Buy tickets button. · LTR and RTL · the venue's theme |
| Pattern | listDetail (comfortable density): `listProducts` reads the population and `getWaitTimes` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `planId` (GST-053), `conversationId` (deepLink), `venueId` (session) · cold entry: A planner link from a notification: opens the plan and its conversation, or the plan alone if the conversation was closed. |
| Route | `/general/ai-optimized-itinerary` |

**What the spec says about it.** Minuted 10 Aug §4.9. **The AI half is Wave 2** — the manual planner must work without it (CF-41). **Guest concierge confirmed in Phase 1 on 17 August (CF-14), charged per token and bounded by `AiPolicy.guestCapabilityScope`.** Still degrades to the manual planner rather than to an error. ** wired 24 August.** The board drew four bespoke AI endpoints for itinerary planning; **one operation with a kind answers all of them** (ADR-0028), and recording the outcome is what lets a model replace the heuristic later. **`recordSuggestionOutcome` removed from the guest surface.** `check-screens` refused it and was right: **a guest does not record an outcome — the platform observes what they did.** A guest app that self-reports whether it took the advice is a training label the guest could forge, and the observation belongs server-side where the plan and the visit can be compared. **Out of the first release** (decided 28 September, audit R187): the itinerary planner is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for the release that builds it. **Itinerary suggestion removed 28 September** (decided 28 September, audit R209): the planner is deferred (R187) and `requestSuggestion` refuses a guest anything but prepPlan, upsell and waitTime, so this screen no longer asks for a day plan. **Rev 3 (decided 29 September).** Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below. **Brought into Block A on 29 September** (Chinmay, the 29 September re-plan, MOB-6): a rules-based planner with the AI planner agent on top. This supersedes …

**From the AI & Intelligence process.** The AI planner: on the Plan tab, the guest asks in their own words to change the rules-built day plan ("less walking", "lunch near the wave pool", "add a show after 4") and the planner agent proposes a change the guest applies as a new plan version. The rules plan always stands on its own - with AI off, failing or unlicensed the guest keeps the plan and edits it by hand. The one thing to get right: the agent proposes, the guest applies; every applied change can be undone, and nothing is booked or paid from here.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The AI review (30 Sep §8) says ai.yaml has no planner operation and GST-054 is deferred. (CHG-SGU-025)
- The 30 September tracker says retail and kiosks are to be added to the planner. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): createAiConversation is triggered onLoad. (CHG-SGU-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does each applied AI change show what it cost or saves (e.g. a fast pass it added)?** → Drawn default stands (answer: "Default / recommended accepted"): An item that costs money shows its price on the proposal and is added to the cart only when the guest books the plan. *(decided by Chinmay, 2026-10-02; DEC-014 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Version | number field | — | min 1 | `getVisitPlan` ?version |

**Sent by *Apply this change*** (`updateVisitPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Base version `baseVersion` | number field | required | — | min 1 | — | — | `updateVisitPlan` body |
| Changes `changes` | repeatable rows | required | — | at least 1; at most 20 | — | — | `updateVisitPlan` body |
| Op `changes[].op` | select | required | — | Swap · Remove · Add · Move · PIN · Accept add on · Decline add on · Revert to | — | — | `updateVisitPlan` body |
| Item `changes[].itemId` | picker: choose an item | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Date `changes[].date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateVisitPlan` body |
| Point `changes[].pointId` | picker: choose a point | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Performance `changes[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `updateVisitPlan` body |
| Starts at `changes[].startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateVisitPlan` body |
| Version `changes[].version` | number field | optional | — | — | — | For `revertTo`, the earlier version to restore (undo). | `updateVisitPlan` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **request (chat)**: A chat input with example requests on first open ("Fewer queues", "We have a 4-year-old", "Indian food for lunch", "Finish by 5 pm"). The party, dates and pace from GST-053 are context, not re-asked. *(source: screens/P02-guest-mobile-app.yaml#GST-054 (states.emptyFirstRun) / DI-1021)*

#### Outputs: what the screen shows and produces

**Shown**

**Your plan** (timeline, from `getVisitPlan`): The current plan version, updated as the agent changes it.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**Ask the planner** (assistant panel, from `sendAiMessage`): e.g. *More shows, fewer coasters on day 2*. The agent calls `requestSuggestion` kind `itinerary` and applies the result with `updateVisitPlan`; Undo on GST-053 reverts it. **Grounded in each day's park** (client meeting 30 September, MoM 4.7): it proposes only rides, dining and shops (kiosks included) that the plan operations return for that day's venue; asked for something the park lacks …

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Role | chip: User, Assistant, System | — |
| Content | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Kind | chip: Document, Product, Entitlement, Report, Record | — |
| ID | text | — |
| Title | text | — |
| Collection | the name it points at, never the id | — |
| Excerpt | text | — |
| Relevance | 1,234.5 | — |
| Confidence | 1,234.5 | 8.1.5, 8.3.67. Nullable on purpose — a provider that does not report confidence must yield null rather than an invented number, and an … |
| Rationale | text | 8.3.68, 8.3.69. |
| Proposed action | grouped details | Present where the answer suggests a change. A draft, never applied here. |
| ID | the name it points at, never the id | — |
| Interaction | the name it points at, never the id | — |
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |
| Payload | grouped details | The request body a person would submit, ready to review. Open on purpose: its shape is the request body of `targetOperation` in … |

**Planner unavailable** (banner, from `getVisitPlan`): **The rules plan never fails over to an error**: with AI off, not licensed or failing, the guest keeps the rules plan and the Plan tab works in full. Shown when AI is off for the venue, the tenant has no AI licence, or the call fails or times out.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Subject | the name it points at, never the id | The signed-in guest. From the session, never from the body. |
| Session ref | text | The anonymous device session that owns the plan until sign-in. |
| Status | chip: Draft, Booked, Archived | `booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date. |
| Source | chip: Rules, Preset, AI agent | What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. |
| Inputs | grouped details | What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050. |
| Venue | the name it points at, never the id | The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. |
| Day venues | list or chips (count when long) | Which venue on which date, in a multi-venue tenant (30 September client meeting, MoM 4.7, Allam's requirement). |
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Dates | list or chips (count when long) | — |
| Party | list or chips (count when long) | One entry per person. Height where the guest knows it, age otherwise: height is what ride eligibility rules test, and an age band is the … |
| Height cm | 1,234 | — |
| Age years | 1,234 | — |
| Pace | chip: Packed, Relaxed | — |
| Interest tags | list or chips (count when long) | The same closed list as `VenuePoint.interestTags`. |
| Cuisine tags | list or chips (count when long) | Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). |
| Retail tags | list or chips (count when long) | Shops the party would like to visit (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner … |
| Must include points | list or chips (count when long) | Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never … |

**The wait time** (detail panel, from `getWaitTimes`): Live waits the agent plans around.

| Shows | Format | Notes |
|---|---|---|
| Queue | the name it points at, never the id | — |
| Queue name | in the reader's language | — |
| Attraction product | the name it points at, never the id | — |
| Attraction category | the name it points at, never the id | The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Source | chip: Sensor, Throughput, Manual, Unavailable | Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Apply this change (primary button) | `updateVisitPlan` PUT `/visit-plans/{planId}` | VisitPlanUpdate | VisitPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` … | — |
| Back to your plan (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **proposed change**: Shown as a before/after on the day timeline (items swapped, moved, removed or added highlighted), with one line why and the new wait-time estimates; "Apply this change" commits it, "Not this" leaves the plan untouched. *(source: contracts/satellite/venue-map.yaml#updateVisitPlan / contracts/satellite/ai.yaml#requestSuggestion (kind itinerary))*
- **"Not at this park" banner**: A preference the day's park cannot meet is said, not filled: e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)." Every suggested ride, dining or retail point (shops and kiosks included) comes from that day's park only. *(source: DI-1112 / DI-1113 / DI-1099 / MoM 30 Sep 4.7)*
- **wait times on the plan**: Each ride shows "about 20 min" with its basis on tap; estimates are labelled estimates. *(source: contracts/satellite/queue.yaml#getWaitTimes)*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Apply this change**: Writes a new plan version (updateVisitPlan with baseVersion); the timeline re-lays and an Undo appears. 409 (the plan changed elsewhere) reloads and re-proposes; 422 point-not-at-day-venue is never shown to the guest - the agent simply does not propose it. *(source: contracts/satellite/venue-map.yaml#updateVisitPlan / screens/P02-guest-mobile-app.yaml#GST-054 (notes, grounding))*
- **Back to your plan**: Returns to GST-053 with the current version. *(source: screens/P02-guest-mobile-app.yaml#GST-054)*

**Data it reads**: `getWaitTimes` (onLoad, Wait times across a venue); `getVisitPlan` (onLoad, The plan: days, timed items and add-on suggestions, at its …)

**Where the user goes next**

- → `GST-053` Your Plan: *Back to your plan*; carries `planId`
- → `GST-059` Plan in Progress: *They follow it through the day*; carries `planId`
- → `GST-001` Home: *Home tab*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The plan builds in place; the inputs stay on screen. |
| Error (`?state=error`) | Could not load the plan. Names what failed; the inputs are kept so trying again costs nothing. |
| Empty, first run (`?state=emptyFirstRun`) | No conversation yet: the plan is shown with example requests. |
| Empty, no results (`?state=emptyNoResults`) | Nothing suits the whole party on that day (for example every ride is over a child's height): says so and offers to change the answers. |
| Permission denied (`?state=emptyNoAccess`) | A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it. |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| AI unavailable (`?state=aiUnavailable`) | **Falls back to the rules plan, never to an error** (MOB-6): the plan from `getVisitPlan` stays on screen with a short note, and the guest carries on editing it on GST-053. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `baseVersion` is not the current version (`plan-version-conflict`), or the plan is already `booked` (`plan-booked`; a booked plan is read-only, generate a new …; 422 A change names an item not on the plan, a `revertTo` version that does not exist, or a point the party is not eligible for (`item-not-eligible`, with the rule …; 422 A setting the answer cannot do without is missing (29 … |
| In progress (`plannerMode`) | starts at *rulesPlan*; *rulesPlan*: The rules plan is shown; the chat is open.; *refining*: The agent is working on a request.; *proposed*: A change is proposed, not yet saved.; *aiUnavailable*: **The rules plan never fails over to an error**: with AI off, not licensed or failing, the guest keeps the rules plan … |

#### Edge cases to draw

- **AI unavailable, paused, over budget or not licensed**: The plan stays on screen with a short note "The planner can't chat right now - you can still edit your plan" and the manual edit controls; never an error page. *(source: screens/P02-guest-mobile-app.yaml#GST-054 (states.aiUnavailable) / ADR-0059)*
- **Nothing suits the whole party (e.g. every ride over a child's height)**: Says so and offers to change the answers. *(source: screens/P02-guest-mobile-app.yaml#GST-054 (states.emptyNoResults))*
- **The guest asks the planner to book or pay**: The agent may prepare the booking but the guest must press Book in the app; it never checks out. *(source: screens/P02-guest-mobile-app.yaml#GST-054 (planner tool notes in ai.yaml: bookVisitPlan requiresGuestConfirmation))*
- **Signed-out guest**: Can chat and build a plan; asked to sign in only to save or book. *(source: screens/P02-guest-mobile-app.yaml#GST-054 (states.emptyNoAccess))*

#### Consistency with other screens

- Match `GST-053`: The rules plan screen (ticketing-guest process); same timeline component, same Undo and version history.
- Match `GST-031`: Same assistant bubbles and Sahli identity; the planner is Sahli in planning mode, not a second persona.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Summit Peaks (day 1), Aqua Park (day 2)
party: 2 adults, 2 children (6 and 4, 105 cm)
request: We want lunch near the wave pool and fewer queues after 2 pm
proposal:
- Move Wave Rider to 10:15 (about 10 min wait, was 35)
- Lunch at Lagoon Grill 12:30, next to the wave pool
- Swap Twister Tubes (min 120 cm) for Lazy River at 14:30
banner: No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2).
```

#### Permissions

- `getWaitTimes` → no permission · guest, public
- `sendAiMessage` → `AI_USE` (operate) · staff, guest
- `getVisitPlan` → no permission · guest
- `updateVisitPlan` → no permission · guest
- `createAiConversation` → `AI_USE` (operate) · staff, guest
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** A guest holds no permission. A plan that is not theirs says so without saying whose it is; a signed-out guest can still build a plan and is asked to sign in only to save or book it.

#### Requirements it meets

29 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| … 17 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A preference a day's park cannot meet is said, not filled: a "Not at this park" banner per day names the cuisine or shop and the park that has it (e.g. "No Indian restaurant at Summit Peaks. Indian food is at Aqua Park (day 2)."), hidden when all are met. Lunch cuisine options name the parks serving them ("Indian - Summit Peaks only"). *(agreed · MoM 30 Sep 2026, 4.7 · DI-1113)*
- Allam: multi-venue visit planner. In a multi-venue tenant the guest picks a park per chosen day ("Which park each day?", hidden otherwise); each day tab names its park and every item, swap candidate and AI-planner suggestion comes only from that park's rides, dining and shops, never another park's. *(agreed · MoM 30 Sep 2026, 4.7 · DI-1112)*
- Allam: the planner applies multi-venue intelligence; it checks actual venue-level amenities before including a preference, e.g. if only one of several parks has an Indian restaurant. It pulls only rides, F&B and retail available at each specific venue. *(agreed · MoM 30 Sep 2026, 4.7 Mobile App — Itinerary Planner & Multi-Venue Intelligence · DI-1099)*
- "Plan Your Adventure": guided itinerary planner (Skidata benchmark) where the guest picks which rides/attractions and in what order ahead of time, tied to the ticket purchase and saved as a personal visit profile. *(client request · MoM 10 Aug 2026, 4.9 "Plan Your Adventure" (Itinerary Planner) · DI-217)*

Also apply: 41 for all of P02, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · names this screen)*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P02 Guest App.dc.html#gst-054` · status **notStarted** · provenance client-verified
- Prototype (mobile v4 (30 September build), verified 2026-10-01, match partial): `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`, view *Ask Sahli (the assistant chat; v4 has no plan-specific chat)*. Differences: v4 draws the rules plan and a general assistant chat; it has no plan-specific chat. Built from this definition.
- Flow F49 *A guest plans a day and follows it*, step 3: They ask the AI planner to change the plan in their own words. → **The agent refines the rules plan** through the plan operations (`requestSuggestion` kind `itinerary`, guest-allowed since 29 September). With AI off or failing the rules plan stays.
- Flow F49 branch at step 3 (recoverable): when AI is off for the venue, not licensed, or the call fails or times out., **Falls back to the rules plan, never to an error.** The planner chat says it is unavailable; everything on GST-053 keeps working.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)
- ADR-0028 *Seventeen modules, and the data boundary decides where they split* (`docs/adr/0028-service-decomposition.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (71 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#GST-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, aiUnavailable.
- [ ] Every action is wired with its success and its failure: Apply this change, Back to your plan.
- [ ] Every transition is wired: `GST-053`, `GST-059`, `GST-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 4 edge case(s) from the process notes are drawn.
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

**P02 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html`: Mobile App v4, the newest guest look (29 September, with the 30 September feedback in the booking flows). It replaces the 28 September Mobile v2 build.
- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the booking engine that runs inside the app. Keep both files in the same folder.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P02 as a whole** (30: 3 open, 27 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- … 16 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P02 Guest App

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- Products can be presented in multiple card layout styles: carousel, video poster, split, etc. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1089)*
- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- The revised mobile app design is approved in direction: Qossai liked the opening video and visual polish, Allam the UI/graphics quality. Its flow is deliberately different from the web application (after front-end team input), not a reused structure. Detailed feedback to follow. *(agreed · MoM 30 Sep 2026, 4.4 Guest Mobile App — Revised Design Walkthrough · DI-1086)*
- Every web product and flow stays bookable in the mobile app (incl. cabanas, surf, 2D/3D stadium, theatre plan, bus route map), each with its own step order; a toggle switches back to one decision per screen. *(agreed · design review 29 Sep 2026, Mobile app (v4) — All web products and flows available · DI-1084)*
- Mobile app must not open straight into booking (client found it unclear). Tabs: Home · Explore · Plan · Tickets (Yas Island / Six Flags references), with a persistent "Buy tickets" button on every screen (raised centre button, or floating / flat per venue). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tabs Home · Explore · Plan · Tickets, persistent Buy tickets · DI-1081)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Optional intro video on opening the app, with a "Skip introduction" control. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1020)*
- A persistent "Buy tickets" button appears on every screen of the mobile app. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1017)*
- Mobile tabs: Home, Explore, Plan, Tickets (Yas Island / Six Flags references). *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1016)*
- The current mobile build goes straight into the booking journey and the client finds it unclear: redesign the UI. All web products and flows, including cabanas and surf, must remain available. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1015)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Accreditation is primarily completed in the web portal (document upload and photo checks suit a larger screen); the same submission is also available in the guest mobile app as a secondary option for individuals. *(agreed · MoM 7 Sep 2026, 4.8 Accreditation Channel Placement & API Access · DI-666)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

**37 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"bookVisitPlan": {"method":"POST","path":"/visit-plans/{planId}/booking","contract":"venue-map","summary":"Book this plan — turn it into cart lines","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VisitPlanBooking"},
"checkoutCart": {"method":"POST","path":"/carts/{cartId}/checkout","contract":"orders","summary":"Turn the cart into an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"createAiConversation": {"method":"POST","path":"/conversations","contract":"ai","summary":"Open a conversation","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConversation"},
"createGuestFnbOrder": {"method":"POST","path":"/guest-orders","contract":"fnb","summary":"A guest orders food","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGuestOrderRequest","responds":"GuestOrderResult"},
"generateVisitPlan": {"method":"POST","path":"/visit-plans","contract":"venue-map","summary":"Build a visit plan from the party, the dates and what they like","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisitPlanRequest","responds":"VisitPlan"},
"getCart": {"method":"GET","path":"/carts/{cartId}","contract":"orders","summary":"The cart, priced and checked, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getForm": {"method":"GET","path":"/forms/{formId}","contract":"marketing-crm","summary":"One form, to fill in or to edit","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"FormDefinition"},
"getGuestMenu": {"method":"GET","path":"/outlets/{outletId}/guest-menu","contract":"fnb","summary":"The menu a guest sees","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"at","in":"query","required":null},{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"GuestMenu"},
"getGuestOrderStatus": {"method":"GET","path":"/guest-orders/{orderId}","contract":"fnb","summary":"Track an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestOrderStatus"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getVisitPlan": {"method":"GET","path":"/visit-plans/{planId}","contract":"venue-map","summary":"A visit plan, at its current version or an earlier one","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"VisitPlan"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"handoverToAgent": {"method":"POST","path":"/conversations/{conversationId}/handover","contract":"marketing-crm","summary":"Pass an assistant conversation to a person","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Conversation"},
"listAiConversations": {"method":"GET","path":"/conversations","contract":"ai","summary":"A principal's conversation history","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listMyCases": {"method":"GET","path":"/my/cases","contract":"marketing-crm","summary":"The cases this guest raised","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyNotifications": {"method":"GET","path":"/me/notifications","contract":"marketing-crm","summary":"The signed-in guest's notification feed","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":"unreadOnly","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"Page"},
"listMyOrders": {"method":"GET","path":"/my/orders","contract":"orders","summary":"The orders this guest placed","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"since","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedContentPages": {"method":"GET","path":"/storefront/pages","contract":"white-label","summary":"The live content pages, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"categoryCode","in":"query","required":false},{"name":"slug","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPublishedFaqs": {"method":"GET","path":"/storefront/faqs","contract":"white-label","summary":"The published FAQs, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PublishedFaqCategory"},
"listPublishedPolicies": {"method":"GET","path":"/storefront/policies","contract":"white-label","summary":"The tenant's current legal policies, readable before sign-in","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"kind","in":"query","required":false}],"requestBody":null,"responds":"PublishedPolicy"},
"listVisitPlanAlternatives": {"method":"GET","path":"/visit-plans/{planId}/items/{itemId}/alternatives","contract":"venue-map","summary":"What could take this item's place","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"markMyNotificationsRead": {"method":"POST","path":"/me/notifications/read","contract":"marketing-crm","summary":"Mark the signed-in guest's notifications read","permission":null,"offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"raiseMyCase": {"method":"POST","path":"/my/cases","contract":"marketing-crm","summary":"Report something — lost property, a complaint, a question","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Case"},
"recordAnswerFeedback": {"method":"POST","path":"/messages/{messageId}/feedback","contract":"ai","summary":"Say whether an answer helped","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAnswerFeedback"},
"replyToMyCase": {"method":"POST","path":"/my/cases/{caseId}/messages","contract":"marketing-crm","summary":"Reply on a case the guest raised","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CaseDetail"},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"sendConversationMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"marketing-crm","summary":"Say something, as a guest or an agent","permission":"CASE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConversationMessage"},
"submitForm": {"method":"POST","path":"/form-submissions","contract":"marketing-crm","summary":"Sign a waiver, answer a survey, capture details","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FormSubmission","responds":"FormSubmission"},
"submitReview": {"method":"POST","path":"/reviews","contract":"marketing-crm","summary":"Submit a review","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitReviewRequest","responds":"Review"},
"updateVisitPlan": {"method":"PUT","path":"/visit-plans/{planId}","contract":"venue-map","summary":"Swap, remove, add, move or undo, as a new version","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisitPlanUpdate","responds":"VisitPlan"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"AiAnswerFeedback": {"type":"object","x-ticvai-persistence":"ai.answer_feedback","description":"**What a person thought of an answer** (AIC-062). One label per message per person; it feeds the golden sets and the knowledge-gap list, never an online update (design 3.5).","required":["messageId","rating"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"messageId":{"type":"string","format":"uuid","x-ticvai-references":"ai.message"},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"rating":{"type":"string","enum":["helpful","notHelpful"]},"reason":{"type":"string","enum":["wrong","outdated","incomplete","notGrounded","unsafe","other"],"nullable":true},"comment":{"type":"string","nullable":true,"maxLength":1000},"audience":{"type":"string","enum":["staff","guest"],"readOnly":true},"principalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest, where the audience is `guest`."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConversation": {"type":"object","x-ticvai-persistence":"ai.conversation","required":["id","principalId","module","startedAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"locale":{"type":"string"},"messageCount":{"type":"integer"},"startedAt":{"type":"string","format":"date-time"},"lastMessageAt":{"type":"string","format":"date-time"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE and then the in-cell open-weights model as the fallback chain. OpenAI UAE is `openai` with a UAE `endpoint`; the in-cell model is `localLlm`.\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"Case": {"x-ticvai-persistence":"marketing.case","x-ticvai-retired-columns":["guest_name","subject","is_sla_breached"],"type":"object","required":["id","caseNumber","subject","status","priority","createdAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Created on the device (`CreateCaseRequest.id`, `raiseMyCase`), so a UUIDv7."},"caseNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity. Assigned when the case reaches the server, so a retry with the same `id` keeps its number.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"**Resolved from `pii.subject` when the case is read, never stored on the case.** A name copied onto a case row is personal data outside the erasable store (ADR-0023), and it had no source anyway — no request carries it. Returned only to callers holding `GUEST_VIEW_PII`, as `searchGuests` does.\n"},"subject":{"type":"string","x-ticvai-column":"title","description":"**The case's one-line title**, not a person. Stored as `title` so the table does not hold `subject` beside `subject_id`; the wire keeps `subject` because screens bind it.\n"},"kind":{"allOf":[{"$ref":"#/components/schemas/CaseKind"}],"nullable":true,"description":"What the guest said it was about, where the guest raised it."},"channel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"description":"How the guest reached the venue — `CreateCaseRequest.channel`, or `inApp` for a case raised through `raiseMyCase`."},"recordedAt":{"type":"string","format":"date-time","description":"Device time the case was raised — the start of the SLA clock."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the case arrived. Equal to `recordedAt` for a case raised online."},"categoryId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The `ServiceQueue` the case waits in, set by routing (`CaseRoutingRule.queueId`). Null once routed straight to an agent. (decided 29 September, data model for the agreed operations)"},"membershipId":{"type":"string","format":"uuid","nullable":true,"description":"The identity membership this case concerns (`identity.customer_membership`); member case notes are cases with this set. (decided 29 September, coordinator decision DM4, writers pass)"},"status":{"$ref":"#/components/schemas/CaseStatus"},"priority":{"$ref":"#/components/schemas/CasePriority"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"relatedOrderId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"isSlaBreached":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"**Computed when read, never stored.** True once the case has been open longer than its SLA allows — the time from `recordedAt` to `resolvedAt` (or to now, while unresolved), less `slaPausedSeconds`, is past the target that set `slaDueAt`. A stored flag would need a job to flip it at the moment of breach, and no such job is designed; `listCases?breachedSla` filters on the same computation.\n"},"slaPausedSeconds":{"type":"integer","description":"Accrued only while awaiting the guest. Waiting on an internal team does not pause the clock.\n"},"escalationCount":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"CaseDetail": {"x-ticvai-persistence":"marketing.case","allOf":[{"$ref":"#/components/schemas/Case"},{"type":"object","properties":{"description":{"type":"string"},"resolutionNote":{"type":"string","nullable":true},"messages":{"type":"array","items":{"$ref":"#/components/schemas/CaseMessage"}}}}]},
"CaseKind": {"type":"string","description":"**What the guest says the case is about**, in their words rather than the venue's taxonomy — `raiseMyCase` asks for it and `categoryId` is what staff file it under. Stored on the case, because a lost-property report that forgets it was one cannot be routed to the lost and found desk.\n**`other` only with a note (decided 28 September, audit R222).** A case raised as `other` must carry a non-empty `detail` (`raiseMyCase`), or it is refused with 400; the notes are reviewed quarterly to add the real kinds they reveal.\n","enum":["lostProperty","complaint","question","accessibility","refundRequest","other"]},
"CaseMessage": {"x-ticvai-persistence":"marketing.case_message","type":"object","required":["id","body","isInternal","authorKind","recordedAt"],"properties":{"resolution":{"type":"string","description":"**What was actually done about it.** Indexed for retrieval: an agent facing a complaint benefits more from how the last one was resolved than from a policy. Without this column `marketing.case` can only embed its subject line.\n"},"id":{"type":"string"},"body":{"type":"string"},"isInternal":{"type":"boolean"},"authorKind":{"type":"string","enum":["agent","guest","system","ai"]},"authorPrincipalId":{"type":"string","format":"uuid","nullable":true},"channel":{"$ref":"#/components/schemas/MessageChannel"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time","description":"Device time — `addCaseMessage` is offline-capable."},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the message arrived."}}},
"CasePriority": {"type":"string","enum":["low","normal","high","urgent"]},
"CaseStatus": {"type":"string","enum":["open","inProgress","awaitingGuest","escalated","resolved","closed"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"Conversation": {"type":"object","x-ticvai-persistence":"marketing.conversation","description":"22.8. **A conversation is not a case.** A case is a ticket measured in hours; a conversation is a live session measured in seconds, with somebody waiting. A conversation may create a case; it is not one.\n","required":["id","channel","state"],"properties":{"id":{"type":"string","format":"uuid"},"telephony":{"type":"object","nullable":true,"description":"BL-083. **`ConversationChannel` included `voice` with nothing behind it** — the model anticipated telephony and stopped at the enum.\n**Not an integration, a binding.** Genesys, Avaya, Amazon Connect, Teams and 3CX all do call control themselves; what the platform needs is the call bound to the guest and the case, so **an agent who answers already knows who is calling and what about.**\n","properties":{"providerCallId":{"type":"string"},"direction":{"type":"string","enum":["inbound","outbound","transferred"]},"fromNumberMasked":{"type":"string","nullable":true,"description":"**Masked, and it is still personal data.** A phone number identifies a person more reliably than a name does.\n"},"recordingRef":{"type":"string","nullable":true,"description":"Held by the provider, referenced here. **Recording consent is jurisdictional and the platform does not assume it** — a reference with no consent record is a recording nobody may play.\n"},"agentState":{"type":"string","enum":["available","onCall","wrapUp","away","offline"],"nullable":true}}},"assistSessionId":{"type":"string","format":"uuid","nullable":true,"description":"BL-094. **`startKioskAssist` recorded a staff member helping a guest and `createCase` recorded a service interaction, and neither referenced the other** — so the traceability 2.13.20 asks for had no link to follow.\n**The link is here rather than on the assist session**, because a case may span several assists and an assist belongs to at most one case.\n"},"channel":{"$ref":"#/components/schemas/ConversationChannel"},"state":{"$ref":"#/components/schemas/ConversationState"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.3. Resolved from phone, email, membership number or a signed-in session. **A conversation with none of those stays anonymous rather than being guessed at.**\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"assignedPrincipalId":{"type":"string","format":"uuid","nullable":true},"queueId":{"type":"string","format":"uuid","nullable":true},"queuePosition":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"Place among the unclaimed conversations in `queueId`, from the live agent queue (audit R149). Null once claimed."},"estimatedWaitSeconds":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onRead","description":"From the live agent queue — the conversations ahead divided across that queue's agents online now (audit R149). Null once claimed."},"handoverReason":{"type":"string","nullable":true,"enum":["guestRequested","assistantRefused","assistantFailed","outOfScope","negativeSentiment","complexIntent","paymentIssue"]},"handoverSummary":{"type":"string","nullable":true,"description":"**The assistant's own account of what the guest wants**, so an agent opens with context rather than reading a transcript while somebody waits.\n"},"sentiment":{"type":"string","nullable":true,"enum":["positive","neutral","negative","escalating"],"description":"22.8.16. **`escalating` is a routing signal**, not a report line."},"intent":{"type":"string","nullable":true,"description":"22.8.13. What the guest appears to want, used for routing."},"locale":{"type":"string"},"caseId":{"type":"string","format":"uuid","nullable":true,"description":"22.8.12. Where the conversation raised one."},"messages":{"type":"array","items":{"$ref":"#/components/schemas/ConversationMessage"}},"firstResponseSeconds":{"type":"integer","nullable":true,"readOnly":true},"startedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"outcome":{"type":"string","nullable":true,"enum":["resolved","caseRaised","abandonedByGuest","timedOut","spam"]}}},
"ConversationChannel": {"type":"string","enum":["webChat","inAppChat","whatsapp","sms","email","kiosk","voice"]},
"ConversationMessage": {"type":"object","x-ticvai-persistence":"marketing.conversation_message + marketing.conversation_message_attachment","required":["id","sender","body","sentAt"],"properties":{"id":{"type":"string","format":"uuid"},"sender":{"type":"string","enum":["guest","agent","assistant","system"],"description":"**Resolved, never declared.** The assistant is labelled as one — a guest talking to a bot that presents as a person is a complaint waiting for the moment they find out.\n"},"senderPrincipalId":{"type":"string","format":"uuid","nullable":true},"body":{"type":"string"},"attachments":{"type":"array","items":{"type":"object","properties":{"assetId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["image","video","document","ticket","qr","paymentLink"]}}}},"aiInteractionId":{"type":"string","format":"uuid","nullable":true,"description":"Where the assistant sent it. **Links the message to its tokens and cost**, so a conversation's spend is attributable (CF-14).\n"},"sentAt":{"type":"string","format":"date-time"},"readAt":{"type":"string","format":"date-time","nullable":true}}},
"ConversationState": {"type":"string","description":"**`withAssistant` and `queued` are different, and the second has a person waiting.** Merging them makes the service level unmeasurable, because time with a bot is not time in a queue.\n","enum":["withAssistant","queued","withAgent","waitingOnGuest","resolved","abandoned","timedOut"]},
"CreateGuestOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1,"maximum":20},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket.\n"}}},
"CreateGuestOrderRequest": {"type":"object","required":["id","lines","quotedTotal","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationSessionId":{"type":"string","format":"uuid","nullable":true,"description":"From `claimLocationSession`. Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"Required for collection. Ignored where a location session is supplied — the session names its outlet."},"fulfilment":{"allOf":[{"$ref":"#/components/schemas/GuestOrderFulfilment"}],"nullable":true,"description":"Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`."},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateGuestOrderLine"}},"quotedTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction.\n"},"paymentMethod":{"type":"string","enum":["card","wallet","roomCharge","addToTab"]},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"FormDefinition": {"type":"object","x-ticvai-persistence":"marketing.form_definition + marketing.form_definition_field","description":"CF-129, CL-04. **A waiver, a survey and a data-capture form are one mechanism.**\nA waiver is this form with a signature. A survey is this form with a scale. A demographic capture is this form at the point of sale. They were raised as three separate gaps and share every part: field configuration, conditional display, versioning, an acceptance record and a stored artefact.\n**Three implementations would drift on the version rule first.** A waiver signed against version 3 must stay bound to version 3, and that is the same requirement a survey has when question wording changes mid-campaign — **an NPS score means nothing if you cannot say which question produced it.**\n","required":["id","name","kind","version","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["waiver","survey","dataCapture","consentForm","incidentReport","registration"]},"consentPurposes":{"type":"array","description":"**What a `consentForm` consents to** (Chinmay, 2 October, batch 4; follows BO-188: biometric capture needs consent on the venue's own form; CHG-CSA-026). A guardian-signed form for a minor carries the guardian fields of the waiver builder (workbook Q237: guardian consent, configurable per country). Empty for any other kind.","items":{"type":"string","enum":["facePass","faceTag","marketing","photography","waiver"]}},"version":{"readOnly":true,"type":"integer","description":"**Set by the server** — 1 on `createForm`, the next number on every change. **Immutable once anything is submitted against it.** A change creates a new version, and the old one stays readable forever — 2.15.13 requires the exact accepted version retained, which is legal evidence rather than a nicety.\n"},"fields":{"type":"array","items":{"$ref":"#/components/schemas/FormField"}},"requiresSignature":{"type":"boolean","default":false,"description":"**What makes it a waiver.** And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it.\n"},"signatureKind":{"type":"string","enum":["drawn","typed","checkbox","none"],"default":"none"},"scoreScale":{"type":"string","nullable":true,"enum":["nps","csat","ces","likert5","likert7","stars"],"description":"**What makes it a survey.** Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's.\n"},"appliesToProductIds":{"type":"array","items":{"type":"string","format":"uuid"}},"validForMonths":{"type":"integer","nullable":true,"description":"**How long an acceptance lasts.** A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry is stated.\n"},"minimumAge":{"type":"integer","nullable":true},"requiresGuardianForMinors":{"type":"boolean","default":true,"description":"**A minor cannot waive their own rights.** A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters.\n"},"status":{"readOnly":true,"type":"string","enum":["draft","published","superseded","retired"]},"legalReviewedBy":{"type":"string","nullable":true},"legalReviewedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"FormField": {"type":"object","description":"One field. **Conditional display is the shared requirement** — a survey branching on an answer and a waiver revealing a medical question on a yes are the same mechanism.\n","required":["key","label","type"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"labelLocalised":{"type":"object","additionalProperties":{"type":"string"}},"type":{"type":"string","enum":["text","longText","number","date","select","multiSelect","boolean","scale","signature","file","phone","email"]},"options":{"type":"array","items":{"type":"string"}},"isRequired":{"type":"boolean","default":false},"isPersonalData":{"type":"boolean","default":false,"description":"**Marked at the field, because retention is decided at the field.** A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the whole thing as sensitive as its most sensitive field.\n"},"consentPurposeId":{"type":"string","format":"uuid","nullable":true},"showWhen":{"type":"object","nullable":true,"properties":{"field":{"type":"string"},"equals":{"type":"string"}}}}},
"FormSubmission": {"type":"object","x-ticvai-persistence":"marketing.form_submission","description":"**The acceptance record, and it is evidence.** Bound to the exact version accepted, with who accepted it and when.\n","required":["id","formId","formVersion","subjectId","submittedAt"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"formId":{"type":"string","format":"uuid"},"formVersion":{"type":"integer","description":"**The version, not the form.** 2.15.13 requires the exact accepted version retained, and a submission pointing at a form that has since changed is a submission proving nothing.\n"},"subjectId":{"type":"string","format":"uuid"},"onBehalfOfSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"A guardian signing for a minor, or a group leader for an attendee."},"answers":{"type":"object","description":"**One entry per answered `FormField`, keyed by its `key`.** The value's type follows the field's `type`: a string for text, long text, date, phone, email, select and `file` (the asset id); a number for number and scale; a boolean for boolean; an array of strings for multi-select. A `signature` field is `signatureAssetId`, not an answer.\n","additionalProperties":{"oneOf":[{"type":"string"},{"type":"number"},{"type":"boolean"},{"type":"array","items":{"type":"string"}}]}},"signatureAssetId":{"type":"string","format":"uuid","nullable":true},"submittedAt":{"type":"string","format":"date-time","description":"**Device time** of the acceptance — `submitForm` is offline-capable, and the time a waiver was signed is the evidence, not the time it synced. The `recorded_at` of naming-and-style 5.2 for this row.\n"},"syncedAt":{"type":"string","format":"date-time","readOnly":true,"description":"Server time the submission arrived."},"expiresAt":{"readOnly":true,"type":"string","format":"date-time","nullable":true,"description":"From `validForMonths`. **A returning participant with a live acceptance does not sign again**, which is the whole point of holding it against the guest.\n"},"capturedAtChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"ipAddress":{"type":"string","nullable":true}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuestMenu": {"type":"object","x-ticvai-persistence":"none — projection over menu, item and availability","required":["outletId","menuId","name","inForceUntil","sections"],"properties":{"outletId":{"type":"string","format":"uuid"},"menuId":{"type":"string","format":"uuid"},"name":{"type":"string"},"inForceUntil":{"type":"string","format":"date-time","nullable":true,"description":"When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know.\n"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"sections":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","items":{"type":"object","required":["menuItemId","name","price","isAvailable","allergens"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"Marked, not removed. A guest who saw a dish yesterday and cannot find it today assumes the app is broken; \"sold out\" is an answer.\n"},"unavailableReason":{"type":"string","nullable":true},"allergens":{"type":"array","description":"Always present. Not a field a tenant may choose to omit.","items":{"$ref":"#/components/schemas/AllergenCode"}},"preparationMinutes":{"type":"integer","nullable":true},"modifierGroups":{"type":"array","items":{"$ref":"#/components/schemas/ModifierGroup"}}}}}}}}}},
"GuestNotification": {"type":"object","description":"One in-app message as the guest sees it. A view of `marketing.message_dispatch`, channel `inApp`.","required":["id","title","queuedAt","read"],"properties":{"id":{"type":"string"},"kind":{"type":"string","enum":["queueCall","orderReady","bookingChange","venueAlert","offer","other"]},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid","nullable":true},"deepLink":{"type":"string","nullable":true,"description":"Where tapping the notification leads in the app (an order, a queue ticket, a booking)."},"queuedAt":{"type":"string","format":"date-time"},"read":{"type":"boolean"}}},
"GuestOrderFulfilment": {"type":"object","x-ticvai-persistence":"fnb.order_fulfilment","description":"How a guest's order leaves the kitchen: collected, delivered to an address, or taken to a place in the venue.","required":["mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"orderId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-column":"service_order_id","description":"The guest order this fulfils (`FnbOrder.id`). Set by the server from the order it arrives with."},"mode":{"type":"string","enum":["collection","delivery","inVenue"],"description":"`collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). `GuestOrderResult.fulfilment` reports the same choice."},"collectionAt":{"type":"string","format":"date-time","nullable":true},"windowStart":{"type":"string","format":"date-time","nullable":true},"windowEnd":{"type":"string","format":"date-time","nullable":true},"deliveryAddress":{"type":"object","nullable":true,"properties":{"building":{"type":"string","maxLength":200},"unit":{"type":"string","maxLength":60,"nullable":true},"emirate":{"type":"string","maxLength":60},"directions":{"type":"string","maxLength":500,"nullable":true}}},"deliveryFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true},"cutlery":{"type":"boolean","default":false},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"GuestOrderResult": {"type":"object","x-ticvai-persistence":"none — projection over fnb_order","required":["orderId","orderNumber","status","total"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string","description":"Short and readable. It gets called out across a counter."},"fulfilment":{"type":"string","enum":["collect","deliverToLocation","tableService","deliverToAddress"],"description":"How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is `delivery`; `inVenue` is `tableService` where the location session is a table and `deliverToLocation` for a seat, cabana or named location. `KitchenTicket.serviceMode` is the kitchen's view and uses `ServiceMode`."},"deliveryLabel":{"type":"string","nullable":true,"description":"Where it is going, as a runner would read it."},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"collectionPoint":{"type":"string","nullable":true},"tableLabel":{"type":"string","nullable":true}}},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModifierGroup": {"x-ticvai-persistence":"fnb.modifier_group + fnb.modifier_option","type":"object","description":"**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n","required":["id","code","name","minSelections","maxSelections","options"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"minSelections":{"type":"integer","minimum":0,"description":"Greater than zero makes the group required."},"maxSelections":{"type":"integer","minimum":1},"options":{"type":"array","minItems":1,"items":{"type":"object","required":["id","name","priceDelta"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean"},"isAvailable":{"type":"boolean"},"allergens":{"type":"array","description":"What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PolicyKind": {"type":"string","enum":["privacy","termsAndConditions","refund","cookie","accessibility"]},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"PublishedContentPage": {"x-ticvai-persistence":"none — a public projection of whitelabel.content_page","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"A live content page as a guest reads it (`listPublishedContentPages`). Only published and enabled pages exist in this view, so it carries no status.","required":["id","slug","title","body"],"properties":{"id":{"type":"string","format":"uuid"},"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"}}},
"PublishedFaqCategory": {"x-ticvai-persistence":"none — a public projection of whitelabel.faq_category + whitelabel.faq_entry","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"One FAQ category with its published entries only (`listPublishedFaqs`).","required":["code","name","entries"],"properties":{"code":{"type":"string"},"name":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"entries":{"type":"array","items":{"type":"object","required":["id","question","answer"],"properties":{"id":{"type":"string","format":"uuid"},"question":{"$ref":"#/components/schemas/LocalisedText"},"answer":{"$ref":"#/components/schemas/LocalisedRichText"},"sortOrder":{"type":"integer"}}}}}},
"PublishedPolicy": {"x-ticvai-persistence":"none — a public projection of whitelabel.policy","type":"object","x-ticvai-agreed":"2 October: decided by Chinmay, fix before Block A starts (GFIX-2)","description":"The current version of one policy as a guest reads it (`listPublishedPolicies`). Who published it and the partition key stay on `Policy`.","required":["kind","version","body","effectiveFrom"],"properties":{"kind":{"$ref":"#/components/schemas/PolicyKind"},"title":{"type":"string"},"version":{"type":"string","description":"The version a consent records (a guest who consented to version 3 consented to version 3)."},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"effectiveFrom":{"type":"string","format":"date"},"requiresReconsent":{"type":"boolean","description":"True when guests who consented to an earlier version are asked again on next launch."}}},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"Review": {"x-ticvai-persistence":"marketing.review","allOf":[{"$ref":"#/components/schemas/SubmitReviewRequest"},{"type":"object","required":["status"],"properties":{"status":{"type":"string","enum":["pendingModeration","published","hidden","rejected"]},"response":{"type":"string","nullable":true},"responseIsPublic":{"type":"boolean"},"respondedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"openedCaseId":{"type":"string","nullable":true,"description":"Case raised automatically where the rating fell below the venue's threshold. Feedback that goes nowhere is worse than no feedback mechanism.\n"}}}]},
"SubmitReviewRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","rating","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"relatedOrderId":{"type":"string"},"rating":{"type":"integer","minimum":1,"maximum":5},"body":{"type":"string","maxLength":5000},"aspects":{"type":"array","description":"Aspect chips — the closed set the description always named.","uniqueItems":true,"items":{"type":"string","enum":["exhibitions","staff","cleanliness","food","value"]}},"recordedAt":{"type":"string","format":"date-time"}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}},
"VisitPlan": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan","description":"**A guest's visit plan** (29 September, MOB-6): the Plan tab. One row per plan; its items are `venuemap.visit_plan_item` rows carrying the version they belong to, so every earlier version stays readable and undo is a new version equal to an old one. **Owned by the guest session**, like a cart: `subjectId` when signed in, `sessionRef` for an anonymous device session, claimed on sign-in.\n","required":["id","venueId","status","version","days"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`."},"subjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"marketing.guest_profile","description":"The signed-in guest. From the session, never from the body."},"sessionRef":{"type":"string","nullable":true,"readOnly":true,"description":"The anonymous device session that owns the plan until sign-in."},"status":{"type":"string","enum":["draft","booked","archived"],"readOnly":true,"description":"`booked` after `bookVisitPlan`; a booked plan is read-only. `archived` after its last date."},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"The current version. Every `updateVisitPlan` adds one."},"source":{"type":"string","enum":["rules","preset","aiAgent"],"readOnly":true,"description":"What produced the current version: the rules planner, a preset, or the AI planner agent acting for the guest. **The guest sees which**, as every AI answer says what it is based on.\n"},"inputs":{"$ref":"#/components/schemas/VisitPlanRequest"},"mapVersion":{"type":"integer","readOnly":true,"description":"The published map version the plan was laid out on."},"cartId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"orders.cart","description":"The cart `bookVisitPlan` filled."},"excluded":{"type":"array","readOnly":true,"description":"**What was left out and why**, e.g. a coaster excluded because one of the party is under its 120 cm minimum. Shown on GST-053, so the planner never looks as if it forgot.\n","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","enum":["heightRule","ageRule","closedOnDate","notInInterests","noTime","notAtVenue"],"description":"`notAtVenue` (30 September, MoM 4.7): a must-include point that is at none of the plan's venues, so no day could hold it.\n"}}}},"unmatchedPreferences":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**A preference a day's venue cannot meet is said, never faked** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per day and preference that no point of that day's venue matches: a cuisine (`cuisineTags`), a shop (`retailTags`) or an interest (`interestTags`). `availableAtVenueIds` names the tenant's other active venues whose published map does match, so GST-053 and WEB-050 can say *Indian food is at the other park (day 2)* instead of quietly placing a restaurant the party cannot reach. Empty when every preference is met on every day. Worked out on read for the version read (a swap can meet or lose a preference), never stored.\n","items":{"type":"object","required":["date","venueId","preference","tag"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"The day's venue, which has no match."},"preference":{"type":"string","enum":["cuisine","retail","interest"]},"tag":{"type":"string","maxLength":30},"availableAtVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Other active venues of the tenant where the tag is matched. Empty when none is."}}}},"days":{"type":"array","readOnly":true,"description":"One per date, in order. The items of the version read.","items":{"type":"object","required":["date","venueId","items"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid","description":"**The venue this day is planned at** (30 September, MoM 4.7): `VisitPlanRequest.dayVenues` for the date, else `venueId`. Every item of the day is at this venue.\n"},"opensAt":{"type":"string","nullable":true},"closesAt":{"type":"string","nullable":true},"items":{"type":"array","items":{"$ref":"#/components/schemas/VisitPlanItem"}}}}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"VisitPlanAlternative": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"One candidate for a swap (29 September, MOB-6).","required":["kind","venueId","startsAt","reason"],"properties":{"kind":{"type":"string","enum":["attraction","show","meal","shop","rest"]},"venueId":{"type":"string","format":"uuid","description":"The item's day venue; an alternative is never from another venue (30 September, MoM 4.7)."},"pointId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"name":{"type":"string"},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer"},"walkMinutes":{"type":"integer","nullable":true},"expectedWaitMinutes":{"type":"integer","nullable":true},"matchedInterests":{"type":"array","items":{"type":"string"}},"reason":{"type":"string","description":"Why it is offered, in words the sheet shows, e.g. *Same thrill level, 4 minutes closer*."}}},
"VisitPlanBooking": {"type":"object","x-ticvai-persistence":"none — computed; the lines are orders.cart_line rows","description":"What `bookVisitPlan` returns (29 September, MOB-6): the cart handoff.","required":["planId","cartId","added","notAdded"],"properties":{"planId":{"type":"string","format":"uuid"},"cartId":{"type":"string","format":"uuid"},"added":{"type":"array","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"cartLineId":{"type":"string","format":"uuid"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true}}}},"notAdded":{"type":"array","description":"Items that could not be added, with the `addCartLine` refusal each met.","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"reason":{"type":"string","description":"The orders `CartProblem` code, e.g. `soldOutForSession`, `productInfoOnly`, `seatLimitExceeded`."}}}},"freeItems":{"type":"integer","description":"Stops that need nothing bought."}}},
"VisitPlanItem": {"type":"object","x-ticvai-persistence":"venuemap.visit_plan_item","description":"**One timed stop on a plan day** (29 September, MOB-6). Rows are kept per `planVersion`: a change writes the day's items again under the new version, and an older version's rows are never updated.\n","required":["id","planId","planVersion","date","sequence","kind","startsAt","endsAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"venuemap.visit_plan"},"planVersion":{"type":"integer","minimum":1,"readOnly":true},"date":{"type":"string","format":"date"},"sequence":{"type":"integer","minimum":1},"kind":{"type":"string","enum":["attraction","show","meal","shop","rest","travel"],"description":"`meal` is a stop at a dining point (restaurant, cafe or food kiosk); `shop` is a retail stop at a shop or a retail kiosk (30 September client meeting, MoM 4.7: retail is placed from the day venue's own points, as dining is).\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The venue of this stop** (30 September client meeting, MoM 4.7): always the day's venue, and the venue whose map `pointId` is on. Carried on the item so the screens, `bookVisitPlan` and the AI planner agent read it rather than infer it. **Worked out on read, not stored**: from the plan's `inputs` (`dayVenues` for the item's date, else `venueId`). A stored `venue_id` would move the item rows from the plan's own row-level policy to a venue policy and hide a second park's items from the guest who owns the plan.\n"},"pointId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"venuemap.point"},"productId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.product","description":"What is bought for this stop, where it is bought. Null for a free stop."},"bundleId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"promotions.bundle","description":"A meal combo or package, from the point's `featuredOffer`."},"performanceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"catalogue.performance"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"walkMinutesBefore":{"type":"integer","minimum":0,"nullable":true},"expectedWaitMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"The typical wait at that hour when the plan was laid out; GST-059 replaces it with the live one."},"addOnSuggestion":{"type":"object","nullable":true,"description":"A suggested add-on for this stop, e.g. Fast Track where the wait is long. Never added by itself.","properties":{"productId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}},"addOnAccepted":{"type":"boolean","default":false},"pinned":{"type":"boolean","default":false,"description":"The guest fixed this stop; a re-lay moves other stops around it."},"note":{"type":"string","nullable":true,"maxLength":200}}},
"VisitPlanRequest": {"type":"object","x-ticvai-persistence":"none — request only; kept as `inputs` on venuemap.visit_plan","description":"What `generateVisitPlan` takes (29 September, MOB-6): the Plan tab's form on GST-051 and WEB-050.\n","required":["venueId","dates","party"],"properties":{"venueId":{"type":"string","format":"uuid","description":"The venue the guest picked in the app (GST-001 / WEB-001), which scopes the plan. Every date is planned at this venue unless `dayVenues` puts it somewhere else.\n"},"dayVenues":{"type":"array","maxItems":7,"description":"**Which venue on which date, in a multi-venue tenant** (30 September client meeting, MoM 4.7, Allam's requirement). One entry per date that is not at `venueId`; each date of `dates` at most once. Each venue must be an active venue of the caller's tenant (the options `getTenantAppStatus.venues` lists), else 422 `venue-not-in-tenant`. **Each day is then planned from that venue's own published map only**: its rides, its dining and its retail points, never another venue's.\n","items":{"type":"object","required":["date","venueId"],"properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"}}}},"dates":{"type":"array","minItems":1,"maxItems":7,"items":{"type":"string","format":"date"}},"party":{"type":"array","minItems":1,"maxItems":20,"description":"One entry per person. **Height where the guest knows it, age otherwise**: height is what ride eligibility rules test, and an age band is the fallback the rule may also state. Nothing here identifies a person.\n","items":{"type":"object","properties":{"heightCm":{"type":"integer","minimum":40,"maximum":230,"nullable":true},"ageYears":{"type":"integer","minimum":0,"maximum":120,"nullable":true}}}},"pace":{"type":"string","enum":["packed","relaxed"],"default":"relaxed"},"interestTags":{"type":"array","maxItems":12,"description":"The same closed list as `VenuePoint.interestTags`.","items":{"type":"string"}},"cuisineTags":{"type":"array","maxItems":8,"description":"Matched per day against the `cuisineTags` of that day's venue's dining points only (30 September, MoM 4.7). A cuisine no dining point of the day's venue serves is not forced into the day; it is reported in `VisitPlan.unmatchedPreferences`.\n","items":{"type":"string"}},"retailTags":{"type":"array","maxItems":8,"description":"**Shops the party would like to visit** (30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options), e.g. `souvenirs`, `toys`, `apparel`, `essentials`. Matched per day against `VenuePoint.retailTags` of that day's venue's shops and retail kiosks; an unmatched tag is reported, as a cuisine is.\n","items":{"type":"string","maxLength":30}},"mustIncludePointIds":{"type":"array","maxItems":10,"description":"Placed on a day whose venue has the point. A point at none of the plan's venues is listed in `VisitPlan.excluded` with `notAtVenue`, never placed on another venue's day.\n","items":{"type":"string","format":"uuid"}},"preset":{"type":"string","nullable":true,"enum":["highlights","family","thrillSeeker","waterDay","relaxed","showsAndDining"],"description":"A ready-made day plan (GST-052 Suggested Itineraries): the preset fixes the interests and the pace, and the party still decides eligibility.\n"},"presetKey":{"type":"string","nullable":true,"maxLength":64,"pattern":"^[a-z][a-zA-Z0-9]*$","description":"The ready-made plan the guest took on GST-052 (30 September, second wave of the 29 September pass, MOB-6): one of the built-in `preset` keys above, or a key of a ready-made plan the venue defines. **The same rules planner runs**: the preset only supplies interests, pace and must-include points, and the party still decides eligibility. When both `preset` and `presetKey` are sent they must name the same plan; `presetKey` is the field new clients send. An unknown key is refused 422 `unknown-preset`.\n"},"startTime":{"type":"string","nullable":true,"pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"When the party arrives. Null means opening time."},"locale":{"type":"string","nullable":true}}},
"VisitPlanUpdate": {"type":"object","x-ticvai-persistence":"none — request only; lands as a new version of venuemap.visit_plan_item rows","description":"What `updateVisitPlan` takes (29 September, MOB-6).","required":["baseVersion","changes"],"properties":{"baseVersion":{"type":"integer","minimum":1},"changes":{"type":"array","minItems":1,"maxItems":20,"items":{"type":"object","required":["op"],"properties":{"op":{"type":"string","enum":["swap","remove","add","move","pin","acceptAddOn","declineAddOn","revertTo"]},"itemId":{"type":"string","format":"uuid","nullable":true},"date":{"type":"string","format":"date","nullable":true},"pointId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","nullable":true,"description":"For `revertTo`, the earlier version to restore (undo)."}}}}}},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]}
}
```
