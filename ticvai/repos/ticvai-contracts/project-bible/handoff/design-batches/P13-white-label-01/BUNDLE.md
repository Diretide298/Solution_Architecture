# P13-white-label-01 — P13 · White Label (1 of 3)

**10 screens · 57 operations · 55 schemas · 6 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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
  `AI_USE, ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, PRODUCT_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `CMS-001` | Tenant Workspace | A | 20 | 35 | 5 | 5 | 1 | 0 | configures | notStarted (generated) |
| `CMS-002` | Brand Kit | A | 12 | 10 | 5 | 3 | 4 | 6 | configures | notStarted (generated) |
| `CMS-003` | Typography | A | 5 | 6 | 5 | 1 | 4 | 6 | configures | notStarted (generated) |
| `CMS-004` | Logo & Assets | A | 13 | 19 | 5 | 11 | 3 | 6 | configures | notStarted (generated) |
| `CMS-005` | Theme Editor | A | 27 | 10 | 5 | 4 | 9 | 6 | configures | notStarted (generated) |
| `CMS-006` | Component Preview | A | 6 | 63 | 6 | 10 | 4 | 0 | — | notStarted (generated) |
| `CMS-007` | Page Builder | A | 42 | 37 | 5 | 29 | 4 | 6 | configures | notStarted (generated) |
| `CMS-008` | Content Blocks | A | 62 | 40 | 6 | 10 | 2 | 6 | configures | notStarted (generated) |
| `CMS-009` | Navigation & Menus | A | 46 | 37 | 5 | 9 | 4 | 6 | configures | notStarted (generated) |
| `CMS-010` | Media Library | A | 91 | 37 | 6 | 14 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**CMS-002, CMS-003, CMS-005 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-001` Tenant Workspace

**Land a tenant somewhere that shows what is live and what is not, and hold step 1 of the Site Builder (venue and modules).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-001 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/tenant-workspace` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **The tenant workspace.** Lands a tenant on what is live rather than on a form. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **Drawn 31 August** — `Marketing Board 7.dc.html` frame `crm-7f` (*Agent Workspace*), matched on title at 0.84 within this board’s platforms. **Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose.

**From the White Label & CMS process.** The CMS home: one look tells a tenant admin what guests see now, what is waiting in the draft, and what is live outside the draft (maintenance, sold out, minimum app version). It is also Site Builder step 1 (modules and features). The one thing to get right is the split between "Published", "Draft (unpublished changes)" and "Live now" controls, because only the last group changes guests without a publish.

**Fixed on main** (the package already carries these; draw what it says): The layout dumps every TenantConfig part (brand, theme, fonts, footer, header...) as a detail panel. (CHG-SGU-022); emptyFirstRun says "No tenant yet. Offers no create action". (CHG-SGU-022); The navigation exits include DAM, privacy and waiver command centres (CMS-021..CMS-091) as if white-label. (CHG-SGU-022); Maintenance, minimum app version, contact and availability are edited through one modal labelled "Save maintenance mode". (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should switching on a module or feature be possible without TENANT_PUBLISH approval when the tenant runs an approval matrix (ApprovalKind configurationChange)?** → Drawn default accepted: Draw save-to-draft only; the approval appears on CMS-014 at publish. *(decided by Chinmay, 2026-10-02; DEC-146 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**Form: Save module enablement** (modal, opened by *Save module enablement*; *Save module enablement* calls `setModuleEnablement`, *Cancel* sends nothing)

**Collects what `setModuleEnablement` sends before it is called.** Required: `modules`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Modules `modules` | repeatable rows | required | — | — | — | — | `setModuleEnablement` body |
| Module key `modules[].moduleKey` | field | required | — | — | — | — | `setModuleEnablement` body |
| Is enabled `modules[].isEnabled` | toggle | required | — | — | — | — | `setModuleEnablement` body |

Errors to draw in the form: 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem)

**Form: Save feature toggles** (modal, opened by *Save feature toggles*; *Save feature toggles* calls `setFeatureToggles`, *Cancel* sends nothing)

**Collects what `setFeatureToggles` sends before it is called.** Required: `features`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Features `features` | repeatable rows | required | — | — | — | — | `setFeatureToggles` body |
| Feature key `features[].featureKey` | select | required | — | Digital companion mode · AI concierge chat · Lost and found · Push notifications · Social sharing · Multi language · Apple wallet · Google pay · Apple pay · Cash on delivery · Guest checkout · Uae pass login | — | The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum. | `setFeatureToggles` body |
| Is enabled `features[].isEnabled` | toggle | required | — | — | — | — | `setFeatureToggles` body |

**Form: Live now** (modal, opened by *Live now*; *Save maintenance mode* calls `setMaintenanceMode`, *Cancel* sends nothing)

**Live now: four controls, each labelled by what it does**, applied at once and never published or restored: Maintenance (on, message, back at), Minimum app version (iOS, Android), Contact (phone, email, WhatsApp, address, hours) and today’s availability (open, sold out, closed, message). The confirmation names the consequence ("Guests on web and app see the maintenance page from now until you clear it") (CHG-SGU-022). **Collects what `setMaintenanceMode` sends before it is called.** Required: `isInMaintenance`. Optional: `message`, `expectedBackAt`, `minimumAppVersion` (`ios`, `android`), `contact` (`phone`, `email`, `whatsapp`, `address`, `openingHours`), `availability` (`open` …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is in maintenance `isInMaintenance` | toggle | required | — | — | — | — | `setMaintenanceMode` body |
| Message `message` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setMaintenanceMode` body |
| Expected back at `expectedBackAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setMaintenanceMode` body |
| Minimum app version `minimumAppVersion` | group | optional | — | — | — | The oldest guest app build still allowed to run (decided 28 September, audit R073). | `setMaintenanceMode` body |
| Ios `minimumAppVersion.ios` | text field | optional | — | pattern `^\d+\.\d+\.\d+$` | — | — | `setMaintenanceMode` body |
| Android `minimumAppVersion.android` | text field | optional | — | pattern `^\d+\.\d+\.\d+$` | — | — | `setMaintenanceMode` body |
| Contact `contact` | group | optional | — | — | — | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). | `setMaintenanceMode` body |
| Phone `contact.phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `setMaintenanceMode` body |
| Email `contact.email` | email field | optional | — | — | name@example.ae | — | `setMaintenanceMode` body |
| Whatsapp `contact.whatsapp` | text field | optional | — | — | — | — | `setMaintenanceMode` body |
| Address `contact.address` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setMaintenanceMode` body |
| Opening hours `contact.openingHours` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Prose, as the guest reads it. The bookable hours are the catalogue's. | `setMaintenanceMode` body |
| Availability `availability` | segmented control | optional | Open | Open · Sold out · Closed | — | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. | `setMaintenanceMode` body |
| Availability message `availabilityMessage` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setMaintenanceMode` body |

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **modules[].isEnabled**: A switch per module. A module whose isLicensed is false is shown locked with "Not in your licence" and cannot be switched on. Switching one off that navigation or a homepage section still uses is refused (400); show the referencedBy list from the refusal with links to CMS-009 and CMS-007 to clear them first. *(source: contracts/satellite/white-label.yaml#setModuleEnablement)*
- **modules[visitPlanner]**: Off hides the app's Plan tab and WEB-050; say so beside the switch. *(source: contracts/satellite/white-label.yaml#/components/schemas/ModuleKey)*
- **features[].isEnabled**: A switch per feature. appleWallet, googlePay, applePay (wallet and payment) carry a "Needs an app update" tag (changeScope buildTime). guestCheckout defaults off and its helper text says it decides whether a guest can pay without an account after a one-time code; the fields the code pop-up asks are set on CMS-016 (guestContactFields). requiresConfiguration true shows "Set up first" with where. *(source: contracts/satellite/white-label.yaml#/components/schemas/FeatureToggle; ADR-0045)*
- **setMaintenanceMode body**: One "Live now" panel, never inside the publish. isInMaintenance switch with message per enabled language and expectedBackAt (date and time in the tenant's time zone); availability as three radio cards Open / Sold out today / Closed with availabilityMessage per language; minimumAppVersion iOS and Android as x.y.z (pattern ^\d+\.\d+\.\d+$, empty forces nothing); contact phone, email, WhatsApp, address and opening hours (prose, per language). Only the fields touched are sent: clearing maintenance must not clear contact. *(source: contracts/satellite/white-label.yaml#setMaintenanceMode; R073)*

#### Outputs: what the screen shows and produces

**Shown**

**Status** (banner, from `getTenantAppStatus`): Three badges in this order: Published (version and time, or "Never published"), Draft ("Unpublished changes"), Live now (maintenance, sold out today, closed, forced update). Counts: active of licensed modules, active pages.

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

**Site Builder** (card list, from `getSiteSetupProgress`): Shown while the minimum path is not done, with the next unfinished step; opens CMS-102.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Preset key | chip: Theme park, Water park, Museum, Theatre and arena, Single attraction, Play centre… | The starting point. Each preset proposes the modules, the booking flow types (with their default step order), the homepage sections, the … |
| Current step | chip: Venue and modules, Ticketing flows, Compose steps, Help me choose, Look and feel … | The seven Site Builder steps, in order (decided 29 September, W12): venue and modules (CMS-001), ticketing flows (CMS-103), compose steps … |
| Steps | grouped details | One entry per `SiteSetupStepKey`. |
| Minimum path done | yes / no (icon or chip) | True once the minimum path is done: a logo, the four theme colours, at least one enabled valid booking flow and a published version. |

**White label** (card list): Tiles: Brand kit, Theme, Typography, Logo and assets, Homepage and pages, Navigation, Banners, Booking settings, Booking flows, Help me choose, Languages, Domain, Versions, Publish, App build.

**Other areas** (card list): The DAM, privacy and waiver command centres (CMS-021 to CMS-100) are other modules' areas, grouped apart so the white-label path stays short (the 30-minute site, DI-988).

**The module enablement** (detail panel, from `getModuleEnablement`)

| Shows | Format | Notes |
|---|---|---|
| Module key | text | — |
| Display name | text | — |
| Is licensed | yes / no (icon or chip) | From the tenant's subscription. False makes enablement impossible. |
| Is enabled | yes / no (icon or chip) | — |
| Referenced by | list or chips (count when long) | Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same … |

**The feature toggle** (detail panel, from `getFeatureToggles`)

| Shows | Format | Notes |
|---|---|---|
| Feature key | chip: Digital companion mode, AI concierge chat, Lost and found, Push notifications … | `guestCheckout` is off by default (decided 17 September 2026, matrix 2.6.28, placement settled by … |
| Display name | text | — |
| Is enabled | yes / no (icon or chip) | — |
| Change scope | chip: Runtime, Build time | Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish. |
| Requires configuration | yes / no (icon or chip) | True where the feature needs credentials or setup elsewhere first. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save module enablement (primary button) | `setModuleEnablement` PUT `/tenant-config/modules` | inline | ModuleEnablement[] | 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem) | opens modal first |
| Save feature toggles (secondary button) | `setFeatureToggles` PUT `/tenant-config/features` | inline | FeatureToggle[] | — | opens modal first |
| Live now (secondary button) | `setMaintenanceMode` PUT `/tenant-config/status` | inline | TenantAppStatus | — | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Status header**: Three badges, in this order: Published (publishedVersion and publishedAt, or "Never published"), Draft ("Unpublished changes" when hasUnpublishedChanges), Live now (Maintenance on / Sold out today / Closed / Update forced for iOS x.y.z). Counts: active modules of licensed modules, active pages. *(source: contracts/satellite/white-label.yaml#/components/schemas/TenantAppStatus)*
- **Recent changes**: Newest first, area, description, who (name, never a raw principal id) and relative time; staff only. *(source: contracts/satellite/white-label.yaml#getTenantAppStatus)*
- **Site Builder card**: Shown while minimumPathDone is false, with the next unfinished step; leads to CMS-102. *(source: contracts/satellite/white-label.yaml#/components/schemas/SiteSetupProgress; DI-997)*
- **Workspace tiles**: Brand kit, Theme, Typography, Logo and assets, Homepage and pages, Navigation, Banners, Booking settings, Booking flows, Help me choose, Languages, Domain, Versions, Publish, App build. DAM, privacy and waiver command centres belong to other areas and sit in a separate group. *(source: screens/P13-white-label-cms.yaml#CMS-001)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save modules**: Writes the draft (not live). Toast "Saved to draft. Publish to show guests." Refusal lists what still links to the module. *(source: contracts/satellite/white-label.yaml#setModuleEnablement)*
- **Save features**: Writes the draft; for a buildTime feature the toast adds "App users get this with the next app update (CMS-104)". *(source: contracts/satellite/white-label.yaml#setFeatureToggles)*
- **Apply now (live status)**: Confirmation names the consequence ("Guests on web and app see the maintenance page from now until you clear it") and applies at once; no publish needed and a later restore does not undo it. *(source: contracts/satellite/white-label.yaml#setMaintenanceMode; R073)*

**Data it reads**: `getTenantAppStatus` (onLoad, Whether the guest web and app are live); `getModuleEnablement` (onLoad, Which modules guests can see); `getFeatureToggles` (onLoad, Which features are switched on); `getSiteSetupProgress` (onLoad, Where the tenant is in the Site Builder)

**Where the user goes next**

- → `CMS-102` Site Builder: *Site Builder*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-004` Logo & Assets: *Logo & Assets*
- → `CMS-061` Digital Asset Management Command Center: *Digital Asset Management Command Center*
- → `CMS-071` AI Asset Intelligence Command Center: *AI Asset Intelligence Command Center*
- → `CMS-081` DAM Governance & Rights Command Center: *DAM Governance & Rights Command Center*
- → `CMS-091` Asset Distribution & Delivery Command Center: *Asset Distribution & Delivery Command Center*
- → `CMS-008` Content Blocks: *Content Blocks*
- → `CMS-009` Navigation & Menus: *Navigation & Menus*
- → `CMS-010` Media Library: *Media Library*
- → `CMS-011` Translations: *Translations*
- → `CMS-016` Site Settings: *Site Settings*
- → `CMS-019` User Access: *User Access*
- → `CMS-015` Version History: *Version History*; carries `version`
- → `CMS-021` Privacy & Consent Configuration Command Center: *Privacy & Consent Configuration Command Center*
- → `CMS-031` Privacy Operations Command Center: *Privacy Operations Command Center*
- → `CMS-041` Waiver & Consent Command Center: *Waiver & Consent Command Center*
- → `CMS-051` Waiver Operations Command Center: *Waiver Operations Command Center*
- → `CMS-003` Typography: *Typography*
- → `CMS-025` Cookie, Tracking & Digital Technology Registry: *Opens Cookie, Tracking & Digital Technology Registry*
- → `CMS-026` Cookie Banner & Preference Center Designer: *Opens Cookie Banner & Preference Center Designer*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant, read by `getTenantAppStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing published yet: the status shows "Never published" and the Site Builder card offers to start (CMS-102). A tenant always exists here. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem) |

#### Edge cases to draw

- **Tenant has never published**: Status says "Your site is not live yet"; guests get 404 not-configured; the Site Builder card is the primary action. *(source: contracts/satellite/white-label.yaml#getTenantConfig)*
- **Maintenance on while a draft is unpublished**: Both badges show; publishing does not end maintenance (independent). *(source: contracts/satellite/white-label.yaml#setMaintenanceMode)*
- **Minimum app version set above the version in the stores**: Warn before applying that every app user is locked out until a newer build is released (CMS-104 newest released versionName shown beside the field). *(source: contracts/satellite/white-label.yaml#/components/schemas/MinimumAppVersion; contracts/satellite/white-label.yaml#/components/schemas/AppBuild)*
- **Caller has TENANT_CONFIGURE but not TENANT_PUBLISH**: Everything editable; the Publish tile shows "Ask someone with publish rights". *(source: contracts/satellite/white-label.yaml#publishTenantConfig)*

#### Consistency with other screens

- Match `CMS-102`: Step 1 of the Site Builder opens this screen; the module and feature switches are the same components.
- Match `CMS-014`: The Published / Draft badges use the same component and wording as the publish gate.
- Match `WEB-029`: The availability radio labels match the guest wording (Sold out today, Closed).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tenant: Coastal Leisure Group (مجموعة كوستال للترفيه)
publishedVersion: '14'
publishedAt: 2026-09-30 18:05 GST
draft: Unpublished changes (theme, homepage)
modules: ticketsAndBooking on, diningAndFnb on, shop on, map on, visitPlanner off (licensed), parking not licensed
features: guestCheckout off, aiConciergeChat on, applePay on (needs an app update)
liveNow:
  availability: soldOut
  availabilityMessage:
    en: Today is sold out. Book tomorrow from AED 249.
    ar: نفدت تذاكر اليوم. احجز للغد ابتداءً من 249 درهم.
  minimumAppVersion:
    ios: 2.3.0
    android: 2.3.0
contact:
  phone: +971 2 555 0142
  whatsapp: +971 50 555 0142
  email: hello@coastalaqua.ae
```

#### Permissions

- `getTenantAppStatus` → no permission · device, guest, staff
- `getModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `getFeatureToggles` → `TENANT_CONFIGURE` (configure) · staff
- `setModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `setFeatureToggles` → `TENANT_CONFIGURE` (configure) · staff
- `setMaintenanceMode` → `TENANT_CONFIGURE` (configure) · staff
- `getSiteSetupProgress` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.13 | Module Enablement - System shall allow enabling and disabling application modules. | Guest Mobile App & Branding | CONTRACTED | `setModuleEnablement` |
| 19.1.22 | Tenant-Specific Features - System shall support tenant-specific features. | Guest Mobile App & Branding | CONTRACTED | `setFeatureToggles` |
| 22.10.2 | White Label Branding | Marketing & CRM | CONTRACTED | `getSiteSetupProgress` |
| 19.2.83 | Digital Companion Mode - System shall transform the app into an in-venue digital companion experience. | Guest Mobile App & Branding | CONTRACTED | data `FeatureToggle` |
| 1.3.30 | System shall support physical, virtual and hybrid events with configurable attendance rules and access methods. | Ticketing Catalogue | CONTRACTED | data `FeatureToggle` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The CMS is a step-based site builder started from the workspace; a preset keeps the minimum path short (modules, booking flows, home sections and mobile tabs proposed), so an operator supplies only a logo, four colours and Publish; aim about 30 minutes to a working site. *(agreed · MoM 24 Sep 2026, M24-05 · DI-997)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Modules (`modules.modules`) | — | — | every guest screen (web, app and kiosk) | — |
| Modules: module key (`modules.modules[].moduleKey`) | — | — | every guest screen (web, app and kiosk) | — |
| Modules: is enabled (`modules.modules[].isEnabled`) | — | — | every guest screen (web, app and kiosk) | — |
| Features (`features.features`) | — | — | every guest screen (web, app and kiosk) | — |
| Features: feature key (`features.features[].featureKey`) | Digital companion mode · AI concierge chat · Lost and found · Push notifications · Social sharing · Multi language · Apple wallet · Google pay · Apple pay · Cash on delivery · Guest checkout · Uae … | — | every guest screen (web, app and kiosk) | The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum. |
| Features: is enabled (`features.features[].isEnabled`) | — | — | every guest screen (web, app and kiosk) | — |
| Is in maintenance (`maintenance.isInMaintenance`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Availability and maintenance message (`maintenance.message`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Expected back at (`maintenance.expectedBackAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Minimum app version (`maintenance.minimumAppVersion`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | The oldest guest app build still allowed to run (decided 28 September, audit R073). |
| Minimum app version: ios (`maintenance.minimumAppVersion.ios`) | pattern `^\d+\.\d+\.\d+$` | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Minimum app version: android (`maintenance.minimumAppVersion.android`) | pattern `^\d+\.\d+\.\d+$` | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Contact (`maintenance.contact`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (14) | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). |
| Contact: phone (`maintenance.contact.phone`) | +971 5X XXX XXXX (E.164) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Contact: email (`maintenance.contact.email`) | name@example.ae | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Contact: whatsapp (`maintenance.contact.whatsapp`) | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Contact: address (`maintenance.contact.address`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |
| Contact: opening hours (`maintenance.contact.openingHours`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | Prose, as the guest reads it. The bookable hours are the catalogue's. |
| Availability (`maintenance.availability`) | Open · Sold out · Closed | Open | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. |
| Availability message (`maintenance.availabilityMessage`) | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-001` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Marketing Board 7.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Marketing Board 7.dc.html`
- Client design-board frames: `Marketing Board 7.dc.html#crm-7f`
- Flow F102 *A brand is set, previewed, published and rolled back*, step 1: Tenant Workspace. See what is live before changing the brand. → The current published state is known, so a change can be compared against it. Rewired 23 September (L7) from subscription and billing operations, which the screen no longer declares.
- Flow F102 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-001?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save module enablement, Save feature toggles, Live now.
- [ ] Every transition is wired: `CMS-102`, `CMS-002`, `CMS-004`, `CMS-061`, `CMS-071`, `CMS-081`, `CMS-091`, `CMS-008`, `CMS-009`, `CMS-010`, `CMS-011`, `CMS-016`, `CMS-019`, `CMS-015`, `CMS-021`, `CMS-031`, `CMS-041`, `CMS-051`, `CMS-003`, `CMS-025`, `CMS-026`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-002` Brand Kit

**Set the things every surface reads.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-002 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `TENANT_CONFIGURE` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getBrandIdentity` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `uploadId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/white-label/brand-kit` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **This screen owns the marks and the logo variant** (logo, dark logo, variant, favicon); CMS-004 owns the app icons, the splash and the intro video, so the two never edit the same fields (CHG-SGU-022). `splashChangeScope` is read-only and shown, never sent.

**From the White Label & CMS process.** The brand kit at a glance: the marks (logo, dark logo, favicon), the logo variant that drives the theme tint, and a read-only swatch of the current theme and fonts with links to edit them. It is a summary and an upload point, not a second theme editor. Get the upload right: one control that uploads, checks format and size, and attaches.

**Fixed on main** (the package already carries these; draw what it says): formSetBrandIdentity lists splashChangeScope as an optional input. (CHG-SGU-022); Create upload and Complete upload are drawn as two separate buttons with their own modals (filename, contentType, sizeBytes). (CHG-SGU-022); CMS-002 and CMS-004 both edit the full BrandIdentity. (CHG-SGU-022).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Upload a logo | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | One upload control: it asks the platform for an upload (`createUpload`), sends the file and completes it (`completeUpload`) behind the one action; nobody types a file name, content type or size. | `BrandIdentity.logoAssetRef` |

**Form: Save brand identity** (modal, opened by *Save brand identity*; *Save brand identity* calls `setBrandIdentity`, *Cancel* sends nothing)

**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoVariant` (light, dark or duotone: which lockup sits in the nav bar and which colour reading of it drives the theme, decided 29 September, rev 3 CFG-4), `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`. **`showPoweredBy` is not asked here**: it is sent as read, and changed only on CMS-104 (CHG-R1S-012). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Logo `logoAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The primary logo. | `setBrandIdentity` body |
| Logo dark image `logoDarkAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Used on dark backgrounds. Falls back to the primary logo. | `setBrandIdentity` body |
| Logo variant `logoVariant` | segmented control | optional | Light | Light · Dark · Duotone | — | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). | `setBrandIdentity` body |
| Favicon `faviconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The browser tab icon for the guest web app. | `setBrandIdentity` body |
| Splash image `splashImageAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). | `setBrandIdentity` body |
| Splash duration seconds `splashDurationSeconds` | stepper or slider (seconds) | optional | 3 | min 0; max 10 | — | — | `setBrandIdentity` body |
| Splash background colour `splashBackgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setBrandIdentity` body |
| Show loading indicator `showLoadingIndicator` | toggle | optional | on | — | — | — | `setBrandIdentity` body |
| Intro video `introVideoAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). | `setBrandIdentity` body |
| Intro video mode `introVideoMode` | segmented control | optional | Off | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | — | When GST-001 plays it full screen. "Skip introduction" is always shown. | `setBrandIdentity` body |
| Show powered by `showPoweredBy` | toggle | optional | on | — | — | "Powered by TICVAI", a configuration toggle, on by default (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with DI-297; CHG-CSA-036). | `setBrandIdentity` body |

Errors to draw in the form: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 403 `showPoweredBy` false, and the tenant's licence does not allow removing "Powered by TICVAI" (`powered-by-locked`; workbook Q160, DI-297; CHG-CSA-036).

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **logoAssetRef / logoDarkAssetRef / faviconAssetRef**: One drop zone each. Accept PNG or SVG only, at most 2 MB, checked in the browser before upload and again by the server (400); explain the limit under the zone. The upload (createUpload then completeUpload) is invisible plumbing: the user sees one progress bar and the preview. Alt text is asked once at upload (completeUpload altText). *(source: contracts/satellite/white-label.yaml#setBrandIdentity; R270; DI-188)*
- **logoVariant**: Three thumbnails Light / Dark / Duotone, each showing the nav bar with that lockup; default Light. *(source: DI-1068)*

#### Outputs: what the screen shows and produces

**Shown**

**The brand identity** (detail panel, from `getBrandIdentity`): **The Powered-by credit is shown here read-only** and edited on CMS-104 (Chinmay, 3 October 2026, flow-brief defaults: "Powered-by toggle on CMS-104, shown read-only on CMS-002"; CHG-R1S-012).

| Shows | Format | Notes |
|---|---|---|
| Logo | the image or video | The primary logo. |
| Logo dark image | the image or video | Used on dark backgrounds. Falls back to the primary logo. |
| Logo variant | chip: Light, Dark, Duotone | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). |
| Favicon | the image or video | The browser tab icon for the guest web app. |
| Splash image | list or chips (count when long) | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish … |
| Splash duration seconds | 1,234 | — |
| Splash background colour | colour swatch | — |
| Show loading indicator | yes / no (icon or chip) | — |
| Splash change scope | chip: Runtime, Build time | Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163). |
| Show powered by | yes / no (icon or chip) | "Powered by TICVAI", a configuration toggle, on by default (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save brand identity (primary button) | `setBrandIdentity` PUT `/tenant-config/brand` | BrandIdentity | BrandIdentity | 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 403 `showPoweredBy` false, and the tenant's licence does not allow removing "Powered by TICVAI" (`powered-by-locked`; workbook Q160, DI-297 … | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Brand preview strip**: The guest header and the powered-by strip as they will look with the draft logo, theme and fonts, in English and Arabic side by side. *(source: DI-187; DI-111; docs/architecture/rtl-and-theming.md)*
- **Theme and fonts summary**: Read-only swatches of primary, secondary, accent, background, text, and the two font pairs, each linking to CMS-005 or CMS-003. *(source: screens/P13-white-label-cms.yaml#CMS-002)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save brand**: Writes the draft. Splash images are not here (CMS-004). *(source: contracts/satellite/white-label.yaml#setBrandIdentity)*

**Data it reads**: `getBrandIdentity` (onLoad, Read brand identity); `completeUpload` (background, Completes the upload behind the one upload control)

**Where the user goes next**

- → `CMS-005` Theme Editor: *Sets the colour theme*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-003` Typography: *Typography*
- → `CMS-004` Logo & Assets: *Logo & Assets*; carries `uploadId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The brand kit, read by `getBrandIdentity`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the brand kit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No brand kit yet. Offers Create upload (`createUpload`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) |

#### Edge cases to draw

- **SVG with embedded raster or scripts, or a 3 MB PNG**: Refused before upload with the reason; nothing replaces the current logo. *(source: R270)*
- **No dark logo**: The Dark variant previews the primary logo on dark and says it falls back. *(source: contracts/satellite/white-label.yaml#/components/schemas/BrandIdentity)*

#### Consistency with other screens

- Match `CMS-004`: The same logo upload component and limits; CMS-004 also holds icons, splash and intro video.
- Match `ADM-016`: Platform staff see the same brand panel through a grant.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
logo: coastal-aqua-logo.svg (148 KB)
logoDark: coastal-aqua-logo-white.svg (122 KB)
favicon: coastal-aqua-favicon.png 512 x 512 (18 KB)
logoVariant: duotone
```

#### Permissions

- `getBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `setBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.1 | Logo Management - System shall allow changing the mobile app logo through configuration. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 19.1.2 | Splash Screen Management - System shall allow changing splash screens. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | Light · Dark · Duotone | Light | every guest screen (web, app and kiosk) | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every P01 screen | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | every P02 screen | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | min 0; max 10 | 3 | every guest screen (web, app and kiosk) | — |
| Splash background colour (`brand.splashBackgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Show loading indicator (`brand.showLoadingIndicator`) | — | on | every guest screen (web, app and kiosk) | — |
| Intro video (`brand.introVideoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | GST-001 | When GST-001 plays it full screen. "Skip introduction" is always shown. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-002` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 1: Uploads the new logo and icons → **Assets, not code.** A logo change must not be a release
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-002?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save brand identity.
- [ ] Every transition is wired: `CMS-005`, `CMS-001`, `CMS-003`, `CMS-004`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-003` Typography

**Choose the two typefaces, Latin and Arabic; the type scale is TICVAI's fixed token set.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-003 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getFonts` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own · cold entry: Opens on the fonts in the draft; nothing to resolve. |
| Route | `/white-label/typography` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **37 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-015): Typography also read and saved the Theme (getTheme, setTheme); the theme belongs to CMS-005, and two save points for one record drift. The entry parameters … Removed 2 October 2026 (CHG-WIR-015): Typography also read and saved the Theme (getTheme, setTheme); the theme belongs to CMS-005, and two save points for one record drift. The entry parameters …

**From the White Label & CMS process.** Choose the font pairs the guest surfaces use: a primary (body) and an optional secondary (headings), each a Latin face and an Arabic face. The one thing to get right: an Arabic face is mandatory as soon as Arabic is an enabled language, and the preview must show both scripts at the same size so the pair can be judged.

**Fixed on main** (the package already carries these; draw what it says): Typography also reads and saves the Theme (setTheme, Save theme modal). (CHG-WIR-015); Purpose says "the two typefaces and the scale under them". (CHG-SGU-022); Entry parameters bannerId, pageId, policyKind, version and the "version link" cold entry. (CHG-SGU-022); formSetFonts sends changeScope. (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which faces are bundled (runtime) and which need an upload? The contract stores a free face name.** → Drawn default accepted: Offer the seven prototype pairs plus Tajawal and Baloo Bhaijaan 2 as bundled; anything else is an upload. *(decided by Chinmay, 2026-10-02; DEC-147 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**Form: Save fonts** (modal, opened by *Save fonts*; *Save fonts* calls `setFonts`, *Cancel* sends nothing)

**Collects what `setFonts` sends before it is called.** Required: `primaryLatin`. Optional: `primaryArabic`, `secondaryLatin`, `secondaryArabic`, `customFontAssetRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Primary latin `primaryLatin` | text field | required | — | — | — | — | `setFonts` body |
| Primary arabic `primaryArabic` | text field | optional | — | Required when `ar` is among the tenant's languages (audit R163). | — | Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match. | `setFonts` body |
| Secondary latin `secondaryLatin` | text field | optional | — | — | — | — | `setFonts` body |
| Secondary arabic `secondaryArabic` | text field | optional | — | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | `setFonts` body |
| Custom font images `customFontAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Uploaded font files, as `MediaAsset` ids. | `setFonts` body |

Errors to draw in the form: 400 `ar` is among the tenant's languages and `primaryArabic` is not set, or `secondaryLatin` is set without `secondaryArabic` (audit R163)

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **primaryLatin / secondaryLatin**: Pick from the bundled faces (runtime) or an uploaded file (buildTime for the app). Offer the prototype's pairs as presets: Archivo / IBM Plex Sans, Oswald / Barlow, Playfair Display / Karla, Fredoka / Nunito, Baloo 2 / Nunito Sans, Instrument Serif / Public Sans, Manrope. *(source: contracts/satellite/white-label.yaml#/components/schemas/FontConfig; sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html)*
- **primaryArabic / secondaryArabic**: Required when ar is among the tenant languages (primary always; secondary when a secondary Latin is set). Mark the field required with the reason "Arabic is enabled"; the server refuses with 400 otherwise. *(source: contracts/satellite/white-label.yaml#setFonts; R163)*
- **customFontAssetRefs**: Font files (WOFF2, TTF, OTF) through the media library. Tag "Needs an app update" because uploaded files are build-time on the app. Warn about display, script or very heavy weights overflowing banners and buttons. *(source: contracts/satellite/white-label.yaml#/components/schemas/FontConfig; DI-188; TRACKER Actions row 43)*

#### Outputs: what the screen shows and produces

**Shown**

**The font config** (detail panel, from `getFonts`)

| Shows | Format | Notes |
|---|---|---|
| Primary latin | text | — |
| Primary arabic | text | Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match. |
| Secondary latin | text | — |
| Secondary arabic | text | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). |
| Custom font images | list or chips (count when long) | Uploaded font files, as `MediaAsset` ids. |
| Change scope | chip: Runtime, Build time | Custom font files are `buildTime`; selecting a bundled face is `runtime`. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save fonts (primary button) | `setFonts` PUT `/tenant-config/fonts` | FontConfig | FontConfig | 400 `ar` is among the tenant's languages and `primaryArabic` is not set, or `secondaryLatin` is set without `secondaryArabic` (audit R163) | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Specimen**: Heading, body, a price (AED 249.00), a time range (09:00 – 17:00) and a button, in Latin and Arabic side by side and mirrored, at the guest sizes. Numbers and times stay left-to-right inside Arabic lines. *(source: docs/architecture/rtl-and-theming.md)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save fonts**: Writes the draft; the response's changeScope decides whether the toast adds "Needs an app update". *(source: contracts/satellite/white-label.yaml#setFonts)*

**Data it reads**: `getFonts` (onLoad, Read font configuration)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-004` Logo & Assets: *Logo & Assets*
- → `CMS-006` Component Preview: *Component Preview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The typography, read by `getFonts`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the typography untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No typography yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getFonts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `ar` is among the tenant's languages and `primaryArabic` is not set, or `secondaryLatin` is set without `secondaryArabic` (audit R163) |

#### Edge cases to draw

- **Arabic enabled later on CMS-011 with no Arabic face set**: Validation reports arabicFontMissing and the publish is blocked; this screen shows the gap at the top. *(source: contracts/satellite/white-label.yaml#/components/schemas/ConfigFindingKind)*

#### Consistency with other screens

- Match `CMS-011`: Enabling ar on CMS-011 makes primaryArabic required here; link both ways.
- Match `CMS-005`: Colours are edited on CMS-005 only.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
primary:
  latin: Manrope
  arabic: Tajawal
secondary:
  latin: Fredoka
  arabic: Baloo Bhaijaan 2
specimen:
  en: Splash into summer
  ar: انطلق في صيف من المرح
```

#### Permissions

- `getFonts` → `TENANT_CONFIGURE` (configure) · staff
- `setFonts` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getFonts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.5 | Font Management - System shall support configurable fonts. | Guest Mobile App & Branding | CONTRACTED | `setFonts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Primary latin (`fonts.primaryLatin`) | — | — | every guest screen (web, app and kiosk) | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | Required when `ar` is among the tenant's languages (audit R163). | — | every guest screen (web, app and kiosk) | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | — | — | every guest screen (web, app and kiosk) | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | every guest screen (web, app and kiosk) | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | every guest screen (web, app and kiosk) | Uploaded font files, as `MediaAsset` ids. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-003` · status **notStarted** · provenance generated
- Flow F102 *A brand is set, previewed, published and rolled back*, step 2: Typography. → 2 operations, 2 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-003?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save fonts.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-004`, `CMS-006`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-004` Logo & Assets

**Hold the marks every surface needs, at the sizes it needs them, and the mobile app's intro video (Site Builder steps 5 and 6).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-004 |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getBrandIdentity` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `uploadId` (navigation) |
| Route | `/white-label/logo-assets` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose. **This screen owns the app icons, the splash and the intro video**; the marks and the logo variant are CMS-002's (CHG-SGU-022). **Asset ids (the logo, icon source, splash and video) come from the media library (searchMedia) or an upload (createUpload, completeUpload), bound 4 October 2026** (CHG-FXS-003)

**From the White Label & CMS process.** The marks every surface needs at every size, and the parts of the app that only change with a store build: the 1024 px app icon, the splash, plus the streamed intro video that does not. The one thing to get right: separate "changes with the next publish" from "needs an app update" visually, so nobody expects a new icon tomorrow.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The favicon is set here as BrandIdentity.faviconAssetRef and also generated as web icons from the app icon (AppIcons.derived web 16/32/48). (CHG-SGU-025)

**Fixed on main** (the package already carries these; draw what it says): formSetBrandIdentity sends splashChangeScope. (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which favicon does the guest web use when both faviconAssetRef and the derived web icons exist?** → Drawn default accepted: faviconAssetRef when set, else the derived 32 px icon. *(decided by Chinmay, 2026-10-02; DEC-148 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Upload new | picker: choose an id | optional | — | — | shows names, sends the id | createUpload, the file PUT, completeUpload; the asset id fills the field being edited. | `MediaAsset.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | `searchMedia` ?kind |
| Tag | text field | — | — | `searchMedia` ?tag |
| Collection | picker: choose a collection | — | — | `searchMedia` ?collectionId |
| Search | text field | — | — | `searchMedia` ?search |
| Unused only | toggle | off | — | `searchMedia` ?unusedOnly |
| Rights expiring within days | number field (days) | — | — | `searchMedia` ?rightsExpiringWithinDays |

**Form: Save app icons** (modal, opened by *Save app icons*; *Save app icons* calls `setAppIcons`, *Cancel* sends nothing)

**Collects what `setAppIcons` sends before it is called.** Required: `sourceAssetRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source image `sourceAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The `MediaAsset` id of the 1024×1024 source, from `assets` `createUpload` then `completeUpload`. | `setAppIcons` body |

Errors to draw in the form: 400 Source is not 1024×1024, or contains transparency

**Form: Save brand identity** (modal, opened by *Save brand identity*; *Save brand identity* calls `setBrandIdentity`, *Cancel* sends nothing)

**Collects what `setBrandIdentity` sends before it is called.** Required: `logoAssetRef`. Optional: `logoVariant` (light, dark or duotone: which lockup sits in the nav bar and which colour reading of it drives the theme, decided 29 September, rev 3 CFG-4), `logoDarkAssetRef`, `faviconAssetRef`, `splashImageAssetRefs`, `splashDurationSeconds`, `splashBackgroundColour`, `showLoadingIndicator`, `introVideoAssetRef` and `introVideoMode` (off, first launch or every launch; MOB-5). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Logo `logoAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The primary logo. | `setBrandIdentity` body |
| Logo dark image `logoDarkAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Used on dark backgrounds. Falls back to the primary logo. | `setBrandIdentity` body |
| Logo variant `logoVariant` | segmented control | optional | Light | Light · Dark · Duotone | — | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). | `setBrandIdentity` body |
| Favicon `faviconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The browser tab icon for the guest web app. | `setBrandIdentity` body |
| Splash image `splashImageAssetRefs` | media picker (several) | optional | — | — | PNG, JPG, SVG or MP4 from the media library | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). | `setBrandIdentity` body |
| Splash duration seconds `splashDurationSeconds` | stepper or slider (seconds) | optional | 3 | min 0; max 10 | — | — | `setBrandIdentity` body |
| Splash background colour `splashBackgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setBrandIdentity` body |
| Show loading indicator `showLoadingIndicator` | toggle | optional | on | — | — | — | `setBrandIdentity` body |
| Intro video `introVideoAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). | `setBrandIdentity` body |
| Intro video mode `introVideoMode` | segmented control | optional | Off | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | — | When GST-001 plays it full screen. "Skip introduction" is always shown. | `setBrandIdentity` body |
| Show powered by `showPoweredBy` | toggle | optional | on | — | — | "Powered by TICVAI", a configuration toggle, on by default (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with DI-297; CHG-CSA-036). | `setBrandIdentity` body |

Errors to draw in the form: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 403 `showPoweredBy` false, and the tenant's licence does not allow removing "Powered by TICVAI" (`powered-by-locked`; workbook Q160, DI-297; CHG-CSA-036).

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **sourceAssetRef (app icon)**: One square drop zone: PNG, exactly 1024 x 1024, no transparency (400 otherwise, checked before upload). After save show the derived set as a grid by platform (iOS, Android, Web) with each size. *(source: contracts/satellite/white-label.yaml#setAppIcons)*
- **splashImageAssetRefs, splashDurationSeconds, splashBackgroundColour, showLoadingIndicator**: Ordered thumbnails (drag to reorder), duration stepper 0-10 s (default 3), colour picker with hex, indicator switch. *(source: contracts/satellite/white-label.yaml#/components/schemas/BrandIdentity)*
- **introVideoMode, introVideoAssetRef**: Segmented control Off / First launch / Every launch (default Off). Anything but Off requires picking a video from the media library (CMS-010); clips are muted, 6-12 s recommended. *(source: DI-1020; contracts/satellite/white-label.yaml#/components/schemas/BrandIdentity; DI-1080)*

#### Outputs: what the screen shows and produces

**Shown**

**The brand identity** (detail panel, from `getBrandIdentity`): **Intro video (decided 29 September, MOB-5).** Picked from the media library (CMS-010); plays off, on first launch or on every launch, always with Skip introduction. Streamed, so it needs no app build, unlike the splash and icons.

| Shows | Format | Notes |
|---|---|---|
| Logo | the image or video | The primary logo. |
| Logo dark image | the image or video | Used on dark backgrounds. Falls back to the primary logo. |
| Logo variant | chip: Light, Dark, Duotone | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). |
| Favicon | the image or video | The browser tab icon for the guest web app. |
| Splash image | list or chips (count when long) | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish … |
| Splash duration seconds | 1,234 | — |
| Splash background colour | colour swatch | — |
| Show loading indicator | yes / no (icon or chip) | — |
| Splash change scope | chip: Runtime, Build time | Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163). |
| Intro video | the image or video | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode | chip: Off, First launch, Every launch | When GST-001 plays it full screen. "Skip introduction" is always shown. |

**The app icons** (detail panel, from `getAppIcons`)

| Shows | Format | Notes |
|---|---|---|
| Source image | the image or video | The `MediaAsset` id of the 1024×1024 source. |
| Derived | list or chips (count when long) | Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on … |
| Change scope | chip: Runtime, Build time | Always `buildTime` — icons are baked into the binary. |
| Live version | text | Icon currently shipped. Differs from the draft until the next release. |
| Requires rebuild | yes / no (icon or chip) | True while the draft's source differs from the icon in `liveVersion`. |

**Media library** (card list, from `searchMedia`): Picking one fills the logo, icon source, splash and video with its id.

| Shows | Format | Notes |
|---|---|---|
| Filename | text | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 … |
| Content type | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save app icons (primary button) | `setAppIcons` PUT `/tenant-config/app-icons` | inline | AppIcons | 400 Source is not 1024×1024, or contains transparency | opens modal first |
| Save brand identity (secondary button) | `setBrandIdentity` PUT `/tenant-config/brand` | BrandIdentity | BrandIdentity | 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 403 `showPoweredBy` false, and the tenant's licence does not allow removing "Powered by TICVAI" (`powered-by-locked`; workbook Q160, DI-297 … | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Two bands**: "Changes when you publish" (logo, favicon, web icons, web splash, intro video) and "Needs an app update" (app icons, app splash). The second band shows liveVersion (the icon in the store app) beside the draft icon while requiresRebuild is true, with a link to CMS-104. *(source: contracts/satellite/white-label.yaml#/components/schemas/AppIcons; contracts/satellite/white-label.yaml#publishTenantConfig)*
- **Device previews**: Home-screen icon on an iPhone and an Android launcher, the splash at launch, the intro video frame with "Skip introduction". *(source: screens/P02-guest-mobile-app.yaml#GST-001)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save app icon**: Writes the draft and returns requiresRebuild true; the toast says app users see it after the next app update. *(source: contracts/satellite/white-label.yaml#setAppIcons)*
- **Save splash and intro**: Writes the draft. *(source: contracts/satellite/white-label.yaml#setBrandIdentity)*

**Data it reads**: `getBrandIdentity` (onLoad, The logo, favicon and splash in use); `getAppIcons` (onLoad, The app icon set at every size); `searchMedia` (onLoad, The media library, to pick an existing asset by name); `completeUpload` (background, Finish the upload once the file PUT succeeds; the asset id …)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*; carries `uploadId`
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The logo assets, read by `getBrandIdentity`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the logo assets untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No logo assets yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires to show this screen, and names that permission (the screen's other reads need `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An asset is larger than 2 MB, or is not PNG or SVG (audit R270); 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 400 Source is not 1024×1024, or contains transparency; 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is … |

#### Edge cases to draw

- **Icon with transparency or 1000 x 1000**: Refused before upload with the rule. *(source: contracts/satellite/white-label.yaml#setAppIcons)*
- **Intro video mode set without a video**: Save disabled with the reason (server 400 otherwise). *(source: contracts/satellite/white-label.yaml#/components/schemas/BrandIdentity)*

#### Consistency with other screens

- Match `CMS-104`: The store checklist's "App icons" item turns done from this screen.
- Match `GST-001`: The intro video overlay drawn there is what this preview shows.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
appIcon: coastal-aqua-icon-1024.png
liveIcon: version 2.2.0 (old wave mark)
splash:
  images:
  - splash-wave.png
  duration: 3
  background: '#0E7C86'
  indicator: true
introVideo:
  mode: firstLaunch
  asset: coastal-aqua-intro.mp4 (9 s
  muted): null
```

#### Permissions

- `getBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `getAppIcons` → `TENANT_CONFIGURE` (configure) · staff
- `setAppIcons` → `TENANT_CONFIGURE` (configure) · staff
- `setBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getBrandIdentity` requires to show this screen, and names that permission (the screen's other reads need `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.3 | App Icon Management - System shall support configurable app icons. | Guest Mobile App & Branding | CONTRACTED | `setAppIcons` |
| 19.1.1 | Logo Management - System shall allow changing the mobile app logo through configuration. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 19.1.2 | Splash Screen Management - System shall allow changing splash screens. | Guest Mobile App & Branding | CONTRACTED | `setBrandIdentity` |
| 22.1.9 | Campaign Asset Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 22.10.25 | Media Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 23.1.1 | System shall provide a centralized repository for storing and managing digital assets including images, videos, documents, PDFs, marketing materials, brand assets, audio files, templates, and … | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.5 | System shall support searching assets using keywords, metadata, tags, categories, and filters. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.15 | System shall expose DAM functionality through APIs and support integration with CMS, CRM, marketing platforms, mobile applications, and third-party systems. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |
| 23.1.3 | System shall support configurable metadata including asset type, owner, department, campaign, venue, event, creation date, expiry date, and usage rights. | Digital Asset Management | CONTRACTED | data `MediaAsset` |
| 23.1.10 | System shall support secure sharing of assets across departments, venues, tenants, and external partners. | Digital Asset Management | CONTRACTED | data `MediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | Light · Dark · Duotone | Light | every guest screen (web, app and kiosk) | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every P01 screen | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | PNG, JPG, SVG or MP4 from the media library | — | every P02 screen | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | min 0; max 10 | 3 | every guest screen (web, app and kiosk) | — |
| Splash background colour (`brand.splashBackgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Show loading indicator (`brand.showLoadingIndicator`) | — | on | every guest screen (web, app and kiosk) | — |
| Intro video (`brand.introVideoAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | GST-001 | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Source image (`appIcons.sourceAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | no guest screen: the phone's home screen and the store listing | The `MediaAsset` id of the 1024×1024 source, from `assets` `createUpload` then `completeUpload`. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-004` · status **notStarted** · provenance generated
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-004?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save app icons, Save brand identity.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-005` Theme Editor

**Tune the theme and watch it apply everywhere at once.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-005 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTheme` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/theme-editor` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **A failing colour contrast is refused, not warned (decided 28 September, audit R139 (a)).** `setTheme` answers `400` with a `ContrastProblem` naming each failing pair (foreground, background, ratio, the ratio required, where it is used); the theme is not saved, and the editor keeps the entered colours and marks the failing pairs so they can be corrected. There is no save-anyway. **No dark or light mode (decided by Chinmay, 2 October 2026; DEC-150).** White label applies the venue's chosen theme; `Theme.darkMode` is deprecated and ignored (CHG-CSA-035), so the editor never draws it (CHG-SGU-007).

**From the White Label & CMS process.** Tune the guest colours, shape and button style and watch every guest component change at once. Colour pairs that fail WCAG 2.2 AA are refused, not warned: the editor must show the failure live while the user picks, so the save never comes as a surprise. Per-element colours (call to action, pay, add to cart, Buy tickets, links, badges) sit under the palette, empty by default.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- screens/_design-tokens.yaml whiteLabel.overridable says only three tokens (accentSolid, surfaceRaised, typography.family.ui) are tenant-overridable. (CHG-SGU-025)
- Theme.cornerRadius has no default. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun "No theme editor yet. Offers no create action". (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What does secondaryColour colour on guest surfaces? The prototype palette has brand, accent, ink and surface only.** → Not answered: the workbook cell repeats the dark-mode answer. secondaryColour colours secondary buttons, the selected-tab underline and the footer background (drawn default). *(decided by Chinmay, 2026-10-02; DEC-149 / CHG-NOTE-009)*
- **May a tenant choose a dark guest app? rtl-and-theming.md says the tenant chooses colour, not theme; the contract has darkMode and the mobile prototype a Light/Dark mode.** → White label has no dark or light mode: the venue's chosen theme is applied. Theme.darkMode is deprecated: kept in the contract for compatibility, ignored, never used or drawn; the guest app has no Light/Dark switch (Pre-apply round, 2 October). *(decided by Chinmay, 2026-10-02; DEC-150 / CHG-NOTE-009 / CHG-SGU-007)*

#### Inputs: what the user enters or picks

**Form: Save theme** (modal, opened by *Save theme*; *Save theme* calls `setTheme`, *Cancel* sends nothing)

**Collects what `setTheme` sends before it is called.** Required: `primaryColour`, `secondaryColour`, `backgroundColour`, `textColour`. Optional: `accentColour`, `cornerRadius`, `surfaceStyle` (glass or solid, default glass) and `buttonStyle` (solid, outline or pill, default solid; decided 29 September, rev 3 CFG-3) and `componentColours` (M17-11). **A colour pair that fails contrast is refused** (`400 ContrastProblem`, decided 28 September, audit R139 (a)): the modal stays open with the failing pairs marked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Primary colour `primaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Secondary colour `secondaryColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Accent colour `accentColour` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Background colour `backgroundColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Text colour `textColour` | colour picker | required | — | — | #RRGGBB | — | `setTheme` body |
| Corner radius `cornerRadius` | stepper or slider | optional | — | min 0; max 32 | — | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). | `setTheme` body |
| Surface style `surfaceStyle` | segmented control | optional | Glass | Glass · Solid | — | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Button style `buttonStyle` | segmented control | optional | Solid | Solid · Outline · Pill | — | Button shape (decided 29 September, rev 3 CFG-3). | `setTheme` body |
| Component colours `componentColours` | group | optional | — | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. | `setTheme` body |
| Primary CTA `componentColours.primaryCta` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.primaryCta.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.primaryCta.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Pay button `componentColours.payButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.payButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.payButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Add to cart `componentColours.addToCart` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.addToCart.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.addToCart.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Buy tickets button `componentColours.buyTicketsButton` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.buyTicketsButton.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.buyTicketsButton.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Link `componentColours.link` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.link.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.link.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Badge `componentColours.badge` | group | optional | — | — | — | — | `setTheme` body |
| Background `componentColours.badge.background` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |
| Text `componentColours.badge.text` | colour picker | optional | — | — | #RRGGBB | — | `setTheme` body |

Errors to draw in the form: 400 A colour pair fails the contrast requirement. (ContrastProblem)

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **primaryColour, secondaryColour, accentColour, backgroundColour, textColour**: Colour pickers with a hex field (#RRGGBB, six digits; three-digit and rgba are not accepted). Primary, secondary, background and text required; accent optional. Offer named palette presets (prototype: Sunset amber, Deep teal, Stadium red, Playhouse plum, Saffron cream, Midnight ink, Desert gold, Ticvai blue...) which fill the five fields; a preset is not stored. *(source: contracts/satellite/white-label.yaml#/components/schemas/Theme; DI-393; DI-1066; sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html)*
- **live contrast check**: On every change call setTheme with Prefer validate-only (nothing written) and mark each failing pair with its ratio and the 4.5:1 required, and where it is used (e.g. "white text on primary button 3.2:1"). Save stays enabled but the server will refuse while any pair fails. *(source: contracts/satellite/white-label.yaml#setTheme; R139; DI-922)*
- **componentColours.{primaryCta, payButton, addToCart, buyTicketsButton, link, badge}**: Each a background and text pair, both optional; empty shows "Follows theme". Same contrast check per pair. *(source: DI-922; contracts/satellite/white-label.yaml#/components/schemas/Theme)*
- **cornerRadius**: Slider 0-22 px as the prototype (the contract allows up to 32); buttons are not affected (buttonStyle). *(source: DI-1066; sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html)*
- **surfaceStyle, buttonStyle**: Glass (default) / Solid; Solid (default) / Outline / Pill, each as a thumbnail. *(source: DI-1067)*
- **darkMode**: Deprecated: the field stays in the contract for compatibility, is ignored and is never drawn. White label has no dark or light mode; the venue's chosen theme applies. *(source: contracts/satellite/white-label.yaml#/components/schemas/Theme; screens/P01-guest-web-storefront.yaml; decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

#### Outputs: what the screen shows and produces

**Shown**

**The theme** (detail panel, from `getTheme`): **Per-element colours (decided 17 September, M17-11).** Pickers for the main call to action, the pay button, add to cart, the Buy tickets button, links and badges, each with a live contrast warning; left empty they follow the theme. The guest flow itself stays standard.

| Shows | Format | Notes |
|---|---|---|
| Primary colour | colour swatch | — |
| Secondary colour | colour swatch | — |
| Accent colour | colour swatch | — |
| Background colour | colour swatch | — |
| Text colour | colour swatch | — |
| Corner radius | 1,234 | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). |
| Surface style | chip: Glass, Solid | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). |
| Button style | chip: Solid, Outline, Pill | Button shape (decided 29 September, rev 3 CFG-3). |
| Component colours | grouped details | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |

**Contrast refused** (banner, from `setTheme`): Shown when `setTheme` answers 400. Lists every failing pair; the theme was not saved (decided 28 September, audit R139 (a)).

| Shows | Format | Notes |
|---|---|---|
| Failures | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save theme (primary button) | `setTheme` PUT `/tenant-config/theme` | Theme | Theme | 400 A colour pair fails the contrast requirement. (ContrastProblem) | opens modal first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Live component sheet**: The real guest components with the draft values: header, primary and secondary buttons, a ticket card with tags and a badge, the step indicator, the cart with Pay, the mobile tab bar with the Buy tickets button, a link, an input and an error message. LTR and RTL toggle (no light or dark toggle). Semantic colours (success, warning, danger) stay TICVAI's and are labelled "Fixed". *(source: DI-918; screens/_design-tokens.yaml; docs/architecture/rtl-and-theming.md; decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save theme**: Writes the draft (runtime, so guests see it after publish). On 400 ContrastProblem the entered colours stay and each failure is listed; there is no save anyway. *(source: contracts/satellite/white-label.yaml#setTheme; R139)*
- **Open full preview**: Goes to CMS-006 with the draft. *(source: screens/P13-white-label-cms.yaml#CMS-006)*

**Data it reads**: `getTheme` (onLoad, Read colour theme)

**Where the user goes next**

- → `CMS-007` Page Builder: *Rearranges the homepage*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*
- → `CMS-006` Component Preview: *Component Preview*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The theme editor, read by `getTheme`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the theme editor untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Before the first save `getTheme` answers 404 not-configured: the editor opens pre-filled from the preset with Save, and the first `setTheme` creates the part. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getTheme` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A colour pair fails the contrast requirement. (ContrastProblem) |

#### Edge cases to draw

- **Brand yellow #FFC845 as primary with white button text**: Marked live "white on #FFC845 1.5:1, needs 4.5:1"; suggest dark text #1F2937 which passes. *(source: R139)*
- **Logo variant duotone changes the tint**: The sheet re-reads the logo colours; the stored theme colours are still what is saved. *(source: DI-1068)*

#### Consistency with other screens

- Match `CMS-006`: The same component sheet, larger, with versions.
- Match `ADM-016`: Same editor through a grant; ADM-016 must include surfaceStyle, buttonStyle and componentColours too.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
primary: '#0E7C86'
secondary: '#0B4F6C'
accent: '#FFC845'
background: '#F7FAFB'
text: '#1F2937'
cornerRadius: 12
surfaceStyle: glass
buttonStyle: pill
componentColours:
  payButton:
    background: '#0B4F6C'
    text: '#FFFFFF'
contrastFailure:
  foreground: '#FFFFFF'
  background: '#FFC845'
  ratio: 1.54
  required: 4.5
  usage: badge text
```

#### Permissions

- `getTheme` → `TENANT_CONFIGURE` (configure) · staff
- `setTheme` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getTheme` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.4 | Color Theme Management - System shall support configurable color palettes. | Guest Mobile App & Branding | CONTRACTED | `setTheme` |
| 2.6.50 | System shall allow administrators to upload brand assets, logos, colors, fonts, content, images, and documents, and use AI to generate a white-label website layout including homepage, menus, headers … | Ticketing Sales | CONTRACTED | `setTheme` |
| 22.4.6 | Multi-Brand Support | Marketing & CRM | CONTRACTED | `setTheme` |
| 2.6.4 | The system should offer white label e-commerce engine for B2C sales (internal CMS). The interface of e-commerce engine should have configurable theming: - Color scheme can be updated - Background … | Ticketing Sales | CONTRACTED | data `Theme` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Per-element colours in the theme editor: pickers for the main call to action, pay button, add to cart, Buy tickets button, links and badges, each with a live contrast warning; left empty they follow the theme. The guest flow itself stays standard. *(agreed · MoM 17 Sep 2026, M17-11 · DI-922)*
- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Primary colour (`theme.primaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | body text on the background |
| Corner radius (`theme.cornerRadius`) | min 0; max 32 | — | every guest screen (web, app and kiosk) | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | Glass · Solid | Glass | every guest screen (web, app and kiosk) | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | Solid · Outline · Pill | Solid | every guest screen (web, app and kiosk) | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | — | — | every guest screen (web, app and kiosk) | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | — | — | every guest screen (web, app and kiosk) | the one main call to action on each screen, when it should differ from the brand colour |
| Primary CTA: background (`theme.componentColours.primaryCta.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Primary CTA: text (`theme.componentColours.primaryCta.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: pay button (`theme.componentColours.payButton`) | — | — | every guest screen (web, app and kiosk) | the Pay button at checkout |
| Pay button: background (`theme.componentColours.payButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Pay button: text (`theme.componentColours.payButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: add to cart (`theme.componentColours.addToCart`) | — | — | every guest screen (web, app and kiosk) | every Add to cart button |
| Add to cart: background (`theme.componentColours.addToCart.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Add to cart: text (`theme.componentColours.addToCart.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: buy tickets button (`theme.componentColours.buyTicketsButton`) | — | — | every guest screen (web, app and kiosk) | the persistent Buy tickets button (mobile tab bar) |
| Buy tickets button: background (`theme.componentColours.buyTicketsButton.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Buy tickets button: text (`theme.componentColours.buyTicketsButton.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: link (`theme.componentColours.link`) | — | — | every guest screen (web, app and kiosk) | text links |
| Link: background (`theme.componentColours.link.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Link: text (`theme.componentColours.link.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Component colours: badge (`theme.componentColours.badge`) | — | — | every guest screen (web, app and kiosk) | badges on cards (LIMITED, NEW, 11 left) |
| Badge: background (`theme.componentColours.badge.background`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Badge: text (`theme.componentColours.badge.text`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-005` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 2: Sets the colour theme → **Contrast checked and enforced**: a colour pair that fails 4.5:1 is refused by `setTheme` (`400 ContrastProblem`), because a brand colour that fails it is inaccessible (decided 28 September, audit …
- Flow F22 branch at step 2 (recoverable): when The brand colour fails contrast, **Refused, not warned** (decided 28 September, audit R139 (a)). `setTheme` answers `400 ContrastProblem` naming the failing pair, and the tenant picks a shade that passes 4.5:1. Nothing inaccessible …

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-005?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save theme.
- [ ] Every transition is wired: `CMS-007`, `CMS-001`, `CMS-002`, `CMS-003`, `CMS-006`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 9 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-006` Component Preview

**Check the theme against the components that carry it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-006 |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `TENANT_CONFIGURE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `productId` (CMS-006) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/white-label/component-preview` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **36 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-015): The screen was wired to the version table and publish gate (listConfigVersions, diffConfigVersion, publishTenantConfig, restoreConfigVersion), which are CMS-015 … Removed 2 October 2026 (CHG-WIR-015): The screen was wired to the version table and publish gate (listConfigVersions, diffConfigVersion, publishTenantConfig, restoreConfigVersion), which are CMS-015 … Removed 2 October 2026 (CHG-WIR-015): The screen was wired to the version table and publish gate (listConfigVersions, diffConfigVersion, publishTenantConfig, restoreConfigVersion), which are CMS-015 …

**From the White Label & CMS process.** Check the draft theme against every component that carries it, on web, iPhone and Android, LTR and RTL, and share a preview link before publishing. It is a preview screen, not version history.

**Fixed on main** (the package already carries these; draw what it says): The screen is wired to listConfigVersions, diffConfigVersion, publishTenantConfig and restoreConfigVersion (a version table and publish … (CHG-WIR-015); F102 step 3 to step 4 jumps from CMS-006 to ADM-016 (cross-device, platform console). (CHG-CLN-005).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the preview also render the PDF ticket and Apple / Google Wallet pass?** → Previews of the PDF ticket and the Apple/Google Wallet pass are in Block A. *(decided by Chinmay, 2026-10-02; DEC-151 / CHG-NOTE-009 / CHG-SGU-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product for the ticket preview | picker: choose an id | optional | — | — | shows names, sends the id | The product whose ticket and passes are previewed. | `Product.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Effective for venue | picker: choose an effective for venue | — | — | `getBookingFlowConfig` ?effectiveForVenueId |

**Form: Create preview** (modal, opened by *Create preview*; *Create preview* calls `createPreview`, *Cancel* sends nothing)

**Collects what `createPreview` sends before it is called.** Nothing in the body is required. Optional: `platform`, `language`, `expiresInHours`. Dismissing sends nothing; the screen behind is unchanged. Optional `outputs` (app, pdfTicket, appleWalletPass, googleWalletPass) and `productId` add the ticket and pass previews (CHG-SGU-008).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Platform `platform` | segmented control | optional | — | Ios · Android · Web | — | — | `createPreview` body |
| Language `language` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `createPreview` body |
| Outputs `outputs` | multi-select chips | optional | — | App · Pdf ticket · Apple wallet pass · Google wallet pass | — | What to render besides the app (CHG-CSA-041). Absent means `app` only. | `createPreview` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | The product whose ticket and passes to render; a sample ticket where absent. | `createPreview` body |
| Expires in hours `expiresInHours` | number field (hours) | optional | 24 | min 1; max 168 | — | — | `createPreview` body |

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **createPreview {platform, theme, language, expiresInHours}**: Platform web / ios / android; theme always light (the venue's theme; darkMode is deprecated); language from the enabled languages; link expiry 1-168 hours (default 24). *(source: contracts/satellite/white-label.yaml#createPreview / decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

#### Outputs: what the screen shows and produces

**Shown**

**Theme** (detail panel, from `getTheme`)

| Shows | Format | Notes |
|---|---|---|
| Primary colour | colour swatch | — |
| Secondary colour | colour swatch | — |
| Accent colour | colour swatch | — |
| Background colour | colour swatch | — |
| Text colour | colour swatch | — |
| Corner radius | 1,234 | The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). |
| Surface style | chip: Glass, Solid | Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3). |
| Button style | chip: Solid, Outline, Pill | Button shape (decided 29 September, rev 3 CFG-3). |
| Component colours | grouped details | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary CTA | grouped details | — |
| Background | colour swatch | — |
| Text | colour swatch | — |
| Pay button | grouped details | — |
| Background | colour swatch | — |
| Text | colour swatch | — |
| Add to cart | grouped details | — |
| Background | colour swatch | — |
| Text | colour swatch | — |
| Buy tickets button | grouped details | — |
| Background | colour swatch | — |

**Fonts** (detail panel, from `getFonts`)

| Shows | Format | Notes |
|---|---|---|
| Primary latin | text | — |
| Primary arabic | text | Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match. |
| Secondary latin | text | — |
| Secondary arabic | text | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). |
| Custom font images | list or chips (count when long) | Uploaded font files, as `MediaAsset` ids. |
| Change scope | chip: Runtime, Build time | Custom font files are `buildTime`; selecting a bundled face is `runtime`. |

**Brand** (detail panel, from `getBrandIdentity`)

| Shows | Format | Notes |
|---|---|---|
| Logo | the image or video | The primary logo. |
| Logo dark image | the image or video | Used on dark backgrounds. Falls back to the primary logo. |
| Logo variant | chip: Light, Dark, Duotone | Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4). |
| Favicon | the image or video | The browser tab icon for the guest web app. |
| Splash image | list or chips (count when long) | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish … |
| Splash duration seconds | 1,234 | — |
| Splash background colour | colour swatch | — |
| Show loading indicator | yes / no (icon or chip) | — |
| Splash change scope | chip: Runtime, Build time | Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163). |
| Intro video | the image or video | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode | chip: Off, First launch, Every launch | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Show powered by | yes / no (icon or chip) | "Powered by TICVAI", a configuration toggle, on by default (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with … |

**Booking flow** (detail panel, from `getBookingFlowConfig`)

| Shows | Format | Notes |
|---|---|---|
| Preset | chip: Auto, Ticket box, Play centre, Venue site, Marketplace, Single event… | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator | chip: Bar, Numbered, Dots, Segmented, Breadcrumb, Pills… | — |
| Cart layout | chip: Sidebar right, Sidebar left, Slide in right, Slide up bottom, Single column … | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). |
| Cart side in RTL | chip: Keep right, Mirror | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). |
| Card layout | chip: Stacked rows, Split rows, Cards across, Poster cards | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked … |
| Card size | chip: Compact, Standard, Large, Extra large | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). |
| Seat picker | chip: Bowl, Zones then seats, Zones only, Seats only | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view | chip: 2D, 3D | — |
| Density | chip: Compact, Standard, Roomy | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). |
| Embed mode | chip: Full page, Embedded | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. |
| Hero banner | yes / no (icon or chip) | — |
| Search in banner | yes / no (icon or chip) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates | yes / no (icon or chip) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page | yes / no (icon or chip) | — |
| Quantities on add ons | yes / no (icon or chip) | — |
| Times per page | chip: 8, 12, 24, All | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 … |
| Day part filter | yes / no (icon or chip) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries | grouped details | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Afternoon starts at | text | — |
| Evening starts at | text | — |

**PDF ticket and wallet passes** (live preview, from `previewProductTickets`): **In Block A (decided by Chinmay, 2 October 2026; DEC-151).** The PDF ticket and the Apple and Google Wallet passes rendered with the draft theme; `createPreview` with `outputs` pdfTicket, appleWalletPass, googleWalletPass and a `productId` returns a link per output (CHG-CSA-041) (CHG-SGU-008).

| Shows | Format | Notes |
|---|---|---|
| Template | the name it points at, never the id | — |
| Media type | chip: Thermal ticket, A4 pdf, Wristband, RFID card, Wallet pass, QR only… | — |
| Locale | text | — |
| Content ref | text | Where the rendered proof can be fetched or sent to the printer from. |
| Wallet platform | chip: Apple wallet, Google wallet | Which wallet the pass preview is for, where `mediaType` is `walletPass` (DEC-151; CHG-CSP-038). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create preview (primary button) | `createPreview` POST `/tenant-config/preview` | inline | Preview | — | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Component gallery**: Every guest component in its states (default, hover, pressed, disabled, error, selected) rendered from the draft: buttons, cards in the four card layouts and four sizes, step indicator styles, cart layouts, tab bar and Buy tickets button styles, inputs, badges and tags, banners, the powered-by strip. *(source: DI-036; DI-395; DI-1040)*
- **Preview link**: The URL with expiry time, copy and QR code for testing on a phone; says it shows the draft, not what is live. *(source: contracts/satellite/white-label.yaml#/components/schemas/Preview)*
- **PDF ticket and wallet pass**: In Block A the preview also renders the PDF ticket and the Apple and Google Wallet passes with the draft theme. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Create preview link**: A short-lived link rendering the working draft; nothing is published. *(source: contracts/satellite/white-label.yaml#createPreview)*

**Data it reads**: `getTheme` (onLoad, The theme being previewed); `getFonts` (onLoad, The fonts being previewed); `getBrandIdentity` (onLoad, The marks being previewed); `getBookingFlowConfig` (onLoad, The booking presentation being previewed)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*
- → `CMS-014` Publishing Workflow: *White-Label Branding Management*; calls `createPreview`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The component preview list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the component preview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No component preview yet. Offers Create preview (`createPreview`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters its list, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getTheme` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_VIEW` for `previewProductTickets`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Preview link opened after expiry**: The guest-side page says the preview expired and offers nothing else (never the live site under a preview label). *(source: contracts/satellite/white-label.yaml#/components/schemas/Preview)*

#### Consistency with other screens

- Match `CMS-005`: The same component sheet.
- Match `CMS-012`: RTL preview is the same renderer with language ar.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
preview:
  platform: ios
  theme: light
  language: ar
  expiresAt: 2026-10-02 18:00 GST
  url: https://preview.coastalaqua.ticvai.com/p/7f3c...
```

#### Permissions

- `createPreview` → `TENANT_CONFIGURE` (configure) · staff
- `getTheme` → `TENANT_CONFIGURE` (configure) · staff
- `getFonts` → `TENANT_CONFIGURE` (configure) · staff
- `getBrandIdentity` → `TENANT_CONFIGURE` (configure) · staff
- `getBookingFlowConfig` → `TENANT_CONFIGURE` (configure) · staff
- `previewProductTickets` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getTheme` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_VIEW` for `previewProductTickets`.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.5 | System shall support pricing calendar management. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.6 | System shall support automatic activation of future pricing. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.7 | System shall support overlapping pricing schedules with priority rules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.8 | System shall maintain pricing schedule history. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.9 | System shall provide pricing schedule audit trails. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 2.6.4 | The system should offer white label e-commerce engine for B2C sales (internal CMS). The interface of e-commerce engine should have configurable theming: - Color scheme can be updated - Background … | Ticketing Sales | CONTRACTED | data `Theme` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)*
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-006` · status **notStarted** · provenance generated
- Flow F102 *A brand is set, previewed, published and rolled back*, step 3: Component Preview. → 2 operations, 2 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (63 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create preview, What publishing changes.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `CMS-014`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-007` Page Builder

**Assemble a storefront page from blocks the tenant cannot break.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-007 |
| Who uses it | venue staff holding `AI_USE`, `TENANT_CONFIGURE`, `TENANT_PUBLISH` (1 operate, 2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getHomepageLayout` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `pageId` (navigation), `actionId` (navigation), `blockId` (navigation) |
| Route | `/white-label/page-builder` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **A section whose module is off is disabled in the builder (decided 28 September, audit R163 (4)).** The builder reads `getModuleEnablement` and applies the mapping on `HomepageSectionKind`: `tickets` needs `ticketsAndBooking`, `whatsOn` needs `events`, `attractions` needs `attractions`, `membership` needs `membership`, `dining` needs `diningAndFnb`, `shop` needs `shop`, `map` needs `map`; `heroBanner`, `quickActions`, `promotions`, `customContent` and `spacer` need none. A section whose module is off cannot be added or made visible, and says which module to switch on (on CMS-001). `setHomepageLayout` refuses such a section with 400 in any case. **The builder loads and edits existing blocks with listContentBlocks and updateContentBlock (agreed, ledger) 4 October 2026** (CHG-FXS-003) **Save block edits an existing block (updateContentBlock)** (CHG-FXS-003)

**From the White Label & CMS process.** Arrange the guest homepage (web Home and app Home) from fixed section kinds, and set the header and footer and the content pages. Sections reorder by drag and drop; a section whose module is off cannot be added or shown. Get right that the tenant arranges and fills, never invents components.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- formCreateContentPage requires id and status and offers isReferenced and scopePath; formSetFooter requires id and scopePath. (CHG-SGU-024)
- One HomepageLayout and one HeaderConfig serve both web and app. (CHG-SGU-024)
- screens/_components.yaml defines an appHeader region (tenant-branded) and no footer region, and no guest screen reads HeaderConfig or FooterConfig. (CHG-SGU-025)

**Fixed on main** (the package already carries these; draw what it says): setHeader is in apis but no control or form is drawn. (CHG-SGU-006); Content blocks (createContentBlock, publishContentBlock) are declared by no Block A screen (only BO-839). (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Fixed 2-3 card layout or N-count for the experiences and dining section on the app landing?** → Every customisation option in the approved wireframe/prototype, including the card count per section. *(decided by Chinmay, 2026-10-02; DEC-152 / CHG-NOTE-009 / CHG-SGU-009)*
- **Selectable scroll animations on the landing page (Rise, Scale, Slide, Blur, None) have no field.** → Scroll animation (Rise, Scale, Slide, Blur, None) is a field on landing-page sections. *(decided by Chinmay, 2026-10-02; DEC-153 / CHG-NOTE-009 / CHG-SGU-009)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Draft · Published · Archived | `listContentPages` ?status |
| Category code | text field | — | — | `listContentPages` ?categoryCode |
| Slug | text field | — | pattern `^[a-z0-9-]+$` | `listContentPages` ?slug |
| Page key | text field | — | — | `listContentBlocks` ?pageKey |

**Form: Create content page** (modal, opened by *Create content page*; *Create content page* calls `createContentPage`, *Cancel* sends nothing)

**Collects what `createContentPage` sends.** Required: `slug`, `title`, `body`. Optional: `isEnabled`, `iconAssetRef`, `categoryCode`, `sortOrder`. are the server's and never asked. Dismissing sends nothing. Not asked, because the server sets them (readOnly in the contract): `id`, `isReferenced`, `scopePath`, `status` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Slug `slug` | text field | required | — | pattern `^[a-z0-9-]+$` | — | — | `createContentPage` body |
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createContentPage` body |
| Body `body` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `createContentPage` body |
| Is enabled `isEnabled` | toggle | optional | on | — | — | BL-005. Enablement is not publication. | `createContentPage` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createContentPage` body |
| Category code `categoryCode` | text field | optional | — | — | — | — | `createContentPage` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `createContentPage` body |

Errors to draw in the form: 409 Slug already in use

**Form: Save content page** (modal, opened by *Save content page*; *Save content page* calls `updateContentPage`, *Cancel* sends nothing)

**Collects what `updateContentPage` sends before it is called.** Required: `slug`, `title`, `body`. Optional: `isEnabled`, `iconAssetRef`, `categoryCode`, `sortOrder`, `status`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Slug `slug` | text field | required | — | pattern `^[a-z0-9-]+$` | — | — | `updateContentPage` body |
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `updateContentPage` body |
| Body `body` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `updateContentPage` body |
| Is enabled `isEnabled` | toggle | optional | on | — | — | — | `updateContentPage` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateContentPage` body |
| Category code `categoryCode` | text field | optional | — | — | — | — | `updateContentPage` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `updateContentPage` body |
| Status `status` | segmented control | optional | — | Draft · Published · Archived | — | Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). | `updateContentPage` body |

Errors to draw in the form: 409 The page is `published` and the body changes more than its status to `archived` (audit R163).

**Form: Save homepage layout** (modal, opened by *Save homepage layout*; *Save homepage layout* calls `setHomepageLayout`, *Cancel* sends nothing)

**Collects what `setHomepageLayout` sends before it is called.** Required: `sections`. Dismissing sends nothing; the screen behind is unchanged. Per section: `maxItems` (the venue's choice) and `scrollAnimation` (rise, scale, slide, blur, none); `templateKey` and `landingSource` (CHG-SGU-009). Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Template key `templateKey` | text field | optional | — | — | — | The landing-page template this layout started from (`listLandingPageTemplates`), or null for a layout composed from scratch (CHG-CSA-037). | `setHomepageLayout` body |
| Landing source `landingSource` | segmented control | optional | Storefront | Storefront · Own site | — | `storefront`: this home is the tenant's landing page. `ownSite`: the tenant's own website is the landing page and links in with deep links; this home is still served at the … | `setHomepageLayout` body |
| Sections `sections` | repeatable rows | required | — | — | — | — | `setHomepageLayout` body |
| Kind `sections[].kind` | select | required | — | Hero banner · Quick actions · Tickets · Whats on · Attractions · Membership · Dining · Shop · Promotions · Map · Custom content · Venue overview …; `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events`; `attractions` needs `attractions`; `membership` … | — | Which module each section needs, proposed, client to correct (decided 28 September, audit R163). | `setHomepageLayout` body |
| Title `sections[].title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setHomepageLayout` body |
| Sort order `sections[].sortOrder` | number field | required | — | — | — | — | `setHomepageLayout` body |
| Is visible `sections[].isVisible` | toggle | required | — | — | — | — | `setHomepageLayout` body |
| Content page `sections[].contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `setHomepageLayout` body |
| Max items `sections[].maxItems` | number field | optional | — | — | — | How many cards the section shows, the venue's choice (Chinmay, 2 October, workbook Q152: every customisation option of the approved wireframe, including the card count per … | `setHomepageLayout` body |
| Scroll animation `sections[].scrollAnimation` | radio group | optional | Rise | Rise · Scale · Slide · Blur · None | — | How the section enters as the guest scrolls (Chinmay, 2 October, workbook Q153: "must be there"; DI-1088; CHG-CSA-040). | `setHomepageLayout` body |
| Hero style `sections[].heroStyle` | radio group | optional | — | Carousel · Video · Poster · Split | — | For `heroBanner` only (decided 29 September, MOB-3). | `setHomepageLayout` body |

Errors to draw in the form: 400 A section references a disabled module or a missing content block

**Form: New content block** (modal, opened by *New content block*; *New content block* calls `createContentBlock`, *Cancel* sends nothing)

The block's content per language, where it shows, when (schedule) and for whom (audience), as the block editor fields; ids and scope are the server's.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Page `pageId` | picker: choose a page | optional | — | — | shows names, sends the id | — | `createContentBlock` body |
| Kind `kind` | select | required | — | Rich text · Image · Video · Gallery · CTA · FAQ · Form · Embed · Product grid · Countdown · Testimonial | — | — | `createContentBlock` body |
| Position `position` | number field | optional | — | — | — | — | `createContentBlock` body |
| Body `body` | key and value settings | optional | — | — | — | Typed by `kind`, and validated against the block's own schema at save. | `createContentBlock` body |
| Locale variants `localeVariants` | key and value settings | optional | — | — | — | Per-locale bodies, not per-locale pages. A venue running Arabic and English should not maintain two page trees that drift — the structure is shared and the words are not. | `createContentBlock` body |
| Publish at `publishAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Content scheduling, which the configuration model had no room for. A seasonal banner that needs somebody awake at midnight is the same defect `Product.onSaleFrom` fixed. | `createContentBlock` body |
| Expire at `expireAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createContentBlock` body |
| Audience segment `audienceSegmentId` | picker: choose an audience segment | optional | — | — | shows names, sends the id | Personalisation, evaluated at render. A block shown only to members, or only to first-time visitors. | `createContentBlock` body |

**Form: Publish block** (modal, opened by *Publish block*; *Publish block* calls `publishContentBlock`, *Cancel* sends nothing)

Publish now or at a set time; says whether the venue's review step applies.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Publish at `publishAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishContentBlock` body |
| Expire at `expireAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishContentBlock` body |

**Form: Save block** (modal, opened by *Save block*; *Save block* calls `updateContentBlock`, *Cancel* sends nothing)

**Collects what `updateContentBlock` sends before it is called**, for the block selected in Blocks on this page. At least one of: `body` (the block's content, typed by its kind, in the block editor's fields), `localeVariants` (the per-language bodies), `position` (its order on the page; a drag sets it), `publishAt`, `expireAt` and `audienceSegmentId` (who sees it). Only what changed is sent. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | key and value settings | optional | — | — | — | As `ContentBlock.body`. | `updateContentBlock` body |
| Locale variants `localeVariants` | key and value settings | optional | — | — | — | As `ContentBlock.localeVariants`. | `updateContentBlock` body |
| Position `position` | number field | optional | — | — | — | — | `updateContentBlock` body |
| Publish at `publishAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateContentBlock` body |
| Expire at `expireAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateContentBlock` body |
| Audience segment `audienceSegmentId` | picker: choose an audience segment | optional | — | — | shows names, sends the id | — | `updateContentBlock` body |

Carried, not typed: `blockId`

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The block is published (`content-block-published`).

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **sections[] (kind, sortOrder, isVisible, title, maxItems, heroStyle, contentPageId)**: A vertical list of section cards, drag to reorder, eye icon for isVisible, title per language. heroStyle only on heroBanner (Carousel / Video / Poster / Split). Every customisation option in the approved wireframe, including the card count per section (maxItems). contentPageId only on customContent (a picker of pages). Disabled kinds show "Needs <module> (switch on in CMS-001)". *(source: contracts/satellite/white-label.yaml#/components/schemas/HomepageLayout; R163; DI-1018; decided 2 October 2026 by Chinmay (CHG-NOTE-009))*
- **header (HeaderConfig)**: Layout thumbnails Logo left / Logo centre / Logo with menu (required), switches for logo, menu, notifications, background colour. *(source: contracts/satellite/white-label.yaml#/components/schemas/HeaderConfig)*
- **footer (FooterConfig)**: Columns of links (heading, label, URL, or "opens cookie preferences"), then a separate locked group of legal links (terms and privacy required, accessibility and cookie policy optional), copyright, social links. The Powered by TICVAI credit shows in the preview; whether it shows is the Powered by toggle (CMS-104, default on). *(source: contracts/satellite/white-label.yaml#setFooter; DI-111; decided 2 October 2026 by Chinmay (CHG-NOTE-009))*
- **content page (slug, title, body, isEnabled, icon, categoryCode, sortOrder)**: Slug lowercase letters, digits and hyphens, unique (409); title and body per enabled language; a published page is read-only except Archive. *(source: contracts/satellite/white-label.yaml#createContentPage; contracts/satellite/white-label.yaml#updateContentPage)*
- **Scroll animation**: Per landing-page section: Rise, Scale, Slide, Blur or None (a field to be added). *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-009))*

#### Outputs: what the screen shows and produces

**Shown**

**Start from a template** (card list, from `listLandingPageTemplates`): **For a tenant without its own landing page** (decided by Chinmay, 2 October 2026; DEC-548): the storefront home starts from a TICVAI template (`HomepageLayout.templateKey`, `landingSource` storefront). A tenant with its own site keeps it and links in with deep links (CMS-009) (CHG-SGU-005).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Template key | text | — |
| Name | text | — |
| Preset key | text | The Site Builder preset it belongs to (`SiteSetupProgress.presetKey`). |
| Thumbnail URL | text | — |
| Layout | grouped details | The client-approved web and app wireframes are the layout (Chinmay, 2 October, workbook Q163; CHG-CSA-040): sections, their order and their … |
| Template key | text | The landing-page template this layout started from (`listLandingPageTemplates`), or null for a layout composed from scratch (CHG-CSA-037). |
| Landing source | chip: Storefront, Own site | `storefront`: this home is the tenant's landing page. `ownSite`: the tenant's own website is the landing page and links in with deep links … |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Sections | list or chips (count when long) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The homepage layout** (detail panel, from `getHomepageLayout`): **Also the mobile Home editor (decided 29 September, MOB-3; Site Builder steps 5 and 6).** The `venueOverview` section (description, opening hours, type tiles), the hero's style (carousel, video, poster or split) and the highlights for attractions, dining, what's on and shop (`maxItems`, the venue\'s choice per section, DEC-152). The header and footer are set here too (`setHeader`, `setFooter`). …

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Sections | list or chips (count when long) | — |

**Modules the sections need** (detail panel, from `getModuleEnablement`): A section whose module is off (mapping on `HomepageSectionKind`) is shown disabled and cannot be added or made visible (decided 28 September, audit R163 (4)).

| Shows | Format | Notes |
|---|---|---|
| Module key | text | — |
| Display name | text | — |
| Is enabled | yes / no (icon or chip) | — |

**Every content page** (data table, from `listContentPages`)

| Shows | Format | Notes |
|---|---|---|
| Slug | text | — |
| Title | in the reader's language | — |
| Status | chip: Draft, Published, Archived | Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`). |
| Icon | the image or video | — |
| Category code | text | — |
| Sort order | 1,234 | — |

**Blocks on this page** (card list, from `listContentBlocks`): In page order; drag to reorder (updateContentBlock position).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Page | the name it points at, never the id | — |
| Kind | chip: Rich text, Image, Video, Gallery, CTA, FAQ… | — |
| Position | 1,234 | — |
| Body | grouped details | Typed by `kind`, and validated against the block's own schema at save. |
| Locale variants | grouped details | Per-locale bodies, not per-locale pages. A venue running Arabic and English should not maintain two page trees that drift — the structure … |
| Status | chip: Draft, Scheduled, Published, Expired, Archived | Created as `draft`; moved by `publishContentBlock` and the `publishAt`/`expireAt` timer (`states/content-block.yaml`), never by the body of … |
| Publish at | 1 Oct 2026, 14:30 | Content scheduling, which the configuration model had no room for. A seasonal banner that needs somebody awake at midnight is the same … |
| Expire at | 1 Oct 2026, 14:30 | — |
| Audience segment | the name it points at, never the id | Personalisation, evaluated at render. A block shown only to members, or only to first-time visitors. |
| Approved by principal | the name it points at, never the id | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save block (secondary button) | `updateContentBlock` PATCH `/content-blocks/{blockId}` | inline | ContentBlock | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The block is published (`content-block-published`). | opens modal first |
| Save homepage layout (primary button) | `setHomepageLayout` PUT `/tenant-config/homepage` | HomepageLayout | HomepageLayout | 400 A section references a disabled module or a missing content block | opens modal first |
| Create content page (secondary button) | `createContentPage` POST `/tenant-config/pages` | ContentPage | ContentPage | 409 Slug already in use | opens modal first |
| Save content page (secondary button) | `updateContentPage` PUT `/tenant-config/pages/{pageId}` | UpdateContentPageRequest | ContentPage | 409 The page is `published` and the body changes more than its status to `archived` (audit R163). | opens modal first |
| New content block (secondary button) | `createContentBlock` POST `/content-blocks` | ContentBlock | ContentBlock | — | opens modal first |
| Publish block (secondary button) | `publishContentBlock` POST `/content-blocks/{blockId}/publish` | inline | ContentBlock | — | opens modal first |
| What publishing a block changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Split preview**: Web Home and app Home side by side with the draft order, updated on every drag. *(source: DI-394; F22 step 3)*
- **Pages list**: Slug, title (default language), status Draft / Published / Archived, Enabled, "Linked" when isReferenced. *(source: contracts/satellite/white-label.yaml#/components/schemas/ContentPage)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save homepage**: Writes the draft; 400 names a section whose module is off or whose page is missing. *(source: contracts/satellite/white-label.yaml#setHomepageLayout)*
- **Save header / Save footer**: Writes the draft. *(source: contracts/satellite/white-label.yaml#setHeader; contracts/satellite/white-label.yaml#setFooter)*
- **Delete page**: Refused 409 while navigation or the homepage links to it; the dialog names the links. *(source: contracts/satellite/white-label.yaml#deleteContentPage)*
- **Draft with AI**: Proposes section copy or a page from a brief; the author edits and applies; the choice is recorded. *(source: MATRIX 22.10.16; screens/P13-white-label-cms.yaml#CMS-007)*

**Data it reads**: `listContentPages` (onLoad, The guest app's content pages); `getHomepageLayout` (onLoad, Read homepage layout); `getModuleEnablement` (onLoad, Which modules are on, so a section whose module is off is …); `listLandingPageTemplates` (onLoad, The landing-page templates TICVAI provides (DEC-548)); `listContentBlocks` (onLoad, The page's existing blocks, in order: agreed with the …)

**Where the user goes next**

- → `CMS-012` RTL Preview: *Previews in both directions*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record, read by `getHomepageLayout`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No record yet. Offers Create content page (`createContentPage`). |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listContentPages` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `proposeMarketingContent`, `decideProposedAction`; `TENANT_PUBLISH` for `publishContentBlock`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A section references a disabled module or a missing content block; 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and …; 409 Page is referenced by navigation or the homepage; 409 Slug already in use |

#### Edge cases to draw

- **Editing a published page**: Fields read-only, banner "Published pages can only be archived. Archive it and create a new page." (409 published-page-locked). *(source: contracts/satellite/white-label.yaml#updateContentPage)*
- **Disabling a page that is on the homepage**: Allowed (enablement is not publication); the section shows "Page disabled, section hidden". *(source: contracts/satellite/white-label.yaml#/components/schemas/ContentPage)*

#### Consistency with other screens

- Match `WEB-001`: The web Home renders these sections in this order.
- Match `GST-001`: The app Home renders venueOverview, hero, type tiles and highlights from these sections.
- Match `CMS-009`: Navigation links to pages are made there; isReferenced comes from both.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sections:
- heroBanner (video)
- venueOverview
- tickets
- attractions (2)
- dining (1)
- promotions
- map
header:
  layout: logoLeft
  showNotifications: true
footer:
  columns:
  - heading: Visit
    links:
    - Opening hours
    - Getting here
    - Accessibility
  - heading: Help
    links:
    - FAQ
    - Contact us
    - Cookie preferences
  legal:
    termsUrl: /p/terms
    privacyUrl: /p/privacy
  copyright: © 2026 Coastal Leisure Group
page:
  slug: plan-your-visit
  title:
    en: Plan your visit
    ar: خطط لزيارتك
```

#### Permissions

- `listContentPages` → `TENANT_CONFIGURE` (configure) · staff, guest
- `createContentPage` → `TENANT_CONFIGURE` (configure) · staff
- `updateContentPage` → `TENANT_CONFIGURE` (configure) · staff
- `getHomepageLayout` → `TENANT_CONFIGURE` (configure) · staff
- `setHomepageLayout` → `TENANT_CONFIGURE` (configure) · staff
- `getModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `deleteContentPage` → `TENANT_CONFIGURE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `createContentBlock` → `TENANT_CONFIGURE` (configure) · staff
- `publishContentBlock` → `TENANT_PUBLISH` (configure) · staff
- `listLandingPageTemplates` → `TENANT_CONFIGURE` (configure) · staff
- `listContentBlocks` → `TENANT_CONFIGURE` (configure) · staff
- `updateContentBlock` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listContentPages` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `proposeMarketingContent`, `decideProposedAction`; `TENANT_PUBLISH` for `publishContentBlock`.

#### Requirements it meets

29 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.20 | Tenant-Specific Content - System shall support tenant-specific content. | Guest Mobile App & Branding | CONTRACTED | `listContentPages` |
| 2.6.19 | - General information for Guests | Ticketing Sales | CONTRACTED | `listContentPages` |
| 19.1.15 | Custom Content Pages - System shall support custom content pages. | Guest Mobile App & Branding | CONTRACTED | `createContentPage` |
| 19.1.9 | Homepage Layout Management - System shall support configurable homepage layouts. | Guest Mobile App & Branding | CONTRACTED | `setHomepageLayout` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| … 17 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)*
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)*
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)*
- Custom content pages per venue (e.g. "Plan Your Visit", Accessibility) that follow accessibility guidelines. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-190)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Landing-page template (`homepage.templateKey`) | — | — | WEB-001 | the landing-page template the home started from (listLandingPageTemplates); a tenant with no landing page of its own starts from one, and the sections it fills stay editable |
| Landing source (`homepage.landingSource`) | Storefront · Own site | Storefront | the guest home screens | whether the storefront home is the landing page, or the tenant's own site is and links in with deep links |
| Sections (`homepage.sections`) | — | — | the guest home screens | — |
| Sections: kind (`homepage.sections[].kind`) | Hero banner · Quick actions · Tickets · Whats on · Attractions · Membership · Dining · Shop · Promotions · Map · Custom content · Venue overview …; `tickets` needs `ticketsAndBooking`; `whatsOn` … | — | the guest home screens | Which module each section needs, proposed, client to correct (decided 28 September, audit R163). |
| Sections: title (`homepage.sections[].title`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Sections: sort order (`homepage.sections[].sortOrder`) | — | — | the guest home screens | — |
| Sections: is visible (`homepage.sections[].isVisible`) | — | — | the guest home screens | — |
| Sections: content page (`homepage.sections[].contentPageId`) | shows names, sends the id | — | the guest home screens | — |
| Sections: card count (`homepage.sections[].maxItems`) | — | — | GST-001, WEB-001 | how many cards the section shows, the counts the approved wireframe offers |
| Sections: scroll animation (`homepage.sections[].scrollAnimation`) | Rise · Scale · Slide · Blur · None | Rise | the guest home screens | how the section enters as the guest scrolls: rise, scale, slide, blur or none (none whenever the device asks for reduced motion) |
| Sections: hero style (`homepage.sections[].heroStyle`) | Carousel · Video · Poster · Split | — | GST-001 | For `heroBanner` only (decided 29 September, MOB-3). |
| Slug (`pages.slug`) | pattern `^[a-z0-9-]+$` | — | the content and policy pages | — |
| Content pages title (`pages.title`) | English and Arabic (Arabic right to left) | — | the content and policy pages | — |
| Body (`pages.body`) | English and Arabic (Arabic right to left) | — | the content and policy pages | Keyed by language code. Values are sanitised HTML. |
| Content pages is enabled (`pages.isEnabled`) | — | on | the content and policy pages | BL-005. Enablement is not publication. |
| Icon (`pages.iconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the content and policy pages | — |
| Category code (`pages.categoryCode`) | — | — | GST-057 | — |
| Content pages sort order (`pages.sortOrder`) | — | — | the content and policy pages | — |
| Content pages status (`pages.status`) | Draft · Published · Archived | — | the content and policy pages | Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-007` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 3: Rearranges the homepage → Sections reordered, drag and drop
- Flow F22 branch at step 3 (recoverable): when Content exists only in English, Published anyway, with the gap listed per locale. **A CMS that blocks publishing until every locale is complete is a CMS nobody publishes from.**

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-007?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save block, Save homepage layout, Create content page, Save content page, New content block, Publish block, What publishing a block changes.
- [ ] Every transition is wired: `CMS-012`, `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `AI_USE`, `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-008` Content Blocks

**Define what a block can and cannot contain, and set the banners (Site Builder step 5).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-008 |
| Who uses it | venue staff holding `AI_USE`, `TENANT_CONFIGURE` (1 operate, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPromoBlocks` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `bannerId` (navigation), `promoBlockId` (navigation), `actionId` (navigation) |
| Route | `/white-label/content-blocks` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Banners and promo blocks go live on their own schedule, not with Publish** (the contract header lists them outside the draft); the screen says so beside each (CHG-SGU-022).

**From the White Label & CMS process.** Schedule banners and promotional blocks for the guest Home, Explore and checkout. Each has a time window in the tenant's time zone and moves by itself from draft to scheduled to live to expired. The one thing to get right: show the state and window clearly, and lock a promo block once it has gone live (withdraw only).

**Fixed on main** (the package already carries these; draw what it says): Create forms require id and offer state and scopePath (readOnly). (CHG-SGU-022); deleteBanner is in apis but no button; banners have no detail panel (only promo blocks). (CHG-SGU-022); Banners and promo blocks are scheduled outside the publish, while the header says every set* writes the draft. (CHG-SGU-022).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a banner's isActive switch a manual pause on top of the schedule?** → Drawn default accepted: Draw it as Pause / Resume; a paused banner does not show even inside its window. *(decided by Chinmay, 2026-10-02; DEC-154 / CHG-NOTE-009)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| State | radio group | — | Draft · Scheduled · Active · Expired | `listBanners` ?state |

**Form: Create banner** (modal, opened by *Create banner*; *Create banner* calls `createBanner`, *Cancel* sends nothing)

**Collects what `createBanner` sends before it is called.** Required:, `title`, `imageAssetRef`, `startsAt`. Optional: `subtitle`, `placement`, `linkTarget`, `endsAt`, `sortOrder`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createBanner` body |
| Subtitle `subtitle` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createBanner` body |
| Image `imageAssetRef` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createBanner` body |
| Placement `placement` | radio group | optional | — | Homepage hero · Homepage block · Explore · Checkout | — | — | `createBanner` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `createBanner` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `createBanner` body |
| Module key `linkTarget.moduleKey` | field | optional | — | — | — | — | `createBanner` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `createBanner` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `createBanner` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `createBanner` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `createBanner` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `createBanner` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createBanner` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. | `createBanner` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `createBanner` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createBanner` body |

**Form: Save banner** (modal, opened by *Save banner*; *Save banner* calls `updateBanner`, *Cancel* sends nothing)

**Collects what `updateBanner` sends before it is called.** Nothing in the body is required. Optional: `title`, `subtitle`, `imageAssetRef`, `placement`, `linkTarget`, `startsAt`, `endsAt`, `sortOrder`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateBanner` body |
| Subtitle `subtitle` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateBanner` body |
| Image `imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateBanner` body |
| Placement `placement` | radio group | optional | — | Homepage hero · Homepage block · Explore · Checkout | — | — | `updateBanner` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `updateBanner` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `updateBanner` body |
| Module key `linkTarget.moduleKey` | field | optional | — | — | — | — | `updateBanner` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `updateBanner` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `updateBanner` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updateBanner` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `updateBanner` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `updateBanner` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateBanner` body |
| Ends at `endsAt` | date and time picker | optional | — | When set, must follow `startsAt` (audit R163), or 400. | 1 Oct 2026, 14:30 (venue time zone) | Null runs the banner with no end. When set, must follow `startsAt` (audit R163), or 400. | `updateBanner` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `updateBanner` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateBanner` body |

**Form: Create promo block** (modal, opened by *Create promo block*; *Create promo block* calls `createPromoBlock`, *Cancel* sends nothing)

**Collects what `createPromoBlock` sends before it is called.** Required:, `title`. Optional: `description`, `iconAssetRef`, `promotionId`, `linkTarget`, `startsAt`, `endsAt`, `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createPromoBlock` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createPromoBlock` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createPromoBlock` body |
| Promotion `promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | Presentation only. A block may point at a promotion; it does not create or price one. | `createPromoBlock` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `createPromoBlock` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `createPromoBlock` body |
| Module key `linkTarget.moduleKey` | field | optional | — | — | — | — | `createPromoBlock` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `createPromoBlock` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `createPromoBlock` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `createPromoBlock` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `createPromoBlock` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `createPromoBlock` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPromoBlock` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Must follow `startsAt` when both are set (decided 28 September, audit R163). | `createPromoBlock` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `createPromoBlock` body |

Errors to draw in the form: 400 `endsAt` is not after `startsAt` (audit R163)

**Form: Save promo block** (modal, opened by *Save promo block*; *Save promo block* calls `updatePromoBlock`, *Cancel* sends nothing)

**Collects what `updatePromoBlock` sends before it is called.** Nothing in the body is required. Optional: `title`, `description`, `iconAssetRef`, `promotionId`, `linkTarget`, `startsAt`, `endsAt`, `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updatePromoBlock` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updatePromoBlock` body |
| Icon `iconAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updatePromoBlock` body |
| Promotion `promotionId` | picker: choose a promotion | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| Link target `linkTarget` | group | optional | — | — | — | — | `updatePromoBlock` body |
| Kind `linkTarget.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `updatePromoBlock` body |
| Module key `linkTarget.moduleKey` | field | optional | — | — | — | — | `updatePromoBlock` body |
| App section `linkTarget.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `updatePromoBlock` body |
| Content page `linkTarget.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| Product `linkTarget.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| Event `linkTarget.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `updatePromoBlock` body |
| URL `linkTarget.url` | text field | optional | — | — | — | — | `updatePromoBlock` body |
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePromoBlock` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePromoBlock` body |
| Sort order `sortOrder` | number field | optional | — | — | — | — | `updatePromoBlock` body |

Errors to draw in the form: 400 `endsAt` is not after `startsAt` (audit R163); 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The block is `active` or `expired`, and may only be withdrawn (audit R163).

**Form: Delete banner** (confirmDialog, opened by *Delete banner*; *Delete banner* calls `deleteBanner`, *Cancel* sends nothing)

Names the banner and where it shows; it disappears from the storefront at once.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Banner {title, subtitle, imageAssetRef, placement, linkTarget, startsAt, endsAt, sortOrder}**: Title and subtitle per language; image from the media library (landscape, at least 1600 px wide, crop preview for web and app); placement Home hero / Home block / Explore / Checkout; link picker (module, page, product, event, URL); startsAt required, endsAt optional and after startsAt (400). *(source: contracts/satellite/white-label.yaml#/components/schemas/Banner; R163; DI-1080)*
- **PromoBlock {title, description, iconAssetRef, promotionId, linkTarget, startsAt, endsAt}**: A block may point at a promotion but never prices one; dates optional, end after start. *(source: contracts/satellite/white-label.yaml#createPromoBlock)*

#### Outputs: what the screen shows and produces

**Shown**

**Every promo block** (data table, from `listPromoBlocks`)

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Description | in the reader's language | — |
| Icon | the image or video | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | Must follow `startsAt` when both are set (decided 28 September, audit R163). |
| State | chip: Draft, Scheduled, Active, Expired | Moved by the schedule timer at `startsAt` and `endsAt`, in the tenant's timezone, as for `Banner.state`. |

**Every banner** (data table, from `listBanners`)

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Subtitle | in the reader's language | — |
| Image | the image or video | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. |
| State | chip: Draft, Scheduled, Active, Expired | Moved by `updateBanner` between `draft` and `scheduled`, and by the schedule timer from `scheduled` to `active` and `active` to `expired` … |

**The selected promo block** (detail panel, from `listPromoBlocks`)

| Shows | Format | Notes |
|---|---|---|
| Title | in the reader's language | — |
| Description | in the reader's language | — |
| Icon | the image or video | — |
| Link target | grouped details | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | Must follow `startsAt` when both are set (decided 28 September, audit R163). |
| State | chip: Draft, Scheduled, Active, Expired | Moved by the schedule timer at `startsAt` and `endsAt`, in the tenant's timezone, as for `Banner.state`. |
| Sort order | 1,234 | — |

**The selected banner** (detail panel, from `listBanners`): Select, edit and delete a banner as for promo blocks.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Title | in the reader's language | — |
| Subtitle | in the reader's language | — |
| Image | the image or video | — |
| Placement | chip: Homepage hero, Homepage block, Explore, Checkout | — |
| Link target | grouped details | — |
| Kind | chip: Module, Content page, Product, Event, External URL, App section… | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore … |
| Module key | text | — |
| App section | chip: Home, Explore, Plan, Tickets, Map, Account… | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses … |
| Content page | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| URL | text | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. |
| State | chip: Draft, Scheduled, Active, Expired | Moved by `updateBanner` between `draft` and `scheduled`, and by the schedule timer from `scheduled` to `active` and `active` to `expired` … |
| Sort order | 1,234 | — |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create banner (primary button) | `createBanner` POST `/tenant-config/banners` | Banner | Banner | — | opens modal first |
| Save banner (secondary button) | `updateBanner` PATCH `/tenant-config/banners/{bannerId}` | inline | Banner | — | opens modal first |
| Create promo block (secondary button) | `createPromoBlock` POST `/tenant-config/promo-blocks` | PromoBlock | PromoBlock | 400 `endsAt` is not after `startsAt` (audit R163) | opens modal first |
| Save promo block (secondary button) | `updatePromoBlock` PATCH `/tenant-config/promo-blocks/{promoBlockId}` | inline | PromoBlock | 400 `endsAt` is not after `startsAt` (audit R163); 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The block is `active` or `expired`, and may only be … | opens modal first |
| Delete promo block (destructive button) | `deletePromoBlock` DELETE `/tenant-config/promo-blocks/{promoBlockId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Delete banner (destructive button) | `deleteBanner` DELETE `/tenant-config/banners/{bannerId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens confirmDialog first |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Calendar strip and list**: Each banner and block with its state badge (Draft, Scheduled, Live, Expired), window in the tenant time zone, placement and a thumbnail; filter by state. *(source: contracts/satellite/white-label.yaml#listBanners; contracts/satellite/white-label.yaml#/components/schemas/ScheduleState)*

**What each action does** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Save banner / Save block**: Saves; a scheduled one goes live at startsAt without anyone acting. *(source: contracts/satellite/white-label.yaml#createBanner)*
- **Withdraw block**: deletePromoBlock; the only change allowed once a block is live or expired (amend is 409 published-block-locked). *(source: contracts/satellite/white-label.yaml#updatePromoBlock)*
- **Delete banner**: Removes it; the dialog says whether it is live now. *(source: contracts/satellite/white-label.yaml#deleteBanner)*

**Data it reads**: `listPromoBlocks` (onLoad, List promotional blocks); `listBanners` (onLoad, List banners)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

**What opens over it**

- confirmDialog *Delete promo block*: **Names what `deletePromoBlock` changes and what it leaves alone**, in the consequence rather than the verb. A content blocks this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The content blocks list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the content blocks untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No content blocks yet. Offers Create banner (`createBanner`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listPromoBlocks` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listPromoBlocks` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `proposeMarketingContent`, `decideProposedAction`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `endsAt` is not after `startsAt` (audit R163); 409 Drafting is not allowed at this scope now: the capability is paused (`capability-paused`) or governance blocks it (`governance-blocked`, naming the policy and …; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 409 The block is `active` or `expired`, and may only be withdrawn … |

#### Edge cases to draw

- **A Ramadan banner from 18:00 to 02:00 next day**: Window shown in GST with the date change; it starts and ends by the timer. *(source: contracts/satellite/white-label.yaml#createBanner)*
- **Banner linked to a disabled module**: Draw the link picker without disabled modules. *(source: contracts/satellite/white-label.yaml#setNavigation)*

#### Consistency with other screens

- Match `WEB-001`: homepageHero and homepageBlock placements render there.
- Match `GST-002`: explore placement renders there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
banner:
  title:
    en: Summer splash nights
    ar: ليالي الصيف المائية
  placement: homepageHero
  startsAt: 2026-10-10 16:00 GST
  endsAt: 2026-11-30 23:59 GST
  link: product Night Splash Pass
promoBlock:
  title:
    en: Family of four from AED 799
    ar: عائلة من أربعة أفراد ابتداءً من 799 درهم
  state: active
```

#### Permissions

- `createBanner` → `TENANT_CONFIGURE` (configure) · staff
- `updateBanner` → `TENANT_CONFIGURE` (configure) · staff
- `createPromoBlock` → `TENANT_CONFIGURE` (configure) · staff
- `updatePromoBlock` → `TENANT_CONFIGURE` (configure) · staff
- `deletePromoBlock` → `TENANT_CONFIGURE` (configure) · staff
- `listPromoBlocks` → `TENANT_CONFIGURE` (configure) · staff
- `listBanners` → `TENANT_CONFIGURE` (configure) · staff
- `deleteBanner` → `TENANT_CONFIGURE` (configure) · staff
- `proposeMarketingContent` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listPromoBlocks` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `proposeMarketingContent`, `decideProposedAction`.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.10 | Banner Management - System shall support configurable promotional banners. | Guest Mobile App & Branding | CONTRACTED | `createBanner` |
| 19.1.11 | Promotional Block Management - System shall support configurable promotional content blocks. | Guest Mobile App & Branding | CONTRACTED | `updatePromoBlock` |
| 22.3.18 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.9 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.4.10 | AI Subject Line Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.9.17 | AI Language Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.14 | AI Content Generation | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.16 | AI Website Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 22.10.17 | AI Mobile App Content Builder | Marketing & CRM | CONTRACTED | `proposeMarketingContent` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Reusable page components per venue type are to be documented (e.g. seat-map component for stadiums/amphitheatres, park-map component for attraction venues) so one layout serves many venues with only imagery/data swapped. Documentation pending from Allam. *(open · MoM 20 Aug 2026, 4.10 CMS & White-Label; 6. Open Items · DI-395)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Banners title (`banners.title`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Banners subtitle (`banners.subtitle`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Image (`banners.imageAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the guest home screens | — |
| Banners placement (`banners.placement`) | Homepage hero · Homepage block · Explore · Checkout | — | the guest home screens | — |
| Banners link target (`banners.linkTarget`) | — | — | the guest home screens | — |
| Link target: kind (`banners.linkTarget.kind`) | Module · Content page · Product · Event · External URL · App section · None | — | the guest home screens | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. |
| Link target: module key (`banners.linkTarget.moduleKey`) | — | — | the guest home screens | — |
| Link target: app section (`banners.linkTarget.appSection`) | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | the guest home screens | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. |
| Link target: content page (`banners.linkTarget.contentPageId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: product (`banners.linkTarget.productId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: event (`banners.linkTarget.eventId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: uRL (`banners.linkTarget.url`) | — | — | the guest home screens | — |
| Banners starts at (`banners.startsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | — |
| Banners ends at (`banners.endsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. |
| Banners sort order (`banners.sortOrder`) | — | — | the guest home screens | — |
| Is active (`banners.isActive`) | — | — | the guest home screens | — |
| Promo blocks title (`promoBlocks.title`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Promo blocks description (`promoBlocks.description`) | English and Arabic (Arabic right to left) | — | the guest home screens | — |
| Icon (`promoBlocks.iconAssetRef`) | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the guest home screens | — |
| Promotion (`promoBlocks.promotionId`) | shows names, sends the id | — | the guest home screens | Presentation only. A block may point at a promotion; it does not create or price one. |
| Promo blocks link target (`promoBlocks.linkTarget`) | — | — | the guest home screens | — |
| Link target: kind (`promoBlocks.linkTarget.kind`) | Module · Content page · Product · Event · External URL · App section · None | — | the guest home screens | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. |
| Link target: module key (`promoBlocks.linkTarget.moduleKey`) | — | — | the guest home screens | — |
| Link target: app section (`promoBlocks.linkTarget.appSection`) | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | the guest home screens | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. |
| Link target: content page (`promoBlocks.linkTarget.contentPageId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: product (`promoBlocks.linkTarget.productId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: event (`promoBlocks.linkTarget.eventId`) | shows names, sends the id | — | the guest home screens | — |
| Link target: uRL (`promoBlocks.linkTarget.url`) | — | — | the guest home screens | — |
| Promo blocks starts at (`promoBlocks.startsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | — |
| Promo blocks ends at (`promoBlocks.endsAt`) | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | Must follow `startsAt` when both are set (decided 28 September, audit R163). |
| Promo blocks sort order (`promoBlocks.sortOrder`) | — | — | the guest home screens | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-008` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (62), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create banner, Save banner, Create promo block, Save promo block, Delete promo block, Delete banner.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `AI_USE`, `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-009` Navigation & Menus

**Three editors, each saved on its own: the header, the footer and the mobile tab bar with the Buy tickets button (Site Builder steps 5 and 6); and the links a tenant's own site uses to deep-link in.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-009 |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listMenus` reads the population and `getMenu` reads one of them — list, select, act |
| Offline | online only |
| Opens with | nothing: it opens on its own · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/white-label/navigation-menus` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): "Navigation & Menus" means site navigation menus; the F&B menu operations (listMenus, getMenu, createMenu, setMenuSections, updateMenu) were attached by name … Removed 2 October 2026 (CHG-WIR-008): "Navigation & Menus" means site navigation menus; the F&B menu operations (listMenus, getMenu, createMenu, setMenuSections, updateMenu) were attached by name … Removed 2 October 2026 (CHG-WIR-008): "Navigation & Menus" means site navigation menus; the F&B menu operations (listMenus, getMenu, createMenu, setMenuSections, updateMenu) were attached by name …

**From the Food, Beverage & Retail process.** Where a venue decides what appears in its website header and footer and in the mobile app's tab bar, plus the Buy tickets button. From the food and retail side, Dining and Shop entries can exist only while those modules are enabled. The one thing to get right: every option visibly changes the preview, and an entry that would lead nowhere is refused before saving.

**Fixed on main** (the package already carries these; draw what it says): The screen is wired to F&B menus: listMenus, getMenu, createMenu, setMenuSections and updateMenu, with an "Outlet id" text box, an "Active … (CHG-WIR-008); The screen requires the fnb module. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is one navigation configuration held per surface (web header, web footer, mobile tabs), as DI-285 needs? The contract has one NavigationConfig with a kind.** → Three navigation editors (header, footer, tab bar), each saved on its own. The DNS/custom-domain and landing-page-template parts of this answer are separate decisions (see related). *(decided by Chinmay, 2026-10-02; DEC-049 / CHG-NOTE-004 / CHG-SGU-006)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | text field | — | — | `getTenantConfig` ?version |

**Form: Save tab bar** (modal, opened by *Save tab bar*; *Save tab bar* calls `setNavigation`, *Cancel* sends nothing)

**Collects what `setNavigation` sends.** Required: `kind`, `items` (label, icon, target, visible, order; a mobile tab targets an `appSection`). Optional: `buyButton` (`style`, `label`). Refused `400` when a tab targets a disabled module or more than five are visible. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | segmented control | required | — | Bottom navigation · Drawer · Tabs | — | — | `setNavigation` body |
| Items `items` | repeatable rows | required | — | at most 12 | — | — | `setNavigation` body |
| Label `items[].label` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `setNavigation` body |
| Icon `items[].icon` | text field | optional | — | — | — | — | `setNavigation` body |
| Target `items[].target` | group | required | — | — | — | — | `setNavigation` body |
| Kind `items[].target.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `setNavigation` body |
| Module key `items[].target.moduleKey` | field | optional | — | — | — | — | `setNavigation` body |
| App section `items[].target.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `setNavigation` body |
| Content page `items[].target.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `setNavigation` body |
| Product `items[].target.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setNavigation` body |
| Event `items[].target.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `setNavigation` body |
| URL `items[].target.url` | text field | optional | — | — | — | — | `setNavigation` body |
| Is visible `items[].isVisible` | toggle | required | — | At most five may be visible in bottom navigation; the rest overflow. | — | At most five may be visible in bottom navigation; the rest overflow. | `setNavigation` body |
| Sort order `items[].sortOrder` | number field | required | — | — | — | — | `setNavigation` body |
| Buy button `buyButton` | group | optional | — | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. | `setNavigation` body |
| Style `buyButton.style` | radio group | optional | Raised | Raised · Floating · Flat · Hidden | — | `raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off. | `setNavigation` body |
| Label `buyButton.label` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setNavigation` body |

Errors to draw in the form: 400 An item targets a disabled module, or more than five are marked visible

**Form: Save header** (modal, opened by *Save header*; *Save header* calls `setHeader`, *Cancel* sends nothing)

The header: logo placement, menu items and the Buy tickets button; saved on its own.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Layout `layout` | segmented control | required | — | Logo left · Logo centre · Logo with menu | — | — | `setHeader` body |
| Show logo `showLogo` | toggle | optional | on | — | — | — | `setHeader` body |
| Show menu `showMenu` | toggle | optional | on | — | — | — | `setHeader` body |
| Show notifications `showNotifications` | toggle | optional | on | — | — | — | `setHeader` body |
| Background colour `backgroundColour` | colour picker | optional | — | — | #RRGGBB | — | `setHeader` body |

**Form: Save footer** (modal, opened by *Save footer*; *Save footer* calls `setFooter`, *Cancel* sends nothing)

Footer columns, legal links, copyright text and social links; `id` and `scopePath` are the server's and never asked (the contract still lists them as required: CHG-SGU-024).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Columns `columns` | repeatable rows | optional | — | — | — | — | `setFooter` body |
| Heading `columns[].heading` | text field | optional | — | — | — | — | `setFooter` body |
| Links `columns[].links` | repeatable rows | optional | — | — | — | — | `setFooter` body |
| Label `columns[].links[].label` | text field | optional | — | — | — | — | `setFooter` body |
| URL `columns[].links[].url` | text field | optional | — | — | — | — | `setFooter` body |
| Opens cookie preferences `columns[].links[].opensCookiePreferences` | toggle | optional | off | — | — | — | `setFooter` body |
| Legal links `legalLinks` | group | optional | — | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. | `setFooter` body |
| Terms URL `legalLinks.termsUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Privacy URL `legalLinks.privacyUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Accessibility URL `legalLinks.accessibilityUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Cookie policy URL `legalLinks.cookiePolicyUrl` | text field | optional | — | — | — | — | `setFooter` body |
| Copyright text `copyrightText` | text field | optional | — | — | — | — | `setFooter` body |
| Social links `socialLinks` | repeatable rows | optional | — | — | — | — | `setFooter` body |
| Platform `socialLinks[].platform` | text field | optional | — | — | — | — | `setFooter` body |
| URL `socialLinks[].url` | text field | optional | — | — | — | — | `setFooter` body |

**Form: Build a link** (modal, opened by *Build a link*; *Build a link* calls `buildDeepLink`, *Cancel* sends nothing)

Pick the target (a product, an event, a booking step or a page); the link comes back to copy.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target `target` | group | required | — | — | — | — | `buildDeepLink` body |
| Kind `target.kind` | select | required | — | Module · Content page · Product · Event · External URL · App section · None | — | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | `buildDeepLink` body |
| Module key `target.moduleKey` | field | optional | — | — | — | — | `buildDeepLink` body |
| App section `target.appSection` | select | optional | — | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | `buildDeepLink` body |
| Content page `target.contentPageId` | picker: choose a content page | optional | — | — | shows names, sends the id | — | `buildDeepLink` body |
| Product `target.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `buildDeepLink` body |
| Event `target.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `buildDeepLink` body |
| URL `target.url` | text field | optional | — | — | — | — | `buildDeepLink` body |
| Utm `utm` | key and value settings | optional | — | — | — | Campaign tags appended to the link, e.g. `utm_source`. | `buildDeepLink` body |

Errors to draw in the form: 400 Validation failed

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Where (web header, web footer, mobile tab bar)**: Web and mobile are configured independently (a different mobile arrangement is normal). The tab bar is the bottom navigation; the web uses tabs or a drawer. *(source: DI-285 / DI-1087 / contracts/satellite/white-label.yaml#/components/schemas/NavigationConfig)*
- **Items (label, icon, links to, visible, order)**: The label in English and Arabic. Links to a module (Dining, Shop and so on), a content page, a product, an event, an outside link (the venue's own site), or an app section (Home, Explore, Plan, Tickets, Map, Account). Drag to reorder. At most 12 items, and at most 5 visible tabs, with the rest in "More". *(source: contracts/satellite/white-label.yaml#/components/schemas/LinkTarget / DI-397 / DI-424 / MATRIX 19.1.8 / MATRIX 19.1.12)*
- **Buy tickets button**: Raised in the centre (default), floating, flat or hidden, plus its label. It shows on every app screen except the booking and checkout steps. *(source: contracts/satellite/white-label.yaml#/components/schemas/NavigationConfig / DI-1081)*

#### Outputs: what the screen shows and produces

**Shown**

**Load the working header and footer** (card list, from `getTenantConfig`)

| Shows | Format | Notes |
|---|---|---|
| Brand | grouped details | Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB … |
| App icons | grouped details | — |
| Booking flow | grouped details | Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11). One tenant with several venues (the Kids Club branches … |
| Booking flows | list or chips (count when long) | Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12). |
| Theme | grouped details | — |
| Fonts | grouped details | — |
| Footer | grouped details | BL-002. `setHeader` and `HeaderConfig` exist and the footer does not, which looked like symmetry until you notice it is not: a header is … |
| Expected back at | 1 Oct 2026, 14:30 | — |

**Tab bar** (detail panel, from `getNavigation`): **The mobile tab editor (decided 29 September, MOB-1 and MOB-2).** Which tabs, their order, labels and icons; each tab is an `appSection` link. The default is Home, Explore, Plan and Tickets; Map is optional; Plan needs the `visitPlanner` module. The Buy tickets button: raised in the centre (default), floating, flat or hidden, and its label. At most five tabs are visible.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Bottom navigation, Drawer, Tabs | — |
| Items | list or chips (count when long) | — |
| Buy button | grouped details | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps … |

**Header** (detail panel, from `setHeader`): **Three navigation editors, each saved on its own** (decided by Chinmay, 2 October 2026; DEC-049): the header here, the footer below, the mobile tab bar above (CHG-SGU-006).

| Shows | Format | Notes |
|---|---|---|
| Layout | chip: Logo left, Logo centre, Logo with menu | — |
| Show logo | yes / no (icon or chip) | — |
| Show menu | yes / no (icon or chip) | — |
| Show notifications | yes / no (icon or chip) | — |
| Background colour | colour swatch | — |

**Footer** (detail panel, from `setFooter`): Footer columns, legal links, copyright and social; the legal links a regulator checks and the Powered by credit (DI-111).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Columns | list or chips (count when long) | — |
| Heading | text | — |
| Links | list or chips (count when long) | — |
| Label | text | — |
| URL | text | — |
| Opens cookie preferences | yes / no (icon or chip) | — |
| Legal links | grouped details | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy … |
| Terms URL | text | — |
| Privacy URL | text | — |
| Accessibility URL | text | — |
| Cookie policy URL | text | — |
| Copyright text | text | — |
| Social links | list or chips (count when long) | — |
| Platform | text | — |
| URL | text | — |

**Links into the storefront** (card list, from `getDeepLinkScheme`): **For a tenant with its own landing page** (DEC-548): the published deep-link scheme and a link builder, so the tenant's site links straight to a product, an event or a booking step (CHG-SGU-005).

| Shows | Format | Notes |
|---|---|---|
| Base URL | text | The primary domain, or the platform subdomain where none is primary. |
| Patterns | list or chips (count when long) | The patterns, fixed (4 October 2026, CHG-FXC-009). One per target kind, under `baseUrl`: `product` `/p/{productId}`, `event` … |
| Kind | text | A `LinkTarget.kind`, or `bookingFlow`. |
| Pattern | text | e.g. `/p/{productId}`, `/e/{eventId}`, `/book/{flowKey}`. |
| App links enabled | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save tab bar (secondary button) | `setNavigation` PUT `/tenant-config/navigation` | NavigationConfig | NavigationConfig | 400 An item targets a disabled module, or more than five are marked visible | opens modal first |
| Save header (secondary button) | `setHeader` PUT `/tenant-config/header` | HeaderConfig | HeaderConfig | — | opens modal first |
| Save footer (secondary button) | `setFooter` PUT `/footer` | FooterConfig | FooterConfig | — | opens modal first |
| Build a link (secondary button) | `buildDeepLink` POST `/deep-links` | inline | inline | 400 Validation failed | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Preview**: A live web header and phone tab-bar preview with the venue's theme, switchable to Arabic (mirrored). The default set before the venue saves is Home, Explore, Plan, Tickets plus the Buy tickets button. *(source: DI-988 / DI-975 / contracts/satellite/white-label.yaml#/components/schemas/NavigationConfig)*
- **Module-gated entries**: An entry linking to a module that is not enabled (Dining needs Dining & F&B, Shop needs Shop, Plan needs the visit planner, Map needs Map) is listed greyed with "Turn on Dining & F&B first" and a link to module settings. *(source: contracts/satellite/white-label.yaml#setNavigation / contracts/satellite/white-label.yaml#/components/schemas/ModuleKey / DI-193)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save navigation**: Saved for the next publish. Refused with the reason named when a tab targets a disabled module or more than 5 are visible; fix-ups are highlighted on the item. *(source: contracts/satellite/white-label.yaml#setNavigation)*

**Data it reads**: `getNavigation` (onLoad, The navigation and the mobile tab set (MOB-1)); `getDeepLinkScheme` (onLoad, The published deep-link scheme (DEC-548)); `getTenantConfig` (onLoad, Load the working header and footer)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The navigation menus list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the navigation menus untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing configured yet: the header, footer and tab bar open with the preset's defaults, each with its own Save. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getNavigation` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An item targets a disabled module, or more than five are marked visible; 400 Validation failed |

#### Edge cases to draw

- **Someone tries to switch off Dining while a tab still links to it**: Module settings refuse it and list the entries that still point at Dining (shown here as "Used by Dining tab"). *(source: contracts/satellite/white-label.yaml#/components/schemas/ModuleEnablement)*
- **Header link to a non-booking page**: It goes to the venue's own website as an outside link. *(source: DI-397)*

#### Consistency with other screens

- Match `CMS-016`: Module enablement; the greyed entries link there.
- Match `GST-001`: The tab bar it renders.
- Match `WEB-001`: The header it renders.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mobileTabs:
- Home
- Explore
- Buy tickets (raised)
- Plan
- Tickets
webHeader:
- Tickets
- Dining
- Shop
- Plan your visit
- 'About us (outside link: aquapark.example/about)'
arabicLabels:
  Dining: المطاعم
  Shop: المتجر
  Tickets: التذاكر
```

#### Permissions

- `getNavigation` → `TENANT_CONFIGURE` (configure) · staff
- `setNavigation` → `TENANT_CONFIGURE` (configure) · staff
- `setHeader` → `TENANT_CONFIGURE` (configure) · staff
- `setFooter` → `TENANT_CONFIGURE` (configure) · staff
- `getDeepLinkScheme` → `TENANT_CONFIGURE` (configure) · staff
- `buildDeepLink` → `TENANT_CONFIGURE` (configure) · staff
- `getTenantConfig` → `TENANT_CONFIGURE` (configure) · staff, guest

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getNavigation` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.8 | Menu Configuration - System shall support configurable navigation menus. | Guest Mobile App & Branding | CONTRACTED | `setNavigation` |
| 19.1.12 | Navigation Label Management - System shall support configurable navigation labels. | Guest Mobile App & Branding | CONTRACTED | `setNavigation` |
| 19.1.6 | Header Configuration - System shall support configurable headers. | Guest Mobile App & Branding | CONTRACTED | `setHeader` |
| 19.1.19 | Tenant-Specific Branding - System shall support tenant-specific branding. | Guest Mobile App & Branding | CONTRACTED | `getTenantConfig` |
| 22.10.1 | Multi-Site CMS | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 22.10.3 | Multi-Brand Management | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 19.1.7 | Footer Configuration - System shall support configurable footers. | Guest Mobile App & Branding | CONTRACTED | data `FooterConfig` |
| 19.1.21 | Tenant-Specific Notifications - System shall support tenant-specific notifications. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |
| 19.1.23 | Tenant-Specific Payment Methods - System shall support tenant-specific payment methods. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Header layout (`header.layout`) | Logo left · Logo centre · Logo with menu | — | every guest screen (web, app and kiosk) | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | — | on | every guest screen (web, app and kiosk) | — |
| Show menu (`header.showMenu`) | — | on | every guest screen (web, app and kiosk) | — |
| Show notifications (`header.showNotifications`) | — | on | every guest screen (web, app and kiosk) | — |
| Background colour (`header.backgroundColour`) | #RRGGBB | — | every guest screen (web, app and kiosk) | — |
| Navigation kind (`navigation.kind`) | Bottom navigation · Drawer · Tabs | — | every guest screen (web, app and kiosk) | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | at most 12 | — | every guest screen (web, app and kiosk) | — |
| Items: label (`navigation.items[].label`) | English and Arabic (Arabic right to left) | — | every guest screen (web, app and kiosk) | — |
| Items: icon (`navigation.items[].icon`) | — | — | every guest screen (web, app and kiosk) | — |
| Items: target (`navigation.items[].target`) | — | — | every guest screen (web, app and kiosk) | — |
| Target: kind (`navigation.items[].target.kind`) | Module · Content page · Product · Event · External URL · App section · None | — | every guest screen (web, app and kiosk) | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. |
| Target: module key (`navigation.items[].target.moduleKey`) | — | — | every guest screen (web, app and kiosk) | — |
| Target: app section (`navigation.items[].target.appSection`) | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | every guest screen (web, app and kiosk) | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. |
| Target: content page (`navigation.items[].target.contentPageId`) | shows names, sends the id | — | every guest screen (web, app and kiosk) | — |
| Target: product (`navigation.items[].target.productId`) | shows names, sends the id | — | every guest screen (web, app and kiosk) | — |
| Target: event (`navigation.items[].target.eventId`) | shows names, sends the id | — | every guest screen (web, app and kiosk) | — |
| Target: uRL (`navigation.items[].target.url`) | — | — | every guest screen (web, app and kiosk) | — |
| Items: is visible (`navigation.items[].isVisible`) | At most five may be visible in bottom navigation; the rest overflow. | — | every guest screen (web, app and kiosk) | At most five may be visible in bottom navigation; the rest overflow. |
| Items: sort order (`navigation.items[].sortOrder`) | — | — | every guest screen (web, app and kiosk) | — |
| Buy button (`navigation.buyButton`) | — | — | GST-003 | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Buy button: style (`navigation.buyButton.style`) | Raised · Floating · Flat · Hidden | Raised | every P02 screen | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |
| Buy button: label (`navigation.buyButton.label`) | English and Arabic (Arabic right to left) | — | every guest screen (web, app and kiosk) | — |
| Footer columns (`footer.columns`) | — | — | every website screen | — |
| Columns: heading (`footer.columns[].heading`) | — | — | every website screen | — |
| Columns: links (`footer.columns[].links`) | — | — | every website screen | — |
| Links: label (`footer.columns[].links[].label`) | — | — | every website screen | — |
| Links: uRL (`footer.columns[].links[].url`) | — | — | every website screen | — |
| Links: opens cookie preferences (`footer.columns[].links[].opensCookiePreferences`) | — | off | every website screen | — |
| Legal links (`footer.legalLinks`) | — | — | every website screen | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Legal links: terms URL (`footer.legalLinks.termsUrl`) | — | — | every website screen | — |
| Legal links: privacy URL (`footer.legalLinks.privacyUrl`) | — | — | every website screen | — |
| Legal links: accessibility URL (`footer.legalLinks.accessibilityUrl`) | — | — | every website screen | — |
| Legal links: cookie policy URL (`footer.legalLinks.cookiePolicyUrl`) | — | — | every website screen | — |
| Copyright text (`footer.copyrightText`) | — | — | every website screen | — |
| Social links (`footer.socialLinks`) | — | — | every website screen | — |
| Social links: platform (`footer.socialLinks[].platform`) | — | — | GST-018, GST-066, WEB-018 | — |
| Social links: uRL (`footer.socialLinks[].url`) | — | — | every website screen | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-009` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (46), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-009?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save tab bar, Save header, Save footer, Build a link.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-010` Media Library

**Hold the imagery, and know where it is used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-CMS-010 |
| Who uses it | venue staff holding `AI_USE`, `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 operate, 1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `searchMedia` reads the population and `getMediaEntitlements` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `mediaId` (deepLink), `uploadId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/white-label/media-library` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Archive and quarantine are reversible; deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA).** An archived asset offers **Restore** (`updateMediaAsset` with `status: ready`); a quarantined one offers **Release**, which is the same call after a reviewer has cleared the scan flag (the state model marks that move as needing approval). **Delete media asset** (`deleteMediaAsset`) removes the asset for good and is refused while it is referenced.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): getMediaEntitlements and appendEntitlementToMedia (orders) operate on ticket media, a wristband or card carrying entitlements, not on digital assets; the word … Removed 2 October 2026 (CHG-WIR-021): getMediaEntitlements and appendEntitlementToMedia (orders) operate on ticket media, a wristband or card carrying entitlements, not on digital assets; the word …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The tenant's library of images, video and documents used by the guest apps and websites: upload, describe (title, alt text in Arabic and English, tags, collections), record usage rights and their expiry, and see where each asset is used before replacing or deleting it. The rule: deleting is the only end of an asset's life and is refused or warned while it is in use.

**Fixed on main** (the package already carries these; draw what it says): getMediaEntitlements and appendEntitlementToMedia (orders) are on the media library, and emptyNoAccess names ORDER_VIEW. (CHG-WIR-021); requiresModule is 'ticketing'. (CHG-SGU-019); Filters are free-text fields for kind, tag, collection id and venue id. (CHG-SGU-019); formAppendEntitlementToMedia asks the person for id. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every media asset' drop id, customMetadata; 'Every collection' drop id, venueId … (CHG-SGU-019).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | select | optional | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | — | The media kinds (image, video, document, audio) as a choice; sends `kind`. | `MediaAsset.kind` |
| Tag | list of values (chips) | optional | — | — | — | Tags picked from the taxonomy; sends `tag`. | `MediaAsset.tags` |
| Collection | text field | optional | — | A name already used by any collection in the tenant, at any venue or level, is refused with `409 duplicate-code`. | — | Collections by name; sends `collectionId`. | `Collection.name` |
| Venue | picker: choose a venue | optional | — | — | shows names, sends the id | Venues by name; sends `venueId`. | `MediaAsset.venueId` |
| Search | text field | optional | — | — | — | Sends `?search=` to `searchMedia`. | `searchMedia` ?search |
| Unused only | toggle | optional | off | — | — | Sends `?unusedOnly=` to `searchMedia`. | `searchMedia` ?unusedOnly |
| Rights expiring within days | number field (days) | optional | — | — | — | Sends `?rightsExpiringWithinDays=` to `searchMedia`. | `searchMedia` ?rightsExpiringWithinDays |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | `searchMedia` ?kind |
| Tag | text field | — | — | `searchMedia` ?tag |
| Collection | picker: choose a collection | — | — | `searchMedia` ?collectionId |
| Within days | number field (days) | 60 | — | `getExpiringRights` ?withinDays |

**Form: Restore media asset** (confirmDialog, opened by *Restore media asset*; *Restore* calls `updateMediaAsset`, *Cancel* sends nothing)

**Returns an archived asset to `ready`**, so it can be used again (decided 28 September, audit STATE-MEDIA). Names the asset.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

**Form: Release from quarantine** (confirmDialog, opened by *Release from quarantine*; *Release* calls `updateMediaAsset`, *Cancel* sends nothing)

**Releases a quarantined asset to `ready` after review** (decided 28 September, audit STATE-MEDIA). Names the asset and the scan finding, and records the reviewer; the state model marks this reversal as needing approval.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

**Form: Complete upload** (modal, opened by *Complete upload*; *Complete upload* calls `completeUpload`, *Cancel* sends nothing)

**Collects what `completeUpload` sends before it is called.** Nothing in the body is required. Optional: `title`, `altText`, `tags`, `collectionIds`, `rights`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `completeUpload` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `completeUpload` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | — | `completeUpload` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `completeUpload` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `completeUpload` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `completeUpload` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `completeUpload` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `completeUpload` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `completeUpload` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `completeUpload` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `completeUpload` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `completeUpload` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `completeUpload` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `completeUpload` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `completeUpload` body |

Errors to draw in the form: 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem)

**Form: Create collection** (modal, opened by *Create collection*; *Create collection* calls `createCollection`, *Cancel* sends nothing)

**Collects what `createCollection` sends before it is called.** Required: `name`. Optional: `description`, `venueId`, `parentCollectionId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createCollection` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createCollection` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCollection` body |
| Parent collection `parentCollectionId` | picker: choose a parent collection | optional | — | — | shows names, sends the id | — | `createCollection` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Create upload** (modal, opened by *Create upload*; *Create upload* calls `createUpload`, *Cancel* sends nothing)

**Collects what `createUpload` sends before it is called.** Required: `filename`, `contentType`, `sizeBytes`. Optional: `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Filename `filename` | text area | required | — | max length 256 | — | — | `createUpload` body |
| Content type `contentType` | text field | required | — | — | — | — | `createUpload` body |
| Size bytes `sizeBytes` | number field | required | — | min 1 | — | — | `createUpload` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createUpload` body |

Errors to draw in the form: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.

**Form: Replace media asset** (modal, opened by *Replace media asset*; *Replace media asset* calls `replaceMediaAsset`, *Cancel* sends nothing)

**Collects what `replaceMediaAsset` sends before it is called.** Required: `uploadId`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Upload `uploadId` | picker: choose an upload | required | — | — | shows names, sends the id | — | `replaceMediaAsset` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `replaceMediaAsset` body |

Errors to draw in the form: 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem)

**Form: Save media asset** (modal, opened by *Save media asset*; *Save media asset* calls `updateMediaAsset`, *Cancel* sends nothing)

**Collects what `updateMediaAsset` sends before it is called.** Nothing in the body is required. Optional: `title`, `description`, `altText`, `tags`, `collectionIds`, `rights`, `status`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Upload**: Brand assets PNG or SVG up to 2 MB; library images and video within the size and pixel limits shown before the upload (e.g. banner image at most 1024 px wide), validated on upload with the reason stated. The signed upload is requested, the file sent, then completed with title, alt text, tags, collections and rights. *(source: R270; DI-188; contracts/satellite/assets.yaml#createUpload; contracts/satellite/assets.yaml#completeUpload)*
- **Alt text**: Required for images used on guest surfaces, in each of the tenant's languages. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Every media asset** (data table, from `searchMedia`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 … |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |

**Every collection** (data table, from `listCollections`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | Unique per tenant (decided 28 September, audit R108). A name already used by any collection in the tenant, at any venue or level, is … |
| Description | text | — |
| Asset count | 1,234 | — |

**The selected media asset** (detail panel, from `searchMedia`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 … |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Duration seconds | 1,234.5 | — |

**The expiring media** (detail panel, from `getExpiringRights`)

| Shows | Format | Notes |
|---|---|---|
| Filename | text | — |
| Thumbnail URL | text | — |
| Licensor | text | — |
| Valid to | 1 Oct 2026 | — |
| Days remaining | 1,234 | — |
| Is expired | yes / no (icon or chip) | — |
| Is in use | yes / no (icon or chip) | True while `liveUsageCount` is above zero, that is, while live (published) content references the asset (audit R106 (10)). |
| Live usage count | 1,234 | References from live (published) content only (audit R106 (10)). Expired and live is the combination that matters. |

**The media asset** (detail panel, from `getMediaAsset`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 … |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Duration seconds | 1,234.5 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Complete upload (secondary button) | `completeUpload` POST `/media/uploads/{uploadId}/complete` | inline | MediaAsset | 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) | opens modal first |
| Create collection (secondary button) | `createCollection` POST `/media/collections` | inline | Collection | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Create upload (secondary button) | `createUpload` POST `/media/uploads` | inline | UploadTicket | 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes. | opens modal first |
| Delete media asset (destructive button) | `deleteMediaAsset` DELETE `/media/{mediaId}` | — | — | 409 Asset is in use. (MediaInUseProblem) | — |
| Replace media asset (secondary button) | `replaceMediaAsset` POST `/media/{mediaId}/replace` | inline | MediaReplaceResult | 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem) | opens modal first |
| Save media asset (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Restore media asset (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Release from quarantine (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Asset grid**: Thumbnail, title, kind, size, dimensions, status chip (ready, processing, quarantined, archived), usage count and rights expiry; unused and expiring filters. *(source: contracts/satellite/assets.yaml#searchMedia; contracts/satellite/assets.yaml#getExpiringRights)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Restore / Release from quarantine**: Restore returns an archived asset to ready; Release is for a reviewer after the scan finding is cleared and records the reviewer. *(source: contracts/satellite/assets.yaml#updateMediaAsset)*
- **Replace**: New file behind the same asset; every usage updates. The confirmation lists where it is used. *(source: contracts/satellite/assets.yaml#replaceMediaAsset)*
- **Delete**: Cannot be undone; the confirmation names live usages and refuses or warns while it is used. *(source: contracts/satellite/assets.yaml#deleteMediaAsset)*

**Data it reads**: `searchMedia` (onLoad, Search the asset library); `getExpiringRights` (onLoad, Assets whose licence is expiring or expired); `listCollections` (onLoad, List collections)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*; carries `uploadId`
- → `CMS-003` Typography: *Typography*

**What opens over it**

- confirmDialog *Delete media asset*: **Names what `deleteMediaAsset` changes and what it leaves alone**, in the consequence rather than the verb. A media this affects should be identified in the dialog, not just counted. **Deletion is the only end of an asset's life and cannot be undone** (decided 28 September, audit STATE-MEDIA); the …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The media list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the media untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No media yet. Offers Create collection (`createCollection`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on kind, tag, collectionId, venueId, search, unusedOnly and the media are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ASSET_LIBRARY_VIEW`, which `searchMedia` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `semanticSearch`; `ASSET_LIBRARY_MANAGE` for `completeUpload`, `createCollection`, `createUpload`, `deleteMediaAsset` and 2 more. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 Asset is in use. (MediaInUseProblem); 409 Status change refused: archiving an asset … |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds ASSET_LIBRARY_VIEW, ORDER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: ORDER_CREATE for Append entitlement to media; ASSET_LIBRARY_MANAGE for Complete upload, Create collection, Create upload; AI_USE for semanticSearch. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/orders.yaml#appendEntitlementToMedia)*
- **appendEntitlementToMedia answers 409**: Show it as something the person can act on, not a failure: Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media (`entitlementCannotShareMedia`) — a single-entry ticket surrendered at the gate is not a claim token for anything bought afterwards. Also refused where the media was issued for another... *(source: contracts/spine/orders.yaml#appendEntitlementToMedia)*
- **completeUpload answers 409**: Show it as something the person can act on, not a failure: The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed (`sizeExceeded`). A file that fails scanning is not refused here — see above *(source: contracts/satellite/assets.yaml#completeUpload)*
- **deleteMediaAsset answers 409**: Show it as something the person can act on, not a failure: Asset is in use. Every reference is listed *(source: contracts/satellite/assets.yaml#deleteMediaAsset)*
- **replaceMediaAsset answers 409**: Show it as something the person can act on, not a failure: The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed (`sizeExceeded`) *(source: contracts/satellite/assets.yaml#replaceMediaAsset)*

#### Consistency with other screens

- Match `CMS-061`: The DAM board's command centre counts the same library.
- Match `CMS-002`: Brand assets picked there come from this library.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
assets:
- title: Lazy river at sunset
  kind: image
  size: 1.2 MB
  dimensions: 1920 × 1080
  status: ready
  usedIn: 4
  rightsExpire: 31/12/2026
- title: Wave pool promo (Arabic)
  kind: video
  size: 48 MB
  status: processing
  usedIn: 0
- title: Logo AquaCove horizontal
  kind: image
  size: 86 KB
  status: ready
  usedIn: 12
```

#### Permissions

- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `createCollection` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `deleteMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `getExpiringRights` → `ASSET_LIBRARY_VIEW` (read) · staff
- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff
- `listCollections` → `ASSET_LIBRARY_VIEW` (read) · staff
- `replaceMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `updateMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `semanticSearch` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ASSET_LIBRARY_VIEW`, which `searchMedia` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `AI_USE` for `semanticSearch`; `ASSET_LIBRARY_MANAGE` for `completeUpload`, `createCollection`, `createUpload`, `deleteMediaAsset` and 2 more.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.9 | Campaign Asset Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 22.10.25 | Media Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 23.1.1 | System shall provide a centralized repository for storing and managing digital assets including images, videos, documents, PDFs, marketing materials, brand assets, audio files, templates, and … | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.5 | System shall support searching assets using keywords, metadata, tags, categories, and filters. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.15 | System shall expose DAM functionality through APIs and support integration with CMS, CRM, marketing platforms, mobile applications, and third-party systems. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.2 | System shall support configurable asset categories, folders, collections, tags, and classifications. | Digital Asset Management | CONTRACTED | `createCollection` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |
| 23.1.11 | System shall track asset ownership, copyright information, licensing terms, and expiration dates. | Digital Asset Management | CONTRACTED | `getExpiringRights` |
| 23.1.12 | System shall track where assets are used across websites, mobile applications, campaigns, kiosks, emails, and digital channels. | Digital Asset Management | CONTRACTED | `getMediaAsset` |
| 23.1.8 | System shall maintain historical versions of assets and allow comparison, rollback, and restoration. | Digital Asset Management | CONTRACTED | `replaceMediaAsset` |
| 8.4.39 | System shall support semantic search across products, tickets, memberships, documents, knowledge bases, support content, assets, and operational data using vector-based retrieval and relevance … | Unified Operations Dashboard | CONTRACTED | `semanticSearch` |
| 23.1.6 | AI shall support semantic search allowing users to locate assets using natural language queries. | Digital Asset Management | CONTRACTED | `semanticSearch` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-010` · status **notStarted** · provenance generated
- ADR-0069 *In-park 3D navigation is built natively, from a venue model, a pathway file and GPS* (`docs/adr/0069-in-park-3d-navigation-is-built-natively.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (91), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Complete upload, Create collection, Create upload, Delete media asset, Replace media asset, Save media asset, Restore media asset, Release from quarantine.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `AI_USE`, `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 6 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P13 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P13 as a whole** (5: 0 open, 5 closed). Open first; a closed row says where it went on 30 September.

- **A47** Advise Qossai/Allam on the Apple/Google Developer account ownership model and a simplified, low-effort app-publishing workflow for white-labelled tenant apps (incl. how to reflect "Powered by TICVAI" branding) *(Pradnya Yeram · Low · Done → 30 Sep: Closed, Done (as recorded earlier) · 24 Sep 2026 · workshop tracker)*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker)*
- **A338** Build the real white-label CMS builder (client builds a site in ~30 min) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Sep 2026 · workshop tracker)*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker)*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker)*

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

### Across P13 Venue CMS

- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P13 · White Label

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Qossai (rated the CMS prototype ~70%): a client should be able to build a working site "within 30 minutes", easily adding header, footer, fonts and its own images/graphics self-service; Allam: every CMS option must visibly change something and the interface must be intuitive to navigate. *(client request · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-988)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- Base structure (header, footer, layout) is fixed across tenants; logo, colour, font and module visibility (e.g. hide Dining or Retail) are configurable per tenant, and independently for web and mobile (e.g. a different mobile header). *(agreed · MoM 14 Aug 2026, 4. White-Labeling and Customization Boundaries · DI-285)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Modules enabled/disabled per tenant by licence: Ticketing & Booking, Membership, Events, Attractions, Virtual Queue, F&B, Retail, Parking; add-ons (Lost & Found, AI Concierge Chat, multi-language, integrations) toggle the same way and appear automatically as new integrations are built. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-193)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*

**36 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"buildDeepLink": {"method":"POST","path":"/deep-links","contract":"white-label","summary":"Build a deep link to a target","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":null},
"completeUpload": {"method":"POST","path":"/media/uploads/{uploadId}/complete","contract":"assets","summary":"Confirm an upload and create the asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"createBanner": {"method":"POST","path":"/tenant-config/banners","contract":"white-label","summary":"Create a banner","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Banner","responds":"Banner"},
"createCollection": {"method":"POST","path":"/media/collections","contract":"assets","summary":"Create a collection","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Collection"},
"createContentBlock": {"method":"POST","path":"/content-blocks","contract":"white-label","summary":"Author a block of content","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ContentBlock","responds":"ContentBlock"},
"createContentPage": {"method":"POST","path":"/tenant-config/pages","contract":"white-label","summary":"Create a content page","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ContentPage","responds":"ContentPage"},
"createPreview": {"method":"POST","path":"/tenant-config/preview","contract":"white-label","summary":"Generate a preview link","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Preview"},
"createPromoBlock": {"method":"POST","path":"/tenant-config/promo-blocks","contract":"white-label","summary":"Create a promotional block","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PromoBlock","responds":"PromoBlock"},
"createUpload": {"method":"POST","path":"/media/uploads","contract":"assets","summary":"Request a signed upload URL","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UploadTicket"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"deleteBanner": {"method":"DELETE","path":"/tenant-config/banners/{bannerId}","contract":"white-label","summary":"Delete a banner","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteContentPage": {"method":"DELETE","path":"/tenant-config/pages/{pageId}","contract":"white-label","summary":"Delete a content page","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteMediaAsset": {"method":"DELETE","path":"/media/{mediaId}","contract":"assets","summary":"Delete an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deletePromoBlock": {"method":"DELETE","path":"/tenant-config/promo-blocks/{promoBlockId}","contract":"white-label","summary":"Delete a promotional block","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getAppIcons": {"method":"GET","path":"/tenant-config/app-icons","contract":"white-label","summary":"Read app icon set","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AppIcons"},
"getBookingFlowConfig": {"method":"GET","path":"/tenant-config/booking-flow","contract":"white-label","summary":"How the guest booking flow looks and steps","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"effectiveForVenueId","in":"query","required":false}],"requestBody":null,"responds":"BookingFlowConfig"},
"getBrandIdentity": {"method":"GET","path":"/tenant-config/brand","contract":"white-label","summary":"Read brand identity","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"BrandIdentity"},
"getDeepLinkScheme": {"method":"GET","path":"/deep-links","contract":"white-label","summary":"The published deep-link scheme","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"DeepLinkScheme"},
"getExpiringRights": {"method":"GET","path":"/media/rights-expiring","contract":"assets","summary":"Assets whose licence is expiring or expired","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"withinDays","in":"query","required":null}],"requestBody":null,"responds":"ExpiringMedia"},
"getFeatureToggles": {"method":"GET","path":"/tenant-config/features","contract":"white-label","summary":"Read tenant feature toggles","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"FeatureToggle"},
"getFonts": {"method":"GET","path":"/tenant-config/fonts","contract":"white-label","summary":"Read font configuration","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"FontConfig"},
"getHomepageLayout": {"method":"GET","path":"/tenant-config/homepage","contract":"white-label","summary":"Read homepage layout","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"HomepageLayout"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getModuleEnablement": {"method":"GET","path":"/tenant-config/modules","contract":"white-label","summary":"Read module enablement","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ModuleEnablement"},
"getNavigation": {"method":"GET","path":"/tenant-config/navigation","contract":"white-label","summary":"Read navigation","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"NavigationConfig"},
"getSiteSetupProgress": {"method":"GET","path":"/tenant-config/site-setup","contract":"white-label","summary":"Where the tenant is in the Site Builder","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SiteSetupProgress"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getTenantConfig": {"method":"GET","path":"/tenant-config","contract":"white-label","summary":"Full working configuration","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"TenantConfig"},
"getTheme": {"method":"GET","path":"/tenant-config/theme","contract":"white-label","summary":"Read colour theme","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Theme"},
"listBanners": {"method":"GET","path":"/tenant-config/banners","contract":"white-label","summary":"List banners","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"state","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCollections": {"method":"GET","path":"/media/collections","contract":"assets","summary":"List collections","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Collection"},
"listContentBlocks": {"method":"GET","path":"/content-blocks","contract":"white-label","summary":"The content blocks of a page","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"pageKey","in":"query","required":true},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listContentPages": {"method":"GET","path":"/tenant-config/pages","contract":"white-label","summary":"List custom content pages","permission":"TENANT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"categoryCode","in":"query","required":null},{"name":"slug","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLandingPageTemplates": {"method":"GET","path":"/landing-page-templates","contract":"white-label","summary":"The landing-page templates TICVAI provides","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromoBlocks": {"method":"GET","path":"/tenant-config/promo-blocks","contract":"white-label","summary":"List promotional blocks","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"PromoBlock"},
"previewProductTickets": {"method":"GET","path":"/products/{productId}/ticket-previews","contract":"orders","summary":"Preview a product's PDF ticket and wallet passes","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locale","in":"query","required":null}],"requestBody":null,"responds":"TicketProof"},
"proposeMarketingContent": {"method":"POST","path":"/ai/content-drafts","contract":"ai","summary":"Draft marketing content for a person to edit and apply","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishContentBlock": {"method":"POST","path":"/content-blocks/{blockId}/publish","contract":"white-label","summary":"Publish now, or schedule it","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ContentBlock"},
"replaceMediaAsset": {"method":"POST","path":"/media/{mediaId}/replace","contract":"assets","summary":"Replace the file behind an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplaceResult"},
"searchMedia": {"method":"GET","path":"/media","contract":"assets","summary":"Search the asset library","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"tag","in":"query","required":null},{"name":"collectionId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":"unusedOnly","in":"query","required":null},{"name":"rightsExpiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"semanticSearch": {"method":"POST","path":"/search","contract":"ai","summary":"Search meaning, not words","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SearchResult"},
"setAppIcons": {"method":"PUT","path":"/tenant-config/app-icons","contract":"white-label","summary":"Set app icons","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AppIcons"},
"setBrandIdentity": {"method":"PUT","path":"/tenant-config/brand","contract":"white-label","summary":"Set logo, favicon and splash","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BrandIdentity","responds":"BrandIdentity"},
"setFeatureToggles": {"method":"PUT","path":"/tenant-config/features","contract":"white-label","summary":"Set feature toggles","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FeatureToggle"},
"setFonts": {"method":"PUT","path":"/tenant-config/fonts","contract":"white-label","summary":"Set fonts","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"FontConfig","responds":"FontConfig"},
"setFooter": {"method":"PUT","path":"/footer","contract":"white-label","summary":"Footer columns, legal links and social","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FooterConfig","responds":"FooterConfig"},
"setHeader": {"method":"PUT","path":"/tenant-config/header","contract":"white-label","summary":"Configure the header","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"HeaderConfig","responds":"HeaderConfig"},
"setHomepageLayout": {"method":"PUT","path":"/tenant-config/homepage","contract":"white-label","summary":"Set homepage section order","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"HomepageLayout","responds":"HomepageLayout"},
"setMaintenanceMode": {"method":"PUT","path":"/tenant-config/status","contract":"white-label","summary":"Enable or clear maintenance mode, and set the live app status","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TenantAppStatus"},
"setModuleEnablement": {"method":"PUT","path":"/tenant-config/modules","contract":"white-label","summary":"Enable or disable modules","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ModuleEnablement"},
"setNavigation": {"method":"PUT","path":"/tenant-config/navigation","contract":"white-label","summary":"Set main and overflow navigation","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"NavigationConfig","responds":"NavigationConfig"},
"setTheme": {"method":"PUT","path":"/tenant-config/theme","contract":"white-label","summary":"Set colour theme","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"Theme","responds":"Theme"},
"updateBanner": {"method":"PATCH","path":"/tenant-config/banners/{bannerId}","contract":"white-label","summary":"Amend or activate a banner","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Banner"},
"updateContentBlock": {"method":"PATCH","path":"/content-blocks/{blockId}","contract":"white-label","summary":"Change a draft content block","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"blockId","in":"path","required":true}],"requestBody":null,"responds":"ContentBlock"},
"updateContentPage": {"method":"PUT","path":"/tenant-config/pages/{pageId}","contract":"white-label","summary":"Amend a content page","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpdateContentPageRequest","responds":"ContentPage"},
"updateMediaAsset": {"method":"PATCH","path":"/media/{mediaId}","contract":"assets","summary":"Amend metadata, tags or rights","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"updatePromoBlock": {"method":"PATCH","path":"/tenant-config/promo-blocks/{promoBlockId}","contract":"white-label","summary":"Amend a promotional block","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PromoBlock"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibilitySettings": {"type":"object","description":"BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n","properties":{"largeTextAvailable":{"type":"boolean","default":true},"highContrastAvailable":{"type":"boolean","default":true},"simplifiedNavigationAvailable":{"type":"boolean","default":true},"screenReaderSupported":{"type":"boolean","default":true},"reachableHeightModeAvailable":{"type":"boolean","default":false,"description":"**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"},"sessionTimeoutMultiplier":{"type":"number","default":1,"description":"**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"}}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppIcons": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["sourceAssetRef","changeScope"],"properties":{"sourceAssetRef":{"type":"string","format":"uuid","description":"The `MediaAsset` id of the 1024×1024 source."},"derived":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).","items":{"type":"object","properties":{"platform":{"type":"string","enum":["ios","android","web"]},"size":{"type":"string"},"assetRef":{"type":"string","format":"uuid"}}}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` — icons are baked into the binary."},"liveVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Icon currently shipped. Differs from the draft until the next release."},"requiresRebuild":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True while the draft's source differs from the icon in `liveVersion`."}}},
"Banner": {"x-ticvai-persistence":"whitelabel.banner","type":"object","required":["id","title","imageAssetRef","startsAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"$ref":"#/components/schemas/LocalisedText"},"subtitle":{"$ref":"#/components/schemas/LocalisedText"},"imageAssetRef":{"type":"string","format":"uuid"},"placement":{"type":"string","enum":["homepageHero","homepageBlock","explore","checkout"]},"linkTarget":{"$ref":"#/components/schemas/LinkTarget"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","nullable":true,"description":"Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end."},"state":{"allOf":[{"$ref":"#/components/schemas/ScheduleState"}],"readOnly":true,"x-ticvai-derived":"sweeper","description":"Moved by `updateBanner` between `draft` and `scheduled`, and by the schedule timer from `scheduled` to `active` and `active` to `expired` at `startsAt` and `endsAt`, in the tenant's timezone (`states/schedule.yaml`)."},"sortOrder":{"type":"integer"},"isActive":{"type":"boolean"}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","description":"**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n","allOf":[{"$ref":"#/components/schemas/BookingFlowSettings"},{"type":"object","properties":{"venueOverrides":{"type":"array","maxItems":200,"default":[],"description":"Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.","items":{"$ref":"#/components/schemas/BookingFlowVenueOverride"}}}}]},
"BookingFlowSettings": {"type":"object","x-ticvai-persistence":"none — embedded in tenant_config","description":"**Every guest booking-flow setting, once.** `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue (decided 29 September, rev 3 CFG-11). The Rev 3 settings (`timesPerPage` onwards) are the options the client's rev 3 prototype shows under Config → Booking rules and Build your experience.\n**Venue-wide only (decided 29 September, W12).** The settings that belong to one flow moved to `BookingFlowLevelSettings` on each `BookingFlow`; `categoryDisplay` was removed (W7).\n","properties":{"preset":{"type":"string","enum":["auto","ticketBox","playCentre","venueSite","marketplace","singleEvent","season","custom"],"default":"auto","description":"L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. The UI preset of the prototype's drawer (rev 3 CFG-1, no change)."},"stepIndicator":{"type":"string","enum":["bar","numbered","dots","segmented","breadcrumb","pills","ticks","none"],"default":"bar"},"cartLayout":{"type":"string","enum":["sidebarRight","sidebarLeft","slideInRight","slideUpBottom","singleColumn","floatingIcon"],"default":"sidebarRight","description":"`floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). Which side a sidebar or the icon sits on in a right-to-left language is `cartSideInRtl`."},"cartSideInRtl":{"type":"string","enum":["keepRight","mirror"],"default":"keepRight","description":"**The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10).** `keepRight` keeps the cart (and the floating icon) on the right, as the client confirmed; `mirror` flips it to the left with the rest of the layout.\n"},"cardLayout":{"type":"string","enum":["stackedRows","splitRows","cardsAcross","posterCards"],"default":"stackedRows","description":"How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards."},"cardSize":{"type":"string","enum":["compact","standard","large","extraLarge"],"default":"compact","description":"Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). `standard` replaces `regular`."},"seatPicker":{"type":"string","enum":["bowl","zonesThenSeats","zonesOnly","seatsOnly"],"default":"bowl","description":"Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event."},"mapView":{"type":"string","enum":["2d","3d"],"default":"3d"},"density":{"type":"string","enum":["compact","standard","roomy"],"default":"compact","description":"Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). `standard` and `roomy` replace `comfortable` and `airy`."},"embedMode":{"type":"string","enum":["fullPage","embedded"],"default":"fullPage","description":"`embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site."},"heroBanner":{"type":"boolean","default":true},"searchInBanner":{"type":"boolean","default":false,"description":"Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6)."},"eventBannerDates":{"type":"boolean","default":false,"description":"**Dates in event banner (decided 29 September, rev 3 23SEP-19).** On, the event banner lists the next dates; off by default. Either way the date picker sits at the top of the booking step.\n"},"singleEventPage":{"type":"boolean","default":false},"quantitiesOnAddOns":{"type":"boolean","default":true},"timesPerPage":{"type":"string","enum":["8","12","24","all"],"default":"24","description":"**Times per page (decided 29 September, rev 3 REV3-1).** When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` shows every one. A string because `all` is one of the values.\n"},"dayPartFilter":{"type":"boolean","default":true,"description":"**Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1).** Where each part begins is `dayPartBoundaries`.\n"},"dayPartBoundaries":{"type":"object","description":"**Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1).** Morning is before `afternoonStartsAt`, afternoon runs to `eveningStartsAt`, evening is from `eveningStartsAt`. A venue sets its own through `venueOverrides`. `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400.\n","properties":{"afternoonStartsAt":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","default":"12:00"},"eveningStartsAt":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","default":"17:00"}}},"seatViewPosition":{"type":"string","enum":["bottom","right","left","top"],"default":"bottom","description":"**Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5).** Web only; on mobile and on a narrow screen it is always below the map.\n"},"seatTimeBar":{"type":"boolean","default":true,"description":"**Time bar above the seat map (decided 29 September, rev 3 REV3-6).** Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one.\n"},"ticketCategories":{"type":"string","enum":["categoryThenSubcategory","flatList"],"default":"categoryThenSubcategory","description":"**How tickets are grouped (decided 29 September, rev 3 REV3-16).** `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once.\n"},"ticketTags":{"type":"boolean","default":true,"description":"**Tags on tickets (decided 29 September, rev 3 23SEP-3).** Shows a product's display tags (such as \"2 Hours\", \"Min 1.10 m\", \"Valid 90 days\") on its card.\n"},"cardInfo":{"type":"boolean","default":true,"description":"**Extra info on cards (decided 29 September, rev 3 23SEP-6).** Shows each ticket type's description, who it is for and what it includes, under its name.\n"},"conciergeMascot":{"type":"boolean","default":true,"description":"**The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5).** Read only where the `aiConciergeChat` feature is on.\n"},"showInfoOnly":{"type":"boolean","default":true,"description":"**Show info-only products (decided 29 September, rev 3 REV3-14).** On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it.\n"},"locationSwitcher":{"type":"boolean","default":false,"description":"**Location switcher (decided 29 September, rev 3 REV3-18).** On, the booking screens carry a \"Booking at\" bar with Change location, reusing the guest's venue choice (audit R267). Off unless the tenant or venue enables it; it has no effect for a tenant with one venue.\n"},"guestContactFields":{"type":"array","minItems":1,"maxItems":3,"uniqueItems":true,"default":["email"],"items":{"type":"string","enum":["email","mobile","name"]},"description":"**What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1).** The prototype's Email only, + name and + mobile. Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.matchBy`), or 400. After the code is verified the guest is not asked for these again: the flow goes to the terms and payment, and the profile is completed later (WEB-020, GST-039). Read only where the `guestCheckout` feature is on.\n"},"dateStripDays":{"type":"integer","minimum":3,"maximum":31,"default":7,"description":"**The date strip (decided 17 September, M17-08).** How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar.\n"}}},
"BookingFlowVenueOverride": {"type":"object","x-ticvai-persistence":"none — embedded in tenant_config","description":"**One venue's booking-flow settings where they differ from the tenant's (decided 29 September, rev 3 CFG-11).** `settings` carries only the fields the venue changes; a field left out inherits the tenant value, and the schema defaults do not apply inside an override.\n","required":["venueId","settings"],"properties":{"venueId":{"type":"string","format":"uuid","description":"One of the tenant's active venues. At most one override per venue."},"settings":{"$ref":"#/components/schemas/BookingFlowSettings"}}},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."},"showPoweredBy":{"type":"boolean","default":true,"description":"**\"Powered by TICVAI\", a configuration toggle, on by default** (Chinmay, 2 October, workbook Q160 and the pre-apply round; consistent with DI-297; CHG-CSA-036). Shown on the launch screen and at the foot of Account and the web footer while true. **Switching it off needs the tenant's licence to allow it**: `setBrandIdentity` refuses `false` with `403 powered-by-locked` unless the tenant's plan carries the `poweredByRemoval` add-on (subscription `LicencePosition.poweredByRemovable`)."}}},
"ChangeScope": {"type":"string","description":"Whether a change reaches guests on publish or needs a store release.\n","enum":["runtime","buildTime"]},
"Collection": {"x-ticvai-persistence":"assets.media_collection","type":"object","required":["id","name","assetCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A name already used by any collection in the tenant, at any venue or level, is refused with `409 duplicate-code`.\n"},"description":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"parentCollectionId":{"type":"string","format":"uuid","nullable":true},"assetCount":{"type":"integer"},"coverAssetId":{"type":"string","format":"uuid","nullable":true}}},
"ContentBlock": {"type":"object","x-ticvai-persistence":"control.content_block","description":"BL-172. **`white-label` is excellent as a configuration model and is not an authoring surface.** `HomepageLayout` with ordered sections, `Banner`, `PromoBlock` and `ContentPage` describe what a venue has chosen; **none of them lets a marketer write something new without a developer.**\nA block is a piece of authored content with a type, a body and a schedule. **The page builder is a frontend over this**, the same way the venue map's canvas is a frontend over its graph.\n","required":["id","kind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"pageId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["richText","image","video","gallery","cta","faq","form","embed","productGrid","countdown","testimonial"]},"position":{"type":"integer"},"body":{"type":"object","additionalProperties":true,"description":"Typed by `kind`, and validated against the block's own schema at save."},"localeVariants":{"type":"object","additionalProperties":true,"description":"**Per-locale bodies, not per-locale pages.** A venue running Arabic and English should not maintain two page trees that drift — the structure is shared and the words are not.\n"},"status":{"type":"string","readOnly":true,"description":"Created as `draft`; moved by `publishContentBlock` and the `publishAt`/`expireAt` timer (`states/content-block.yaml`), never by the body of a create.","enum":["draft","scheduled","published","expired","archived"]},"publishAt":{"type":"string","format":"date-time","nullable":true,"description":"**Content scheduling, which the configuration model had no room for.** A seasonal banner that needs somebody awake at midnight is the same defect `Product.onSaleFrom` fixed.\n"},"expireAt":{"type":"string","format":"date-time","nullable":true},"audienceSegmentId":{"type":"string","format":"uuid","nullable":true,"description":"**Personalisation, evaluated at render.** A block shown only to members, or only to first-time visitors. Null shows it to everybody, which is what every block does today.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ContentPage": {"x-ticvai-persistence":"whitelabel.content_page","type":"object","required":["id","slug","title","body","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"isEnabled":{"type":"boolean","default":true,"description":"BL-005. **Enablement is not publication.** A published page that is disabled exists, keeps its URL and its history, and does not render — which is what a tenant wants when a section is seasonal.\n**Unpublishing loses the version; disabling does not.** Collapsing them means a venue turning off its water-park section for winter has to republish it every spring.\n"},"status":{"allOf":[{"$ref":"#/components/schemas/ContentStatus"}],"readOnly":true,"description":"Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`)."},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"},"isReferenced":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"True when navigation or the homepage links to this page. Blocks deletion. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ContentStatus": {"type":"string","enum":["draft","published","archived"]},
"DeepLinkScheme": {"x-ticvai-persistence":"none — derived from the primary domain and the published configuration","type":"object","description":"The URL patterns a tenant's own site uses to link into the storefront and the app (CHG-CSA-037).","required":["baseUrl","patterns"],"properties":{"baseUrl":{"type":"string","description":"The primary domain, or the platform subdomain where none is primary."},"patterns":{"type":"array","description":"**The patterns, fixed** (4 October 2026, CHG-FXC-009). One per target kind, under `baseUrl`:\n`product` `/p/{productId}`, `event` `/e/{eventId}`, `contentPage` `/c/{contentPageId}`, `module` `/m/{moduleKey}`,\n`appSection` `/s/{appSection}`, `bookingFlow` `/book/{productId}` (optionally `?date=YYYY-MM-DD`). `externalUrl` and\n`none` have no pattern. Campaign tags are appended as `utm_*` query parameters. A released pattern never changes: a new\ntarget kind gets a new prefix, so a link a tenant printed keeps working. Where app links are enabled the same path opens\nthe app (universal links and app links on the primary domain) and the storefront where the app is not installed;\n`buildDeepLink` returns the URL from these patterns and `appLink` as the same URL.","items":{"type":"object","required":["kind","pattern"],"properties":{"kind":{"type":"string","description":"A `LinkTarget.kind`, or `bookingFlow`."},"pattern":{"type":"string","description":"e.g. `/p/{productId}`, `/e/{eventId}`, `/book/{flowKey}`."}}}},"appLinksEnabled":{"type":"boolean"}}},
"ExpiringMedia": {"x-ticvai-persistence":"none — computed","type":"object","required":["assetId","filename","validTo","isExpired","isInUse"],"properties":{"assetId":{"type":"string","format":"uuid"},"filename":{"type":"string"},"thumbnailUrl":{"type":"string","nullable":true},"licensor":{"type":"string","nullable":true},"validTo":{"type":"string","format":"date"},"daysRemaining":{"type":"integer"},"isExpired":{"type":"boolean"},"isInUse":{"type":"boolean","description":"True while `liveUsageCount` is above zero, that is, while live (published) content references the asset (audit R106 (10)). Drafts and collections do not count."},"liveUsageCount":{"type":"integer","description":"References from live (published) content only (audit R106 (10)). Expired and live is the combination that matters."}}},
"FeatureKey": {"type":"string","description":"The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum.\n","enum":["digitalCompanionMode","aiConciergeChat","lostAndFound","pushNotifications","socialSharing","multiLanguage","appleWallet","googlePay","applePay","cashOnDelivery","guestCheckout","uaePassLogin"]},
"FeatureToggle": {"x-ticvai-persistence":"whitelabel.feature_toggle","type":"object","required":["featureKey","isEnabled","changeScope"],"properties":{"featureKey":{"allOf":[{"$ref":"#/components/schemas/FeatureKey"}],"description":"`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"},"requiresConfiguration":{"type":"boolean","description":"True where the feature needs credentials or setup elsewhere first."}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_layout + whitelabel.homepage_section","x-ticvai-retired-columns":["whitelabel.homepage_section.homepage_section_id"],"type":"object","description":"**The client-approved web and app wireframes are the layout** (Chinmay, 2 October, workbook Q163; CHG-CSA-040): sections, their order and their options follow the approved wireframes and change only where the spec breaks. **Landing-page templates** (workbook Q41 batch 2; CHG-CSA-037): a tenant with no landing page of its own starts from a TICVAI template (`templateKey`, `listLandingPageTemplates`); a tenant with its own site links into the storefront with deep links (`getDeepLinkScheme`, `buildDeepLink`).","required":["sections"],"properties":{"templateKey":{"type":"string","nullable":true,"description":"The landing-page template this layout started from (`listLandingPageTemplates`), or null for a layout composed from scratch (CHG-CSA-037)."},"landingSource":{"type":"string","enum":["storefront","ownSite"],"default":"storefront","description":"`storefront`: this home is the tenant's landing page. `ownSite`: the tenant's own website is the landing page and links in with deep links; this home is still served at the storefront address."},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"**How many cards the section shows, the venue's choice** (Chinmay, 2 October, workbook Q152: every customisation option of the approved wireframe, including the card count per section; CHG-CSA-040). Replaces the fixed 1 or 2 highlights of MOB-3: the CMS offers the counts the approved wireframe offers."},"scrollAnimation":{"type":"string","enum":["rise","scale","slide","blur","none"],"default":"rise","description":"**How the section enters as the guest scrolls** (Chinmay, 2 October, workbook Q153: \"must be there\"; DI-1088; CHG-CSA-040). Rise, Scale, Slide, Blur or None, as the v4 prototype offers; `none` for guests who asked the device for reduced motion is applied whatever is set."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"HomepageSectionKind": {"type":"string","description":"**Which module each section needs, proposed, client to correct (decided 28 September, audit R163).** `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events`; `attractions` needs `attractions`; `membership` needs `membership`; `dining` needs `diningAndFnb`; `shop` needs `shop`; `map` needs `map`. `heroBanner`, `quickActions`, `promotions`, `customContent`, `venueOverview` and `spacer` need no module. `venueOverview` (decided 29 September, MOB-3) is the mobile Home's description, opening hours (from `getTenantAppStatus`) and type tiles. `setHomepageLayout` refuses a visible section whose module is not enabled, and `setModuleEnablement` refuses to disable a module a section still needs.\n","enum":["heroBanner","quickActions","tickets","whatsOn","attractions","membership","dining","shop","promotions","map","customContent","venueOverview","spacer"]},
"LandingPageTemplate": {"x-ticvai-persistence":"none — TICVAI's template catalogue, read-only","type":"object","description":"A home page TICVAI provides for a tenant with no landing page of its own (CHG-CSA-037).","required":["templateKey","name","layout"],"properties":{"templateKey":{"type":"string"},"name":{"type":"string"},"presetKey":{"type":"string","nullable":true,"description":"The Site Builder preset it belongs to (`SiteSetupProgress.presetKey`)."},"thumbnailUrl":{"type":"string","nullable":true},"layout":{"$ref":"#/components/schemas/HomepageLayout"}}},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","description":"**A tenant may add or select interface languages beyond English and Arabic** (Chinmay, 2 October, workbook Q145; CHG-CSA-039). Any ISO 639-1 language. English and Arabic ship with complete interface strings; for any other, the interface strings come as a TICVAI string pack drafted by AI translation and reviewed (T03), and a string with no translation falls back to English. Content (pages, products, banners) is the tenant's to translate (`translationGaps`).","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"uiStringCoverage":{"type":"array","readOnly":true,"description":"How complete the interface strings are in each enabled language (CHG-CSA-039). English and Arabic are always complete.","items":{"type":"object","properties":{"language":{"type":"string"},"coveragePercent":{"type":"number","minimum":0,"maximum":100},"status":{"type":"string","enum":["complete","draft","missing"]}}}},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LinkTarget": {"x-ticvai-persistence":"none — embedded","type":"object","required":["kind"],"properties":{"kind":{"type":"string","enum":["module","contentPage","product","event","externalUrl","appSection","none"],"description":"`appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets."},"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"appSection":{"type":"string","enum":["home","explore","plan","tickets","map","account","buyTickets"],"description":"Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it."},"contentPageId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"url":{"type":"string"}}},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive","model3d"],"description":"`model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. No rendition or derivative is generated for it; the guest app downloads the file as uploaded.\n"},
"MediaReplaceResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","affectedSurfaces"],"properties":{"asset":{"$ref":"#/components/schemas/MediaAsset"},"affectedSurfaces":{"type":"integer","description":"How many surfaces now show the new file."},"liveSurfaces":{"type":"integer","description":"Of those, how many are published to guests right now."},"derivativesRegenerating":{"type":"boolean"}}},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleEnablement": {"x-ticvai-persistence":"whitelabel.module_enablement","type":"object","required":["moduleKey","isLicensed","isEnabled"],"properties":{"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"displayName":{"type":"string"},"isLicensed":{"type":"boolean","description":"From the tenant's subscription. False makes enablement impossible."},"isEnabled":{"type":"boolean"},"referencedBy":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.","items":{"type":"string"}}}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_config + whitelabel.navigation_item","x-ticvai-retired-columns":["whitelabel.navigation_item.navigation_item_id"],"type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Preview": {"x-ticvai-persistence":"none — short-lived, cache only","type":"object","required":["previewId","url","expiresAt"],"properties":{"previewId":{"type":"string","format":"uuid"},"url":{"type":"string"},"platform":{"type":"string","enum":["ios","android","web"]},"theme":{"type":"string","deprecated":true,"enum":["light","dark"],"description":"Deprecated with `Theme.darkMode` (CHG-CSA-035); the preview always renders the venue's theme."},"language":{"type":"string","pattern":"^[a-z]{2}$"},"outputPreviews":{"type":"array","readOnly":true,"description":"**The PDF ticket and the Apple and Google Wallet passes, previewed with the app** (Chinmay, 2 October, workbook Q151: in Block A; CHG-CSA-041). One entry per output asked for in `outputs`.","items":{"type":"object","required":["output","url"],"properties":{"output":{"type":"string","enum":["app","pdfTicket","appleWalletPass","googleWalletPass"]},"url":{"type":"string","description":"A short-lived link to the rendered output (the PDF, the `.pkpass`, or the Google pass preview), expiring with the preview."}}}},"expiresAt":{"type":"string","format":"date-time"}}},
"PromoBlock": {"x-ticvai-persistence":"whitelabel.promo_block","type":"object","required":["id","title"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"$ref":"#/components/schemas/LocalisedText"},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"promotionId":{"type":"string","format":"uuid","nullable":true,"description":"Presentation only. A block may point at a promotion; it does not create or price one.\n"},"linkTarget":{"$ref":"#/components/schemas/LinkTarget"},"startsAt":{"type":"string","format":"date-time","nullable":true},"endsAt":{"type":"string","format":"date-time","nullable":true,"description":"Must follow `startsAt` when both are set (decided 28 September, audit R163)."},"state":{"allOf":[{"$ref":"#/components/schemas/ScheduleState"}],"readOnly":true,"x-ticvai-derived":"sweeper","description":"Moved by the schedule timer at `startsAt` and `endsAt`, in the tenant's timezone, as for `Banner.state`. Once `active` or `expired` the block may only be withdrawn (audit R163)."},"sortOrder":{"type":"integer"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"translationJobId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `proposeTranslations` job that drafted this proposal; `getTranslationProposals` reads a job's rows by it. Null on every other proposal (CHG-RFM-004)."},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"ScheduleState": {"type":"string","enum":["draft","scheduled","active","expired"]},
"SearchResult": {"type":"object","x-ticvai-persistence":"none — computed","properties":{"kind":{"type":"string"},"id":{"type":"string"},"title":{"type":"string"},"excerpt":{"type":"string"},"relevance":{"type":"number"},"collectionId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"For kind `media`, the asset (29 September, build; 23.1.6)."},"mediaType":{"type":"string","nullable":true,"enum":["image","video","audio","document"]},"matchedOn":{"type":"string","nullable":true,"enum":["title","description","tags","aiDescription"],"description":"Which text the match came from, so a wrong hit can be traced to a wrong tag."}}},
"SiteSetupProgress": {"x-ticvai-persistence":"whitelabel.site_setup_progress","type":"object","description":"**The Site Builder's saved progress, one row per tenant (decided 29 September, W12 and M24-05).** Not configuration and not published. `presetKey` is the starting point the operator picked; the builder pre-fills each step from it, which is what keeps the minimum path to a working site at about 30 minutes.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"presetKey":{"type":"string","nullable":true,"enum":["themePark","waterPark","museum","theatreAndArena","singleAttraction","playCentre","multiVenue",null],"description":"The starting point. Each preset proposes the modules, the booking flow types (with their default step order), the homepage sections, the mobile tabs and a booking-flow `preset`; nothing is written until the operator accepts a step."},"currentStep":{"allOf":[{"$ref":"#/components/schemas/SiteSetupStepKey"}],"nullable":true},"steps":{"type":"object","description":"One entry per `SiteSetupStepKey`.","additionalProperties":{"type":"object","required":["status"],"properties":{"status":{"type":"string","enum":["notStarted","inProgress","done","skipped"]},"completedAt":{"type":"string","format":"date-time","nullable":true},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}},"minimumPathDone":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True once the minimum path is done: a logo, the four theme colours, at least one enabled valid booking flow and a published version. Everything else keeps its preset or schema default."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"SiteSetupStepKey": {"type":"string","description":"The seven Site Builder steps, in order (decided 29 September, W12): venue and modules (CMS-001), ticketing flows (CMS-103), compose steps (CMS-103), Help me choose (CMS-101), look and feel (CMS-007, CMS-009, CMS-002, CMS-004, CMS-008, CMS-005, CMS-003), mobile app (CMS-009, CMS-004, CMS-007), preview and publish (CMS-006, CMS-012, CMS-014).\n","enum":["venueAndModules","ticketingFlows","composeSteps","helpMeChoose","lookAndFeel","mobileApp","previewAndPublish"]},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"TenantConfig": {"x-ticvai-persistence":"whitelabel.tenant_config","type":"object","description":"**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n","required":["tenantId","version"],"properties":{"tenantId":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The draft's working version label; the published one is `ConfigVersion.version`."},"isDraft":{"type":"boolean","readOnly":true,"description":"True for the working draft, which is the only row."},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"bookingFlow":{"$ref":"#/components/schemas/BookingFlowConfig"},"bookingFlows":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12).","items":{"$ref":"#/components/schemas/BookingFlow"}},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"notificationBranding":{"type":"object","nullable":true,"description":"BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n","properties":{"senderName":{"type":"string"},"replyToEmail":{"type":"string","format":"email"},"smsSenderId":{"type":"string","nullable":true},"whatsappBusinessId":{"type":"string","nullable":true},"logoAssetId":{"type":"string","format":"uuid","nullable":true}}},"enabledPaymentMethods":{"type":"array","nullable":true,"description":"BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n","items":{"type":"string"}},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"modules":{"type":"array","items":{"$ref":"#/components/schemas/ModuleEnablement"}},"features":{"type":"array","items":{"$ref":"#/components/schemas/FeatureToggle"}},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"updatedAt":{"type":"string","format":"date-time"},"isInMaintenance":{"type":"boolean","default":false,"description":"Written by `setMaintenanceMode`; read by `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The message on the branded maintenance screen."},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"allOf":[{"$ref":"#/components/schemas/MinimumAppVersion"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"contact":{"allOf":[{"$ref":"#/components/schemas/VenueContact"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availability":{"allOf":[{"$ref":"#/components/schemas/AppAvailability"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"venues":{"type":"array","x-ticvai-derived":"onRead","description":"The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"name":{"$ref":"#/components/schemas/LocalisedText"},"city":{"type":"string","nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","x-ticvai-contrast-pairs":[{"foreground":"textColour","background":"backgroundColour","use":"text","ratio":4.5},{"foreground":"textColour","background":"backgroundColour","use":"largeText","ratio":3.0},{"foreground":"primaryColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"secondaryColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"accentColour","background":"backgroundColour","use":"nonText","ratio":3.0},{"foreground":"componentColours.*.text","background":"componentColours.*.background","use":"text","ratio":4.5},{"foreground":"componentColours.*.background","background":"backgroundColour","use":"nonText","ratio":3.0}],"required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","deprecated":true,"description":"**Deprecated and ignored** (Chinmay, 2 October, workbook Q150 and the pre-apply round; CHG-CSA-035). White label has no dark or light mode: the venue's chosen theme is applied, on every device setting. The field is kept so a client built at r1 still parses, is accepted on `setTheme` and returned as stored, and **is never used to render anything or drawn on any screen**; the guest app has no Light/Dark switch.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"ThemeComponentColour": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","properties":{"background":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"text":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"TicketProof": {"type":"object","x-ticvai-persistence":"none — rendered on request, nothing is stored","description":"A sample ticket from a template, **marked as a proof on the artefact itself** so it cannot be presented at a gate.","required":["templateId","mediaType","contentRef"],"properties":{"templateId":{"type":"string","format":"uuid"},"mediaType":{"type":"string","enum":["thermalTicket","a4Pdf","wristband","rfidCard","walletPass","qrOnly","sms"]},"locale":{"type":"string","nullable":true},"contentRef":{"type":"string","format":"uri","description":"Where the rendered proof can be fetched or sent to the printer from."},"walletPlatform":{"type":"string","nullable":true,"enum":["appleWallet","googleWallet"],"description":"Which wallet the pass preview is for, where `mediaType` is `walletPass` (DEC-151; CHG-CSP-038)."}}},
"UpdateContentPageRequest": {"x-ticvai-persistence":"none — request only; the fields land on whitelabel.content_page","type":"object","description":"The body of `updateContentPage`: the fields a tenant edits. `id`, `isReferenced` and `scopePath` are the server's, and `status` moves only to `archived` here — publishing is `publishTenantConfig` (`states/content.yaml`).\n","required":["slug","title","body"],"properties":{"slug":{"type":"string","pattern":"^[a-z0-9-]+$"},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"isEnabled":{"type":"boolean","default":true},"iconAssetRef":{"type":"string","format":"uuid","nullable":true},"categoryCode":{"type":"string","nullable":true},"sortOrder":{"type":"integer"},"status":{"allOf":[{"$ref":"#/components/schemas/ContentStatus"}],"description":"Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). Any other value is a 400 `validation`. Omit to leave the status as it is."}}},
"UploadTicket": {"x-ticvai-persistence":"assets.media_upload","type":"object","required":["uploadId","uploadUrl","method","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"uploadId":{"type":"string","format":"uuid"},"uploadUrl":{"type":"string","description":"Signed. PUT the file here, then confirm with `/complete`."},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"maxSizeBytes":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"venueId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}}
}
```
