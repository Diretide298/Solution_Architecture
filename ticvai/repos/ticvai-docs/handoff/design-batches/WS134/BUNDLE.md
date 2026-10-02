# WS134 — F&B Backend Structure Module Sample Reference v1.0 board 1

**7 screens · 8 operations · 19 schemas · 6 permissions**

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
  `DEVICE_MANAGE, DEVICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW`. A control nobody can use must say so,
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

### Food, Beverage & Retail

Food & beverage, retail, rentals, inventory and procurement across the till (P04), the kitchen display (P15), the staff app (P06), Venue Management (P08), the guest web and app (P01/P02), the kiosk (P05) and the CMS (P13). COUNTER SERVICE (F108): the cashier takes the order on the Food & Drink board from the outlet's menu in force (sections in the outlet's order, option groups attached to the item), sends it to the kitchen, and only then charges — send to kitchen, then charge, for every POS F&B order (R261, upheld against the v2 frame by POSV2-4). The kitchen ticket is on the rail while the card is in the guest's hand; an unpaid sent order is cancelled while ordered or accepted and voided with a reason after (R125(3), R091(5)); the guest gets an order number, and the customer-facing status board (numbers only) is the kitchen display's KIT-007, mirrored on the till's queue (POSV2-7). TABLE SERVICE (F29, F80, F94): a party is seated with its covers, orders across the visit, courses are fired by the pass (DI-333, DI-407), the bill is printed and settled at the end and split by amount, covers, category, item or seat (DI-106); the client's table statuses are Available → Ordered → Table closed → Reserved with no cleaning status (DI-336); moving and merging tables stay on the staff app until after r2 (POSV2-8). GUEST ORDERING (F11, F48): a guest inside the venue orders in the app or web for pickup or delivery to a seat or a scanned location (DI-288, DI-291); F&B and retail are optional licensed modules completed inside TICVAI (DI-505), kept simple (DI-1091); no food without an admission ticket (DI-292); table reservations and the waitlist do not go through the cart and a dining deposit is a venue option, off by default (DI-1048, DI-1049, R077). KITCHEN (P15, F83, F88): TICVAI's own display on commodity screens (19 September, replacing the 31 July "integration point only", DI-077); one kitchen ticket per preparation station from the outlet's routing rules with a fallback display (DI-323); a fired timer counts up and resets per course, not shown for quick service (DI-334); displays are assigned to stations and filter by course, with no station-load tile in r1 (R277). 86 takes an item off sale on every till and guest menu immediately (R110(c)); guests always see "Sold out", never a missing dish. RETAIL (F17, F34, F51): scan and sell through the same cart, charge and payment as tickets and food (DI-795), one cart, one receipt and one QR per guest (DI-293); system stock per venue gates the sale (DI-294); returns by receipt or order number only in r1 (R139(c)), refund to the original tender with a reason code and note (DI-796, DI-797); Shop & Drop is paid online and collected on the way out (R236), a merchandise reservation lasts to the end of the visit day (R169, R215). TILL MONEY (F32, F73, F74, F87): the float is counted by denomination with note images and typed quantities (DI-775, DI-776, R229) while the hardware checks itself (DI-778); the close is a …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Send to kitchen | Put the order on the kitchen rail. On the till it always comes before Charge. | Fire, Fire order, Submit order, kitchen fires on payment | R261 / POSV2-4 / F108 step 3 |
| Charge | The till's single tender step (Payment, POS-005); the button reads "Charge AED 110.25". | Checkout (on staff screens), Pay now | F108 step 4 / screens/P04-point-of-sale.yaml#POS-021 |
| Fire / Hold (a course) | Kitchen-pass words for releasing or holding the next course of a table, and the "fired" timer. | using "fire" for sending an order from the till | DI-333 / DI-334 / DI-407 |
| Kitchen ticket | The slip on the kitchen display, one per preparation station. | Order (on the kitchen display), KOT | R210 |
| Ready · Served · Collected · Delivered | How an order reaches the guest; a server marks Served, a counter Collected, a runner Delivered (with the location). | Done, Complete, Bumped (as a status) | R125 / contracts/satellite/fnb.yaml#recordOrderHandover |
| Recall (kitchen) / Recall held sale (till) | Bring a mis-bumped kitchen ticket back to the rail; separately, bring a held cart back into a sale. Never "Recall" alone where both could apply. | Undo bump, Restore | contracts/satellite/fnb.yaml#recallKitchenTicket / POSV2-6 |
| Unavailable (86) / Sold out | Staff screens say "Unavailable" and may add "86"; guest screens say "Sold out". Immediate everywhere. | Out of stock (for food), Disabled, Hidden | R110 / contracts/satellite/fnb.yaml#getGuestMenu |
| Order type | Dine-in · Quick service · Takeaway · Delivery, chosen in the cart. | Service mode, Fulfilment source (on the till) | DI-789 / contracts/satellite/fnb.yaml#/components/schemas/ServiceMode |
| Covers | The number of guests at a table, entered when seating; drives split-by-covers. | Pax (except as a small suffix on the floor plan), Heads | DI-104 / contracts/satellite/fnb.yaml#openTableVisit |
| Vacant · Seated · Ordered · Bill requested · Table closed · … | Table statuses on every floor plan (till and staff app); "Table closed" is the client's word for after payment. | Cleaning, Needs clearing, Dirty | DI-336 / DI-792 |
| Till · Cash drawer | Staff copy may say "till" for the workstation; the cash drawer is the deposit box. | Terminal id as a heading, Deposit box (on staff screens) | R156 |
| Float · Count · Blind count · Variance | The opening float; the denomination count; the closing count made without seeing the expected cash; counted minus expected. | Expected in drawer, Discrepancy, Error | R080 / POSV2-3 |
| Cash out · Cash in · Safe drop | Taking cash out of the drawer mid-shift, adding change, and a supervisor moving cash to the safe with the cashier as witness. | Lift, Withdrawal (as button labels) | DI-274 / contracts/spine/shift.yaml#createCashMovement / … |
| Menu item · Merchandise item · Inventory item · SKU | The scoped product words; SKU is a variant's code, Product stays the sellable thing. | SKU as the item's name, Article | R131 |
| Stock on hand · Allocated · Available | Available is on hand minus allocated. | Inventory (as a number), Free stock | R171 / DI-361 |
| Requisition · Purchase order · Goods receipt · Transfer · … | The procurement and stock words, in that flow. | GRN as the only label, Indent | DI-341 / DI-348 / DI-362 / DI-363 |
| Shop & Drop | Bought and paid now, collected on the way out. | Click & collect | R236 |
| Check-out (rental) · Return (rental) | Handing equipment to the guest and taking it back. On the same screens payment is "Charge" or "Pay". | Checkout (for a handover), Check-in (for a return) | DI-758 / DI-765 |
| Deposit hold · Release · Capture | A refundable deposit held, given back in full, or partly kept for damage with the rest released. | Charge deposit, Refund deposit | DI-752 / R127 |
| Extension · Swap · Overdue · Late fee | The active-rental words; a quick swap restarts the clock, a late swap earns a free extension. | Renewal, Exchange (for a swap) | DI-761 / DI-762 / DI-764 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-727` | F&B Command Center | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-728` | Outlet Management | B–D | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-729` | Create / Edit Outlet | B–D | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-730` | Outlet Types & Templates | B–D | 10 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-731` | Operating Hours & Service Periods | B–D | 16 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-732` | POS & Device Assignment | B–D | 7 | 22 | 6 | 11 | 3 | 0 | — | notStarted (—) |
| `BO-733` | Service Channel Configuration | B–D | 0 | 33 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-728, BO-729, BO-730, BO-731, BO-733 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-727` F&B Command Center

**F&B Command Center**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Top KPI cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/f-b-command-center-bo-727` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-024): No operation returns outlet KPIs (sales, orders, preparation time, stock alerts) per outlet.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The F&B operations hub for the venue: today's sales, orders, average order value, open outlets, preparation times, unavailable items and alerts, opening the outlet screens. The only operation is the outlet list; every tile lacks a source.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Ten tiles (sales, orders, preparation time, stock alerts) with only listOutlets behind them. (CHG-WIR-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Today's Sales** (metric tile)

**Orders Today** (metric tile)

**Average Order Value** (metric tile)

**Open Outlets** (metric tile)

**Active POS** (metric tile)

**Orders in Preparation** (metric tile)

**Average Preparation Time** (metric tile)

**Unavailable Items** (metric tile)

**Critical Stock Alerts** (metric tile)

**Operational Alerts** (metric tile)

**Data it reads**: `listOutlets` (onLoad, F&B outlets)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-728` Outlet Management: *Outlet Management*
- → `BO-729` Create / Edit Outlet: *Create / Edit Outlet*; carries `outletId`
- → `BO-730` Outlet Types & Templates: *Outlet Types & Templates*
- → `BO-731` Operating Hours & Service Periods: *Operating Hours & Service Periods*
- → `BO-732` POS & Device Assignment: *POS & Device Assignment*
- → `BO-733` Service Channel Configuration: *Service Channel Configuration*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the record are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Today's Sales: 128
  Orders Today: 46
  Average Order Value: AED 12,400.00
  Open Outlets: 74
  Active POS: 19
  Orders in Preparation: 233
  Average Preparation Time: 3 h 20 min
  Unavailable Items: 11
  Critical Stock Alerts: 1
  Operational Alerts: 3
```

#### Permissions

- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** F&B dashboards are role-based: the F&B Director sees all outlets, an outlet manager sees only their own outlet. Detailed design of the role-based dashboards (Director vs. outlet-level roles) is still to be finalised. *(open · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions; 6. Open Items · DI-318)*
- F&B Command Center gives a real-time consolidated view across all outlets: total sales, orders, average order value, average preparation time, kitchen load, top-selling items, operational alerts, food cost and gross margin, with breakdowns by sales channel and by hour. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup; 4.10 F&B Stock, Wastage & Requisitions · DI-317)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-727` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-727`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 1: Opens F&B Command Center → F&B Command Center
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 branch at step 1 (expected): when Nothing has been set up on F&B Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F243 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-727?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-728`, `BO-729`, `BO-730`, `BO-731`, `BO-732`, `BO-733`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-728` Outlet Management

**Outlet Management (merged into BO-044 F&B Outlets).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/outlet-management-bo-728` |

**What the spec says about it.** **Merged into BO-044** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). BO-044 F&B Outlets is the outlet register and its create/edit form; the client pack's Outlet Management and Create / Edit Outlet are the same register (R276, DI-319; design-note corrections fnb-retail BO-044, BO-729). The outlet type and department (DEC-196) and the opening hours are edited on BO-044. **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-044, and nothing on it is built separately.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The venue's F&B and retail outlets: name, kind, zone, opening hours, stock location, cost centre. Outlets are configuration units for F&B and retail.

**Fixed on main** (the package already carries these; draw what it says): The table has no columns and there is no create or update operation. (CHG-SBO-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-044 while it opens. |
| Error (`?state=error`) | Could not open BO-044; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-044, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-044. |
| Permission denied (`?state=emptyNoAccess`) | As BO-044: shown when the caller lacks the access BO-044 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlets:
- name: Lagoon Grill
  kind: restaurant
  zone: Lagoon Zone
  hours: 11:00-17:30
  costCentre: CC-AUH-FNB-01
- name: Wave Shop
  kind: retail
  zone: Main Gate
  hours: 10:00-18:00
```

#### Permissions

**A refused user sees:** As BO-044: shown when the caller lacks the access BO-044 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retail store setup reuses the F&B department/venue/zone structure with department type "Retail" and the shop as a sub-department; retail needs no sub-classification (unlike fine dining vs. QSR) since operations are scan-and-sell. Inventory stays outlet-level. *(agreed · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-350)*
- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-728` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-728`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 2: Works in Outlet Management → Outlet Management

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-728?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-727`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-729` Create / Edit Outlet

**Create / Edit Outlet (merged into BO-044 F&B Outlets).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `outletId` (BO-727) · cold entry: Opened from BO-727 with the outlet picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/operations/create-edit-outlet-bo-729` |

**What the spec says about it.** **Merged into BO-044** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). BO-044 F&B Outlets is the outlet register and its create/edit form; the client pack's Outlet Management and Create / Edit Outlet are the same register (R276, DI-319; design-note corrections fnb-retail BO-044, BO-729). The outlet type and department (DEC-196) and the opening hours are edited on BO-044. **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-044, and nothing on it is built separately.

**From the Food, Beverage & Retail process.** The client pack's Create / Edit Outlet form: an outlet's identity, type, department and sub-department, cost centre, status and hours. For a shop, the same form with department type Retail and no sub-classification.

**Fixed on main** (the package already carries these; draw what it says): Binds createTable, updateTable, setSectionLayout and listMenus ("Create table" is the primary act) and neither createOutlet nor … (CHG-WIR-008); The same form as BO-044's Create/Save outlet. (CHG-SBO-021).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where are outlet type and department stored? The outlet has kind and cost centre only.** → Outlet type and department are fields on the outlet (DI-319). *(decided by Chinmay, 2026-10-02; DEC-196 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet type**: Fine dining, quick service, coffee… — the type switches features (no floor plan for quick service). Outlet type and department are fields on the outlet (DI-319). *(source: DI-319 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Department / sub-department / cost centre / status**: Department Food & Beverage (or Retail), sub-department is the outlet's name, cost centre picker, Active/Inactive. *(source: DI-319 / DI-350)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-044 while it opens. |
| Error (`?state=error`) | Could not open BO-044; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-044, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-044. |
| Permission denied (`?state=emptyNoAccess`) | As BO-044: shown when the caller lacks the access BO-044 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet:
  name: Oasis Bistro
  type: Fine dining
  department: Food & Beverage
  sub_department: Oasis Bistro
  cost_centre: CC-410 Lagoon F&B
  status: Active
```

#### Permissions

**A refused user sees:** As BO-044: shown when the caller lacks the access BO-044 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retail store setup reuses the F&B department/venue/zone structure with department type "Retail" and the shop as a sub-department; retail needs no sub-classification (unlike fine dining vs. QSR) since operations are scan-and-sell. Inventory stays outlet-level. *(agreed · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-350)*
- Operating hours and service periods (breakfast, lunch, dinner, late night) are defined per outlet so revenue can be analysed by time slot. Recipe-based stock depletion is set per outlet, real-time or end-of-day, by outlet type. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-320)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-729` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-729`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 4: Works in Create / Edit Outlet → Create / Edit Outlet

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-729?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-727`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-730` Outlet Types & Templates

**Outlet Types & Templates**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/outlet-types-templates-bo-730` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-008): The content table was bound to listMenus ("Menu items"); the templates list (listOutletTemplates, declared) is the screen (design-notes correction fnb-retail …

**From the Food, Beverage & Retail process.** Outlet templates: a starting configuration (type, service model, default menus, coursing, kitchen target, delivery policy) that a new outlet copies at creation. Changing a template never changes outlets already made from it.

**Known correction pending (do not draw the wrong version)**

- **createOutlet takes no template, although a template is what a new outlet "copies at creation".** Why: There is no way to create an outlet from a template. *(source: contracts/spine/tenancy.yaml#createOutlet / contracts/satellite/fnb.yaml#setOutletTemplate; Food, Beverage & Retail)*
- **apisNote says setOutletTemplate and listOutletTemplates are "still owed by a contract change".** Why: Both now exist in fnb.yaml; the note is stale. *(source: screens/P08-venue-back-office.yaml#BO-730; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The content table is bound to listMenus ("Menu items"), not listOutletTemplates. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet type | radio group | — | Restaurant · Bar · Cafe · Kiosk · Mobile | `listOutletTemplates` ?outletType |
| Include inactive | toggle | off | — | `listOutletTemplates` ?includeInactive |

**Sent by *+ Create Template*** (`setOutletTemplate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$` | — | — | `setOutletTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setOutletTemplate` body |
| Outlet type `outletType` | radio group | required | — | Restaurant · Bar · Cafe · Kiosk · Mobile | — | The F&B kinds of `tenancy.OutletKind`, repeated here because a satellite does not reference another contract's schema. | `setOutletTemplate` body |
| Service model `serviceModel` | multi-select chips | required | — | Quick service · Table service · Room service · Collection · Delivery; at least 1 | — | The service modes the outlet offers, e.g. `[tableService, collection]`. | `setOutletTemplate` body |
| Default menus `defaultMenuIds` | multi-picker: choose default menus | optional | — | at most 20 | — | — | `setOutletTemplate` body |
| Course rules `courseRules` | group | optional | — | — | — | The coursing default a new outlet starts with; the same shape `setCourseRules` stores per outlet. | `setOutletTemplate` body |
| Default coursing `courseRules.defaultCoursing` | radio group | optional | — | Fire and forget · Hold and fire · Phased · Timed · Delayed | — | How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock … | `setOutletTemplate` body |
| Kitchen sla minutes `kitchenSlaMinutes` | number field (minutes) | optional | — | min 1; max 240 | — | The default ticket target, in minutes, before `setKitchenSla` sets per-mode targets. | `setOutletTemplate` body |
| Delivery policy `deliveryPolicyId` | picker: choose a delivery policy | optional | — | — | shows names, sends the id | — | `setOutletTemplate` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setOutletTemplate` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Template**: Code unique per venue (letters, digits, - and _), name, outlet type (Restaurant, Bar, Café, Kiosk, Mobile), service model (one or more of Dine-in, Quick service, Takeaway, Delivery, Room service), default menus (up to 20, active only), kitchen target 1–240 min, delivery policy, active. *(source: contracts/satellite/fnb.yaml#setOutletTemplate)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| + Create Template (primary button) | `setOutletTemplate` PUT `/outlet-templates` | OutletTemplateInput | OutletTemplate | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 A `defaultMenuIds` entry that is not an active menu at this venue (`unknownMenu`), or a … | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Template list**: Name, type, service model, outlets created from it; ordered by name. *(source: contracts/satellite/fnb.yaml#listOutletTemplates)*

**Data it reads**: `listOutletTemplates` (onLoad, The outlet templates)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The outlet types templates list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the outlet types templates untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No outlet types templates yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the outlet types templates are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A `defaultMenuIds` entry that is not an active menu at this venue (`unknownMenu`), or a `deliveryPolicyId` that does not exist (`unknownDeliveryPolicy`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
templates:
- code: QSR-KIOSK
  name: Quick-service kiosk
  type: Kiosk
  service_model:
  - Quick service
  - Takeaway
  kitchen_target: 8 min
- code: FD-ROOM
  name: Fine-dining room
  type: Restaurant
  service_model:
  - Dine-in
  kitchen_target: 20 min
```

#### Permissions

- `listOutletTemplates` → `PRODUCT_VIEW` (read) · staff
- `setOutletTemplate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-730` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-730`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 6: Works in Outlet Types & Templates → Outlet Types & Templates

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 403, 412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-730?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: + Create Template, Cancel.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-731` Operating Hours & Service Periods

**Operating Hours & Service Periods**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REGION_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `outletId` (session) |
| Route | `/operations/operating-hours-service-periods-bo-731` |

**What the spec says about it.** **A late-night window is one window past midnight, marked "ends next day" (decided 2 October 2026 by Chinmay, DEC-197; CHG-CSP-007, `OpeningHoursWindow.endsNextDay`).**

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-008): The only operation was listKitchenTickets (the kitchen rail), nothing to do with hours or periods; opening hours are Outlet.openingHours, written by updateOutlet …

**From the Food, Beverage & Retail process.** Per outlet: the weekly opening hours and the service periods (breakfast, lunch, dinner, late night) that revenue is analysed by, and whether recipe stock depletes in real time or at end of day.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No service-period entity for revenue by time slot, and no per-outlet recipe depletion mode (real time or end of day). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The only operation bound is listKitchenTickets (the kitchen rail). (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is a late-night window that crosses midnight (23:00–01:00) entered? OpeningHoursWindow states no overnight rule.** → A late-night window is one window past midnight, marked 'ends next day'. *(decided by Chinmay, 2026-10-02; DEC-197 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

**Form: Save hours** (modal, opened by *Save hours*; *Save hours* calls `updateOutlet`, *Cancel* sends nothing)

**Collects what `updateOutlet` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateOutlet` body |
| Name translations `nameTranslations` | key and value settings | optional | — | localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. | — | The outlet's name in other languages, keyed by ISO 639-1 code (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: "Yes, where a country needs it: the local language plus … | `updateOutlet` body |
| Stock location `stockLocationId` | picker: choose a stock location | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Outlet type `outletType` | select | optional | — | Fine dining · Casual dining · Quick service · Coffee shop · Bar lounge · Food court · Buffet · Commissary · Retail | — | How an F&B or retail outlet trades, which switches features on or off (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: "Add both fields: outlet type and department … | `updateOutlet` body |
| Payment timing `paymentTiming` | segmented control | optional | Send first | Send first · Pay first | — | When an F&B order is paid, set per outlet (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). | `updateOutlet` body |
| Admission context `admissionContext` | segmented control | optional | — | Inside venue · Standalone | — | Whether an outlet sits behind the admission gate (decided 2 October 2026, Chinmay, batch 1, WEB-036: "Inside the venue, a ticket is needed. | `updateOutlet` body |
| Produces for outlets `producesForOutletIds` | multi-picker: choose produces for outlets | optional | — | — | — | Replaces the whole list of outlets this one produces for (CHG-CSP-005). | `updateOutlet` body |
| Sale board `saleBoardId` | picker: choose a sale board | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | Replaces the whole weekly pattern. An empty array clears it. | `updateOutlet` body |
| Day `openingHours[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `updateOutlet` body |
| From `openingHours[].from` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet opens. | `updateOutlet` body |
| To `openingHours[].to` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet closes. | `updateOutlet` body |
| Ends next day `openingHours[].endsNextDay` | toggle | optional | off | With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours. | — | A late-night window is one window past midnight (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). | `updateOutlet` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateOutlet` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 As `createOutlet`: a missing required local-language name (`local-name-required`), a window that ends before it starts (`window-ends-before-start`), or a …

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Opening hours**: Weekly windows per outlet, several per day, local HH:MM in the region time zone. A late-night window is one window past midnight, marked "ends next day" (23:00 to 01:00). *(source: contracts/spine/tenancy.yaml#/components/schemas/OpeningHoursWindow / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Service periods**: Named periods with days and times; today only expressible as each menu's availability window. *(source: DI-320 / contracts/satellite/fnb.yaml#/components/schemas/MenuAvailability)*

#### Outputs: what the screen shows and produces

**Shown**

**Outlets** (data table, from `listOutlets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005). |
| Name translations | grouped details | The outlet's name in other languages, keyed by ISO 639-1 code (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: "Yes, where a country … |
| Venue | the name it points at, never the id | — |
| Kind | chip: Shop, Restaurant, Bar, Cafe, Kiosk, Game floor… | — |
| Outlet type | chip: Fine dining, Casual dining, Quick service, Coffee shop, Bar lounge, Food court… | The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail. |
| Department | the name it points at, never the id | The department the outlet belongs to (DI-319: department, sub-department, cost centre and status; DEC-196; CHG-CSP-005): an `OrgUnit` of … |
| Zone | text | — |
| Stock location | the name it points at, never the id | Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not. |
| Cost center | the name it points at, never the id | Revenue and cost attribution. Outlet is the natural grain for both. |
| Payment timing | chip: Send first, Pay first | Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004). |
| Admission context | chip: Inside venue, Standalone | Inside the venue (needs an admission ticket) or standalone (no ticket) (DEC-070; CHG-CSP-004). |
| Produces for outlets | list or chips (count when long) | One kitchen serving several outlets is a producing outlet (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: "Yes: via a producing … |
| Sale board | the name it points at, never the id | The till layout every till in this outlet uses, unless a till overrides it (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: "Per … |
| Opening hours | list or chips (count when long) | The weekly pattern, one entry per window. Several windows on a day are allowed. |
| Day | chip: Mon, Tue, Wed, Thu, Fri, Sat… | — |
| From | text | Local time, 24-hour `HH:MM`, when the outlet opens. |
| To | text | Local time, 24-hour `HH:MM`, when the outlet closes. |
| Ends next day | yes / no (icon or chip) | A late-night window is one window past midnight (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save hours (secondary button) | `updateOutlet` PATCH `/outlets/{outletId}` | inline | Outlet | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `listOutlets` (onLoad, The outlets and their opening hours)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operating hours service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operating hours service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operating hours service yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operating hours service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 As `createOutlet`: a missing required local-language name (`local-name-required`), a window that ends before it starts (`window-ends-before-start`), or a … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlet: Oasis Bistro
hours:
- Mon–Thu 12:00–15:00, 18:00–23:00
- Fri–Sat 12:00–00:00
periods:
- name: Lunch
  from: '12:00'
  to: '15:00'
- name: Dinner
  from: '18:00'
  to: '23:00'
- name: Late night
  from: '23:00'
  to: 01:00
```

#### Permissions

- `listOutlets` → `SCOPE_VIEW` (read) · staff
- `updateOutlet` → `REGION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operating hours and service periods (breakfast, lunch, dinner, late night) are defined per outlet so revenue can be analysed by time slot. Recipe-based stock depletion is set per outlet, real-time or end-of-day, by outlet type. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-320)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-731` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-731`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 8: Works in Operating Hours & Service Periods → Operating Hours & Service Periods

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-731?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save hours.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `REGION_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-732` POS & Device Assignment

**POS & Device Assignment**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_MANAGE`, `DEVICE_VIEW`, `SCOPE_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Device cards/table) and no metric row |
| Offline | online only |
| Opens with | `deviceId` (session) |
| Route | `/operations/pos-device-assignment-bo-732` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Which till, printer and card terminal belong to which outlet and cashier in F&B. Assignment is per workstation.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 1 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Only listOutlets; nothing assigns a device. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |
| Workstation | picker: choose a workstation | — | — | `listDevices` ?workstationId |
| Kind | select | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | `listDevices` ?kind |

**Form: Assign device** (modal, opened by *Assign device*; *Assign device* calls `setDeviceAssignment`, *Cancel* sends nothing)

**Collects what `setDeviceAssignment` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Owner org unit `ownerOrgUnitId` | picker: choose an owner org unit | optional | — | — | shows names, sends the id | Who the device belongs to — the cost centre that replaces it when it breaks. | `setDeviceAssignment` body |
| Custodian principal `custodianPrincipalId` | picker: choose a custodian principal | optional | — | — | shows names, sends the id | Who is holding it right now. The fact a loss investigation needs. | `setDeviceAssignment` body |
| Assigned workstation `assignedWorkstationId` | picker: choose an assigned workstation | optional | — | — | shows names, sends the id | — | `setDeviceAssignment` body |
| Location scope path `locationScopePath` | text field | optional | — | — | — | — | `setDeviceAssignment` body |
| Asset tag `assetTag` | text field | optional | — | — | — | — | `setDeviceAssignment` body |
| Acquired at `acquiredAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | A calendar date in the region's time zone. | `setDeviceAssignment` body |
| Warranty expires at `warrantyExpiresAt` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | A calendar date in the region's time zone. | `setDeviceAssignment` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Every pos device** (data table)

| Shows | Format | Notes |
|---|---|---|
| Terminal outlet type cashier payment printer status | text | not in the schema: `Terminal Outlet Type Cashier Payment Printer Status` |

**Devices** (data table, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change … |
| Identifier | text | — |
| Workstation | the name it points at, never the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control … |
| Model | text | — |
| Hardware type | chip: Standard turnstile, Full height turnstile, Tripod turnstile, Speed gate, Wide lane … | The specific hardware under `kind` (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into … |
| Hardware model | the name it points at, never the id | The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it. |
| Serial number | text | The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). |
| Ip network reference | text | Network address or reference the device is reached at (ADR-0067). |
| Configuration version | text | Access configuration version the device reports running (ADR-0067). |
| Local rule version | text | Admission rule package the device reports running (ADR-0067). |
| Credential security package version | text | Credential security package the device reports running (ADR-0067). |
| Scanner health | text | Component health as the device or vendor reports it on its heartbeat (ADR-0067). |
| Controller health | text | — |
| Camera health | text | Where the device has a camera. |
| Connectivity | text | Reported connectivity. |
| Push token | text | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count … |
| Push platform | chip: Ios, Android, Web, Windows | — |

**The selected pos device** (detail panel): The pack groups this record's detail under its own headings: “Main”, “Restaurant”, “I would also display”.

| Shows | Format | Notes |
|---|---|---|
| Terminal outlet type cashier payment printer status | text | not in the schema: `Terminal Outlet Type Cashier Payment Printer Status` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign device (secondary button) | `setDeviceAssignment` PUT `/devices/{deviceId}/assignment` | DeviceAssignment | DeviceAssignment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `listOutlets` (onLoad, Outlet configuration); `listDevices` (onLoad, The tills, readers and printers that can be assigned)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pos device list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pos device untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pos device yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pos device are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listOutlets (Outlet):
- code: AQC-AUH
  name: AquaCove Abu Dhabi
  kind: standard
  isActive: true
- code: AQC-DXB
  name: Main Gate Till 3
  kind: standard
  isActive: true
```

#### Permissions

- `listOutlets` → `SCOPE_VIEW` (read) · staff
- `listDevices` → `DEVICE_VIEW` (read) · staff
- `setDeviceAssignment` → `DEVICE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.18 | POS and kiosk devices shall be linked to the Device Management module so administrators can monitor device status, location, software version, connectivity, errors, paper levels, and assigned … | Ticketing Sales | CONTRACTED | `listDevices` |
| 2.1.26 | System shall provide centralized monitoring of kiosk health including online status, stock levels, payment devices, printers, connectivity, and alerts. | Ticketing Sales | CONTRACTED | `listDevices` |
| 8.9.6 | System shall monitor scanners, POS devices, kiosks, handhelds, printers, gates, network connectivity, and infrastructure health. | Unified Operations Dashboard | CONTRACTED | `listDevices` |
| 16.2.7 | Device Inventory Management - System shall maintain device inventories. | Device Management | CONTRACTED | `listDevices` |
| 16.2.8 | Device Classification - System shall support device categorization. | Device Management | CONTRACTED | `listDevices` |
| 16.2.12 | Device Asset Tracking - System shall maintain device asset records. | Device Management | CONTRACTED | `listDevices` |
| 16.9.55 | Device APIs - System shall expose device management APIs. | Device Management | CONTRACTED | `listDevices` |
| 16.2.9 | Device Ownership - System shall maintain ownership records. | Device Management | CONTRACTED | `setDeviceAssignment` |
| 16.2.10 | Device Assignment - System shall support assignment of devices to users and locations. | Device Management | CONTRACTED | `setDeviceAssignment` |
| 16.2.11 | Device Location Tracking - System shall maintain device location records. | Device Management | CONTRACTED | `setDeviceAssignment` |
| 16.5.28 | Warranty Tracking - System shall track device warranties. | Device Management | CONTRACTED | `setDeviceAssignment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Retail POS/device assignment covers workstation name/code, receipt printer, barcode scanner and cash drawer; global retail settings include sales channels, primary/replenishment store and offline sales support. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-352)*
- POS & device management configures receipt printers, kitchen printers and KDS devices per outlet/terminal. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-321)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-732` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-732`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 10: Works in POS & Device Assignment → POS & Device Assignment
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-732?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Assign device.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `DEVICE_MANAGE`, `DEVICE_VIEW`, `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-733` Service Channel Configuration

**Service Channel Configuration**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/service-channel-configuration-bo-733` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-008): The table was bound to getKpiValues (no per-channel KPI is seeded) and setFnbReservationPolicy (table turn times) belongs to reservations; the screen could read … Removed 2 October 2026 (CHG-WIR-008): The table was bound to getKpiValues (no per-channel KPI is seeded) and setFnbReservationPolicy (table turn times) belongs to reservations; the screen could read …

**From the Food, Beverage & Retail process.** Per outlet, which sales channels the outlet sells on and which items each channel may sell (till, kiosk, QR table ordering, app, web), with the channel's own rules (menu, payment, guest login, minimum order).

**Known correction pending (do not draw the wrong version)**

- **The pack's channel list mixes channels and order types (POS Counter, Dine-In, Takeaway, Delivery, VIP / Hospitality).** Why: Order type is a separate dimension (ServiceMode); mixing them double-counts in channel reporting. *(source: contracts/shared/common.yaml#/components/schemas/SalesChannel; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): No channel-configuration operation exists; the table is bound to getKpiValues (no per-channel KPI is seeded), and setFnbReservationPolicy … (CHG-WIR-008); setFnbServiceChargePolicy is described as "the service charge per channel". (CHG-WIR-008).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Channel**: The platform's sales channels (Till, Kiosk, Guest app, Guest web, Call centre, Partner…). Dine-in, Takeaway and Delivery are order types, not channels. *(source: contracts/shared/common.yaml#/components/schemas/SalesChannel / contracts/satellite/fnb.yaml#/components/schemas/ServiceMode)*
- **Items per channel**: Enable or disable items per channel per outlet; the nearest existing mechanism is publishing a menu version to chosen channels. *(source: DI-322 / contracts/satellite/fnb.yaml#publishMenu)*

#### Outputs: what the screen shows and produces

**Shown**

**Service channels** (data table): POS Counter, Dine-In, QR Table Order, Mobile App, B2C Web, Kiosk, Takeaway, Delivery, VIP / Hospitality, Event Catering. The bound read is `getKpiValues`, which carries no channel configuration.

| Shows | Format | Notes |
|---|---|---|
| Channel | text | not in the schema: `Channel` |
| Status | text | not in the schema: `Status` |
| Available outlets | text | not in the schema: `Available outlets` |
| Menu | text | not in the schema: `Menu` |
| Price book | text | not in the schema: `Price book` |
| Payment | text | not in the schema: `Payment` |
| Guest login | text | not in the schema: `Guest login` |
| Operating hours | text | not in the schema: `Operating hours` |
| Maximum items per order | text | not in the schema: `Maximum items per order` |
| Minimum order | text | not in the schema: `Minimum order` |

**Service charge** (detail panel, from `getFnbServiceChargePolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Basis | chip: None, Percent of subtotal, Fixed per cover, Fixed per bill | `none` is a real answer and the default. A venue that does not levy one should say so, rather than leaving a null that reads as … |
| Rate percent | 1,234.5 | Set when `basis` is `percentOfSubtotal`. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Minimum party size | 1,234 | The common case for an automatic charge — parties of six and above. Null applies it to every cover. |
| Service types | list or chips (count when long) | A delivery order charged a dine-in service charge is a complaint. Empty means every service type. |
| Is taxable | yes / no (icon or chip) | Whether VAT applies to the charge itself. It does in the UAE, and a bill that taxes the subtotal but not the charge is understated. |
| Included in display price | yes / no (icon or chip) | Menu-price inclusive or added at the bill. The pair of this and `shownSeparately` is what a guest is entitled to see before ordering. |
| Shown separately | yes / no (icon or chip) | — |
| Is discretionary | yes / no (icon or chip) | Whether a guest may have it removed. A charge that cannot be declined is a price; a charge that can is a request, and the bill has to say … |
| Distribution | chip: Venue revenue, Staff pool, Split | Not a tip. `orders` separates `serviceCharge` from a gratuity because it is revenue in most jurisdictions and pooling the two is how a … |
| Staff pool percent | 1,234.5 | Set when `distribution` is `split`. |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | — |

**The selected channel rules** (detail panel): The pack's QR Table Ordering example (page 10).

| Shows | Format | Notes |
|---|---|---|
| Status | text | not in the schema: `Status` |
| Available outlets | text | not in the schema: `Available outlets` |
| Menu | text | not in the schema: `Menu` |
| Price book | text | not in the schema: `Price book` |
| Payment | text | not in the schema: `Payment` |
| Guest login | text | not in the schema: `Guest login` |
| Operating hours | text | not in the schema: `Operating hours` |
| Maximum items per order | text | not in the schema: `Maximum items per order` |
| Minimum order | text | not in the schema: `Minimum order` |

**Data it reads**: `getFnbServiceChargePolicy` (onLoad, The service charge in force)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The service channel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the service channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No service channel yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the service channel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
channels:
- channel: Till
  status: true
  outlets:
  - Bite & Go
  - Oasis Bistro
- channel: QR table ordering
  status: true
  outlets:
  - Pool Bar
  minimum_order: AED 30.00
  guest_login: Required
- channel: Kiosk
  status: false
```

#### Permissions

- `setFnbServiceChargePolicy` → `PRODUCT_CONFIGURE` (configure) · staff
- `getFnbServiceChargePolicy` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Service channel configuration enables/disables specific items per sales channel (POS, kiosk, QR ordering, online) per outlet. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-322)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-733` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-733`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 12: Works in Service Channel Configuration → Service Channel Configuration

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-733?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getFnbServiceChargePolicy": {"method":"GET","path":"/service-charge-policy","contract":"fnb","summary":"The service charge a venue applies, and on what","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"FnbServiceChargePolicy"},
"listDevices": {"method":"GET","path":"/devices","contract":"tenancy","summary":"List registered devices","permission":"DEVICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutletTemplates": {"method":"GET","path":"/outlet-templates","contract":"fnb","summary":"List outlet templates","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletType","in":"query","required":false},{"name":"includeInactive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutlets": {"method":"GET","path":"/outlets","contract":"tenancy","summary":"List outlets","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Outlet"},
"setDeviceAssignment": {"method":"PUT","path":"/devices/{deviceId}/assignment","contract":"tenancy","summary":"Who owns it, who holds it, and where it is","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"DeviceAssignment","responds":"DeviceAssignment"},
"setFnbServiceChargePolicy": {"method":"PUT","path":"/service-charge-policy","contract":"fnb","summary":"Set the service charge","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"FnbServiceChargePolicy","responds":"FnbServiceChargePolicy"},
"setOutletTemplate": {"method":"PUT","path":"/outlet-templates","contract":"fnb","summary":"Create or replace an outlet template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"OutletTemplateInput","responds":"OutletTemplate"},
"updateOutlet": {"method":"PATCH","path":"/outlets/{outletId}","contract":"tenancy","summary":"Amend an outlet","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Outlet"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"DeviceApprovalStatus": {"type":"string","description":"Whether a registered device may go into production (DEC-241, DEC-245; CHG-CSP-011). The model is `states/registered-device-approval.yaml`.\n","enum":["pendingApproval","approved","rejected"]},
"DeviceAssignment": {"type":"object","x-ticvai-persistence":"tenancy.device_assignment","description":"16.2.9 to 16.2.11. **Ownership, custody and location are three facts, not one.**","properties":{"deviceId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setDeviceAssignment`."},"ownerOrgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"Who the device belongs to — the cost centre that replaces it when it breaks."},"custodianPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**Who is holding it right now.** The fact a loss investigation needs."},"assignedWorkstationId":{"type":"string","format":"uuid","nullable":true},"locationScopePath":{"type":"string","nullable":true},"lastSeenLocation":{"type":"string","nullable":true,"readOnly":true,"description":"Reported by the heartbeat; distinct from where it is supposed to be."},"assetTag":{"type":"string","nullable":true},"acquiredAt":{"type":"string","format":"date","nullable":true,"description":"A calendar date in the region's time zone."},"warrantyExpiresAt":{"type":"string","format":"date","nullable":true,"description":"A calendar date in the region's time zone."},"assignedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"FnbServiceChargePolicy": {"type":"object","x-ticvai-persistence":"fnb.service_charge_policy","description":"**What the service charge on a bill is, and where it came from.** Every field here answers a question `fnb.sub_bill.service_charge` was being asked and could not answer.\n**Tax and service charge recompute per bill on a split** (`F29`), so the policy is resolved per bill rather than apportioned from the visit — which only works if there is a policy to resolve.","required":["basis","isTaxable","isDiscretionary","distribution"],"properties":{"id":{"type":"string","format":"uuid"},"basis":{"type":"string","enum":["none","percentOfSubtotal","fixedPerCover","fixedPerBill"],"description":"`none` is a real answer and the default. **A venue that does not levy one should say so**, rather than leaving a null that reads as unconfigured."},"ratePercent":{"type":"number","nullable":true,"description":"Set when `basis` is `percentOfSubtotal`."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"minimumPartySize":{"type":"integer","nullable":true,"description":"**The common case for an automatic charge** — parties of six and above. Null applies it to every cover."},"serviceTypes":{"type":"array","items":{"type":"string","enum":["dineIn","takeaway","delivery","roomService"]},"description":"**A delivery order charged a dine-in service charge is a complaint.** Empty means every service type."},"isTaxable":{"type":"boolean","description":"**Whether VAT applies to the charge itself.** It does in the UAE, and a bill that taxes the subtotal but not the charge is understated."},"includedInDisplayPrice":{"type":"boolean","description":"**Menu-price inclusive or added at the bill.** The pair of this and `shownSeparately` is what a guest is entitled to see before ordering."},"shownSeparately":{"type":"boolean"},"isDiscretionary":{"type":"boolean","description":"**Whether a guest may have it removed.** A charge that cannot be declined is a price; a charge that can is a request, and the bill has to say which."},"distribution":{"type":"string","enum":["venueRevenue","staffPool","split"],"description":"**Not a tip.** `orders` separates `serviceCharge` from a gratuity because it is revenue in most jurisdictions and pooling the two is how a payroll dispute starts. This is the field that carries the distinction into payroll."},"staffPoolPercent":{"type":"number","nullable":true,"description":"Set when `distribution` is `split`."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."},"endsNextDay":{"type":"boolean","default":false,"description":"**A late-night window is one window past midnight** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). A bar open 23:00 to 01:00 on Friday is `day: fri`, `from: '23:00'`, `to: '01:00'`, `endsNextDay: true`: one service period, and its takings belong to Friday's trading day, not split across two days. With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours.\n"}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200,"description":"The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005)."},"nameTranslations":{"$ref":"#/components/schemas/OutletNameTranslations"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"outletType":{"allOf":[{"$ref":"#/components/schemas/OutletType"}],"nullable":true,"description":"The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail."},"departmentId":{"type":"string","format":"uuid","nullable":true,"description":"**The department the outlet belongs to** (DI-319: department, sub-department, cost centre and status; DEC-196; CHG-CSP-005): an `OrgUnit` of kind department, as `Workstation.departmentId`. The outlet itself is the sub-department, so it needs no second field.\n"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"paymentTiming":{"allOf":[{"$ref":"#/components/schemas/OutletPaymentTiming"}],"default":"sendFirst","description":"Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004)."},"admissionContext":{"allOf":[{"$ref":"#/components/schemas/OutletAdmissionContext"}],"default":"insideVenue","description":"Inside the venue (needs an admission ticket) or standalone (no ticket) (DEC-070; CHG-CSP-004)."},"producesForOutletIds":{"type":"array","default":[],"description":"**One kitchen serving several outlets is a producing outlet** (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: \"Yes: via a producing outlet (one kitchen outlet produces for several)\"; DEC-188; CHG-CSP-005). The outlets this one prepares food for, in the same venue. The model stays per outlet (DI-330): each outlet keeps its own menu and stations, and an order at a listed outlet may route to this outlet's kitchen stations (fnb `KitchenStation`). Empty on an outlet that only produces for itself. An outlet may not list itself, an outlet of another venue (`422 outlet-not-in-venue`), or one that lists it back.\n","items":{"type":"string","format":"uuid"}},"saleBoardId":{"type":"string","format":"uuid","nullable":true,"description":"**The till layout every till in this outlet uses, unless a till overrides it** (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006). DI-326 puts the layout at the outlet; MATRIX 2.1.9 binds a board to a workstation. Both hold: a workstation with no board of its own (`ConfigureWorkstationRequest.saleBoardId` absent or null) uses this one, and `Workstation.saleBoardSource` says which applied.\n"},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletAdmissionContext": {"type":"string","description":"**Whether an outlet sits behind the admission gate** (decided 2 October 2026, Chinmay, batch 1, WEB-036: \"Inside the venue, a ticket is needed. A restaurant outside the venue (standalone) can sell without one\"; DEC-070; CHG-CSP-004). `insideVenue` (the default): a guest ordering food needs an admission ticket or a place inside, as DI-292 (14 August) decided. `standalone`: a restaurant outside the gate, which may sell takeaway and delivery (DI-1039) with no ticket. DI-292 is amended for standalone outlets only. The admission check itself stays in Access (ADR-0068). F&B keeps its own payment and its own receipt either way. **The canonical name** (2 October 2026, CHG-CLN-008): the field is `admissionContext` on the outlet and on F&B's guest `DiningOutlet`; common `OutletSiting` and the word \"siting\" are deprecated aliases of this.\n","enum":["insideVenue","standalone"]},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"OutletNameTranslations": {"type":"object","x-ticvai-persistence":"none — jsonb column on platform.outlet","description":"**The outlet's name in other languages, keyed by ISO 639-1 code** (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: \"Yes, where a country needs it: the local language plus English\"; DEC-031; CHG-CSP-005). `Outlet.name` stays the English name. Where the region requires a local name (`RegionSettings.localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. The same shape as catalogue's `LocalisedText` (DI-210).\n","additionalProperties":{"type":"string","maxLength":200}},
"OutletPaymentTiming": {"type":"string","description":"**When an F&B order is paid, set per outlet** (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). `sendFirst`, the default and R261's rule: the order goes to the kitchen, then the till charges (table service, and quick service where the venue wants the kitchen started while the guest pays). `payFirst`: the till charges before anything reaches the kitchen; an unpaid order at a `payFirst` outlet is never sent (`fnb.createFnbOrder`, `fnb.fireCourse`). Shared because the outlet (tenancy `Outlet`) holds it and F&B enforces it.\n","enum":["sendFirst","payFirst"],"default":"sendFirst"},
"OutletTemplate": {"type":"object","x-ticvai-persistence":"fnb.outlet_template","description":"**The configuration a new outlet is created from** (decided 29 September, readiness close-out; BO-730). New table. Copied into the outlet at creation and never linked after, so changing a template does not change existing outlets.\n","required":["id","code","name","outletType","serviceModel","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64,"x-ticvai-unique":"venue"},"name":{"type":"string","maxLength":200},"outletType":{"$ref":"#/components/schemas/OutletTemplateType"},"serviceModel":{"type":"array","items":{"$ref":"#/components/schemas/ServiceMode"}},"defaultMenuIds":{"type":"array","items":{"type":"string","format":"uuid"}},"courseRules":{"type":"object","nullable":true,"properties":{"defaultCoursing":{"$ref":"#/components/schemas/CoursingPolicy"}}},"kitchenSlaMinutes":{"type":"integer","nullable":true},"deliveryPolicyId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"The venue it belongs to; server-set."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"OutletTemplateInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setOutletTemplate` takes (decided 29 September, readiness close-out).","required":["code","name","outletType","serviceModel"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","x-ticvai-unique":"venue"},"name":{"type":"string","maxLength":200},"outletType":{"$ref":"#/components/schemas/OutletTemplateType"},"serviceModel":{"type":"array","minItems":1,"description":"The service modes the outlet offers, e.g. `[tableService, collection]`.","items":{"$ref":"#/components/schemas/ServiceMode"}},"defaultMenuIds":{"type":"array","maxItems":20,"items":{"type":"string","format":"uuid"}},"courseRules":{"type":"object","nullable":true,"description":"The coursing default a new outlet starts with; the same shape `setCourseRules` stores per outlet.","properties":{"defaultCoursing":{"$ref":"#/components/schemas/CoursingPolicy"}}},"kitchenSlaMinutes":{"type":"integer","minimum":1,"maximum":240,"nullable":true,"description":"The default ticket target, in minutes, before `setKitchenSla` sets per-mode targets."},"deliveryPolicyId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean","default":true}}},
"OutletTemplateType": {"type":"string","enum":["restaurant","bar","cafe","kiosk","mobile"],"description":"The F&B kinds of `tenancy.OutletKind`, repeated here because a satellite does not reference another contract's schema."},
"OutletType": {"type":"string","description":"**How an F&B or retail outlet trades, which switches features on or off** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: \"Add both fields: outlet type and department (DI-319)\"; DEC-196; CHG-CSP-005). DI-319: a quick-service outlet needs no table booking, a fine-dining outlet needs a table layout. `kind` stays the physical place (a shop, a restaurant, a kiosk); this is the service model inside it. `commissary` is a producing kitchen (DEC-186, DEC-188).\n","enum":["fineDining","casualDining","quickService","coffeeShop","barLounge","foodCourt","buffet","commissary","retail"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"},"approvalStatus":{"allOf":[{"$ref":"#/components/schemas/DeviceApprovalStatus"}],"default":"pendingApproval","readOnly":true,"description":"**A new device waits for approval before it may go live** (decided 2 October 2026, Chinmay, critical set 1, BO-196: \"Secure enrolment code + pending approval\"; DEC-241; CHG-CSP-011; MoM 15 September, DI-892, DI-906). Every device registers `pendingApproval`. It may enrol and be provisioned and tested, but `enrolDevice` refuses `active` until `approveDevice` approves it (`409 device-approval-required`). A separate axis from `enrolmentState`, which keeps its r1 values; the model is `states/registered-device-approval.yaml`.\n"},"enrolmentCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":12,"description":"**A one-time code the device must present to enrol** (DEC-241; CHG-CSP-011). Issued by `registerDevice` and returned once, in its response only; every later read returns null. The installer enters it on the device, and `enrolDevice` to `enrolled` must carry the same code before `enrolmentCodeExpiresAt` (`422 enrolment-code-invalid`). A device that never presents it never gets an identity, so a box plugged into the venue network cannot claim to be a reader.\n"},"enrolmentCodeExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the enrolment code stops working (24 hours after registration, proposed; client to correct)."},"testedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who recorded the device's acceptance test (`DeviceEnrolment.testResult` on the move to `provisioned`). The approver must be someone else (DEC-245).\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who approved the device into production, never the person who tested it** (decided 2 October 2026, Chinmay, critical set 1, BO-203: \"Approver must differ from the tester\"; DEC-245; CHG-CSP-011). `approveDevice` refuses the tester with `403 approver-is-tester`.\n"},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]}
}
```
