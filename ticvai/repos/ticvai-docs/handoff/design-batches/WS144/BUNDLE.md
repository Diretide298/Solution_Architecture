# WS144 — Marketing CRM Configuration Reference v1.0 board 10

**10 screens · 20 operations · 19 schemas · 5 permissions**

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
  `GUEST_VIEW, MARKETING_MANAGE, MARKETING_SEND, MARKETING_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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

### Finance, Ledger & Tax · Reporting & Analytics

Finance and insights run underneath every sale. A sale at a till (P04), kiosk, web storefront (P01) or guest app (P02) is priced and taxed per line at the moment of sale, recorded in the venue's base currency (AED in the UAE; 2 decimals, or 3 for BHD, KWD and OMR, never rounded away), and posted to an append-only dual ledger through account mappings per money event; anything unmapped lands in suspense. Tax follows the jurisdiction's tax profile: inclusive or exclusive, compound where a tax applies on another, zero-rated or exempt with verified evidence, and computed on the discounted price by default or on the price before discount where the region requires it (Egypt). A guest may select a currency the venue charges and pay in it: the rate is locked on the order, the payment partner is asked in that currency, the ledger keeps the base amount with the rate, and a refund goes back in the currency paid (decided 2 October 2026, Chinmay); a currency shown but not charged is an approximate price. Foreign cash at a till is recorded at its base equivalent and change is given in base currency. A paid order can carry a VAT receipt (simplified tax invoice), a full tax invoice with the buyer's TRN, or a consolidated invoice for a company, each numbered without gaps and never edited; corrections are credit memos. Revenue is recognised by rule: POS-style immediate, tickets on the visit, gift cards and wallet on use, annual passes straight-line or per visit, breakage on expiry; deferred revenue is a balance that ages. Each venue's day is reconciled (POS cash, gateways, bank, wallet against the ledger, provider files matched automatically, only genuine mismatches to a person); chargebacks are defended against the bank's deadline; month end runs seven close checks and goes to a finance approver. Nothing posted is deleted: a correction is a reversal, an approver is never the preparer, and ledger approval needs a second factor. Back-office finance lives in Venue Management (P08: chart of accounts, mapping, FX, journals, recognition, reconciliation, period close, chargebacks); tax profiles, calculation validation and platform reconciliation in the TICVAI Console (P09); partner settlement in P10. Reporting is one consolidated, permission-based area (Analytics, P16): seeded standard dashboards and reports plus no-code builders over a governed business catalogue; the P08 report screens, the POS terminal day view and the kitchen performance view are scoped windows onto the same definitions and must show the same numbers. Every figure is read from a lag-tolerant reporting copy and shows its "as of" time; scope comes from the person's rights, never from a filter; AI explains and recommends but never acts, answers only within the person's role, labels forecasts, and is phase two for finance ledgers.

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Base currency | The venue's region currency; the currency every record and ledger posting is in. A guest may pay in a currency they select (where the venue charges it); the books still hold the base amount and the rate. | Home currency, Local price, Default currency | DI-211 / DI-282 / contracts/spine/orders.yaml#/components/schemas/Order |
| Pay in USD (a currency the venue charges) | The guest's selected payment currency; the card is charged in it at the rate locked on the order, and refunds go back in it. | Converted price, Approx. (for a charged currency) | contracts/spine/orders.yaml#checkoutCart / … |
| ≈ (approx.) price in USD / SAR / … | A conversion of a base-currency price for a currency the venue shows but does not charge, always next to the base price. | Converted price, USD price | DI-211 / screens/P02-guest-mobile-app.yaml#GST-044 |
| Takings | Money received in the period less refunds (cash-basis); the seeded KPI on hubs. | Revenue, Sales, Income | contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / R283 |
| Gross sales | Issued sales before discounts and refunds; whether tax is included must be stated on the tile. | Revenue, Turnover | MATRIX 6.1.78 |
| Net revenue | Gross sales less discounts less refunds, adjusted per finance policy. | Net sales, Revenue, Income | MATRIX 6.1.78 |
| Recognised revenue / Deferred revenue | Earned under the recognition rules / paid for but not yet earned. Kept distinct from sales. | Realised revenue, Unearned income, Wallet revenue | MATRIX 5.12.6 / DI-260 / contracts/spine/finance.yaml#getDeferredRevenue |
| VAT receipt | The simplified tax invoice issued on a paid order. | Receipt (when it is a tax document), Bill | contracts/spine/finance.yaml#issueTaxInvoice |
| Tax invoice / Combined tax invoice | A full invoice with the buyer's details / one invoice for several paid orders of one buyer. | Bill, Statement | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceType |
| Credit memo | The document that corrects an issued invoice after a refund; the invoice itself is never edited. | Credit note (until the client's tax adviser chooses "Tax credit note"), Edit invoice | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoice |
| VAT (or the jurisdiction's tax name) | Use the tax profile's own name on every surface; "Tax" only where several kinds are summed. | GST in UAE, Service charge for a tax | contracts/spine/catalogue.yaml#setTaxProfileJurisdiction |
| Price before discount | The taxable base where the jurisdiction taxes the undiscounted price. | Gross price, List tax | DI-598 |
| Post / Reverse | A journal reaches the ledger when approved and posted; a correction is a reversal, never an edit or delete. | Edit entry, Delete entry, Undo | contracts/spine/finance.yaml#reverseJournalEntry |
| Period (Open / Closing / Closed) | A fiscal period's state; closing stops postings, closed locks them. | Month locked, Frozen | contracts/spine/finance.yaml#/components/schemas/PeriodStatus |
| Variance (Over / Short) | The difference between expected and counted or recorded, always saying between which two figures. | Discrepancy, Error, Loss | DI-275 / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation |
| Settlement / Exception / Resolve | A provider's file for a day / a line that did not match / the recorded explanation. | Payout file, Error, Close | contracts/spine/finance.yaml#/components/schemas/SettlementException |
| Chargeback | A bank-initiated reversal with an evidence deadline; not a refund. | Dispute refund, Reversal | contracts/spine/orders.yaml#/components/schemas/Chargeback |
| Report / Dashboard / Tile / KPI | A runnable, exportable, schedulable definition / a page of tiles / one visual bound to a report / a company-wide measure defined once. | Widget (outside the builder's library), Board (for a user-facing dashboard) | contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / … |
| Warning / Critical | KPI status bands set by a target's amber and red thresholds; always words plus colour. | Amber, Red (alone), Bad | contracts/satellite/reporting.yaml#/components/schemas/KpiTarget |
| As of HH:MM / Updated N sec ago | The freshness of every figure read from the reporting copy; stale shows a warning. | Live (unless refreshed), Real-time | MATRIX 8.7.22 |
| Forecast | Any projected figure, with its range; never shown as a fact. | Expected, Will be | DI-973 |
| Outlet / Workstation (till) | A sales point / the device; staff copy may say "till" for the workstation. | Store, POS (in copy), Drawer (for the device) | R156 |
| Channel | POS, Web, App, Kiosk, B2B, OTA, from one closed list. | Source, Platform | MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-824` | Gamification Command Center | B | 0 | 5 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-825` | Challenge Builder | A | 15 | 35 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-826` | Achievement & Badge Engine | A | 0 | 10 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-827` | Points & Activity Rules | A | 0 | 26 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-828` | Milestones & Reward Rules | A | 31 | 10 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `BO-829` | Family, Team & Event Challenges | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-830` | Referral & Streak Management | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-831` | Progress, Leaderboards & Hub | D | 3 | 18 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-832` | AI Engagement Optimization | D | 0 | 0 | 6 | 9 | 0 | 0 | — | notStarted (—) |
| `BO-833` | Gamification Analytics & Audit | D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-826, BO-829, BO-830, BO-832, BO-833 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-824` Gamification Command Center

**Monitor engagement programs and their financial and behavioral impact. Show active challenges, participants, completion, points issued, rewards claimed, streaks and referrals. Report engagement lift, repeat visits, revenue impact and unredeemed points/reward liability. Compare by challenge, audience, venue, event, membership, team, season and period. Surface fraud anomalies, overspend, low participation and explainable AI opportunities. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block B · task VM-BO-824 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/gamification-command-center-bo-824` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): getMyChallenges returns the caller's own challenges; a command centre needs programme-wide figures (design-notes correction customer-marketing BO-824). Contract gap recorded 2 October 2026 (CHG-WIR-007): No staff read of challenges across the programme.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Engagement programmes and their impact: active challenges, participants, completion, points issued, rewards claimed, streaks, referrals; engagement lift, repeat visits, revenue; unredeemed points and reward liability; fraud anomalies and low participation.

**Fixed on main** (the package already carries these; draw what it says): The tiles and table are bound to getMyChallenges, the caller's own challenges. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Participants** (metric tile): The pack asks for participants; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Participants | text | not in the schema: `Participants` |

**Completion rate** (metric tile): The pack asks for completion rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Completion rate | text | not in the schema: `Completion rate` |

**Points issued** (metric tile): The pack asks for points issued; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Points issued | text | not in the schema: `Points issued` |

**Rewards claimed** (metric tile): The pack asks for rewards claimed; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Rewards claimed | text | not in the schema: `Rewards claimed` |

**Unredeemed points / reward liability** (metric tile): The pack asks for unredeemed points / reward liability; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Unredeemed points / reward liability | text | not in the schema: `Unredeemed points / reward liability` |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Liability**: Unredeemed points and outstanding rewards as a money figure (points are a liability from the moment they are earned). *(source: contracts/satellite/marketing-crm.yaml#createLoyaltyProgramme)*
- **Challenge row**: Name, scope, participants, completion rate, reward cost to date, status. *(source: screens/P08-venue-back-office.yaml#BO-824)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-825` Challenge Builder: *Challenge Builder*
- → `BO-826` Achievement & Badge Engine: *Achievement & Badge Engine*
- → `BO-827` Points & Activity Rules: *Points & Activity Rules*
- → `BO-828` Milestones & Reward Rules: *Milestones & Reward Rules*
- → `BO-829` Family, Team & Event Challenges: *Family, Team & Event Challenges*
- → `BO-830` Referral & Streak Management: *Referral & Streak Management*
- → `BO-831` Progress, Leaderboards & Hub: *Progress, Leaderboards & Hub*
- → `BO-832` AI Engagement Optimization: *AI Engagement Optimization*
- → `BO-833` Gamification Analytics & Audit: *Gamification Analytics & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gamification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gamification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gamification yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gamification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  activeChallenges: 6
  participants: 3420
  completion: 28%
  pointsIssued: 412000
  liability: AED 41
  200.0: null
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-824` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-824`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 1: Opens Gamification Command Center → Monitor engagement programs and their financial and behavioral impact. Show active challenges, participants, completion, points issued, rewards claimed, streaks and referrals. Report engagement lift …
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F253 branch at step 1 (expected): when Nothing has been set up on Gamification Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F253 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-824?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-825`, `BO-826`, `BO-827`, `BO-828`, `BO-829`, `BO-830`, `BO-831`, `BO-832`, `BO-833`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-825` Challenge Builder

**Create a governed challenge from objective through publication. Configure challenge name, objective, audience, actions, progress logic, start/end, recurrence and capacity. Define eligibility, terms, visibility, multilingual content, image, completion rule and reward. Support visit, purchase, scan, activity, referral, survey and approved social actions. Validate overlapping rules, reward budget, fraud controls, legal terms and approval before activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-BO-825 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_SEND`, `MARKETING_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `challengeId` (navigation) |
| Route | `/engagement-support/challenge-builder-bo-825` |

**Known gaps.** **`Challenge.kind` lacks scan, activity and purchase**, which the client keeps (decided 28 September, audit R275 (c)); handed to the contracts group to add to the enum. **Challenge Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The marketer defines a challenge, mission or streak: what a guest must do (visit, spend, ride, collect, streak, refer, survey, social, milestone, scan, activity, purchase), for whom, by when, and for what reward. Gamification is not loyalty. A challenge pays for behaviour spend does not produce, such as a second visit, a quiet Tuesday, or a ride nobody rides.

**Fixed on main** (the package already carries these; draw what it says): No list or read operation for challenges exists (only createChallenge and the guest's getMyChallenges), but the screen has list states. (CHG-SBO-013).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Challenge action | select field | — | — | — | — | **Scan, activity and purchase are kept** (decided 28 September, audit R275 (c)) beside the contract's `Challenge.kind` values (visit, spend, ride, collection, streak, referral, survey, social … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Active · Paused · Ended · Archived | `listChallenges` ?status |

**Form: Create challenge** (modal, opened by *Create challenge*; *Create challenge* calls `createChallenge`, *Cancel* sends nothing)

**Collects what `createChallenge` sends before it is called.** Required: `name`, `kind`, `goal`. Optional: `scope`, `eventId`, `rewardKind`, `rewardValue`, `rewardAmount`, `badgeAssetId`, `startsAt`, `endsAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | — | — | — | `createChallenge` body |
| Kind `kind` | select | required | — | Visit · Spend · Ride · Collection · Streak · Referral · Survey · Social · Milestone · Scan · Activity · Purchase | — | What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)): `scan` counts scans of a named code or … | `createChallenge` body |
| Scope `scope` | radio group | optional | Individual | Individual · Family · Group · Team | — | 22.6.7 and 22.6.8. A family challenge is not a per-person challenge counted twice — members contribute toward one shared goal, and a school competing against another school is a … | `createChallenge` body |
| Goal `goal` | group | required | — | — | — | What completes it. | `createChallenge` body |
| Metric `goal.metric` | text field | optional | — | — | — | — | `createChallenge` body |
| Target `goal.target` | number field | optional | — | — | — | — | `createChallenge` body |
| Within days `goal.withinDays` | number field (days) | optional | — | — | — | — | `createChallenge` body |
| Event `eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `createChallenge` body |
| Reward kind `rewardKind` | select | optional | — | Badge · Loyalty points · Wallet credit · Voucher · Entitlement · None | — | 22.6.13. A reward that issues wallet credit is money, and it goes through the same stored-value mechanism as everything else rather than a parallel one. | `createChallenge` body |
| Reward value `rewardValue` | number field | optional | — | min 1 | — | Points, for `rewardKind: loyaltyPoints` only. A count, not an amount — a money reward is `rewardAmount`, never this. | `createChallenge` body |
| Reward amount `rewardAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | The credit, for `rewardKind: walletCredit` only. The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the region, because a wallet credit is money … | `createChallenge` body |
| Badge image `badgeAssetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createChallenge` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createChallenge` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createChallenge` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Action**: One of the challenge kinds; scan, activity and purchase are kept from the client pack beside the contract's kinds. *(source: contracts/satellite/marketing-crm.yaml#createChallenge; screens/P08-venue-back-office.yaml#BO-825)*
- **Scope**: Individual, family, group or team; a family challenge counts the linked family's progress together. *(source: contracts/satellite/marketing-crm.yaml#/components/schemas/Challenge)*
- **Reward**: A reward from the rewards catalogue, points, or a badge; a reward budget cap is validated before activation. *(source: screens/P08-venue-back-office.yaml#BO-825)*
- **Guest-facing text and image**: Name and terms in English and Arabic; image from the asset library. *(source: DI-019; screens/P08-venue-back-office.yaml#BO-825)*

#### Outputs: what the screen shows and produces

**Shown**

**Challenges** (data table, from `listChallenges`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Name | text | — |
| Kind | chip: Visit, Spend, Ride, Collection, Streak, Referral… | What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)) … |
| Scope | chip: Individual, Family, Group, Team | 22.6.7 and 22.6.8. A family challenge is not a per-person challenge counted twice — members contribute toward one shared goal, and a school … |
| Goal | grouped details | What completes it. |
| Metric | text | — |
| Target | 1,234.5 | — |
| Within days | 1,234 | — |
| Event | the name it points at, never the id | — |
| Reward kind | chip: Badge, Loyalty points, Wallet credit, Voucher, Entitlement, None | 22.6.13. A reward that issues wallet credit is money, and it goes through the same stored-value mechanism as everything else rather than a … |
| Reward value | 1,234 | Points, for `rewardKind: loyaltyPoints` only. A count, not an amount — a money reward is `rewardAmount`, never this. |
| Reward amount | AED 1,234.50 | The credit, for `rewardKind: walletCredit` only. The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the … |
| Badge image | the image or video | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Draft, Active, Paused, Ended, Archived | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The challenge** (detail panel, from `getChallenge`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Kind | chip: Visit, Spend, Ride, Collection, Streak, Referral… | What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)) … |
| Scope | chip: Individual, Family, Group, Team | 22.6.7 and 22.6.8. A family challenge is not a per-person challenge counted twice — members contribute toward one shared goal, and a school … |
| Goal | grouped details | What completes it. |
| Metric | text | — |
| Target | 1,234.5 | — |
| Within days | 1,234 | — |
| Event | the name it points at, never the id | — |
| Reward kind | chip: Badge, Loyalty points, Wallet credit, Voucher, Entitlement, None | 22.6.13. A reward that issues wallet credit is money, and it goes through the same stored-value mechanism as everything else rather than a … |
| Reward value | 1,234 | Points, for `rewardKind: loyaltyPoints` only. A count, not an amount — a money reward is `rewardAmount`, never this. |
| Reward amount | AED 1,234.50 | The credit, for `rewardKind: walletCredit` only. The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the … |
| Badge image | the image or video | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Draft, Active, Paused, Ended, Archived | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What activating changes (publish gate) | navigation or local | — | — | — | — |
| Create challenge (primary button) | `createChallenge` POST `/challenges` | Challenge | Challenge | — | opens modal first |
| Activate challenge (secondary button) | `activateChallenge` POST `/challenges/{challengeId}/activate` | — | Challenge | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The challenge is not a draft (`challenge-not-draft`). | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Validation**: Overlapping rules with another live challenge, the reward budget, and legal terms are checked before activation; each problem names the other challenge. *(source: screens/P08-venue-back-office.yaml#BO-825)*

**Data it reads**: `listChallenges` (onLoad, Reopen a draft challenge (CHG-CSA-045)); `getChallenge` (onLoad, Open one challenge (CHG-CSA-045))

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The challenge list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the challenge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No challenge yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the challenge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The challenge is not a draft (`challenge-not-draft`). |

#### Consistency with other screens

- Match `BO-829`: Family, team and event challenges are this builder with scope preset.
- Match `GST-036`: Guests see progress as "2 of 3 visits", never just the outcome.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
challenge: Autumn Explorer - visit 3 times between 1 Oct and 30 Nov 2026
scope: Individual
reward: Explorer badge + 500 points
terms: One reward per guest; visits on the same day count once.
```

#### Permissions

- `createChallenge` → `MARKETING_MANAGE` (configure) · staff
- `listChallenges` → `MARKETING_VIEW` (read) · staff
- `getChallenge` → `MARKETING_VIEW` (read) · staff
- `activateChallenge` → `MARKETING_SEND` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-825` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-825`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 2: Works in Challenge Builder → Create a governed challenge from objective through publication. Configure challenge name, objective, audience, actions, progress logic, start/end, recurrence and capacity. Define eligibility, terms …

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-825?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What activating changes, Create challenge, Activate challenge.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_SEND`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-826` Achievement & Badge Engine

**Manage achievements and digital badges. Define achievement type, badge name, tier, rarity, unlock criteria, points value, visibility and validity. Maintain an approved visual badge library and multilingual name/description and accessible alt text. Configuration Scope of Work / Version 1.0 49 Configure automatic or manual issuance, revocation, duplicate prevention and profile/mobile display. Track active challenges and rewards using each achievement before editing or retiring it. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-BO-826 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `customerId` (navigation) · cold entry: Opened from BO-824 with the guest picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/engagement-support/achievement-badge-engine-bo-826` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): The screen manages badges and its primary action was "Create challenge"; listBadges and setBadge are its main act (design-notes correction customer-marketing …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Achievements and badges: type, name, tier, rarity, unlock criteria, points value, visibility, validity, an approved badge image library with multilingual names and alt text; automatic or manual issuance, revocation and duplicate prevention. The status badges the client named are Explorer, Adventurer and Legend.

**Fixed on main** (the package already carries these; draw what it says): The primary action is "Create challenge" and listBadges is not declared. (CHG-WIR-005).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Badge**: Name and description in English and Arabic, alt text, image, unlock criteria. *(source: contracts/satellite/marketing-crm.yaml#setBadge; DI-392)*

#### Outputs: what the screen shows and produces

**Shown**

**Badges** (data table, from `listBadges`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Icon URL | text | — |
| Type | text | — |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save badge (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Award manually**: Records why (source type and reference) so a guest asking how they got it has an answer. *(source: contracts/satellite/marketing-crm.yaml#awardBadge)*

**Data it reads**: `listBadges` (onLoad, The badges defined)

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The achievement badge list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the achievement badge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No achievement badge yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the achievement badge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already held and not expired |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
badges:
- Explorer - 3 visits
- Adventurer - 10 visits or AED 2,000 spend
- Legend - 25 visits
```

#### Permissions

- `setBadge` → `MARKETING_MANAGE` (configure) · staff
- `awardBadge` → `MARKETING_MANAGE` (configure) · staff, service
- `listBadges` → `MARKETING_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Gamification shows badges/status tiers (e.g. Explorer, Adventurer, Legend) earned by spend or engagement thresholds, feeding the loyalty tier structure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-392)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-826` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-826`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 4: Works in Achievement & Badge Engine → Manage achievements and digital badges. Define achievement type, badge name, tier, rarity, unlock criteria, points value, visibility and validity. Maintain an approved visual badge library and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-826?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save badge, Cancel.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-827` Points & Activity Rules

**Translate qualifying guest actions into controlled loyalty points. Configure rules for visits, purchases, ticket scans, activities, referrals, surveys and other approved events. Set base points, multiplier, daily/monthly limit, validity, rounding and posting timing. Apply device, account, velocity, location and transaction fraud checks and exception review. Post through the shared Loyalty Engine and preserve source event, rule/version and adjustment history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-BO-827 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `programmeId` (navigation) |
| Route | `/engagement-support/points-activity-rules-bo-827` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): A whole-set replace (setLoyaltyRules) without reading the current set erases rules, and getLoyaltyRules was consumed by no screen; programme creation belongs on …

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** The loyalty administrator sets how guest actions earn points: base points, multipliers, daily and monthly caps, validity, rounding and when points post. The rules are edited and saved as ONE set, so a live programme is never half-changed. The ratio between earning and redemption is what the administrator is reasoning about, so both are on screen together.

**Fixed on main** (the package already carries these; draw what it says): getLoyaltyRules ("every rule a loyalty programme runs on") is consumed by no screen; BO-827 can replace the set but cannot read it. (CHG-WIR-005); The primary action is "Create loyalty programme" (createLoyaltyProgramme) on a rules screen that enters with a programmeId. (CHG-WIR-005).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Full loyalty configuration (tiers, earn and redemption rules, expiry) is pending a dedicated workshop.** → Drawn default stands (answer: "Default / recommended accepted"): Sample rules above; points expire 12 months after being earned. *(decided by Chinmay, 2026-10-02; DEC-018 / CHG-NOTE-002)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listLoyaltyCampaigns` ?programmeId |
| Active on | date and time picker | — | — | `listLoyaltyCampaigns` ?activeOn |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Earn rules**: Per action (visit, purchase, scan, activity, referral, survey) with base points, multiplier, caps per day and month, rounding, and posting timing. *(source: screens/P08-venue-back-office.yaml#BO-827)*
- **Campaign rules**: Bonus and multiplier rules scoped to a dated campaign window (e.g. double points in Ramadan). *(source: contracts/satellite/marketing-crm.yaml#setLoyaltyRules; contracts/satellite/marketing-crm.yaml#setLoyaltyCampaign)*
- **Tiers and redemption rules**: Shown with the earn rules, because a tier-gated redemption is meaningless without the tiers (500 points off for Gold). *(source: contracts/satellite/marketing-crm.yaml#setLoyaltyRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Show the loyalty campaigns** (card list, from `listLoyaltyCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Start at | 1 Oct 2026, 14:30 | — |
| End at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Created at | 1 Oct 2026, 14:30 | — |

**Rules in force** (detail panel, from `getLoyaltyRules`)

| Shows | Format | Notes |
|---|---|---|
| Programme | the name it points at, never the id | — |
| Campaign rules | list or chips (count when long) | Bonus, multiplier and condition rules, each scoped to a campaign window. |
| ID | the name it points at, never the id | — |
| Campaign | the name it points at, never the id | — |
| Type | text | — |
| Points earning rule | the name it points at, never the id | — |
| Reward | the name it points at, never the id | — |
| Bonus points | 1,234.5 | — |
| Multiplier | 1,234.5 | — |
| Conditions json | text | — |
| Is active | yes / no (icon or chip) | — |
| Tiers | list or chips (count when long) | The programme's tiers, in `rank` order. Read with the rules because a redemption rule that is tier-gated is meaningless without them — 500 … |
| ID | the name it points at, never the id | — |
| Loyalty programme | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Rank | 1,234 | Order, not threshold. Two tiers can share a qualifying rule and still have an order, and sorting by points breaks the moment a tier is … |
| Min lifetime points | 1,234 | What reaching this tier requires. `pointsToNextTier` on the position is this minus the guest's lifetime points, and until now it was this … |
| Retain lifetime points | 1,234 | What keeping it requires, per review period. Usually lower than reaching it, and a scheme that cannot express the difference either never … |
| Validity months | 1,234 | Null means the tier does not lapse on its own. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save loyalty rules (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Ratio hint**: For each redemption, show how many qualifying actions it takes ("2,500 points = 50 visits"). *(source: contracts/satellite/marketing-crm.yaml#getLoyaltyRules)*

**What each action does** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Save rules**: Replaces the programme's rule set as a whole, or not at all; the response is the new set. *(source: contracts/satellite/marketing-crm.yaml#setLoyaltyRules)*

**Data it reads**: `getLoyaltyRules` (onLoad, Every rule the programme runs on); `listLoyaltyCampaigns` (onLoad, Show the loyalty campaigns)

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The points activity rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the points activity rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No points activity rules yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the points activity rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A rule references a reward or product that does not exist |

#### Edge cases to draw

- **Points are a liability**: Show that points post to the ledger when earned, not when redeemed, so raising earn rates raises the liability immediately. *(source: contracts/satellite/marketing-crm.yaml#createLoyaltyProgramme)*

#### Consistency with other screens

- Match `BO-828`: Rewards and milestones are configured on BO-828; their points costs appear here read-only for the ratio.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
programme: Coastal Aqua Rewards
earn:
- Visit - 50 points (max 1 a day)
- Purchase - 1 point per AED 10 (rounded down)
- Survey completed - 20 points
campaign: Ramadan double points - 1 Mar to 30 Mar 2027 - x2 on F&B
```

#### Permissions

- `setLoyaltyRules` → `MARKETING_MANAGE` (configure) · staff
- `setLoyaltyCampaign` → `MARKETING_MANAGE` (configure) · staff
- `getLoyaltyRules` → `MARKETING_VIEW` (read) · staff
- `listLoyaltyCampaigns` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-827` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-827`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 6: Works in Points & Activity Rules → Translate qualifying guest actions into controlled loyalty points. Configure rules for visits, purchases, ticket scans, activities, referrals, surveys and other approved events. Set base points …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-827?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save loyalty rules, Cancel.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-828` Milestones & Reward Rules

**Reward cumulative progress consistently. Define thresholds, tiers and immediate or delayed reward fulfillment. Support loyalty points, wallet credit, voucher, product offer, badge and membership benefit rewards. Configure eligibility, inventory, validity, redemption limit, substitution and approval threshold. Forecast reward cost/liability and prevent issuance when funding, inventory or eligibility fails. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 1 · needs the `marketing` module |
| Block | Block A · task APP-SETUP-BO-828 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/milestones-reward-rules-bo-828` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Rewards for cumulative progress: thresholds, tiers, immediate or delayed fulfilment; reward kinds (points, wallet credit, voucher, product offer, badge, membership benefit); eligibility, inventory, validity, redemption limits and approval thresholds; cost forecast; issuance stops when funding, stock or eligibility fails.

**Fixed on main** (the package already carries these; draw what it says): The primary action is "Create loyalty programme". (CHG-SBO-013).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listRewards` ?programmeId |

**Form: Save milestones and rewards** (modal, opened by *Save milestones and rewards*; *Save milestones and rewards* calls `createLoyaltyProgramme`, *Cancel* sends nothing)

**Collects what `createLoyaltyProgramme` sends before it is called.** Required: `code`, `name`, `earnRules`, `tiers`. Optional: `venueId`, `pointsLiabilityAccountId`, `pointsExpireAfterMonths`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tiers `tiers` | repeatable rows | required | — | — | — | Rows of `marketing.programme_tier`, the same shape `MarketingProgrammeTier` has — one definition of a tier, not a second copy that cannot round-trip. | `createLoyaltyProgramme` body |
| Code `tiers[].code` | text field | required | — | max length 40 | — | — | `createLoyaltyProgramme` body |
| Name `tiers[].name` | text field | required | — | max length 120 | — | — | `createLoyaltyProgramme` body |
| Rank `tiers[].rank` | number field | required | — | — | — | Order, not threshold. Two tiers can share a qualifying rule and still have an order, and sorting by points breaks the moment a tier is granted rather than earned. | `createLoyaltyProgramme` body |
| Min lifetime points `tiers[].minLifetimePoints` | number field | optional | — | — | — | What reaching this tier requires. `pointsToNextTier` on the position is this minus the guest's lifetime points, and until now it was this minus nothing. | `createLoyaltyProgramme` body |
| Retain lifetime points `tiers[].retainLifetimePoints` | number field | optional | — | — | — | What keeping it requires, per review period. Usually lower than reaching it, and a scheme that cannot express the difference either never demotes or demotes on the day a guest … | `createLoyaltyProgramme` body |
| Validity months `tiers[].validityMonths` | number field | optional | — | — | — | Null means the tier does not lapse on its own. | `createLoyaltyProgramme` body |
| Benefits `tiers[].benefits` | list of values (chips) | optional | — | — | — | What the tier gives, as the guest reads it. Text shown, not rules enforced. | `createLoyaltyProgramme` body |
| Earn multiplier `tiers[].earnMultiplier` | number field | optional | — | — | — | Applied to every earn rule while the guest holds this tier. Null means 1. | `createLoyaltyProgramme` body |
| Is active `tiers[].isActive` | toggle | optional | on | — | — | — | `createLoyaltyProgramme` body |
| Code `code` | text field | required | — | A code already used by any loyalty programme in the tenant, at any venue, is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused with `409 duplicate-code`. | `createLoyaltyProgramme` body |
| Name `name` | text field | required | — | — | — | — | `createLoyaltyProgramme` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createLoyaltyProgramme` body |
| Points liability account `pointsLiabilityAccountId` | picker: choose a points liability account | optional | — | — | shows names, sends the id | Points post here on accrual. They are a liability from the moment they are earned, not from the moment they are spent. | `createLoyaltyProgramme` body |
| Earn rules `earnRules` | repeatable rows | required | — | — | — | — | `createLoyaltyProgramme` body |
| Trigger `earnRules[].trigger` | select | required | — | Per currency unit · Per visit · Per product · On signup · On birthday · On review | — | — | `createLoyaltyProgramme` body |
| Points `earnRules[].points` | number field | required | — | — | — | — | `createLoyaltyProgramme` body |
| Product kinds `earnRules[].productKinds` | multi-select chips | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Limits a `perProduct` or `perCurrencyUnit` rule to these kinds. Empty means every kind. | `createLoyaltyProgramme` body |
| Multiplier `earnRules[].multiplier` | number field | optional | — | — | — | — | `createLoyaltyProgramme` body |
| Points expire after months `pointsExpireAfterMonths` | number field | optional | — | — | — | — | `createLoyaltyProgramme` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createLoyaltyProgramme` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Save reward** (modal, opened by *Save reward*; *Save reward* calls `setReward`, *Cancel* sends nothing)

**Collects what `setReward` sends before it is called.** Required: `loyaltyProgramId`, `code`, `name`, `type`, `isActive`. Optional: `productId`, `pointsCost`, `discountValue`, `validityDays`. `id` is a client UUIDv7 generated silently, never asked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setReward` body |
| Loyalty program `loyaltyProgramId` | picker: choose a loyalty program | required | — | — | shows names, sends the id | — | `setReward` body |
| Code `code` | text field | required | — | max length 100 | — | — | `setReward` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setReward` body |
| Type `type` | text field | required | — | max length 30 | — | — | `setReward` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setReward` body |
| Points cost `pointsCost` | number field | optional | — | — | — | — | `setReward` body |
| Discount value `discountValue` | number field | optional | — | — | — | — | `setReward` body |
| Validity days `validityDays` | number field (days) | optional | — | — | — | — | `setReward` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setReward` body |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Reward**: Kind, points cost or trigger milestone, validity, stock, limit per guest. *(source: contracts/satellite/marketing-crm.yaml#setReward)*

#### Outputs: what the screen shows and produces

**Shown**

**Show the rewards a milestone can give** (card list, from `listRewards`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Type | text | — |
| Points cost | 1,234.5 | — |
| Discount value | 1,234.5 | — |
| Validity days | 1,234 | — |

**Show the programmes and their milestones** (data table, from `listLoyaltyProgrammes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Unique per tenant (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused … |
| Name | text | — |
| Points expire after months | 1,234 | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save milestones and rewards (primary button) | `createLoyaltyProgramme` POST `/loyalty/programmes` | LoyaltyProgramme | LoyaltyProgramme | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Save reward (secondary button) | `setReward` PUT `/loyalty/rewards` | MarketingReward | MarketingReward | — | opens modal first |

**Data it reads**: `listLoyaltyProgrammes` (onLoad, Show the programmes and their milestones); `listRewards` (onLoad, Show the rewards a milestone can give)

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The milestones reward rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the milestones reward rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No milestones reward rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the milestones reward rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
milestones:
- 10th visit - free fast pass (stock 200)
- 5,000 lifetime points - Gold welcome pack
```

#### Permissions

- `createLoyaltyProgramme` → `MARKETING_MANAGE` (configure) · staff
- `setReward` → `MARKETING_MANAGE` (configure) · staff
- `listLoyaltyProgrammes` → `MARKETING_VIEW` (read) · staff, guest
- `listRewards` → `MARKETING_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.4.7 | The loyalty program options allow to create loyalty points for a certain type of transactions and to use these points as a form of payment. | F&B & Guest Management | CONTRACTED | `createLoyaltyProgramme` |
| 5.4.28 | Support multiple brands and venues. | F&B & Guest Management | CONTRACTED | `createLoyaltyProgramme` |
| 5.4.1 | The system should have the ability to integrate and exchange client information with a loyalty point system which will manage the loyalty points credited on to the loyalty account as per the … | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |
| 5.4.8 | Loyalty program data can be shared with a third party partner thanks to an API. For example, venue has an agreement with the airplane company Etihad allowing Etihad loyalty program members to spend … | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |
| 5.4.29 | Expose APIs for loyalty integrations. | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-828` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-828`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 8: Works in Milestones & Reward Rules → Reward cumulative progress consistently. Define thresholds, tiers and immediate or delayed reward fulfillment. Support loyalty points, wallet credit, voucher, product offer, badge and membership …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-828?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save milestones and rewards, Save reward.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-829` Family, Team & Event Challenges

**Support collaborative and competitive engagement formats. Configure family/household, team, group and event membership and joining rules. Define individual versus shared contribution, group scoring, maximum members and visibility. Configure ranking, winner calculation, tie-break, prize allocation and guardian rules for minors. Show participant roster, progress, status, exceptions and auditable membership changes. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-829 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/family-team-event-challenges-bo-829` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Collaborative and competitive formats: family, team, group and event challenges with joining rules, individual vs shared contribution, group scoring, ranking, tie-break, prize allocation and guardian rules for minors.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create challenge (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The family team event list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the family team event untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No family team event yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the family team event are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A minor joins a team challenge**: Needs the guardian's authority; the minor's name never appears on a public board. *(source: R205; contracts/satellite/marketing-crm.yaml#setLeaderboardNickname)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
challenge: Family Splash League - families of up to 5 - shared points - winner gets a cabana day
```

#### Permissions

- `createChallenge` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-829` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-829`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 10: Works in Family, Team & Event Challenges → Support collaborative and competitive engagement formats. Configure family/household, team, group and event membership and joining rules. Define individual versus shared contribution, group scoring …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-829?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create challenge, Cancel.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-830` Referral & Streak Management

**Configure repeat-behavior and referral mechanics. Define streak frequency, qualifying event, grace period, reset, maximum, milestone and reward. Configure referral code/link, attribution window, qualifying action, inviter/invitee reward and limits. Apply identity, account, device, payment, velocity and collusion fraud checks. Configuration Scope of Work / Version 1.0 50 Track invitation, qualification, reward posting, reversal and dispute history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-830 |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/referral-streak-management-bo-830` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** Streaks and referrals: streak frequency, qualifying event, grace period, reset; referral code or link, qualifying action (first purchase, first visit, membership purchase), rewards for both sides, limits and fraud checks. The reward fires on the referee's qualifying act, never on sign-up, and may credit points or wallet currency as configured.

**Known correction pending (do not draw the wrong version)**

- **The configuration screen's only operation creates one referral code.** Why: Referral programme rules (qualifying action, rewards, limits) and streak rules have no configuration operation. *(source: contracts/satellite/marketing-crm.yaml#createReferral; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Referral reward**: Points, voucher or wallet credit, business-configurable. *(source: DI-460; contracts/satellite/marketing-crm.yaml#createReferral)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create referral (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The referral streak list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the referral streak untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No referral streak yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the referral streak are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
referral: Bring a friend - friend's first purchase - referrer 500 points, friend 10% off - max 10 a year
```

#### Permissions

- `createReferral` → `MARKETING_MANAGE` (configure) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Referral rewards may be credited as currency/points directly into the guest's wallet (like Swiggy), in addition to discount vouchers — a business-configurable option. *(agreed · MoM 25 Aug 2026, 4.7 Entitlements & Access Control; 5. Key Decisions · DI-460)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-830` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-830`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 12: Works in Referral & Streak Management → Configure repeat-behavior and referral mechanics. Define streak frequency, qualifying event, grace period, reset, maximum, milestone and reward. Configure referral code/link, attribution window …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-830?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create referral, Cancel.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-831` Progress, Leaderboards & Hub

**Control how participants see progress and rankings. Show progress, points, milestones, next reward, streak and challenge status by participant. Configure leaderboard metric, scope, season, filters, dense ranking, privacy display and opt-out. Manage mobile gamification-hub content, featured challenges, quick actions and deep links. Provide near-real-time updates and resolve corrections without losing historical ranking evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-831 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) · cold entry: Opens on the leaderboard; a participant's progress shows once one is picked. |
| Route | `/engagement-support/progress-leaderboards-hub-bo-831` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-005): Participant progress was bound to getLoyaltyPosition (the caller's own position, guest audience); staff read a named guest with getGuestLoyalty (design-notes … Contract gap recorded 2 October 2026 (CHG-WIR-007): No staff-audience leaderboard read.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** How participants see progress and rankings: progress, points, milestones, next reward, streaks; leaderboard metric, scope, season, privacy display and opt-out; the app's gamification hub content. Leaderboards show a nickname the guest chose, never their real name.

**Fixed on main** (the package already carries these; draw what it says): Participant progress is bound to getLoyaltyPosition (the caller's own position, guest audience). (CHG-WIR-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Programme | select field | — | — | — | — | Sends `?programmeId=` (required). | — |
| Leaderboard metric | select field | — | — | — | — | With scope, season and privacy display, the pack's leaderboard configuration. | — |
| Allow opt-out | toggle | — | — | — | — | — | — |

**Rules for these inputs** (from the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process; these refine the tables above and win where they differ)

- **Privacy display**: Nickname only; a guest can opt out of boards entirely. *(source: contracts/satellite/marketing-crm.yaml#setLeaderboardNickname; contracts/satellite/marketing-crm.yaml#listLeaderboard)*

#### Outputs: what the screen shows and produces

**Shown**

**Participant progress** (detail panel, from `getGuestLoyalty`): **The participant being viewed, not the signed-in user** (decided 1 October 2026): the participant picked on the leaderboard, or the guest the screen is opened for, supplies `subjectId`. `getLoyaltyPosition` was here until then, and it returns the caller's own position.

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Programme | the name it points at, never the id | — |
| Points balance | 1,234 | — |
| Lifetime points | 1,234 | — |
| Tier name | text | — |
| Points to next tier | 1,234 | — |
| Next expiry points | 1,234 | — |
| Next expiry at | 1 Oct 2026, 14:30 | — |

**Leaderboard** (data table): Leaderboard metric, scope, season, dense ranking and privacy display; no leaderboard read is bound.

| Shows | Format | Notes |
|---|---|---|
| Rank | text | not in the schema: `Rank` |
| Participant (nickname) | text | not in the schema: `Participant (nickname)` |
| Metric value | text | not in the schema: `Metric value` |
| Season | text | not in the schema: `Season` |
| Scope | text | not in the schema: `Scope` |
| Opted out | text | not in the schema: `Opted out` |

**Hub content** (data table): Mobile gamification-hub content.

| Shows | Format | Notes |
|---|---|---|
| Featured challenge | text | not in the schema: `Featured challenge` |
| Quick action | text | not in the schema: `Quick action` |
| Deep link | text | not in the schema: `Deep link` |
| Order | text | not in the schema: `Order` |

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The progress leaderboards list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the progress leaderboards untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No progress leaderboards yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the progress leaderboards are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `GUEST_VIEW`, which `getGuestLoyalty` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
leaderboard:
- 1. SlideKing - 4,210
- 2. Mermaid_22 - 3,980
- 3. DuneRunner - 3,640
```

#### Permissions

- `getGuestLoyalty` → `GUEST_VIEW` (read) · staff, service

**A refused user sees:** Shown when the caller lacks `GUEST_VIEW`, which `getGuestLoyalty` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

Screen guard: `GUEST_VIEW`

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-831` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-831`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 14: Works in Progress, Leaderboards & Hub → Control how participants see progress and rankings. Show progress, points, milestones, next reward, streak and challenge status by participant. Configure leaderboard metric, scope, season, filters …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-831?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-832` AI Engagement Optimization

**Recommend relevant, sustainable engagement programs. Recommend challenge type, audience, difficulty, actions, reward and timing using historical behavior. Predict participation, completion, engagement uplift, cost and liability with confidence and factors. Support what-if comparison and require approval before a suggestion becomes a challenge or rule. Monitor applied recommendation results and avoid manipulative, discriminatory or age- inappropriate designs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-832 |
| Who uses it | venue staff holding `GUEST_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `guestId` (navigation) |
| Route | `/engagement-support/ai-engagement-optimization-bo-832` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers) process.** AI recommendations for engagement programmes: challenge type, audience, difficulty, reward and timing, with predicted participation, uplift, cost and confidence; what-if comparison; approval before a suggestion becomes a challenge; no manipulative or age-inappropriate mechanics.

**Known correction pending (do not draw the wrong version)**

- **The only operation is getGuestIntelligence for one guest.** Why: Programme-level recommendations need an AI suggestion operation. *(source: contracts/satellite/marketing-crm.yaml#getGuestIntelligence; Customer & Marketing (CRM, guest profiles, consent, segments, campaigns, journeys, loyalty, gamification, cases, voice of customer, waivers))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The engagement optimization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the engagement optimization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No engagement optimization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the engagement optimization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
suggestion: Weekday streak (3 Tuesdays) for lapsing families - predicted +6% weekday visits - cost AED 8,000 - confidence
  0.62
```

#### Permissions

- `getGuestIntelligence` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.25 | Generate AI insights such as predicted next visit, churn risk, preferred products, preferred attractions, lifetime value, and upsell recommendations. | F&B & Guest Management | CONTRACTED_PARTIAL | `getGuestIntelligence` |
| 5.4.22 | Identify customers at risk of disengagement. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 5.4.33 | AI provides personalized engagement and retention recommendations. | F&B & Guest Management | CONTRACTED | `getGuestIntelligence` |
| 22.2.22 | AI Guest Insights | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.23 | AI Churn Prediction | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.2.24 | AI Next Best Action | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.6.19 | AI Engagement Optimization | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.13 | AI Churn Prediction Segments | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |
| 22.14.14 | AI Upgrade Opportunities | Marketing & CRM | CONTRACTED | `getGuestIntelligence` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-832` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-832`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 16: Works in AI Engagement Optimization → Recommend relevant, sustainable engagement programs. Recommend challenge type, audience, difficulty, actions, reward and timing using historical behavior. Predict participation, completion …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-832?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-824`.
- [ ] Every gated control is gated: `GUEST_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-833` Gamification Analytics & Audit

**Measure challenge performance, cost and long-term effect. Report participant funnel, completion, points, rewards, redemption, cost, revenue and repeat visits. Compare challenges, audiences, venues, events, seasons, reward types and membership groups. Measure retention and engagement lift against appropriate baselines and show points/reward liability. Audit definitions, approvals, events, progress adjustments, reward postings, AI recommendations and exports. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 51 Board 11 - CMS, White-Label Content & SEO Figure 11. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 52**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block D · task VM-BO-833 |
| Who uses it | venue staff holding `MARKETING_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/engagement-support/gamification-analytics-audit-bo-833` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** How challenges perform and what they cost: participants, completion, points awarded, rewards redeemed, cost, attributed revenue, repeat visits, and the points liability, compared across challenges and audiences, with an audit of definitions, approvals and reward postings.

**Known correction pending (do not draw the wrong version)**

- **The purpose contains the pack's page footer and the next board's title ("Configuration Scope of Work / Version 1.0 51 Board 11 - CMS ...").** Why: Page bleed. *(source: screens/P08-venue-back-office.yaml#BO-833; Finance, Ledger & Tax · Reporting & Analytics)*
- **Gamification analytics duplicates the reporting area's loyalty dashboard.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-017; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| Refresh | toggle | off | — | `getDashboard` ?refresh |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **points liability**: Shown in money (base currency) and points, because unredeemed points are a liability finance tracks. *(source: contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*

**Data it reads**: `listLoyaltyProgrammes` (onLoad, Gamification analytics); `getKpiValues` (onLoad, Participation, loyalty/membership impact, retention); `getDashboard` (onLoad, Gamification analytics dashboard)

**Where the user goes next**

- → `BO-824` Gamification Command Center: *Back to Gamification Command Center*
- → `BO-827` Points & Activity Rules: *Points & Activity Rules*; carries `programmeId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gamification analytics audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gamification analytics audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gamification analytics audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gamification analytics audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `P16 ANL-017 Customer, Membership & Loyalty Pulse`: Same loyalty and gamification KPI codes.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Summer Splash Challenge · 12,480 participants · completion 31.20% · points liability AED 84,300.00 (8.43 m points)
  · repeat visits +6.10% vs control
```

#### Permissions

- `listLoyaltyProgrammes` → `MARKETING_VIEW` (read) · staff, guest
- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.4.1 | The system should have the ability to integrate and exchange client information with a loyalty point system which will manage the loyalty points credited on to the loyalty account as per the … | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |
| 5.4.8 | Loyalty program data can be shared with a third party partner thanks to an API. For example, venue has an agreement with the airplane company Etihad allowing Etihad loyalty program members to spend … | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |
| 5.4.29 | Expose APIs for loyalty integrations. | F&B & Guest Management | CONTRACTED | `listLoyaltyProgrammes` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-833` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-833`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 10
- Flow F253 *Marketing CRM Configuration Reference v1.0 board 10: Gamification Command Center*, step 18: Works in Gamification Analytics & Audit → Measure challenge performance, cost and long-term effect. Report participant funnel, completion, points, rewards, redemption, cost, revenue and repeat visits. Compare challenges, audiences, venues …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-833?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-824`, `BO-827`.
- [ ] Every gated control is gated: `MARKETING_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"activateChallenge": {"method":"POST","path":"/challenges/{challengeId}/activate","contract":"marketing-crm","summary":"Publish a draft challenge to guests","permission":"MARKETING_SEND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Challenge"},
"awardBadge": {"method":"POST","path":"/customers/{customerId}/badges","contract":"marketing-crm","summary":"Award a badge","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"customerId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"MarketingCustomerBadge","responds":"MarketingCustomerBadge"},
"createChallenge": {"method":"POST","path":"/challenges","contract":"marketing-crm","summary":"Define a challenge, mission or streak","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Challenge","responds":"Challenge"},
"createLoyaltyProgramme": {"method":"POST","path":"/loyalty/programmes","contract":"marketing-crm","summary":"Create a loyalty programme","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoyaltyProgramme","responds":"LoyaltyProgramme"},
"createReferral": {"method":"POST","path":"/referrals","contract":"marketing-crm","summary":"Issue a referral code","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Referral","responds":"Referral"},
"getChallenge": {"method":"GET","path":"/challenges/{challengeId}","contract":"marketing-crm","summary":"One challenge","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Challenge"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getGuestIntelligence": {"method":"GET","path":"/guests/{guestId}/intelligence","contract":"marketing-crm","summary":"Value, engagement, churn and propensity, with their reasons","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestIntelligence"},
"getGuestLoyalty": {"method":"GET","path":"/guests/{subjectId}/loyalty","contract":"marketing-crm","summary":"A guest's loyalty position","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":true}],"requestBody":null,"responds":"LoyaltyPosition"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getLoyaltyRules": {"method":"GET","path":"/loyalty/programmes/{programmeId}/rules","contract":"marketing-crm","summary":"Every rule a loyalty programme runs on","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"path","required":true}],"requestBody":null,"responds":"LoyaltyRuleSet"},
"listBadges": {"method":"GET","path":"/badges","contract":"marketing-crm","summary":"Badges a guest can be awarded","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listChallenges": {"method":"GET","path":"/challenges","contract":"marketing-crm","summary":"The venue's challenges","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLoyaltyCampaigns": {"method":"GET","path":"/loyalty/campaigns","contract":"marketing-crm","summary":"Time-boxed campaigns inside a programme","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"activeOn","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLoyaltyProgrammes": {"method":"GET","path":"/loyalty/programmes","contract":"marketing-crm","summary":"List loyalty programmes","permission":"MARKETING_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRewards": {"method":"GET","path":"/loyalty/rewards","contract":"marketing-crm","summary":"What points can be turned into","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setBadge": {"method":"PUT","path":"/badges","contract":"marketing-crm","summary":"Define a badge","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MarketingBadge","responds":"MarketingBadge"},
"setLoyaltyCampaign": {"method":"PUT","path":"/loyalty/campaigns","contract":"marketing-crm","summary":"Define a loyalty campaign and its window","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MarketingLoyaltyCampaign","responds":"MarketingLoyaltyCampaign"},
"setLoyaltyRules": {"method":"PUT","path":"/loyalty/programmes/{programmeId}/rules","contract":"marketing-crm","summary":"Replace a programme's rules as one set","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"programmeId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"LoyaltyRuleSet","responds":"LoyaltyRuleSet"},
"setReward": {"method":"PUT","path":"/loyalty/rewards","contract":"marketing-crm","summary":"Define a reward and its points cost","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MarketingReward","responds":"MarketingReward"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Challenge": {"type":"object","x-ticvai-persistence":"marketing.challenge","description":"BL-022, CF-137. **Section 22.6 is twenty requirements and 19.2.73–75 three more** — checked against the matrix on 18 August rather than assumed. It is asked for explicitly.\n**Gamification is not loyalty.** Loyalty pays for spend; a challenge pays for behaviour the venue wants and spend does not produce — a second visit, a quiet Tuesday, a ride nobody rides. **A challenge that only rewards spending is a loyalty programme with worse arithmetic.**\n","required":["id","name","kind","goal","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","description":"What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)): `scan` counts scans of a named code or point (a trail marker, a stand), `activity` counts completions of a named attraction or activity that is not a ride, and `purchase` counts purchases of named products or categories. **`purchase` is not `spend`**: `spend` counts money, whatever was bought; `purchase` counts items bought.\n","enum":["visit","spend","ride","collection","streak","referral","survey","social","milestone","scan","activity","purchase"]},"scope":{"type":"string","enum":["individual","family","group","team"],"default":"individual","description":"22.6.7 and 22.6.8. **A family challenge is not a per-person challenge counted twice** — members contribute toward one shared goal, and a school competing against another school is a group scoring against a group.\n**This is the field that needs the portfolio work** (CF-132): a family challenge without a family is an individual challenge with a label.\n"},"goal":{"type":"object","description":"What completes it.","properties":{"metric":{"type":"string"},"target":{"type":"number"},"withinDays":{"type":"integer","nullable":true}}},"eventId":{"type":"string","format":"uuid","nullable":true},"rewardKind":{"type":"string","enum":["badge","loyaltyPoints","walletCredit","voucher","entitlement","none"],"description":"22.6.13. **A reward that issues wallet credit is money**, and it goes through the same stored-value mechanism as everything else rather than a parallel one.\n"},"rewardValue":{"type":"integer","nullable":true,"minimum":1,"description":"**Points, for `rewardKind: loyaltyPoints` only.** A count, not an amount — a money reward is `rewardAmount`, never this.\n"},"rewardAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The credit, for `rewardKind: walletCredit` only.** The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the region, because a wallet credit is money and naming-and-style 5.1 forbids money as a bare number.\n"},"badgeAssetId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","nullable":true},"status":{"readOnly":true,"type":"string","enum":["draft","active","paused","ended","archived"]},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"GuestIntelligence": {"type":"object","description":"Board 1.10. **Explainable, or an agent will ignore it or over-trust it.**","properties":{"subjectId":{"type":"string","format":"uuid"},"scores":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["historicalLtv","predictedLtv","engagement","churnRisk","inactivityRisk","cancellationRisk","upgradePropensity","nextPurchasePropensity"]},"value":{"type":"number"},"band":{"type":"string","nullable":true},"confidence":{"type":"number","nullable":true},"modelId":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"computedAt":{"type":"string","format":"date-time"},"factors":{"type":"array","items":{"type":"object","properties":{"factor":{"type":"string"},"contribution":{"type":"number"}}}},"limitations":{"type":"array","items":{"type":"string"},"description":"**Policy and data limitations travel with the score**, so the rule that prediction never overrides consent cannot be forgotten downstream.\n"}}}},"affinities":{"type":"array","items":{"type":"object","properties":{"productCategoryId":{"type":"string","format":"uuid"},"label":{"type":"string"},"strength":{"type":"number"}}}},"nextBestActions":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"expectedImpact":{"type":"string","nullable":true},"confidence":{"type":"number","nullable":true}}}}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"LoyaltyProgramme": {"x-ticvai-persistence":"marketing.loyalty_programme + marketing.points_earning_rule + marketing.programme_tier","type":"object","required":["id","code","name","earnRules","tiers"],"properties":{"tiers":{"type":"array","description":"**Rows of `marketing.programme_tier`**, the same shape `MarketingProgrammeTier` has — one definition of a tier, not a second copy that cannot round-trip. `loyaltyProgrammeId` and `id` are the server's on create.\n","items":{"$ref":"#/components/schemas/MarketingProgrammeTier"}},"id":{"readOnly":true,"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused with `409 duplicate-code`.\n"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"pointsLiabilityAccountId":{"type":"string","format":"uuid","description":"Points post here on accrual. They are a liability from the moment they are earned, not from the moment they are spent.\n"},"earnRules":{"type":"array","items":{"type":"object","required":["trigger","points"],"properties":{"trigger":{"type":"string","enum":["perCurrencyUnit","perVisit","perProduct","onSignup","onBirthday","onReview"]},"points":{"type":"number"},"productKinds":{"type":"array","description":"Limits a `perProduct` or `perCurrencyUnit` rule to these kinds. Empty means every kind.","items":{"$ref":"../spine/catalogue.yaml#/components/schemas/ProductKind"}},"multiplier":{"type":"number"}}}},"pointsExpireAfterMonths":{"type":"integer","nullable":true},"isActive":{"type":"boolean"}}},
"LoyaltyRuleSet": {"type":"object","x-ticvai-persistence":"none — composed from the rule tables of one programme","description":"**Every rule a programme runs on, read and written as one thing.** Earning, redemption and campaign rules only make sense against each other: a 500-point redemption beside a 5-point earning rule is a hundred visits, and that ratio is the artefact being configured.\nEarning rules are not repeated here — they are `LoyaltyProgramme.earnRules[]` and reached through the programme, which is where they were already declared.\n","required":["programmeId"],"properties":{"programmeId":{"type":"string","format":"uuid"},"campaignRules":{"type":"array","description":"Bonus, multiplier and condition rules, each scoped to a campaign window.","items":{"$ref":"#/components/schemas/MarketingLoyaltyRule"}},"tiers":{"type":"array","description":"The programme's tiers, in `rank` order. **Read with the rules because a redemption rule that is tier-gated is meaningless without them** — 500 points off for Gold members is two facts, and reviewing one without the other is how a tier nobody can reach acquires a benefit.\n","items":{"$ref":"#/components/schemas/MarketingProgrammeTier"}},"redemptionRules":{"type":"array","items":{"$ref":"#/components/schemas/MarketingPointsRedemptionRule"}}}},
"MarketingBadge": {"type":"object","x-ticvai-persistence":"marketing.badge","description":"**Taken from the backend workbook, 20 September.** Defines a digital badge that can be awarded to a customer for challenge completion or other engagement achievement.","required":["code","name","type","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":150},"description":{"type":"string","maxLength":500,"nullable":true},"iconUrl":{"type":"string","maxLength":1000,"nullable":true},"type":{"type":"string","maxLength":30},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"MarketingCustomerBadge": {"type":"object","x-ticvai-persistence":"marketing.customer_badge","description":"**Taken from the backend workbook, 20 September.** Stores badges actually awarded to customers and the source that generated each award.","required":["customerId","badgeId","awardedAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"customerId":{"type":"string","format":"uuid"},"badgeId":{"type":"string","format":"uuid"},"challengeId":{"type":"string","format":"uuid","nullable":true},"sourceType":{"type":"string","maxLength":30,"nullable":true},"sourceReferenceId":{"type":"string","format":"uuid","nullable":true},"awardedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","maxLength":20}}},
"MarketingLoyaltyCampaign": {"type":"object","x-ticvai-persistence":"marketing.loyalty_campaign","description":"**Taken from the backend workbook, 20 September.** Links a marketing campaign to temporary loyalty bonuses, rewards, or earning changes.","required":["programId","code","name","startAt","endAt","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"programId":{"type":"string","format":"uuid"},"campaignId":{"type":"string","format":"uuid","nullable":true},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"startAt":{"type":"string","format":"date-time"},"endAt":{"type":"string","format":"date-time"},"isActive":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"MarketingLoyaltyRule": {"type":"object","x-ticvai-persistence":"marketing.loyalty_rule","description":"**Taken from the backend workbook, 20 September.** Defines temporary bonus points, multipliers, earning rules, or rewards applied by a loyalty campaign.","required":["campaignId","type","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"campaignId":{"type":"string","format":"uuid"},"type":{"type":"string","maxLength":30},"pointsEarningRuleId":{"type":"string","format":"uuid","nullable":true},"rewardId":{"type":"string","format":"uuid","nullable":true},"bonusPoints":{"type":"number","nullable":true},"multiplier":{"type":"number","nullable":true},"conditionsJson":{"type":"string","nullable":true},"isActive":{"type":"boolean"}}},
"MarketingPointsRedemptionRule": {"type":"object","x-ticvai-persistence":"marketing.points_redemption_rule","description":"**Taken from the backend workbook, 20 September.** Defines how loyalty points can be exchanged for discounts, products, or other benefits.","required":["loyaltyProgramId","pointRedemptionRuleCode","name","redemptionType","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"loyaltyProgramId":{"type":"string","format":"uuid"},"pointRedemptionRuleCode":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"redemptionType":{"type":"string","maxLength":30},"required":{"type":"number","nullable":true},"monetaryValue":{"type":"number","nullable":true},"minimumPoints":{"type":"number","nullable":true},"maximumPoints":{"type":"number","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"}}},
"MarketingProgrammeTier": {"type":"object","x-ticvai-persistence":"marketing.programme_tier","description":"**The tier definition decision 8 promised and nobody built.** `marketing.loyalty_position` carried `tierCode`, `tierName` and `pointsToNextTier` as denormalised strings and a number, with no table saying what tiers exist or what each one requires — so `pointsToNextTier` was computed from a threshold that lived nowhere.\n**Not named `marketing.loyalty_tier`**: that name is recorded in `schema-history.json` as renamed to `marketing.points_earning_rule` on 20 September, and a rename record that contradicts the schema is worse than a longer name. Not named `marketing.tier` either, because `subscription.tier_allowance` is a SaaS plan's tier and one bare `tier` in a package with two tier concepts is how `plan_id` came to point at `subscription.plan`.\n**The denormalised copy on the position stays.** A till rendering *Gold* beside a balance must not join, and must certainly not cross a cell boundary to print a word. This table is the source of truth and those columns are its cache.\n","required":["loyaltyProgrammeId","code","name","rank"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"loyaltyProgrammeId":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":120},"rank":{"type":"integer","description":"**Order, not threshold.** Two tiers can share a qualifying rule and still have an order, and sorting by points breaks the moment a tier is granted rather than earned.\n"},"minLifetimePoints":{"type":"integer","nullable":true,"description":"What reaching this tier requires. **`pointsToNextTier` on the position is this minus the guest's lifetime points**, and until now it was this minus nothing.\n"},"retainLifetimePoints":{"type":"integer","nullable":true,"description":"What keeping it requires, per review period. **Usually lower than reaching it**, and a scheme that cannot express the difference either never demotes or demotes on the day a guest stops earning.\n"},"validityMonths":{"type":"integer","nullable":true,"description":"Null means the tier does not lapse on its own."},"benefits":{"type":"array","description":"What the tier gives, as the guest reads it. Text shown, not rules enforced.","items":{"type":"string"}},"earnMultiplier":{"type":"number","nullable":true,"description":"Applied to every earn rule while the guest holds this tier. Null means 1."},"isActive":{"type":"boolean","default":true}}},
"MarketingReward": {"type":"object","x-ticvai-persistence":"marketing.reward","description":"**Taken from the backend workbook, 20 September.** Defines a loyalty reward that can be issued to eligible customers.","required":["loyaltyProgramId","code","name","type","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"loyaltyProgramId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"type":{"type":"string","maxLength":30},"productId":{"type":"string","format":"uuid","nullable":true},"pointsCost":{"type":"number","nullable":true},"discountValue":{"type":"number","nullable":true},"validityDays":{"type":"integer","nullable":true},"isActive":{"type":"boolean"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Referral": {"type":"object","x-ticvai-persistence":"marketing.referral","description":"BL-034. **No referrer, no reward, nothing anywhere.**\n**The reward fires on the referee's qualifying act, not on the sign-up**, because a referral that pays on registration pays for accounts rather than for guests.\n","required":["id","referrerSubjectId","code","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"referrerSubjectId":{"type":"string","format":"uuid"},"refereeSubjectId":{"readOnly":true,"type":"string","format":"uuid","nullable":true},"code":{"readOnly":true,"type":"string"},"status":{"readOnly":true,"type":"string","enum":["issued","registered","qualified","rewarded","expired","void"]},"qualifyingAction":{"type":"string","enum":["firstPurchase","firstVisit","membershipPurchase"]},"referrerRewardId":{"readOnly":true,"type":"string","format":"uuid","nullable":true},"refereeRewardId":{"readOnly":true,"type":"string","format":"uuid","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}}
}
```
