# P17-purchase-activation-01 — P17 · Purchase & Activation

**7 screens · 5 operations · 14 schemas · 4 permissions**

Platform P17 TICVAI Sign-up · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
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
  `PLATFORM_CELL_MANAGE, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `SGN-018` | Purchase / Trial Journey Selection | B | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `SGN-019` | Contract & Billing Cycle Selection | B | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-020` | Billing & Legal Entity Information | B | 29 | 2 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `SGN-021` | Payment Method & Settlement Setup | C | 34 | 0 | 6 | 17 | 1 | 0 | — | notStarted (—) |
| `SGN-022` | Order & Commercial Pricing Review | B | 0 | 10 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `SGN-023` | Commercial Agreement, Billable Definition & Customer Acceptance | B | 0 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `SGN-024` | Subscription Confirmation & Commercial Activation | B | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**SGN-018, SGN-019, SGN-021, SGN-022, SGN-023, SGN-024 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SGN-018` Purchase / Trial Journey Selection

**Determine how the customer enters the commercial activation journey.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | Block B · ticket #29376 (APP-SIGNUP-SGN-018) |
| Who uses it | public |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/purchase-trial-journey-selection-sgn-018` |

**What the spec says about it.** The self-service form of `ADM-409`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-021): setTrialConfiguration sets TICVAI's trial rules (PLATFORM_PLAN_MANAGE); the prospect chooses, TICVAI configures trials on ADM-413 (design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Choose a trial or a purchase to enter activation.

**Fixed on main** (the package already carries these; draw what it says): setTrialConfiguration (TICVAI's trial settings) on the prospect's choice. (CHG-WIR-021).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setTrialConfiguration: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setTrialConfiguration)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `SGN-011` Recommended Package Overview: *Back to Recommended Package Overview*
- → `SGN-019` Contract & Billing Cycle Selection: *Contract & Billing Cycle Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The purchase trial journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the purchase trial journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No purchase trial journey yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the purchase trial journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
choice: Start 30-day trial
alternative: Buy now
```

#### Permissions

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-018` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-011`, `SGN-019`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-019` Contract & Billing Cycle Selection

**Define the contractual duration and billing/reconciliation cycle.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | Block B · ticket #29391 (APP-SIGNUP-SGN-019) |
| Who uses it | public staff holding `PLATFORM_TENANT_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/purchase-activation/contract-billing-cycle-selection-sgn-019` |

**What the spec says about it.** The self-service form of `ADM-410`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Custom Term. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Contract duration and billing cycle.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: setSubscription (staff). (CHG-SOT-016)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Custom Term (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `SGN-018` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*
- → `SGN-020` Billing & Legal Entity Information: *Billing & Legal Entity Information*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contract billing cycle list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contract billing cycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contract billing cycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contract billing cycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed` … |

#### Edge cases to draw

- **setSubscription answers 409**: Show it as something the person can act on, not a failure: Downgrade conflicts with current usage. The response names every module and limit that would be violated. Or the subscription is `expired` and cannot be reactivated (`subscription-expired`, audit STATE-SUBSCRIPTION); start a new one. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 422**: Show it as something the person can act on, not a failure: `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed`, audit R214 (1)). Or the plan is a custom package private to another tenant (`plan-not-offered`, decided 29 September). *(source: contracts/satellite/subscription.yaml#setSubscription)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
term: 36 months
billing: monthly
```

#### Permissions

- `setSubscription` → `PLATFORM_TENANT_MANAGE` (configure) · staff, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-019` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Custom Term, Cancel.
- [ ] Every transition is wired: `SGN-018`, `SGN-020`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-020` Billing & Legal Entity Information

**Capture the company TICVAI will invoice and its trade licence and tax registration, in plain language, saved on the application.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | Block B · ticket #29392 (APP-SIGNUP-SGN-020) |
| Who uses it | public staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | configEditor (compact density): One record (the billing entity) entered and saved on the application; no population to list (CHG-SOT-017). |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/billing-legal-entity-information-sgn-020` |

**What the spec says about it.** The self-service form of `ADM-411`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** Removed 2 October 2026 (CHG-SOT-017, design-notes correction SGN-020): `createLegalEntity` is a tenant-scoped, staff-only ledger operation needing ACCOUNT_CONFIGURE, and a prospect on P17 has no … **No public upload for the trade licence and VAT certificate, and no operation amends a submitted application.** `createUpload` is staff-only, and the application is created once (SGN-002), so the …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The self-service twin of ADM-411 for a prospect buying TICVAI with no account yet: the same billing and legal entity details, in plain language, with save-and-resume. The prospect must understand why each item is asked (it prints on their tax invoice) and leave able to come back.

**Fixed on main** (the package already carries these; draw what it says): The screen calls createLegalEntity (a tenant-scoped, staff-only ledger operation needing the account-configuration permission), but a … (CHG-SOT-017).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the billing entity saved on the onboarding application (public) before verification?** → Drawn default stands (answer: "Yes: saved on the application; nothing provisioned until verified"): Yes; nothing is provisioned until verification passes. *(decided by Chinmay, 2026-10-02; DEC-223 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Company to be invoiced (legal name) | text area | optional | — | max length 300 | — | Prints on the tax invoice exactly as entered. **The commercial customer may differ from the operating venue** (the pack's "Commercial Customer ≠ Operating Venue"). | `BillingEntity.legalName` |
| Country | text field | optional | — | min length 2; max length 2 | — | Decides which documents are required (tenancy `RegionSettings`). | `BillingEntity.countryCode` |
| Trade licence number | text field | optional | — | max length 100 | — | — | `BillingEntity.tradeLicenceNumber` |
| Tax registration number (TRN) | text field | optional | — | max length 30 | — | Optional. Entering one makes the VAT certificate required (decided 2 October 2026, workbook Q210, DEC-210). | `BillingEntity.trn` |
| Billing address | text area | optional | — | max length 1000 | — | — | `BillingEntity.address` |
| Invoice email | email field | optional | — | — | name@example.ae | — | `BillingEntity.invoiceEmail` |

**Sent by *Save and continue*** (`submitOnboardingApplication`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `submitOnboardingApplication` body |
| Company name `companyName` | text field | required | — | — | — | — | `submitOnboardingApplication` body |
| Contact email `contactEmail` | email field | required | — | — | name@example.ae | — | `submitOnboardingApplication` body |
| Contact phone `contactPhone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `submitOnboardingApplication` body |
| Country code `countryCode` | text field | optional | — | — | — | — | `submitOnboardingApplication` body |
| Venue type template `venueTypeTemplateId` | picker: choose a venue type template | optional | — | — | shows names, sends the id | A water park and a theatre need different defaults, and asking a prospect to configure 300 settings from empty is asking them to leave. | `submitOnboardingApplication` body |
| Requested plan `requestedPlanId` | picker: choose a requested plan | optional | — | — | shows names, sends the id | — | `submitOnboardingApplication` body |
| Status `status` | select | required | — | Submitted · Verifying · Approved · Provisioning · Active · Rejected · Abandoned | — | — | `submitOnboardingApplication` body |
| Trial ends at `trialEndsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Trial is a state, not a plan. A tenant on trial has the plan they will pay for and a date by which they must — modelling it as a separate plan means migrating them at conversion … | `submitOnboardingApplication` body |
| Rejection reason `rejectionReason` | text field | optional | — | — | — | — | `submitOnboardingApplication` body |
| Provisioned tenant `provisionedTenantId` | picker: choose a provisioned tenant | optional | — | — | shows names, sends the id | — | `submitOnboardingApplication` body |
| Billing entity `billingEntity` | group | optional | — | — | — | The company to be invoiced, saved on the application before verification (Chinmay, 2 October, workbook Q209 and Q223; CHG-CSA-030). | `submitOnboardingApplication` body |
| Legal name `billingEntity.legalName` | text area | optional | — | max length 300 | — | — | `submitOnboardingApplication` body |
| Trade licence number `billingEntity.tradeLicenceNumber` | text field | optional | — | max length 100 | — | — | `submitOnboardingApplication` body |
| Trn `billingEntity.trn` | text field | optional | — | max length 30 | — | The tax registration number; entering one makes the VAT certificate required. | `submitOnboardingApplication` body |
| Country code `billingEntity.countryCode` | text field | optional | — | min length 2; max length 2 | — | — | `submitOnboardingApplication` body |
| Address `billingEntity.address` | text area | optional | — | max length 1000 | — | — | `submitOnboardingApplication` body |
| Invoice email `billingEntity.invoiceEmail` | email field | optional | — | — | name@example.ae | — | `submitOnboardingApplication` body |
| Documents `billingEntity.documents` | repeatable rows | optional | — | — | — | The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification. | `submitOnboardingApplication` body |
| Document type `billingEntity.documents[].documentType` | segmented control | optional | — | Trade licence · VAT certificate | — | — | `submitOnboardingApplication` body |
| File ref `billingEntity.documents[].fileRef` | text field | optional | — | — | — | — | `submitOnboardingApplication` body |
| Expiry date `billingEntity.documents[].expiryDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `submitOnboardingApplication` body |
| Verification status `billingEntity.documents[].verificationStatus` | radio group | optional | — | Missing · Uploaded · Verified · Rejected · Expired | — | — | `submitOnboardingApplication` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **billing company vs venue operator**: Same switch as ADM-411, phrased "The company paying TICVAI is different from the company running the venue." *(source: screens/P17-ticvai-signup.yaml#SGN-020 / DI-830)*
- **TRN and certificate**: Helper text "Shown on every tax invoice we send you"; upload accepts PDF, JPG or PNG. *(source: DI-830)*

#### Outputs: what the screen shows and produces

**Shown**

**Documents required** (detail panel, from `submitOnboardingApplication`): A trade licence always; a VAT certificate when a TRN is entered. Each shows missing, uploaded, verified, rejected or expired. **Nothing is provisioned until verification passes** (DEC-223).

| Shows | Format | Notes |
|---|---|---|
| Documents | list or chips (count when long) | The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification. |
| Missing documents | list or chips (count when long) | The documents the country's rule requires that are not yet uploaded and verified. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save and continue (primary button) | `submitOnboardingApplication` POST `/onboarding-applications` | OnboardingApplication | OnboardingApplication | — | — |
| Back (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **progress**: Step position in the purchase journey (after contract and billing cycle, before payment method). *(source: screens/P17-ticvai-signup.yaml#SGN-020)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save and continue**: Saves to the application and moves to payment method; leaving keeps what was entered. *(source: screens/P17-ticvai-signup.yaml#SGN-020)*

**Where the user goes next**

- → `SGN-019` Contract & Billing Cycle Selection: *Back to Contract & Billing Cycle Selection*
- → `SGN-021` Payment Method & Settlement Setup: *Payment Method & Settlement Setup*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The application as saved so far. |
| Error (`?state=error`) | Could not save. Names what failed; nothing typed is lost. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing entered yet. Says why each item is asked (it prints on the tax invoice) and that nothing is provisioned until it is verified. The prospect's answers are kept on their sign-up session and they can come back with a one-time code to "Continue saved setup" (decided 2 October 2026, DEC-167). |
| Permission denied (`?state=emptyNoAccess`) | Not applicable: a prospect holds no permission. A signed-out prospect without a saved setup is sent to SGN-001 to start or continue one. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **a returning prospect without access to the saved setup**: Offered "Continue saved setup" or "Sign in", as on the welcome step. *(source: screens/P17-ticvai-signup.yaml#SGN-020)*

#### Consistency with other screens

- Match `ADM-411`: Identical fields and validation; only the tone of the help text differs.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
billingCompany: Al Majaz Leisure Parks LLC · TRN 100398275100003 · Al Qasba, Sharjah · finance@almajazparks.ae
invoicing: Annual · card
```

#### Permissions

- `submitOnboardingApplication` → `TENANT_CONFIGURE` (configure) · public, prospect

**A refused user sees:** Not applicable: a prospect holds no permission. A signed-out prospect without a saved setup is sent to SGN-001 to start or continue one.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-020` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-020?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save and continue, Back.
- [ ] Every transition is wired: `SGN-019`, `SGN-021`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-021` Payment Method & Settlement Setup

**Configure how TICVAI collects its fees.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | Block C · task APP-SIGNUP-SGN-021 |
| Who uses it | public staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/payment-method-settlement-setup-sgn-021` |

**What the spec says about it.** The self-service form of `ADM-412`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). **Diverged from ADM-412 on 28 September; no longer `sameAs`.** ADM-412 gained the platform-staff tenant picker and grant step (audit R098), which does not apply to a prospect with no account and no tenant yet, so `tools/applied/apply-subscription-placement.py` no longer keeps the two in step. The payment-methods change of audit R275 (a) is applied here by hand.

**Known gaps.** **Payment Method & Settlement Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Payment method and settlement during sign-up. After Block A.

**Known correction pending (do not draw the wrong version)**

- **The purpose says how TICVAI collects its fees, but the only operation is setPaymentProvider (the venue's own gateway for guest payments).** Why: Two different things; the screen needs the operation that sets the customer's billing method, or a new purpose. *(source: screens/P17-ticvai-signup.yaml#SGN-021 purpose; screens/P17-ticvai-signup.yaml#SGN-021 gaps; Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Payment methods | multi select | — | — | — | — | **The methods follow the contract (decided 28 September, audit R275 (a))**: the options are the `PaymentProvider.supportedMethods` enum that `setPaymentProvider` accepts. The pack's Credit / Debit … | — |

**Sent by *Save payment provider*** (`setPaymentProvider`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Name `name` | text field | required | — | — | — | — | `setPaymentProvider` body |
| Kind `kind` | select | required | — | Network international · Stripe · Adyen · Checkout · Cash · Wallet · Other | — | — | `setPaymentProvider` body |
| Supported methods `supportedMethods` | multi-select chips | optional | — | Card · Apple pay · Google pay · Samsung pay · Wallet · Bank transfer · Cash · Bnpl | — | — | `setPaymentProvider` body |
| Supported currencies `supportedCurrencies` | list of values (chips) | optional | — | — | — | — | `setPaymentProvider` body |
| Supports tokenisation `supportsTokenisation` | toggle | optional | — | — | — | The keystone. Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them can be designed until this is answered … | `setPaymentProvider` body |
| Supports partial capture `supportsPartialCapture` | toggle | optional | on | — | — | — | `setPaymentProvider` body |
| Accepted on channels `acceptedOnChannels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | BL-115. Which channels may use this provider. | `setPaymentProvider` body |
| Presentment currencies `presentmentCurrencies` | list of values (chips) | optional | — | — | — | BL-070. What a storefront may quote in, distinct from what it settles in. | `setPaymentProvider` body |
| Supports3ds `supports3ds` | toggle | optional | on | — | — | — | `setPaymentProvider` body |
| Terminal `terminal` | group | optional | — | — | — | BL-119. Terminal behaviour, where this provider drives a physical device. | `setPaymentProvider` body |
| Emv certification ref `terminal.emvCertificationRef` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Offline floor limit `terminal.offlineFloorLimit` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What a terminal may approve with no connection. Above it the sale waits; below it the venue carries the risk knowingly — and a floor limit of zero means a till stops when the line … | `setPaymentProvider` body |
| Supports offline approval `terminal.supportsOfflineApproval` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Receipt signature required `terminal.receiptSignatureRequired` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Supports tip on terminal `terminal.supportsTipOnTerminal` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Credential ref `credentialRef` | text field | optional | — | — | — | A vault reference. Never the credential, never returned, and rotated without a contract change. | `setPaymentProvider` body |
| Scope level `scopeLevel` | segmented control | optional | — | Tenant · Region · Venue | — | — | `setPaymentProvider` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setPaymentProvider` body |
| Routing `routing` | repeatable rows | optional | — | — | — | The ordered rules that send payments to this provider. `providerId` on each is this provider's `id`. | `setPaymentProvider` body |
| ID `routing[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Priority `routing[].priority` | number field | required | — | — | — | — | `setPaymentProvider` body |
| Provider `routing[].providerId` | picker: choose a provider | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Conditions `routing[].conditions` | group | optional | — | — | — | Match on what is known before the charge — channel, currency, method, issuer country, amount band. | `setPaymentProvider` body |
| Channel `routing[].conditions.channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `setPaymentProvider` body |
| Currency `routing[].conditions.currency` | text field | optional | — | Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. | — | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per … | `setPaymentProvider` body |
| Method `routing[].conditions.method` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Issuer country `routing[].conditions.issuerCountry` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Min amount `routing[].conditions.minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPaymentProvider` body |
| Max amount `routing[].conditions.maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPaymentProvider` body |
| Fallback provider `routing[].fallbackProviderId` | picker: choose a fallback provider | optional | — | — | shows names, sends the id | Where this provider declines or is unreachable. A decline is not always a fallback case — an insufficient-funds decline should not be retried elsewhere, and a gateway timeout … | `setPaymentProvider` body |
| Scope path `routing[].scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `setPaymentProvider` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save payment provider (primary button) | `setPaymentProvider` PUT `/payment-providers` | SetPaymentProviderRequest | PaymentProvider | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |

**Where the user goes next**

- → `SGN-020` Billing & Legal Entity Information: *Back to Billing & Legal Entity Information*
- → `SGN-022` Order & Commercial Pricing Review: *Order & Commercial Pricing Review*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment method settlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment method settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment method settlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment method settlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
methods:
- card
- bankTransfer
```

#### Permissions

- `setPaymentProvider` → `TENANT_CONFIGURE` (configure) · staff, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.3 | Integrate with Stripe payment gateway and issue ticket and send confirmation email immediately after payment confirmation. | Ticketing Sales | CONTRACTED | `setPaymentProvider` |
| 4.2.9 | The system should be able to process payments by integrating with Stripe payment service provider. | Bundles and Promotions | CONTRACTED | `setPaymentProvider` |
| 2.6.33 | Website should be able to display multi currency and users should be able to switch the prices to the selected foreign currency. All the ticket prices, currency symbol to be shown based on the … | Ticketing Sales | CONTRACTED | data `PaymentProvider` |
| 2.9.1 | The system should display prices in multiple currencies in the B2C portal for guests comparison although the sale will be finalized always in local currency. | Ticketing Sales | CONTRACTED | data `PaymentProvider` |
| 4.2.10 | The system should support multiple different payments. The final list of payment methods will be dependent on the capabilities of the payment service provider. System should allow the admin team to … | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.12 | The system should support configuration of variable payment methods for different sales channels. Payment methods can be different from one sales channel to another. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.14 | The system shall support integration with multiple payment gateways through a unified payment layer, allowing the business to switch or add gateways without changing business logic or sales channels. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.15 | The system shall automatically select the most appropriate payment gateway based on configurable rules such as country, currency, sales channel, transaction amount, gateway availability, and … | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.16 | The system shall support secure tokenization of payment cards through PCI-compliant providers, allowing guests to securely save and reuse payment methods for future purchases. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.3.28 | Automatically reload balances. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.3.29 | Support recurring funding. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 5.7.100 | The system shall support PCI-compliant integration architecture and secure payment processing. Sensitive cardholder information shall not be stored unless specifically certified and authorized. … | F&B & Guest Management | CONTRACTED | data `PaymentProvider` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-021` · status **notStarted** · provenance —
- Workshop pack:  board 5
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (34), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save payment provider.
- [ ] Every transition is wired: `SGN-020`, `SGN-022`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-022` Order & Commercial Pricing Review

**Show the complete financial arrangement before contractual acceptance. This screen must adapt dynamically to the commercial model. Example — Per Ticket + Minimum Guarantee**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | Block B · ticket #29395 (APP-SIGNUP-SGN-022) |
| Who uses it | public staff holding `PLATFORM_TENANT_VIEW` (1 read) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/purchase-activation/order-commercial-pricing-review-sgn-022` |

**What the spec says about it.** The self-service form of `ADM-414`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The complete financial arrangement before acceptance, adapted to the commercial model (e.g. per ticket plus minimum guarantee), with discounts and who approved them.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: previewSubscriptionChange (staff). (CHG-SOT-016)
- The table's columns are the workshop pack's labels with no bound response field (0 of 5 labels bound). (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every order commercial pricing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Discount type | text | not in the schema: `Discount Type` |
| Value | text | not in the schema: `Value` |
| Period | text | not in the schema: `Period` |
| Approved by | text | not in the schema: `Approved By` |
| Expiry | text | not in the schema: `Expiry` |

**The selected order commercial pricing** (detail panel): The pack groups this record's detail under its own headings: “Rate”, “Expected Volume”, “Included Modules”, “Technical Capacity”, “Show where applicable”.

| Shows | Format | Notes |
|---|---|---|
| Discount type | text | not in the schema: `Discount Type` |
| Value | text | not in the schema: `Value` |
| Period | text | not in the schema: `Period` |
| Approved by | text | not in the schema: `Approved By` |
| Expiry | text | not in the schema: `Expiry` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Value)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `previewSubscriptionChange` (onLoad, Order and pricing review)

**Where the user goes next**

- → `SGN-021` Payment Method & Settlement Setup: *Back to Payment Method & Settlement Setup*
- → `SGN-023` Commercial Agreement, Billable Definition & Customer Acceptance: *Commercial Agreement, Billable Definition & Customer Acceptance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order commercial pricing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order commercial pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order commercial pricing yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order commercial pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every order commercial pricing:
- Discount Type: 233
  Value: AED 12,400.00
  Period: 57
  Approved By: Rahul Menon
  Expiry: 57
- Discount Type: 57
  Value: AED 482,300.00
  Period: 11
  Approved By: Fatima Al Mansoori
  Expiry: 11
- Discount Type: 11
  Value: AED 96,750.00
  Period: 128
  Approved By: Omar Haddad
  Expiry: 128
```

#### Permissions

- `previewSubscriptionChange` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.5 | Subscription Upgrade - System shall support subscription upgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |
| 20.2.6 | Subscription Downgrade - System shall support subscription downgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-022` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-021`, `SGN-023`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-023` Commercial Agreement, Billable Definition & Customer Acceptance

**This becomes one of the most important revised screens. The customer must understand and formally accept what TICVAI considers billable.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | Block B · ticket #29393 (APP-SIGNUP-SGN-023) |
| Who uses it | public staff holding `PLATFORM_CELL_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/purchase-activation/commercial-agreement-billable-definition-customer-accept-sgn-023` |

**What the spec says about it.** The self-service form of `ADM-415`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The commercial agreement and what TICVAI counts as billable, accepted formally by the customer with name, role and time.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: setAgreementContractTerm (partner). (CHG-SOT-016)
- The table's columns are the workshop pack's labels with no bound response field (0 of 8 labels bound). (CHG-SOT-016)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial agreement billable** (data table)

| Shows | Format | Notes |
|---|---|---|
| Commercial model | text | not in the schema: `Commercial Model` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Guarantee period | text | not in the schema: `Guarantee Period` |
| Billing cycle | text | not in the schema: `Billing Cycle` |
| Contract duration | text | not in the schema: `Contract Duration` |
| Renewal | text | not in the schema: `Renewal` |
| Payment terms | text | not in the schema: `Payment Terms` |

**The selected commercial agreement billable** (detail panel): The pack groups this record's detail under its own headings: “For a transaction contract”, “For a per-ticket contract”, “Customer confirms”.

| Shows | Format | Notes |
|---|---|---|
| Commercial model | text | not in the schema: `Commercial Model` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Guarantee period | text | not in the schema: `Guarantee Period` |
| Billing cycle | text | not in the schema: `Billing Cycle` |
| Contract duration | text | not in the schema: `Contract Duration` |
| Renewal | text | not in the schema: `Renewal` |
| Payment terms | text | not in the schema: `Payment Terms` |

**Where the user goes next**

- → `SGN-022` Order & Commercial Pricing Review: *Back to Order & Commercial Pricing Review*
- → `SGN-024` Subscription Confirmation & Commercial Activation: *Subscription Confirmation & Commercial Activation*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial agreement billable list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial agreement billable untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial agreement billable yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial agreement billable are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every commercial agreement billable:
- Commercial Model: 128
  Contracted Rate: 94%
  Minimum Guarantee: AED 12,400.00
  Guarantee Period: AED 96,750.00
  Billing Cycle: AED 96,750.00
  Contract Duration: 1.8 s
  Renewal: 11
  Payment Terms: 233
- Commercial Model: 46
  Contracted Rate: 87%
  Minimum Guarantee: AED 482,300.00
  Guarantee Period: AED 12,400.00
  Billing Cycle: AED 12,400.00
  Contract Duration: 3 h 20 min
  Renewal: 128
  Payment Terms: 57
- Commercial Model: 312
  Contracted Rate: 71%
  Minimum Guarantee: AED 96,750.00
  Guarantee Period: AED 482,300.00
  Billing Cycle: AED 482,300.00
  Contract Duration: 42 min
  Renewal: 46
  Payment Terms: 11
```

#### Permissions

- `setAgreementContractTerm` → `PLATFORM_CELL_MANAGE` (configure) · partner, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After accepting (or negotiating and re-proposing) a commercial model, the purchase agreement captures billing cycle, contract period, invoicing frequency (monthly/annually), legal entity information and payment method (bank transfer, card, etc.). *(client request · MoM 10 Sep 2026, 4.10 Purchase Agreement, Billing Terms & Trial/Demo Environment · DI-830)*

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-023` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `SGN-022`, `SGN-024`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SGN-024` Subscription Confirmation & Commercial Activation

**Create the formal active subscription/contract record after successful validation.**

| | |
|---|---|
| App · platform | TICVAI Control · P17 TICVAI Sign-up (web) |
| Module | Purchase & Activation · wave 3 · needs the `core` module |
| Block | Block B · ticket #29398 (APP-SIGNUP-SGN-024) |
| Who uses it | public staff holding `PLATFORM_TENANT_MANAGE` (1 configure) |
| Device and orientation | This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/purchase-activation/subscription-confirmation-commercial-activation-sgn-024` |

**What the spec says about it.** The self-service form of `ADM-417`, for a prospect with no account. Decided 11 September 2026; P09 keeps its screen for the operator-led path (BL-165). `tools/applied/apply-subscription-placement.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The subscription is created after validation; the first plan is active and renews one term from start.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A sign-up screen calls operations a prospect cannot call: setSubscription (staff). (CHG-SOT-016)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save subscription (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Confirmation**: Plan, start date, renewal date (one term from start), first invoice date and what happens next (provisioning). *(source: R214)*

**Where the user goes next**

- → `BO-594` Environment Ready & Handoff to AI Setup: *Environment Ready & Handoff to AI Setup*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription confirmation commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription confirmation commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription confirmation commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription confirmation commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed` … |

#### Edge cases to draw

- **setSubscription answers 409**: Show it as something the person can act on, not a failure: Downgrade conflicts with current usage. The response names every module and limit that would be violated. Or the subscription is `expired` and cannot be reactivated (`subscription-expired`, audit STATE-SUBSCRIPTION); start a new one. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 422**: Show it as something the person can act on, not a failure: `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed`, audit R214 (1)). Or the plan is a custom package private to another tenant (`plan-not-offered`, decided 29 September). *(source: contracts/satellite/subscription.yaml#setSubscription)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plan: Enterprise v1
starts: 01/11/2026
renews: 01/11/2027
firstInvoice: 01/12/2026
```

#### Permissions

- `setSubscription` → `PLATFORM_TENANT_MANAGE` (configure) · staff, prospect

**A refused user sees:** TODO — not decided. A prospect is signed out and holds no permission, so the operator wording on the P09 twin does not apply. The book offers *Continue Saved Setup* and *Sign In* on 2.1, which is where somebody without access to a saved setup would be sent; no minute has decided it.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |

#### Client meeting inputs

None names this screen.

Also apply: 10 for all of P17, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P17 TICVAI Sign-up.dc.html#sgn-024` · status **notStarted** · provenance —
- Workshop pack:  board 5

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SGN-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save subscription, Cancel.
- [ ] Every transition is wired: `BO-594`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P17 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for finish.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P17 TICVAI Sign-up

- The TICVAI marketing site should showcase demo versions of each platform (POS, kiosk, mobile app, menu management). *(client request · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1024)*
- Small/medium venues (e.g. 2 POS, 2 access points, basic B2C site) see pricing, subscribe and start configuring within a few days with no sales involvement; large/enterprise prospects stay sales-assisted (demo, consultative scoping) and enterprise-tier pricing is not exposed through self-service. *(agreed · MoM 10 Sep 2026, 4.9 Sales-Assisted vs. Self-Service Segmentation Philosophy · DI-829)*
- On top of the trade-license review, the applicant confirms access to the submitted domain email (link or OTP, 2FA-style) before portal access. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-828)*
- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Gap (Allam): screens don't show how a prospect logs into a secure portal to view their proposed package; account credentials (user ID and password) are created once onboarding is submitted so the prospect can access and track the proposal. *(client request · MoM 10 Sep 2026, 4.7 Package Builder & Module Marketplace · DI-826)*
- Prospect onboarding: a short questionnaire (venue type, user count, expected annual visitors, modules such as B2C, B2B, seat assignment) via a website/AI-assisted flow; small/medium venues auto-classified and self-configure via AI-assisted setup; enterprise routed to a sales-assisted demo. *(client request · MoM 9 Sep 2026, 4.19 Licensing & Subscription Model - Preliminary Concept · DI-807)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Small-customer self-service subscription flow: select required modules, pay online, enter venue and business details, environment is provisioned automatically, then the customer configures products, tickets, users and venue information and starts using the system. *(client request · MoM 28 Jul 2026, 6. Two Deployment and Commercial Models · DI-011)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"previewSubscriptionChange": {"method":"POST","path":"/tenants/{tenantId}/subscription/preview","contract":"subscription","summary":"Preview the effect of a plan change","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"SubscriptionPreview"},
"setAgreementContractTerm": {"method":"PUT","path":"/agreement-contract-term","contract":"subscription","summary":"Agreement & Contract Terms Builder","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AgreementContractTermsBuilderInput","responds":"AgreementContractTermsBuilderView"},
"setPaymentProvider": {"method":"PUT","path":"/payment-providers","contract":"orders","summary":"Configure a gateway and its routing","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"SetPaymentProviderRequest","responds":"PaymentProvider"},
"setSubscription": {"method":"PUT","path":"/tenants/{tenantId}/subscription","contract":"subscription","summary":"Assign or change a subscription","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"Subscription"},
"submitOnboardingApplication": {"method":"POST","path":"/onboarding-applications","contract":"subscription","summary":"A prospect signs themselves up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OnboardingApplication","responds":"OnboardingApplication"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AgreementContractTermsBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_agreement (PartnerAgreement), a new version per amendment; documents are control.partner_document rows with agreementId; legalEntity, commercialOwner and financeOwner land in legalEntityId, commercialOwnerPrincipalId and financeOwnerPrincipalId (data model DM4)","description":"**What Agreement & Contract Terms Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"agreementId":{"type":"string","format":"uuid","description":"Agreement ID; omit to create"},"agreementName":{"type":"string","description":"Agreement Name"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementType":{"type":"string","description":"Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"},"contractReference":{"type":"string","description":"Contract Reference"},"legalEntity":{"type":"string","description":"Legal Entity"},"brandId":{"type":"string","description":"Brand id","nullable":true},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Venues the agreement covers"},"territory":{"type":"string","description":"Territory"},"settlementCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Settlement currency, ISO 4217"},"validFrom":{"type":"string","format":"date","description":"Effective From"},"validTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"renewalType":{"type":"string","enum":["manual","auto"],"description":"Renewal Type"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff principal id"},"financeOwner":{"type":"string","description":"Finance Owner: staff principal id"},"creditTermDays":{"type":"integer","description":"Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"},"commissionTerms":{"type":"string","description":"Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)","nullable":true},"pricingBasis":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Basis (pack p.27 pricing models)"},"creditTerms":{"type":"string","description":"Credit Terms","nullable":true},"allocationTerms":{"type":"string","description":"Allocation Terms","nullable":true},"cancellationConditions":{"type":"string","description":"Cancellation Conditions","nullable":true},"bookingRestrictions":{"type":"string","description":"Booking Restrictions","nullable":true},"settlementTerms":{"type":"string","description":"Settlement Terms","nullable":true},"minimumCommitment":{"type":"integer","description":"Minimum Commitment: tickets over the agreement term","nullable":true},"salesTarget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales Target over the agreement term"},"renewalNoticeDays":{"type":"integer","description":"Renewal Notice Period in days","nullable":true},"renegotiationRequired":{"type":"boolean","description":"Renegotiation Required"},"renewalRequiresApproval":{"type":"boolean","description":"Renewal Approval: renewal needs approval"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode","description":"Net rate or commission, as on PartnerAgreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"refundConditions":{"type":"string","description":"Refund Conditions (pack p.26)","nullable":true},"agreementValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"},"documents":{"type":"array","description":"Document Association","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["signedContract","addendum","rateSheet","sla","nda","commercialAnnex"]},"documentId":{"type":"string","format":"uuid"}}}}}},
"AgreementContractTermsBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_agreement and control.partner_document and the existing subscription state, assembled at read time (data model DM4)","description":"**What Agreement & Contract Terms Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"agreementId":{"type":"string","format":"uuid","description":"Agreement ID; omit to create"},"agreementName":{"type":"string","description":"Agreement Name"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementType":{"type":"string","description":"Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"},"contractReference":{"type":"string","description":"Contract Reference"},"legalEntity":{"type":"string","description":"Legal Entity"},"brandId":{"type":"string","description":"Brand id","nullable":true},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Venues the agreement covers"},"territory":{"type":"string","description":"Territory"},"settlementCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Settlement currency, ISO 4217"},"validFrom":{"type":"string","format":"date","description":"Effective From"},"validTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"renewalType":{"type":"string","enum":["manual","auto"],"description":"Renewal Type"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff principal id"},"financeOwner":{"type":"string","description":"Finance Owner: staff principal id"},"creditTermDays":{"type":"integer","description":"Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"},"commissionTerms":{"type":"string","description":"Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)","nullable":true},"pricingBasis":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Basis (pack p.27 pricing models)"},"creditTerms":{"type":"string","description":"Credit Terms","nullable":true},"allocationTerms":{"type":"string","description":"Allocation Terms","nullable":true},"cancellationConditions":{"type":"string","description":"Cancellation Conditions","nullable":true},"bookingRestrictions":{"type":"string","description":"Booking Restrictions","nullable":true},"settlementTerms":{"type":"string","description":"Settlement Terms","nullable":true},"minimumCommitment":{"type":"integer","description":"Minimum Commitment: tickets over the agreement term","nullable":true},"salesTarget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales Target over the agreement term"},"renewalNoticeDays":{"type":"integer","description":"Renewal Notice Period in days","nullable":true},"renegotiationRequired":{"type":"boolean","description":"Renegotiation Required"},"renewalRequiresApproval":{"type":"boolean","description":"Renewal Approval: renewal needs approval"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode","description":"Net rate or commission, as on PartnerAgreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"refundConditions":{"type":"string","description":"Refund Conditions (pack p.26)","nullable":true},"agreementValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"},"documents":{"type":"array","description":"Document Association","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["signedContract","addendum","rateSheet","sla","nda","commercialAnnex"]},"documentId":{"type":"string","format":"uuid"}}}},"version":{"type":"integer","description":"Agreement version; amendments create a new one"},"status":{"$ref":"#/components/schemas/PartnerAgreementStatus","description":"Agreement status"}}},
"BillingEntity": {"type":"object","x-ticvai-persistence":"control.billing_entity","description":"**The company TICVAI invoices for a tenant, with its trade licence and VAT certificate** (Chinmay, 2 October, workbook Q209: \"a new billing-entity record in the subscription contract\"; DI-830; CHG-CSA-030). One per tenant, mastered in the control plane. `legalName` and `countryCode` are required on save (400 otherwise); they are not marked required here so the record can ride, optional, on an onboarding application. **Documents** (workbook Q210, the default): a trade licence always; a VAT certificate when a `trn` is entered. Which documents a country requires is configurable per country (tenancy `RegionSettings`); the default is that rule.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null while it rides on an onboarding application."},"legalName":{"type":"string","maxLength":300},"tradeLicenceNumber":{"type":"string","maxLength":100,"nullable":true},"trn":{"type":"string","maxLength":30,"nullable":true,"description":"The tax registration number; entering one makes the VAT certificate required."},"countryCode":{"type":"string","minLength":2,"maxLength":2},"address":{"type":"string","maxLength":1000,"nullable":true},"invoiceEmail":{"type":"string","format":"email","nullable":true},"documents":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification.","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["tradeLicence","vatCertificate"]},"fileRef":{"type":"string","nullable":true},"expiryDate":{"type":"string","format":"date","nullable":true},"verificationStatus":{"type":"string","enum":["missing","uploaded","verified","rejected","expired"]}}}},"missingDocuments":{"type":"array","readOnly":true,"description":"The documents the country's rule requires that are not yet uploaded and verified.","items":{"type":"string"}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CellTier": {"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},
"DowngradeConflictProblem": {"x-ticvai-persistence":"none — error shape","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Problem"},{"type":"object","properties":{"modulesInUse":{"type":"array","description":"Enabled by the tenant but not licensed by the target plan.","items":{"type":"object","properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"}}}},"limitsExceeded":{"type":"array","items":{"type":"object","properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"currentUsage":{"type":"integer"},"targetLimit":{"type":"integer"}}}}}}]},
"OnboardingApplication": {"type":"object","x-ticvai-persistence":"control.onboarding_application","description":"BL-165. **`subscription` handles the operator-led path well and has no prospect-led one.** `createTenant` and `provisionCell` assume somebody at Softlabs decided this tenant exists.\nA prospect signing themselves up is a different shape: **nothing is provisioned until they are verified**, because an unverified application that provisions a cell is a cell somebody has to clean up.\n","required":["id","companyName","contactEmail","status"],"properties":{"id":{"type":"string","format":"uuid"},"companyName":{"type":"string"},"contactEmail":{"type":"string","format":"email"},"contactPhone":{"type":"string","nullable":true},"countryCode":{"type":"string"},"venueTypeTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"**A water park and a theatre need different defaults**, and asking a prospect to configure 300 settings from empty is asking them to leave.\n"},"requestedPlanId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["submitted","verifying","approved","provisioning","active","rejected","abandoned"]},"trialEndsAt":{"type":"string","format":"date-time","nullable":true,"description":"**Trial is a state, not a plan.** A tenant on trial has the plan they will pay for and a date by which they must — modelling it as a separate plan means migrating them at conversion, which is the moment least worth adding risk to.\n"},"rejectionReason":{"type":"string","nullable":true},"provisionedTenantId":{"type":"string","format":"uuid","nullable":true},"billingEntity":{"$ref":"#/components/schemas/BillingEntity","description":"**The company to be invoiced, saved on the application before verification** (Chinmay, 2 October, workbook Q209 and Q223; CHG-CSA-030). Nothing is provisioned until the application is verified; on provisioning it becomes the tenant's billing entity (`getBillingEntity`)."}}},
"PartnerAgreementStatus": {"type":"string","enum":["pendingApproval","active","expiringSoon","expired","suspended","terminated"]},
"PartnerRateMode": {"type":"string","description":"**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n","enum":["netRate","commission"]},
"PaymentProvider": {"type":"object","x-ticvai-persistence":"payments.provider","description":"BL-116, CF-131. **`Payment` carried `providerName` and `providerReference`, which records a provider and does not abstract one.**\nTwo gateways are confirmed for Phase 1 — **Network International and Stripe** — and that is exactly the number that forces this: **one gateway can be hard-coded and two cannot.**\nCredentials live in the vault and never here, following `ai.AiProvider` (ADR-0020's rule applied outside AI): **no surface ever holds a provider key.**\n","required":["id","name","kind","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["networkInternational","stripe","adyen","checkout","cash","wallet","other"]},"supportedMethods":{"type":"array","items":{"type":"string","enum":["card","applePay","googlePay","samsungPay","wallet","bankTransfer","cash","bnpl"]}},"supportedCurrencies":{"type":"array","items":{"type":"string"}},"supportsTokenisation":{"type":"boolean","description":"**The keystone.** Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them can be designed until this is answered per provider.\n"},"supportsPartialCapture":{"type":"boolean","default":true},"acceptedOnChannels":{"type":"array","description":"BL-115. **Which channels may use this provider.** A kiosk taking cash and a website taking cards is not a policy either could infer, and a venue that accepts cash at a till and not online had no way to say so.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"presentmentCurrencies":{"type":"array","description":"BL-070. **What a storefront may quote in**, distinct from what it settles in. A guest sees GBP and the venue books AED — the display currency is the provider's capability and the settlement currency is the venue's (CF-114 on multi-currency).\n","items":{"type":"string"}},"supports3ds":{"type":"boolean","default":true},"terminal":{"type":"object","nullable":true,"description":"BL-119. **Terminal behaviour, where this provider drives a physical device.** Unstated until now, and every field here is one a certification body asks about.\n","properties":{"emvCertificationRef":{"type":"string","nullable":true},"offlineFloorLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What a terminal may approve with no connection.** Above it the sale waits; below it the venue carries the risk knowingly — and a floor limit of zero means a till stops when the line does.\n"},"supportsOfflineApproval":{"type":"boolean","default":false},"receiptSignatureRequired":{"type":"boolean","default":false},"supportsTipOnTerminal":{"type":"boolean","default":false}}},"credentialRef":{"type":"string","writeOnly":true,"description":"A vault reference. **Never the credential**, never returned, and rotated without a contract change.\n"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string"},"isActive":{"type":"boolean"}}},
"PaymentRouting": {"type":"object","x-ticvai-persistence":"payments.routing_rule","description":"**Which provider takes a given payment, and why.** With two gateways the question is live from day one: a UAE card may cost less through one and an international card less through the other.\n**Ordered rules, first match wins, and a fallback that is not optional.** A gateway outage with no fallback is a venue that cannot sell.\n","required":["id","priority","providerId"],"properties":{"id":{"type":"string","format":"uuid"},"priority":{"type":"integer"},"providerId":{"type":"string","format":"uuid"},"conditions":{"type":"object","description":"**Match on what is known before the charge** — channel, currency, method, issuer country, amount band. Not on anything that requires asking the provider first.\n","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"currency":{"type":"string","nullable":true,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"method":{"type":"string","nullable":true},"issuerCountry":{"type":"string","nullable":true},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"fallbackProviderId":{"type":"string","format":"uuid","nullable":true,"description":"**Where this provider declines or is unreachable.** A decline is not always a fallback case — an insufficient-funds decline should not be retried elsewhere, and a gateway timeout should.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SetPaymentProviderRequest": {"x-ticvai-persistence":"none — request only; the provider lands in payments.provider and its rules in payments.routing_rule","description":"Request only. **A provider and the rules that route to it**, because `setPaymentProvider` is *\"configure a gateway and its routing\"* and writes both tables — and the provider schema alone carried no routing field, so the routing half had nothing to arrive in.\n","allOf":[{"$ref":"#/components/schemas/PaymentProvider"},{"type":"object","properties":{"routing":{"type":"array","description":"The ordered rules that send payments to this provider. `providerId` on each is this provider's `id`.","items":{"$ref":"#/components/schemas/PaymentRouting"}}}}]},
"SetSubscriptionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["planId"],"properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string","description":"Defaults to the current version."},"effectiveFrom":{"type":"string","format":"date","description":"Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1))."},"prorate":{"type":"boolean","default":true,"description":"An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). Kept so a preview can show the unprorated figure; `setSubscription` applies the rule whatever is sent."},"note":{"type":"string","maxLength":500}}},
"Subscription": {"x-ticvai-persistence":"subscription.contract","type":"object","required":["tenantId","planId","planVersion","status","startsAt"],"properties":{"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"planVersion":{"type":"string"},"status":{"type":"string","enum":["trial","active","pastDue","cancelled","expired"]},"startsAt":{"type":"string","format":"date"},"renewsAt":{"type":"string","format":"date","nullable":true},"cancelledAt":{"type":"string","format":"date","nullable":true},"scheduledChange":{"type":"object","nullable":true,"readOnly":true,"description":"A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.","properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string"},"effectiveFrom":{"type":"string","format":"date","description":"Always the `renewsAt` it was scheduled against."}}},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string"}}},
"SubscriptionPreview": {"x-ticvai-persistence":"none — computed","type":"object","required":["canApply","priceChange"],"properties":{"canApply":{"type":"boolean"},"priceChange":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proratedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"modulesGained":{"type":"array","items":{"type":"string"}},"modulesLost":{"type":"array","items":{"type":"string"}},"conflicts":{"$ref":"#/components/schemas/DowngradeConflictProblem"},"cellTierChange":{"type":"object","nullable":true,"properties":{"from":{"$ref":"#/components/schemas/CellTier"},"to":{"$ref":"#/components/schemas/CellTier"},"requiresMigration":{"type":"boolean"}}}}}
}
```
