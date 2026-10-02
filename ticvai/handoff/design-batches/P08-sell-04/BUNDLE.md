# P08-sell-04 — P08 · Sell (4 of 4)

**7 screens · 15 operations · 27 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `AUDIT_VIEW, DEVICE_VIEW, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, TENANT_CONFIGURE, WORKSTATION_CONFIGURE`. A control nobody can use must say so,
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
| `BO-122` | POS Experience Dashboard | B–D | 3 | 12 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-123` | POS Profile Management | B–D | 9 | 12 | 6 | 0 | 3 | 0 | — | notStarted (generated) |
| `BO-124` | Layout & Journey Builder | A | 38 | 22 | 6 | 9 | 2 | 6 | — | notStarted (generated) |
| `BO-125` | Product & Category Button Configuration | B–D | 19 | 6 | 6 | 14 | 3 | 0 | — | notStarted (generated) |
| `BO-126` | Deployment, Preview & Audit | B–D | 23 | 47 | 5 | 2 | 0 | 0 | — | notStarted (generated) |
| `BO-142` | Store Rules, Controls & Permissions | B–D | 11 | 9 | 6 | 0 | 1 | 5 | — | notStarted (generated) |
| `BO-143` | Retail Global Settings & Controls | B–D | 10 | 10 | 5 | 0 | 2 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-142, BO-143 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-122` POS Experience Dashboard

**See how each sale board performs on the tills.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSaleBoards` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/pos-experience-dashboard` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-024): No operation reports sales and errors per sale board.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How the POS estate is doing for the venue: boards in use, tills per board, and the experience signals (sale speed, errors) the client board shows. As wired it is only a list of sale boards.

**Fixed on main** (the package already carries these; draw what it says): Purpose is "POS Experience Dashboard — from the client design board, 20 August" and the only operation is listSaleBoards. (CHG-WIR-023); Tables show every schema field, plumbing included: 'Every sale board' drop id, venueId. (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listSaleBoards`. | `listSaleBoards` ?venueId |
| Kind | radio group | optional | — | Ticketing · Fnb · Retail · Mixed | — | Sends `?kind=` to `listSaleBoards`. | `listSaleBoards` ?kind |
| Search pos experience dashboard | search field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Every sale board** (data table, from `listSaleBoards`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**The selected sale board** (detail panel, from `listSaleBoards`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Data it reads**: `listSaleBoards` (onLoad, List sale boards)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pos experience list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pos experience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pos experience yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind and the pos experience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listSaleBoards` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
boards:
- code: TKT-MAIN
  name: Ticketing - Main Gate
  kind: ticketing
  tills: 8
  active: true
- code: FNB-LAGOON
  name: Lagoon Grill
  kind: fnb
  tills: 3
  active: true
```

#### Permissions

- `listSaleBoards` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listSaleBoards` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-122` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 5.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 5.dc.html#ret-5j`
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-122?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-123` POS Profile Management

**Define the configuration profiles that workstations are assigned.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TENANT_CONFIGURE` (1 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSaleBoards` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/pos-profile-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The configuration profiles tills are assigned: a venue defines a profile (sale board, input mode, guest display, terminal toggles, offline policy) once, and workstations are assigned it, so forty tills do not drift.

**Fixed on main** (the package already carries these; draw what it says): Purpose is a placeholder ("from the client design board, 20 August"). (CHG-WIR-023); formSetConfigurationProfile asks the person for status, id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every sale board' drop id, venueId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listSaleBoards`. | `listSaleBoards` ?venueId |
| Kind | radio group | optional | — | Ticketing · Fnb · Retail · Mixed | — | Sends `?kind=` to `listSaleBoards`. | `listSaleBoards` ?kind |
| Search pos profile management | search field | — | — | — | — | — | — |

**Form: Save configuration profile** (modal, opened by *Save configuration profile*; *Save configuration profile* calls `setConfigurationProfile`, *Cancel* sends nothing)

**Collects what `setConfigurationProfile` sends before it is called.** Required: `name`, `venueKindScope`. Optional: `scopePath`, `settings`, `deployedCount`, `publishedAt`. **Not asked:** `id` is a client UUIDv7 generated silently; `status` is set by the server (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setConfigurationProfile` body |
| Name `name` | text field | required | — | — | — | — | `setConfigurationProfile` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setConfigurationProfile` body |
| Venue kind scope `venueKindScope` | list of values (chips) | required | — | — | — | Which workstation types it applies to. A ticketing counter and a kitchen display do not share a profile, and a profile that claims to is a profile somebody deploys to the wrong … | `setConfigurationProfile` body |
| Settings `settings` | key and value settings | optional | — | — | — | — | `setConfigurationProfile` body |
| Status `status` | select | required | — | Draft · Published · Deploying · Deployed · Superseded · Rolled back | — | On input only `draft` or `published`; sending `published` publishes this version. | `setConfigurationProfile` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Profile**: Defined at venue (tenant default inherited); saving creates a new version that is deployed separately; terminal toggles (printer, offline continuity, prompts, guest display, key sounds, training mode) live here. *(source: contracts/spine/tenancy.yaml#setConfigurationProfile; DI-800; ADR-0018)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setConfigurationProfile: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setConfigurationProfile)*

#### Outputs: what the screen shows and produces

**Shown**

**Every sale board** (data table, from `listSaleBoards`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**The selected sale board** (detail panel, from `listSaleBoards`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save configuration profile (primary button) | `setConfigurationProfile` PUT `/configuration-profiles` | ConfigurationProfile | ConfigurationProfile | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |

**Data it reads**: `listSaleBoards` (onLoad, List sale boards)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pos profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pos profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pos profile yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind and the pos profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listSaleBoards` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds SCOPE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for Save configuration profile. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#setConfigurationProfile)*

#### Consistency with other screens

- Match `BO-126`: Deploying a profile version.
- Match `POS-016`: The till shows its assigned profile read-only.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  name: Ticketing till - Abu Dhabi
  version: 7
  saleBoard: Ticketing - Main Gate
  inputMode: hybrid
  trainingMode: false
  offlineContinuity: true
```

#### Permissions

- `setConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff
- `listSaleBoards` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listSaleBoards` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Terminal settings as business-optional toggles: printer, offline continuity, screen prompts, guest-facing display, key sounds, training mode. *(client request · MoM 9 Sep 2026, 4.17 POS Prototype Review - Reports, Settings, Peripherals & Role-Based Access · DI-800)*
- POS profile & layout: link each department to its workstation types and counts; a distinct drag-and-drop product/category layout per workstation type (ticketing, F&B, retail, kiosk); sales rules limiting what a workstation sells (e.g. admission-only vs membership-only). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-310)*
- Each workstation is linked to a front-end "sales board" (e.g. of ten: five ticketing, three F&B, two retail); signing in on it opens the matching front end automatically. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-247)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-123` · status **notStarted** · provenance generated
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-123?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save configuration profile.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-124` Layout & Journey Builder

**Lay out a sale board's buttons and the sales journey for each type of workstation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `core` module |
| Block | Block A · ticket #17825 (APP-SETUP-BO-124) |
| Who uses it | venue staff holding `DEVICE_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `WORKSTATION_CONFIGURE` (2 read, 2 configure); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAuditRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `venueId` (session), `saleBoardId` (deepLink), `deviceId` (deepLink), `profileId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. A device opened from the registry. A profile opened … |
| Route | `/sell/layout-journey-builder` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-1D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): recordDeviceHeartbeat is a device-audience operation the device sends itself; a layout builder in the back office is not the device (R254). Removed 2 October 2026 (CHG-WIR-021): The main table was the audit log (listAuditRecords, AUDIT_VIEW) while the designer works on sale boards, which it did not read; the audit log belongs to BO-068 …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The Sale Board designer: what the cashier sees and in what order, per workstation type (ticketing, F&B, retail, kiosk), built by drag and drop from products and system functions (ticket list, reservation list, transaction list, media lookup), then deployed to tills through a configuration profile. The old interface is a concept, not a design reference.

**Fixed on main** (the package already carries these; draw what it says): The screen's main table is the audit log (listAuditRecords) and its emptyNoAccess names AUDIT_VIEW. (CHG-WIR-021); Create and Save sale board forms ask for `id`, and the deploy form for status, counts and timestamps. (CHG-SBO-015); "Record device heartbeat" button. (CHG-WIR-021); No drag-and-drop canvas, product picker or preview is declared. (CHG-WIR-023); formUpdateSaleBoard asks the person for id. (CHG-SBO-004); formCreateSaleBoard asks the person for id. (CHG-SBO-004); formDeployConfigurationProfile asks the person for status, id. (CHG-SBO-004); formRecordDeviceHeartbeat asks the person for status. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every audit' drop id, principalId, orgUnitId, workstationId; 'Every registered device' … (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search layout | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listDevices` ?workstationId |
| Kind | select | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | `listDevices` ?kind |
| Kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listSaleBoards` ?kind |

**Form: Save sale board** (modal, opened by *Save sale board*; *Save sale board* calls `updateSaleBoard`, *Cancel* sends nothing)

**Collects what `updateSaleBoard` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateSaleBoard` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateSaleBoard` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Kind `kind` | radio group | required | — | Ticketing · Fnb · Retail · Mixed | — | — | `updateSaleBoard` body |
| Pages `pages` | repeatable rows | required | — | at least 1 | — | — | `updateSaleBoard` body |
| Name `pages[].name` | text field | required | — | — | — | — | `updateSaleBoard` body |
| Sort order `pages[].sortOrder` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Tiles `pages[].tiles` | repeatable rows | required | — | — | — | — | `updateSaleBoard` body |
| Position `pages[].tiles[].position` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Kind `pages[].tiles[].kind` | radio group | required | — | Product · Category · Action · Spacer | — | — | `updateSaleBoard` body |
| Variant `pages[].tiles[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Label `pages[].tiles[].label` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Colour `pages[].tiles[].colour` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Image `pages[].tiles[].imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateSaleBoard` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateSaleBoard` body |

Errors to draw in the form: 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Create sale board** (modal, opened by *Create sale board*; *Create sale board* calls `createSaleBoard`, *Cancel* sends nothing)

**Collects what `createSaleBoard` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createSaleBoard` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createSaleBoard` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createSaleBoard` body |
| Kind `kind` | radio group | required | — | Ticketing · Fnb · Retail · Mixed | — | — | `createSaleBoard` body |
| Pages `pages` | repeatable rows | required | — | at least 1 | — | — | `createSaleBoard` body |
| Name `pages[].name` | text field | required | — | — | — | — | `createSaleBoard` body |
| Sort order `pages[].sortOrder` | number field | required | — | — | — | — | `createSaleBoard` body |
| Tiles `pages[].tiles` | repeatable rows | required | — | — | — | — | `createSaleBoard` body |
| Position `pages[].tiles[].position` | number field | required | — | — | — | — | `createSaleBoard` body |
| Kind `pages[].tiles[].kind` | radio group | required | — | Product · Category · Action · Spacer | — | — | `createSaleBoard` body |
| Variant `pages[].tiles[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `createSaleBoard` body |
| Label `pages[].tiles[].label` | text field | optional | — | — | — | — | `createSaleBoard` body |
| Colour `pages[].tiles[].colour` | text field | optional | — | — | — | — | `createSaleBoard` body |
| Image `pages[].tiles[].imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createSaleBoard` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createSaleBoard` body |

Errors to draw in the form: 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope

**Form: Deploy configuration profile** (modal, opened by *Deploy configuration profile*; *Deploy configuration profile* calls `deployConfigurationProfile`, *Cancel* sends nothing)

**Collects what `deployConfigurationProfile` sends before it is called.** Nothing in the body is required. Optional: `targetWorkstationIds`, `targetFilter`, `strategy`. Only the version (profile), the target and the strategy are asked; status, counts and timestamps are the server's. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | number field | required | — | — | — | The published version to deploy. | `deployConfigurationProfile` body |
| Target workstations `targetWorkstationIds` | multi-picker: choose target workstations | optional | — | — | — | — | `deployConfigurationProfile` body |
| Target filter `targetFilter` | group | optional | — | — | — | By department, type or venue, where the target is a set rather than a list. | `deployConfigurationProfile` body |
| Venues `targetFilter.venueIds` | multi-picker: choose venues | optional | — | — | — | — | `deployConfigurationProfile` body |
| Departments `targetFilter.departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `deployConfigurationProfile` body |
| Workstation types `targetFilter.workstationTypes` | list of values (chips) | optional | — | — | — | The same workstation-type values `ConfigurationProfile.venueKindScope` holds. | `deployConfigurationProfile` body |
| Strategy `strategy` | segmented control | optional | On next idle | Immediate · Staged · On next idle | — | — | `deployConfigurationProfile` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Sale board**: Code unique per tenant, name, kind (ticketing, F&B, retail), pages of buttons; a board belongs to one venue. *(source: contracts/spine/tenancy.yaml#createSaleBoard; R108)*
- **Deploy profile**: Choose the published version, the target (named workstations, or a set by department, type or venue) and the strategy: on next idle (default), staged or immediate. Immediate warns that cashiers mid-sale will be interrupted. *(source: contracts/spine/tenancy.yaml#deployConfigurationProfile)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: updateSaleBoard, createSaleBoard: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#updateSaleBoard)*

#### Outputs: what the screen shows and produces

**Shown**

**Every registered device** (data table, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Identifier | text | — |
| Model | text | — |
| Offline scope | chip: None, Read only, Sell and scan, Full venue | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it … |
| Firmware version | text | As the device last reported it on its heartbeat. |
| Is required | yes / no (icon or chip) | True blocks shift open when the device is unreachable. |

**Sale boards** (data table, from `listSaleBoards`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Name | text | — |
| Sort order | 1,234 | — |
| Tiles | list or chips (count when long) | — |
| Position | 1,234 | — |
| Kind | chip: Product, Category, Action, Spacer | — |
| Variant | the name it points at, never the id | — |
| Label | text | — |
| Colour | text | — |
| Image | the image or video | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save sale board (primary button) | `updateSaleBoard` PUT `/sale-boards/{saleBoardId}` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Create sale board (secondary button) | `createSaleBoard` POST `/sale-boards` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Deploy configuration profile (secondary button) | `deployConfigurationProfile` POST `/configuration-profiles/{profileId}/deploy` | ProfileDeployment | ProfileDeployment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version. | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
|  (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Deployment result**: Succeeded and failed counts with failures grouped by reason (40 tills failing for one reason is one problem). *(source: contracts/spine/tenancy.yaml#/components/schemas/ProfileDeployment)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Deploy configuration profile**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/spine/tenancy.yaml#deployConfigurationProfile)*

**Data it reads**: `listDevices` (onLoad, List registered devices); `listSaleBoards` (onLoad, The sale boards to lay out, one per workstation type)

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-125` Product & Category Button Configuration: *Product & Category Button Configuration*; carries `saleBoardId`
- → `BO-126` Deployment, Preview & Audit: *The configuration is deployed and rolled out*; carries `profileId`, `saleBoardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The layout journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the layout journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No layout journey yet. Offers Create sale board (`createSaleBoard`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on orgUnitId, principalId, workstationId, action, subjectRef, from and the layout journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `DEVICE_VIEW`, which `listDevices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tile references an unknown or unsellable variant; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version. |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds AUDIT_VIEW, DEVICE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: WORKSTATION_CONFIGURE for Save sale board, Create sale board; TENANT_CONFIGURE for Deploy configuration profile. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#updateSaleBoard)*
- **deployConfigurationProfile answers 409**: Show it as something the person can act on, not a failure: **The named version is not deployable** — it is still a `draft`, or this profile has no such version. Names the version and its status. *(source: contracts/spine/tenancy.yaml#deployConfigurationProfile)*

#### Consistency with other screens

- Match `BO-125`: Button configuration is part of this designer.
- Match `BO-126`: Deployment, preview and audit continue the deploy step.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
board:
  code: TKT-MAIN
  name: Ticketing - Main Gate
  kind: ticketing
  pages:
  - Day passes
  - Annual passes
  - Add-ons
deploy:
  version: 7
  target: 'Department: Ticketing, AquaCove Abu Dhabi (8 tills)'
  strategy: onNextIdle
  result: '7 succeeded, 1 failed: Main Gate Till 5 offline'
```

#### Permissions

- `updateSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff
- `createSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff
- `deployConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff
- `listDevices` → `DEVICE_VIEW` (read) · staff
- `listSaleBoards` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `DEVICE_VIEW`, which `listDevices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.9 | The system should allow the interface of POS solution to be configurable: - Configurable hot keys on touch screen to link to a specific action. - Configuration of various sales screens (buttons … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.12.19 | Order Sales 1) The POS home page displays available products by category, for the current POS. 2) Staff can click a specific product to add it to the cart; quantity can be adjusted 3) The system … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.1.18 | POS and kiosk devices shall be linked to the Device Management module so administrators can monitor device status, location, software version, connectivity, errors, paper levels, and assigned … | Ticketing Sales | CONTRACTED | `listDevices` |
| 2.1.26 | System shall provide centralized monitoring of kiosk health including online status, stock levels, payment devices, printers, connectivity, and alerts. | Ticketing Sales | CONTRACTED | `listDevices` |
| 8.9.6 | System shall monitor scanners, POS devices, kiosks, handhelds, printers, gates, network connectivity, and infrastructure health. | Unified Operations Dashboard | CONTRACTED | `listDevices` |
| 16.2.7 | Device Inventory Management - System shall maintain device inventories. | Device Management | CONTRACTED | `listDevices` |
| 16.2.8 | Device Classification - System shall support device categorization. | Device Management | CONTRACTED | `listDevices` |
| 16.2.12 | Device Asset Tracking - System shall maintain device asset records. | Device Management | CONTRACTED | `listDevices` |
| 16.9.55 | Device APIs - System shall expose device management APIs. | Device Management | CONTRACTED | `listDevices` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- POS profile & layout: link each department to its workstation types and counts; a distinct drag-and-drop product/category layout per workstation type (ticketing, F&B, retail, kiosk); sales rules limiting what a workstation sells (e.g. admission-only vs membership-only). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-310)*
- Drag-and-drop POS "sales board" designer placing products and system functions (ticket list, reservation list, transaction list, media lookup) as buttons with custom fonts and colours. Allam: the old interface is NOT a design reference — functional concept only. *(agreed · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-157)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-124` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 1.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 1.dc.html#pos-1d`
- Flow F79 *A workstation is registered, configured and rolled out*, step 3: Its sale board layout is built. → What the cashier sees and in what order.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (38), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-124?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save sale board, Create sale board, Deploy configuration profile, What publishing changes, .
- [ ] Every transition is wired: `BO-102`, `BO-125`, `BO-126`.
- [ ] Every gated control is gated: `DEVICE_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `WORKSTATION_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-125` Product & Category Button Configuration

**Set which product or category each sale-board button sells.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `WORKSTATION_CONFIGURE` (1 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getWorkstationHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `saleBoardId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. A device opened from the registry. Resolves from the … |
| Route | `/sell/product-category-button-configuration` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-1E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** **`getWorkstationHealth` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. Removed 2 October 2026 (CHG-WIR-021): recordDeviceHeartbeat is a device-audience operation the device sends itself; a button configuration screen in the back office is not the device (R254). Removed 2 October 2026 (CHG-WIR-021): getWorkstationHealth, listAlerts and Report incident were attached to a button editor by board position; fleet health is BO-128 and incidents are maintenance …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Placing products and categories as buttons on a sale board page: which product, label, colour, position, page. Part of the sale board designer.

**Fixed on main** (the package already carries these; draw what it says): getWorkstationHealth, listAlerts, Report incident and Record device heartbeat on a button editor. (CHG-WIR-021); requiresModule 'ticketing' while F&B and retail boards also have buttons. (CHG-SBO-003); Shows a button or form for recordDeviceHeartbeat, whose only audience is device. (CHG-WIR-021); formUpdateSaleBoard asks the person for id. (CHG-SBO-004); formRecordDeviceHeartbeat asks the person for status. (CHG-WIR-021); formReportIncident asks the person for id. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every product' drop id, venueId, scopePath, createdByPrincipalId … (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |
| Search product | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Form: Save sale board** (modal, opened by *Save sale board*; *Save sale board* calls `updateSaleBoard`, *Cancel* sends nothing)

**Collects what `updateSaleBoard` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateSaleBoard` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateSaleBoard` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Kind `kind` | radio group | required | — | Ticketing · Fnb · Retail · Mixed | — | — | `updateSaleBoard` body |
| Pages `pages` | repeatable rows | required | — | at least 1 | — | — | `updateSaleBoard` body |
| Name `pages[].name` | text field | required | — | — | — | — | `updateSaleBoard` body |
| Sort order `pages[].sortOrder` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Tiles `pages[].tiles` | repeatable rows | required | — | — | — | — | `updateSaleBoard` body |
| Position `pages[].tiles[].position` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Kind `pages[].tiles[].kind` | radio group | required | — | Product · Category · Action · Spacer | — | — | `updateSaleBoard` body |
| Variant `pages[].tiles[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Label `pages[].tiles[].label` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Colour `pages[].tiles[].colour` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Image `pages[].tiles[].imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateSaleBoard` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateSaleBoard` body |

Errors to draw in the form: 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: updateSaleBoard: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#updateSaleBoard)*

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save sale board (primary button) | `updateSaleBoard` PUT `/sale-boards/{saleBoardId}` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (observedValue)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listProducts` (onLoad, List products)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product category button list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product category button untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product category button yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the product category button are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A tile references an unknown or unsellable variant |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds DEVICE_VIEW, PRODUCT_VIEW, REPORT_VIEW_VENUE only)**: Everything reads; the actions needing another permission are not offered as live buttons: WORKSTATION_CONFIGURE for Save sale board; INCIDENT_REPORT for Report incident. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#updateSaleBoard)*

#### Consistency with other screens

- Match `BO-124`: The designer this belongs to.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
buttons:
- page: Day passes
  position: 1
  product: Day Pass Adult
  label: Adult
  colour: '#0E7C86'
- page: Day passes
  position: 2
  product: Day Pass Child
  label: Child (3-11)
```

#### Permissions

- `updateSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.9 | The system should allow the interface of POS solution to be configurable: - Configurable hot keys on touch screen to link to a specific action. - Configuration of various sales screens (buttons … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.12.19 | Order Sales 1) The POS home page displays available products by category, for the current POS. 2) Staff can click a specific product to add it to the cart; quantity can be adjusted 3) The system … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.6 | System shall support automatic activation of future pricing. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.7 | System shall support overlapping pricing schedules with priority rules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Menu Builder defines the front-end POS layout per outlet — categories, item tiles (image, name, price) and configurable button sizes for fast-selling items. Agreed the current (reference) layout is a reference only and the UI/UX can be improved. *(agreed · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-326)*
- POS profile & layout: link each department to its workstation types and counts; a distinct drag-and-drop product/category layout per workstation type (ticketing, F&B, retail, kiosk); sales rules limiting what a workstation sells (e.g. admission-only vs membership-only). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-310)*
- Drag-and-drop POS "sales board" designer placing products and system functions (ticket list, reservation list, transaction list, media lookup) as buttons with custom fonts and colours. Allam: the old interface is NOT a design reference — functional concept only. *(agreed · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-157)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-125` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 1.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 1.dc.html#pos-1e`
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-125?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save sale board.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `WORKSTATION_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-126` Deployment, Preview & Audit

**Preview a configuration, deploy it to the workstations and see what changed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `WORKSTATION_CONFIGURE` (2 read, 2 configure); in the flows as technician, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | online only |
| Opens with | `venueId` (session), `profileId` (deepLink), `saleBoardId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which before the page renders. |
| Route | `/sell/deployment-preview-audit` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-1F, POS-4F** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Start rollout (startRollout, PLATFORM_RELEASE_PROMOTE) is TICVAI's platform release act that tenant staff cannot hold (ADM-029 keeps it), and Run report is … Removed 2 October 2026 (CHG-WIR-021): Start rollout (startRollout, PLATFORM_RELEASE_PROMOTE) is TICVAI's platform release act that tenant staff cannot hold (ADM-029 keeps it), and Run report is …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Deploy a configuration profile version to tills, preview what a till will show, and audit what was deployed where. The deployment names its targets and strategy before it starts and reports failures grouped by reason.

**Fixed on main** (the package already carries these; draw what it says): Start rollout (startRollout, PLATFORM_RELEASE_PROMOTE) on a venue screen. (CHG-WIR-021); Run report on a deployment screen. (CHG-WIR-021); formDeployConfigurationProfile asks the person for status, id. (CHG-SBO-004); formUpdateSaleBoard asks the person for id. (CHG-SBO-004); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search deployment, preview | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Org unit | picker: choose an org unit | — | — | `listAuditRecords` ?orgUnitId |
| Principal | picker: choose a principal | — | — | `listAuditRecords` ?principalId |
| Workstation | picker: choose a workstation | — | — | `listAuditRecords` ?workstationId |
| Action | text field | — | — | `listAuditRecords` ?action |
| Subject ref | text field | — | — | `listAuditRecords` ?subjectRef |
| Platform staff grant | picker: choose a platform staff grant | — | — | `listAuditRecords` ?platformStaffGrantId |
| From | date and time picker | — | — | `listAuditRecords` ?from |
| To | date and time picker | — | — | `listAuditRecords` ?to |
| Kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listSaleBoards` ?kind |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |

**Form: Deploy configuration profile** (modal, opened by *Deploy configuration profile*; *Deploy configuration profile* calls `deployConfigurationProfile`, *Cancel* sends nothing)

**Collects what `deployConfigurationProfile` sends before it is called.** Required: `profileId`. Optional: `targetWorkstationIds`, `targetFilter`, `strategy`, `succeededCount`, `failedCount`, `failureReasons`, `startedAt`, `completedAt`. **Not asked:** `id` is a client UUIDv7 generated silently; `status` is set by the server (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | number field | required | — | — | — | The published version to deploy. | `deployConfigurationProfile` body |
| Target workstations `targetWorkstationIds` | multi-picker: choose target workstations | optional | — | — | — | — | `deployConfigurationProfile` body |
| Target filter `targetFilter` | group | optional | — | — | — | By department, type or venue, where the target is a set rather than a list. | `deployConfigurationProfile` body |
| Venues `targetFilter.venueIds` | multi-picker: choose venues | optional | — | — | — | — | `deployConfigurationProfile` body |
| Departments `targetFilter.departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `deployConfigurationProfile` body |
| Workstation types `targetFilter.workstationTypes` | list of values (chips) | optional | — | — | — | The same workstation-type values `ConfigurationProfile.venueKindScope` holds. | `deployConfigurationProfile` body |
| Strategy `strategy` | segmented control | optional | On next idle | Immediate · Staged · On next idle | — | — | `deployConfigurationProfile` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version.

**Form: Save sale board** (modal, opened by *Save sale board*; *Save sale board* calls `updateSaleBoard`, *Cancel* sends nothing)

**Collects what `updateSaleBoard` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `updateSaleBoard` body |
| Name `name` | text field | required | — | max length 200 | — | — | `updateSaleBoard` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Kind `kind` | radio group | required | — | Ticketing · Fnb · Retail · Mixed | — | — | `updateSaleBoard` body |
| Pages `pages` | repeatable rows | required | — | at least 1 | — | — | `updateSaleBoard` body |
| Name `pages[].name` | text field | required | — | — | — | — | `updateSaleBoard` body |
| Sort order `pages[].sortOrder` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Tiles `pages[].tiles` | repeatable rows | required | — | — | — | — | `updateSaleBoard` body |
| Position `pages[].tiles[].position` | number field | required | — | — | — | — | `updateSaleBoard` body |
| Kind `pages[].tiles[].kind` | radio group | required | — | Product · Category · Action · Spacer | — | — | `updateSaleBoard` body |
| Variant `pages[].tiles[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `updateSaleBoard` body |
| Label `pages[].tiles[].label` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Colour `pages[].tiles[].colour` | text field | optional | — | — | — | — | `updateSaleBoard` body |
| Image `pages[].tiles[].imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateSaleBoard` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateSaleBoard` body |

Errors to draw in the form: 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: updateSaleBoard: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#updateSaleBoard)*

#### Outputs: what the screen shows and produces

**Shown**

**Audit records** (metric tile, from `listAuditRecords`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | Who acted. |
| Org unit | the name it points at, never the id | The scope node the action happened in. |
| Workstation | the name it points at, never the id | The workstation it was done from, where there was one. |
| Action | text | What was done, as the writing operation names it. |
| Subject ref | text | The thing acted on — a profile, a shift, an order. The same value the `subjectRef` filter matches. |
| Occurred at | 1 Oct 2026, 14:30 | When. The list is ordered by this, most recent first. |
| Platform staff grant | the name it points at, never the id | Set when a TICVAI platform operator acted, naming the grant they acted under (`identity.openPlatformStaffGrant`; decided 28 September … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Sale boards** (metric tile, from `listSaleBoards`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Pages | list or chips (count when long) | — |
| Name | text | — |
| Sort order | 1,234 | — |
| Tiles | list or chips (count when long) | — |
| Position | 1,234 | — |
| Kind | chip: Product, Category, Action, Spacer | — |
| Variant | the name it points at, never the id | — |
| Label | text | — |
| Colour | text | — |
| Image | the image or video | — |
| Is active | yes / no (icon or chip) | — |

**Workstations** (metric tile, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | The outlet this till stands in (CHG-CSP-006). Its board is the till's board unless the till overrides it. |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| ID | the name it points at, never the id | — |
| Kind | chip: Ticketing, Fnb, Retail, Mixed | — |
| Name | text | — |
| Sale board source | chip: Outlet, Workstation | Where `saleBoard` came from (decided 2 October 2026, Chinmay, BO-109: "Per outlet, with a till override"; DEC-183; CHG-CSP-006): `outlet` … |
| Cash drawer limit | AED 1,234.50 | This till's drawer limit, overriding the venue's (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point. |
| Devices | list or chips (count when long) | — |
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously … |
| Identifier | text | Serial |
| Is required | yes / no (icon or chip) | When true, the workstation refuses to open a shift if the device is absent. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Deploy configuration profile (primary button) | `deployConfigurationProfile` POST `/configuration-profiles/{profileId}/deploy` | ProfileDeployment | ProfileDeployment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version. | opens modal first |
| Save sale board (secondary button) | `updateSaleBoard` PUT `/sale-boards/{saleBoardId}` | SaleBoard | SaleBoard | 400 A tile references an unknown or unsellable variant; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Deploy configuration profile**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/spine/tenancy.yaml#deployConfigurationProfile)*

**Data it reads**: `listAuditRecords` (onLoad, Who did what, where, and when); `listSaleBoards` (onLoad, List sale boards); `listWorkstations` (onLoad, List workstations)

**Where the user goes next**

- → `BO-102` Sell: *Sell*
- → `BO-036` Device Registry: *Device Registry*; carries `workstationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deployment preview audit figures; each tile loads on its own. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deployment preview audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AUDIT_VIEW`, which `listAuditRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tile references an unknown or unsellable variant; 409 The named version is not deployable — it is still a `draft`, or this profile has no such version. |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds AUDIT_VIEW, SCOPE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for Deploy configuration profile; WORKSTATION_CONFIGURE for Save sale board; REPORT_VIEW_VENUE for Run report; PLATFORM_RELEASE_PROMOTE for Start rollout. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#deployConfigurationProfile)*
- **deployConfigurationProfile answers 409**: Show it as something the person can act on, not a failure: **The named version is not deployable** — it is still a `draft`, or this profile has no such version. Names the version and its status. *(source: contracts/spine/tenancy.yaml#deployConfigurationProfile)*
- **startRollout answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/platform-ops.yaml#startRollout)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
deployment:
  profile: Ticketing till - Abu Dhabi v7
  target: 8 tills
  strategy: onNextIdle
  result: 7 succeeded · 1 failed (offline)
```

#### Permissions

- `deployConfigurationProfile` → `TENANT_CONFIGURE` (configure) · staff
- `updateSaleBoard` → `WORKSTATION_CONFIGURE` (configure) · staff
- `listAuditRecords` → `AUDIT_VIEW` (read) · staff
- `listSaleBoards` → `SCOPE_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `AUDIT_VIEW`, which `listAuditRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.9 | The system should allow the interface of POS solution to be configurable: - Configurable hot keys on touch screen to link to a specific action. - Configuration of various sales screens (buttons … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |
| 2.12.19 | Order Sales 1) The POS home page displays available products by category, for the current POS. 2) Staff can click a specific product to add it to the cart; quantity can be adjusted 3) The system … | Ticketing Sales | CONTRACTED | `updateSaleBoard` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-126` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 1.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 1.dc.html#pos-1f`, `POS Board 4.dc.html#pos-4f`
- Flow F79 *A workstation is registered, configured and rolled out*, step 4: The configuration is deployed and rolled out. → **`startRollout` answers 202 until the release manager approves** (audit R144); a requester cannot approve their own.
- Flow F86 *A POS layout is designed, previewed and deployed*, step 5: Deployment, Preview & Audit. → **Drawn by the client as POS-4F.** 4 operations on this step.
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-126?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Deploy configuration profile, Save sale board, What publishing changes.
- [ ] Every transition is wired: `BO-102`, `BO-036`.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `WORKSTATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-142` Store Rules, Controls & Permissions

**Store Rules, Controls & Permissions — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRoles` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/sell/store-rules-controls-permissions` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `Retail Board 1.dc.html` frame `ret-1j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Store Rules, Controls &amp; Permissions* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): The roles list (needs the role-management permission) and venue settings (no retail setting) are not this screen's data (R091, R254; design-notes correction … Removed 2 October 2026 (CHG-WIR-008): The roles list (needs the role-management permission) and venue settings (no retail setting) are not this screen's data (R091, R254; design-notes correction …

**From the Food, Beverage & Retail process.** Store Rules, Controls & Permissions lists the controls in force in a shop (discount limit, refund threshold, age check, manager override, price override) and who may act past each one. The one thing to get right is that a rule names a permission ("needs Supervisor"), and it is a row with who changed it and when. Roles themselves are managed elsewhere.

**Known correction pending (do not draw the wrong version)**

- **Refund thresholds exist twice: StoreRule (refund threshold) and the outlet's return policy (self-authorise limit, second-user limit, approval limit).** Why: The till will read one and the back office will edit the other. One source should hold the retail return threshold (which needs a supervisor step-up). *(source: R144 / contracts/satellite/retail.yaml#/components/schemas/ReturnPolicy / contracts/satellite/retail.yaml#/components/schemas/StoreRule; Food, Beverage & Retail)*
- **listStoreRules and setStoreRules are stubs whose shape is "a proposal".** Why: The screen cannot be built against an unconfirmed shape. *(source: contracts/satellite/retail.yaml#setStoreRules; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The screen binds the roles list (needs the role-management permission) and venue settings (no retail setting). The no-access state names … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a discount or price-override limit an amount or a percentage?** → A discount or price-override limit is a percentage or an amount, chosen per limit by the venue. *(decided by Chinmay, 2026-10-02; DEC-195 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search store rules, controls | search field | — | — | — | — | — | — |

**Form: Save store rules** (modal, opened by *Save store rules*; *Save store rules* calls `setStoreRules`, *Cancel* sends nothing)

**Collects what `setStoreRules` sends before it is called.** Nothing in the body is required. Optional: `outletId`, `kind`, `thresholdAmount`, `limitKind`, `thresholdPercent`, `minimumAgeYears`, `requiresPermission`, `enabled`. `id` is a client UUIDv7 generated silently, never asked. **Each discount or price-override limit is a percentage or an amount, chosen per limit by the venue (decided 2 October 2026 by Chinmay, DEC-195; CHG-CSA-019):** `limitKind` picks which of `thresholdPercent` and `thresholdAmount` applies. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setStoreRules` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setStoreRules` body |
| Outlet `outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | — | `setStoreRules` body |
| Kind `kind` | radio group | optional | — | Discount limit · Refund threshold · Age check · Manager override · Price override | — | — | `setStoreRules` body |
| Threshold amount `thresholdAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | The amount above which `requiresPermission` is needed. For `refundThreshold`, and for a `discountLimit` or `priceOverride` whose `limitKind` is `amount`. | `setStoreRules` body |
| Limit kind `limitKind` | segmented control | optional | — | Percent · Amount | — | For `discountLimit` and `priceOverride` (workbook Q195; CHG-CSA-019). `percent` uses `thresholdPercent`; `amount` uses `thresholdAmount`. | `setStoreRules` body |
| Threshold percent `thresholdPercent` | stepper or slider | optional | — | min 0; max 100 | — | The percentage of the line or basket above which `requiresPermission` is needed, where `limitKind` is `percent`. | `setStoreRules` body |
| Minimum age years `minimumAgeYears` | number field | optional | — | min 0 | — | The age a guest must have reached. For `ageCheck`. | `setStoreRules` body |
| Requires permission `requiresPermission` | text field | optional | — | — | — | The permission a person needs to act past this rule. | `setStoreRules` body |
| Enabled `enabled` | toggle | optional | — | — | — | — | `setStoreRules` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Rule**: Kind (Discount limit, Refund threshold, Age check, Manager override, Price override), outlet (or all outlets), limit (a percentage or an amount, chosen per limit by the venue, for a discount or price-override limit; an amount in AED for a refund threshold; years for an age check), "Needs" (a picker of permission names in plain words, e.g. "Supervisor approval"), Enabled toggle. *(source: contracts/satellite/retail.yaml#/components/schemas/StoreRule / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Outputs: what the screen shows and produces

**Shown**

**Every store rule** (data table, from `listStoreRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Kind | chip: Discount limit, Refund threshold, Age check, Manager override, Price override | — |
| Threshold amount | AED 1,234.50 | The amount above which `requiresPermission` is needed. For `refundThreshold`, and for a `discountLimit` or `priceOverride` whose … |
| Minimum age years | 1,234 | The age a guest must have reached. For `ageCheck`. |
| Requires permission | text | The permission a person needs to act past this rule. |
| Enabled | yes / no (icon or chip) | — |
| Updated by principal | the name it points at, never the id | Who last changed this rule. Set by the server from the caller of `setStoreRules`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save store rules (primary button) | `setStoreRules` PUT `/store-rules` | StoreRule | StoreRule | — | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Rules table**: Grouped by outlet: rule, limit, who may pass it, enabled, last changed by and when. Changing a rule takes effect on the tills of that outlet. *(source: contracts/satellite/retail.yaml#listStoreRules)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save rule**: Saves one rule. The audit (by whom, when) updates. *(source: contracts/satellite/retail.yaml#setStoreRules)*

**Data it reads**: `listStoreRules` (onLoad, Rules and controls in force)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The store rules controls list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the store rules controls untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No store rules controls yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters its list, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listStoreRules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `POS-011`: The refund threshold here is what makes the till ask for a supervisor's PIN on a return above it.
- Match `BO-106`: Roles and their permissions are edited there. This screen only names them.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- outlet: Marina Bay Store
  rule: Refund threshold
  limit: AED 500.00
  needs: Supervisor PIN
  enabled: true
  changedBy: Daniel Brooks
  changedAt: 2026-10-02 10:14 GST
- outlet: Marina Bay Store
  rule: Discount limit
  limit: 15%
  needs: Manager approval
  enabled: true
- outlet: All outlets
  rule: Age check
  limit: 18 years
  needs: ID check
  enabled: false
```

#### Permissions

- `listStoreRules` → `PRODUCT_VIEW` (read) · staff
- `setStoreRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listStoreRules` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Components/attributes model: a component (e.g. "ticket type") has attributes (adult, youth, senior, infant, child) each priced independently; adding an attribute creates a new sellable variant with no extra setup. Who may sell a product is restricted by site, operating area, workstation or role. *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-164)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-142` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 1.dc.html`
- Client design-board frames: `Retail Board 1.dc.html#ret-1j`

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-142?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save store rules.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-143` Retail Global Settings & Controls

**Set the retail rules every outlet follows, such as returns, and deal with uncollected shop-and-drop items.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `REGION_CONFIGURE` (1 read, 2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getVenueSettings` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `dropId` (navigation), `outletId` (navigation) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/sell/retail-global-settings-controls` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `Retail Board 1.dc.html` frame `ret-1k`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Retail Global Settings &amp; Controls* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): The only settings write was setVenueSettings (support and quiet hours); retail global settings such as returns are outlet configuration in retail, served by … Removed 2 October 2026 (CHG-WIR-021): The only settings write was setVenueSettings (support and quiet hours); retail global settings such as returns are outlet configuration in retail, served by …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Retail-wide settings and the shop-and-drop controls (look up and dispose of uncollected purchases). As wired it edits general venue settings rather than retail ones.

**Fixed on main** (the package already carries these; draw what it says): The only settings write is setVenueSettings. (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search retail global settings | search field | — | — | — | — | — | — |

**Form: Save return policy** (modal, opened by *Save return policy*; *Save return policy* calls `setReturnPolicy`, *Cancel* sends nothing)

**Collects what `setReturnPolicy` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `setReturnPolicy` body |
| Default window days `defaultWindowDays` | number field (days) | required | — | min 0 | — | — | `setReturnPolicy` body |
| Requires receipt `requiresReceipt` | toggle | required | on | — | — | — | `setReturnPolicy` body |
| Allow cash refund on card sale `allowCashRefundOnCardSale` | toggle | optional | off | — | — | — | `setReturnPolicy` body |
| Self authorise limit `selfAuthoriseLimit` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Up to this, one cashier may accept a return alone. | `setReturnPolicy` body |
| Requires second user above `requiresSecondUserAbove` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setReturnPolicy` body |
| Requires approval above `requiresApprovalAbove` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setReturnPolicy` body |
| Restockable conditions `restockableConditions` | multi-select chips | optional | — | Resaleable · Opened · Damaged · Faulty · Missing parts | — | Conditions that return stock to sale. Everything else is written off. | `setReturnPolicy` body |
| Non returnable categorys `nonReturnableCategoryIds` | multi-picker: choose non returnable categorys | optional | — | — | — | — | `setReturnPolicy` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVenueSettings: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setVenueSettings)*

#### Outputs: what the screen shows and produces

**Shown**

**Return policy** (detail panel, from `getReturnPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Outlet | the name it points at, never the id | — |
| Default window days | 1,234 | — |
| Requires receipt | yes / no (icon or chip) | — |
| Allow cash refund on card sale | yes / no (icon or chip) | — |
| Self authorise limit | AED 1,234.50 | Up to this, one cashier may accept a return alone. |
| Requires second user above | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Requires approval above | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Restockable conditions | list or chips (count when long) | Conditions that return stock to sale. Everything else is written off. |
| Non returnable categorys | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save return policy (secondary button) | `setReturnPolicy` PUT `/outlets/{outletId}/return-policy` | ReturnPolicy | ReturnPolicy | — | opens modal first |

**Data it reads**: `getReturnPolicy` (onLoad, The return policy each outlet follows)

**Where the user goes next**

- → `BO-102` Sell: *Sell*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retail global settings, read by `getReturnPolicy`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retail global settings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retail global settings yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getReturnPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 No identifier supplied |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ORDER_VIEW, TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for Save venue settings; PRODUCT_CONFIGURE for disposeShopAndDrop. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*
- **setVenueSettings answers 422**: Show it as something the person can act on, not a failure: **An enable the venue cannot evidence.** Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender verification where no device in the venue reports `genderClassification`. `errors[]` names each missing field or the missing capability. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getVenueSettings (VenueSettings):
- calendarDayStartHour: 12
  currencyCode: AED
  currencyScale: 12
  cartLeaseSeconds: 12
  cartHoldExtensionMinutes: 12
  cartMaxExtensions: 12
  resaleCutoffHours: 12
- calendarDayStartHour: 3
  currencyCode: AED
  currencyScale: 3
  cartLeaseSeconds: 3
  cartHoldExtensionMinutes: 3
  cartMaxExtensions: 3
  resaleCutoffHours: 3
```

#### Permissions

- `lookupShopAndDrop` → `ORDER_VIEW` (read) · staff, guest
- `disposeShopAndDrop` → `PRODUCT_CONFIGURE` (configure) · staff
- `getReturnPolicy` → `ORDER_VIEW` (read) · staff
- `setReturnPolicy` → `REGION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getReturnPolicy` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Online retail offers buy-online-pickup-in-store and buy-online-ship-to-address. Shipping fees are set by region/city (e.g. Dubai, Abu Dhabi, international); decision: operations enter courier rates and margins manually, no live courier-API integration at this stage. *(agreed · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions; 4.8 Online Order Fulfilment & Shipping Configuration · DI-359)*
- Retail POS/device assignment covers workstation name/code, receipt printer, barcode scanner and cash drawer; global retail settings include sales channels, primary/replenishment store and offline sales support. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-352)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-143` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 1.dc.html`
- Client design-board frames: `Retail Board 1.dc.html#ret-1k`

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-143?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save return policy.
- [ ] Every transition is wired: `BO-102`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `REGION_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createSaleBoard": {"method":"POST","path":"/sale-boards","contract":"tenancy","summary":"Create a sale board","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SaleBoard","responds":"SaleBoard"},
"deployConfigurationProfile": {"method":"POST","path":"/configuration-profiles/{profileId}/deploy","contract":"tenancy","summary":"Push a version to a fleet, in stages","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProfileDeployment","responds":null},
"disposeShopAndDrop": {"method":"POST","path":"/shop-and-drop/{dropId}/dispose","contract":"retail","summary":"Dispose of an uncollected item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getReturnPolicy": {"method":"GET","path":"/outlets/{outletId}/return-policy","contract":"retail","summary":"Read the retail return policy","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReturnPolicy"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDevices": {"method":"GET","path":"/devices","contract":"tenancy","summary":"List registered devices","permission":"DEVICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSaleBoards": {"method":"GET","path":"/sale-boards","contract":"tenancy","summary":"List sale boards","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"SaleBoard"},
"listStoreRules": {"method":"GET","path":"/store-rules","contract":"retail","summary":"Rules and controls in force in the store","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupShopAndDrop": {"method":"GET","path":"/shop-and-drop/lookup","contract":"retail","summary":"Find a guest's dropped goods","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"entitlementId","in":"query","required":null},{"name":"dropReference","in":"query","required":null},{"name":"receiptNumber","in":"query","required":null}],"requestBody":null,"responds":"ShopAndDrop"},
"setConfigurationProfile": {"method":"PUT","path":"/configuration-profiles","contract":"tenancy","summary":"What a class of workstation is configured to be","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigurationProfile","responds":"ConfigurationProfile"},
"setReturnPolicy": {"method":"PUT","path":"/outlets/{outletId}/return-policy","contract":"retail","summary":"Set the retail return policy","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReturnPolicy","responds":"ReturnPolicy"},
"setStoreRules": {"method":"PUT","path":"/store-rules","contract":"retail","summary":"Change a store rule","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StoreRule","responds":"StoreRule"},
"updateSaleBoard": {"method":"PUT","path":"/sale-boards/{saleBoardId}","contract":"tenancy","summary":"Update a sale board","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SaleBoard","responds":"SaleBoard"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConfigurationProfile": {"type":"object","x-ticvai-persistence":"platform.configuration_profile","description":"Board 1 of the client's POS design set, 20 August. **The board shows 1,248 workstations across four versions and the package modelled none of it** — a firmware version field on the workstation, and nothing that says what a workstation is configured to be.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks alone*, which is the only reason to version a profile at all.\n","required":["id","name","venueKindScope","version","status"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"scopePath":{"type":"string"},"venueKindScope":{"type":"array","description":"Which workstation types it applies to. **A ticketing counter and a kitchen display do not share a profile**, and a profile that claims to is a profile somebody deploys to the wrong fleet.\n","items":{"type":"string"}},"version":{"type":"integer","readOnly":true,"description":"**Immutable once deployed anywhere.** A change makes a new version, and the old one stays readable — a workstation still running v2.3 must be able to say what v2.3 was. Assigned by the server: 1 on create, and one more each time a change lands on a published version (see `setConfigurationProfile`).\n"},"settings":{"type":"object","additionalProperties":true},"status":{"type":"string","enum":["draft","published","deploying","deployed","superseded","rolledBack"],"description":"On input only `draft` or `published`; sending `published` publishes this version. The other four are set by deployment and refused on input.\n"},"deployedCount":{"type":"integer","readOnly":true},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceApprovalStatus": {"type":"string","description":"Whether a registered device may go into production (DEC-241, DEC-245; CHG-CSP-011). The model is `states/registered-device-approval.yaml`.\n","enum":["pendingApproval","approved","rejected"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProfileDeployment": {"type":"object","x-ticvai-persistence":"platform.profile_deployment","description":"**A deployment is an event with a date, a target and an outcome** — the client's board shows recent deployments with all three and the package had no record of any.\n**Staged rather than all-at-once by default.** Pushing a profile to 1,248 workstations simultaneously is how a venue discovers a bad profile at every till at the same moment.\n","required":["id","profileId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"profileId":{"type":"string","format":"uuid","readOnly":true,"description":"Taken from the path of `deployConfigurationProfile`."},"version":{"type":"integer","description":"The published version to deploy."},"targetWorkstationIds":{"type":"array","items":{"type":"string","format":"uuid"}},"targetFilter":{"type":"object","nullable":true,"description":"By department, type or venue, where the target is a set rather than a list.\n","properties":{"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"workstationTypes":{"type":"array","description":"The same workstation-type values `ConfigurationProfile.venueKindScope` holds.","items":{"type":"string"}}}},"strategy":{"type":"string","enum":["immediate","staged","onNextIdle"],"default":"onNextIdle"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"],"readOnly":true},"succeededCount":{"type":"integer","readOnly":true},"failedCount":{"type":"integer","readOnly":true},"failureReasons":{"type":"object","readOnly":true,"additionalProperties":{"type":"integer"},"description":"**Grouped, because 40 workstations failing for one reason is one problem** and a list of 40 rows is forty.\n"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"},"approvalStatus":{"allOf":[{"$ref":"#/components/schemas/DeviceApprovalStatus"}],"default":"pendingApproval","readOnly":true,"description":"**A new device waits for approval before it may go live** (decided 2 October 2026, Chinmay, critical set 1, BO-196: \"Secure enrolment code + pending approval\"; DEC-241; CHG-CSP-011; MoM 15 September, DI-892, DI-906). Every device registers `pendingApproval`. It may enrol and be provisioned and tested, but `enrolDevice` refuses `active` until `approveDevice` approves it (`409 device-approval-required`). A separate axis from `enrolmentState`, which keeps its r1 values; the model is `states/registered-device-approval.yaml`.\n"},"enrolmentCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":12,"description":"**A one-time code the device must present to enrol** (DEC-241; CHG-CSP-011). Issued by `registerDevice` and returned once, in its response only; every later read returns null. The installer enters it on the device, and `enrolDevice` to `enrolled` must carry the same code before `enrolmentCodeExpiresAt` (`422 enrolment-code-invalid`). A device that never presents it never gets an identity, so a box plugged into the venue network cannot claim to be a reader.\n"},"enrolmentCodeExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the enrolment code stops working (24 hours after registration, proposed; client to correct)."},"testedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who recorded the device's acceptance test (`DeviceEnrolment.testResult` on the move to `provisioned`). The approver must be someone else (DEC-245).\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who approved the device into production, never the person who tested it** (decided 2 October 2026, Chinmay, critical set 1, BO-203: \"Approver must differ from the tester\"; DEC-245; CHG-CSP-011). `approveDevice` refuses the tester with `403 approver-is-tester`.\n"},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ReturnCondition": {"type":"string","description":"Determines whether stock is restored or written off.","enum":["resaleable","opened","damaged","faulty","missingParts"]},
"ReturnPolicy": {"x-ticvai-persistence":"retail.return_policy","type":"object","required":["outletId","defaultWindowDays","requiresReceipt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"outletId":{"type":"string","format":"uuid"},"defaultWindowDays":{"type":"integer","minimum":0},"requiresReceipt":{"type":"boolean","default":true},"allowCashRefundOnCardSale":{"type":"boolean","default":false},"selfAuthoriseLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Up to this, one cashier may accept a return alone."},"requiresSecondUserAbove":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"requiresApprovalAbove":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"restockableConditions":{"type":"array","description":"Conditions that return stock to sale. Everything else is written off.\n\nStored as a `text[]` column on `retail.return_policy`, like `nonReturnableCategoryIds`. The items wrap the enum in `allOf` so the schema derivation reads a list of values rather than a child table.\n","items":{"allOf":[{"$ref":"#/components/schemas/ReturnCondition"}]}},"nonReturnableCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"SaleBoard": {"x-ticvai-persistence":"platform.sale_board","type":"object","required":["id","code","name","venueId","kind","pages"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"pages":{"type":"array","minItems":1,"items":{"type":"object","required":["name","sortOrder","tiles"],"properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"tiles":{"type":"array","items":{"type":"object","required":["position","kind"],"properties":{"position":{"type":"integer"},"kind":{"type":"string","enum":["product","category","action","spacer"]},"variantId":{"type":"string","format":"uuid","nullable":true},"label":{"type":"string"},"colour":{"type":"string","nullable":true},"imageAssetRef":{"type":"string","nullable":true}}}}}}},"isActive":{"type":"boolean"}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"ShopAndDrop": {"type":"object","x-ticvai-persistence":"retail.shop_and_drop + retail.shop_and_drop_line","required":["id","dropReference","collectionPointId","status","collectBy"],"properties":{"id":{"type":"string"},"dropReference":{"type":"string","description":"Short and readable. Printed on the slip a guest may or may not keep."},"saleId":{"type":"string","nullable":true,"description":"The till sale. Null for an online order, which sets `orderId` (audit R236)."},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The paid online order that created this collection (audit R236)."},"entitlementId":{"type":"string","nullable":true,"description":"The ticket that claims these goods. The point of 4.4.7 — a guest does not have to keep a receipt safe for eight hours in a water park.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true},"collectionPointId":{"type":"string","format":"uuid"},"collectionPointName":{"type":"string"},"status":{"type":"string","enum":["awaitingCollection","partiallyCollected","collected","uncollected","disposed"]},"lines":{"type":"array","items":{"type":"object","properties":{"lineId":{"type":"string"},"merchandiseId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"collectedQuantity":{"type":"integer"}}}},"droppedAt":{"type":"string","format":"date-time"},"collectBy":{"type":"string","format":"date-time"},"collectedAt":{"type":"string","format":"date-time","nullable":true},"collectedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"verifiedBy":{"type":"string","nullable":true}}},
"StoreRule": {"type":"object","x-ticvai-persistence":"retail.store_rule","x-ticvai-retired-columns":["threshold_minor"],"description":"**Drafted 4 September.** One rule or control in force in a store - a discount limit, a refund threshold, an age check, a manager override. **A row rather than a config value** because somebody has to be able to say who changed a limit and when, which is what `updatedAt` and `updatedByPrincipalId` record.\n\n**Which limit field a kind uses.** `refundThreshold` uses `thresholdAmount`. `ageCheck` uses `minimumAgeYears`. **A `discountLimit` or a `priceOverride` limit is a percentage or an amount, the venue choosing per limit** (Chinmay, 2 October, workbook Q195; CHG-CSA-019): `limitKind` says which, and the limit is `thresholdAmount` or `thresholdPercent`. Whether a `managerOverride` has a limit at all is still undecided; it carries none.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["discountLimit","refundThreshold","ageCheck","managerOverride","priceOverride"]},"thresholdAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The amount above which `requiresPermission` is needed. For `refundThreshold`, and for a `discountLimit` or `priceOverride` whose `limitKind` is `amount`."},"limitKind":{"type":"string","nullable":true,"enum":["percent","amount"],"description":"For `discountLimit` and `priceOverride` (workbook Q195; CHG-CSA-019). `percent` uses `thresholdPercent`; `amount` uses `thresholdAmount`. The venue chooses per limit."},"thresholdPercent":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"The percentage of the line or basket above which `requiresPermission` is needed, where `limitKind` is `percent`."},"minimumAgeYears":{"type":"integer","minimum":0,"nullable":true,"description":"The age a guest must have reached. For `ageCheck`."},"requiresPermission":{"type":"string","description":"The permission a person needs to act past this rule."},"enabled":{"type":"boolean"},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"Who last changed this rule. Set by the server from the caller of `setStoreRules`."}}},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
