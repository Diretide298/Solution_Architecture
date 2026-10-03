# WS13 — Approval Workflows and Governance board 1

**10 screens · 8 operations · 13 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-364` | Approval Command Center Dashboard | B | 1 | 158 | 6 | 14 | 1 | 3 | — | notStarted (—) |
| `BO-365` | My Approval Inbox | B | 0 | 22 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `BO-366` | Team / Shared Approval Queue | B | 0 | 0 | 6 | 7 | 1 | 6 | — | notStarted (—) |
| `BO-367` | Approval Request Detail | B | 0 | 0 | 6 | 13 | 2 | 3 | — | notStarted (—) |
| `BO-368` | AI Decision Support | B | 0 | 16 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `BO-369` | High Priority & Risk Queue | B | 0 | 0 | 6 | 7 | 0 | 6 | — | notStarted (—) |
| `BO-370` | Escalated Approval Center | B | 0 | 16 | 6 | 2 | 0 | 3 | — | notStarted (—) |
| `BO-371` | Completed Approval History | B | 2 | 0 | 6 | 7 | 0 | 3 | — | notStarted (—) |
| `BO-372` | Approval SLA & Workload Monitor | B | 0 | 44 | 6 | 0 | 2 | 3 | — | notStarted (—) |
| `BO-373` | Approval Activity & Notification Center | B | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-365, BO-366, BO-367, BO-368, BO-369, BO-370, BO-371, BO-373 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-364` Approval Command Center Dashboard

**Provide management and approvers with a real-time overview of approval activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-364 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a display directory (§Key Functions) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/approval-command-center-dashboard-bo-364` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The approval board's hub: pending, awaiting me, approved and rejected today, escalated, SLA breached and high-risk counts, each opening the matching queue. Opens the board's other screens and they return here.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 20 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The KPIs are drawn as table columns of a dataTable. (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Filter by | multi select | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

#### Outputs: what the screen shows and produces

**Shown**

**Pending approvals** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Awaiting my approval** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Approved today** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Rejected** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Escalated** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**SLA breached** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**High-risk requests** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**AI-prioritized requests** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Average approval time** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Approval volume** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Approval trend** (metric tile, from `getApprovalAnalytics`): A tile over the population; the response schema still has to name the measure (logged, CHG-SBO-005).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | chip: Kind, Approver, Venue, Day, Week | The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it. |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**Waiting for a decision** (data table, from `listApprovalRequests`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |
| Requested at | 1 Oct 2026, 14:30 | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Data it reads**: `getApprovalAnalytics` (onLoad, Volume, outcome and SLA); `listApprovalRequests` (onLoad, What is waiting)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-373` Approval Activity & Notification Center: *Approval Activity & Notification Center*
- → `BO-366` Team / Shared Approval Queue: *Team / Shared Approval Queue*
- → `BO-367` Approval Request Detail: *Approval Request Detail*; carries `approvalRequestId`
- → `BO-368` AI Decision Support: *AI Decision Support*; carries `approvalRequestId`
- → `BO-369` High Priority & Risk Queue: *High Priority & Risk Queue*; carries `approvalRequestId`
- → `BO-370` Escalated Approval Center: *Escalated Approval Center*; carries `requestId`
- → `BO-371` Completed Approval History: *Completed Approval History*
- → `BO-372` Approval SLA & Workload Monitor: *Approval SLA & Workload Monitor*
- → `BO-084` Approval Inbox: *My approval inbox*; carries `approvalRequestId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Consistency with other screens

- Match `BO-084`: "Awaiting my approval" opens the approval inbox, not a separate list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every approval:
- Pending approvals: 128
  Awaiting my approval: 1.8 s
  Approved today: 57
  Rejected: 128
  Escalated: 46
  SLA breached: 3 h 20 min
  High-risk requests: 128
  AI-prioritized requests: 128
- Pending approvals: 42
  Awaiting my approval: 3 h 20 min
  Approved today: 11
  Rejected: 46
  Escalated: 312
  SLA breached: 42 min
  High-risk requests: 42
  AI-prioritized requests: 42
- Pending approvals: 7
  Awaiting my approval: 42 min
  Approved today: 128
  Rejected: 312
  Escalated: 74
  SLA breached: 1.8 s
  High-risk requests: 7
  AI-prioritized requests: 7
```

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff
- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.10 | Out-of-Office Routing - System shall automatically reroute approvals when approvers are unavailable. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.28 | Mobile Approvals - System shall support approval actions through mobile applications. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.29 | Email-Based Approvals - System shall support approval actions through email links. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.54 | Approval Reopening - System shall support reopening previously completed approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.73 | AI Risk Assessment - System shall provide AI-generated risk assessments for approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-364` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-364`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 1: Opens Approval Command Center Dashboard → Provide management and approvers with a real-time overview of approval activity.
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F123 branch at step 1 (expected): when Nothing has been set up on Approval Command Center Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F123 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (158 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-364?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-373`, `BO-366`, `BO-367`, `BO-368`, `BO-369`, `BO-370`, `BO-371`, `BO-372`, `BO-084`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-365` My Approval Inbox

**Provide each approver with their personal actionable queue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-365 |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/my-approval-inbox-bo-365` |

**What the spec says about it.** **Merged into BO-084** (decided 2 October 2026, Chinmay: fix the wrong wiring now; CHG-WIR-021). My Approval Inbox duplicated BO-084's queue with its own unbound columns and the same single read; one inbox, and the board tile opens BO-084 (design-notes correction platform-foundation BO-365). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-084, and nothing on it is built separately.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The approver's personal queue from the approval board; the same queue as BO-084.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 11 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Duplicates BO-084's queue with its own unbound columns. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every approval** (data table)

| Shows | Format | Notes |
|---|---|---|
| Request ID | text | not in the schema: `Request ID` |
| Request type | text | not in the schema: `Request type` |
| Requested by | text | not in the schema: `Requested by` |
| Venue | text | not in the schema: `Venue` |
| Department | text | not in the schema: `Department` |
| Requested value | text | not in the schema: `Requested value` |
| Submitted time | text | not in the schema: `Submitted time` |
| SLA remaining | text | not in the schema: `SLA remaining` |
| Risk level | text | not in the schema: `Risk level` |
| Priority | text | not in the schema: `Priority` |
| Current approval stage | text | not in the schema: `Current approval stage` |

**The selected approval** (detail panel): The pack groups this record's detail under its own headings: “Tabs”.

| Shows | Format | Notes |
|---|---|---|
| Request ID | text | not in the schema: `Request ID` |
| Request type | text | not in the schema: `Request type` |
| Requested by | text | not in the schema: `Requested by` |
| Venue | text | not in the schema: `Venue` |
| Department | text | not in the schema: `Department` |
| Requested value | text | not in the schema: `Requested value` |
| Submitted time | text | not in the schema: `Submitted time` |
| SLA remaining | text | not in the schema: `SLA remaining` |
| Risk level | text | not in the schema: `Risk level` |
| Priority | text | not in the schema: `Priority` |
| Current approval stage | text | not in the schema: `Current approval stage` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Requested value)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every approval:
- Request ID: APR-2026-004812
  Request type: Refund above threshold
  Requested by: Rahul Menon
  Venue: AquaCove Abu Dhabi
  Department: Ticketing
  Requested value: AED 482,300.00
  Submitted time: 1.8 s
  SLA remaining: 42 min
- Request ID: APR-2026-004797
  Request type: Price change
  Requested by: Fatima Al Mansoori
  Venue: AquaCove Dubai
  Department: F&B
  Requested value: AED 96,750.00
  Submitted time: 3 h 20 min
  SLA remaining: 1.8 s
- Request ID: APR-2026-004755
  Request type: Discount override
  Requested by: Omar Haddad
  Venue: AquaCove Muscat
  Department: Retail
  Requested value: AED 12,400.00
  Submitted time: 42 min
  SLA remaining: 3 h 20 min
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-365` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-365`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-365?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-366` Team / Shared Approval Queue

**Allow managers and centralized approval teams to manage approvals belonging to their team or department.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-366 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/team-shared-approval-queue-bo-366` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-024): No operation assigns, reassigns or claims an approval request in a shared queue.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A team or department queue: requests assigned to a shared queue that anyone in the team may pick up, with assign/reassign. Picking one up assigns it to that person so two people do not decide the same item.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table has no columns and there is no assign or claim operation. (CHG-WIR-024)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listApprovalRequests` (onLoad, The shared queue)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The team shared approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the team shared approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No team shared approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the team shared approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listApprovalRequests (ApprovalRequest):
- kind: standard
  rerouteOnNoApprover: true
  allowEmailApproval: true
  status: active
  summary: Guest charged twice at Main Gate Till 3
  amount: AED 1,250.00
  justification: Guest charged twice at Main Gate Till 3
- kind: standard
  rerouteOnNoApprover: false
  allowEmailApproval: false
  status: pending
  summary: Group of 40 from Desert Gate Tours
  amount: AED 48,000.00
  justification: Group of 40 from Desert Gate Tours
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-366` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-366`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 4: Works in Team / Shared Approval Queue → Allow managers and centralized approval teams to manage approvals belonging to their team or department.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-366?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-367` Approval Request Detail

**Approval Request Detail**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-367 |
| Who uses it | venue staff holding `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `requestId` (navigation), `approvalRequestId` (navigation) |
| Route | `/venue-operations/approval-request-detail-bo-367` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The single approval request page from the board; the same page as BO-085.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Decide (Approve / Reject / Return / Request information)**: Four outcomes, not two: reject needs a reason the requester reads; return sends it back to amend; request information pauses the SLA clock. Approving records an authorisation and does not perform the action; on a multi-level chain the request moves to the next level. Where the rule demands MFA the decision carries a stepUpToken from the in-place challenge; where it demands a signature, the signature step comes first. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; F14 step 4)*

**Data it reads**: `listApprovalRequests` (onLoad, The request); `getApprovalRequestScore` (onLoad, Risk band, priority and suggested escalation for the …)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval request detail list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval request detail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval request detail yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval request detail are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for decideApprovalRequest. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 403**: Show it as something the person can act on, not a failure: The approver may not decide this request. **Always carries `refusedReason`**, one value per cause — the approver is the requester (`approverIsRequester`), is not in the resolved chain (`notInApproverChain`), lacks the permission the rule demands (`insufficientPermission`), gave no step-up token where the rule requires MFA (`mfaR... *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 409**: Show it as something the person can act on, not a failure: The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and `currentStatus` carries the status it is in. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **The approver raised the request, or sits outside the resolved chain**: Decide is refused 403 with refusedReason (approverIsRequester, notInApproverChain, missing permission or step-up); show the reason in words and who can decide instead. Segregation of duties survives delegation. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-085`: One implementation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listApprovalRequests (ApprovalRequest):
- kind: standard
  rerouteOnNoApprover: true
  allowEmailApproval: true
  status: active
  summary: Guest charged twice at Main Gate Till 3
  amount: AED 1,250.00
  justification: Guest charged twice at Main Gate Till 3
- kind: standard
  rerouteOnNoApprover: false
  allowEmailApproval: false
  status: pending
  summary: Group of 40 from Desert Gate Tours
  amount: AED 48,000.00
  justification: Group of 40 from Desert Gate Tours
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `decideApprovalRequest` → `APPROVAL_DECIDE` (operate) · staff, public
- `getApprovalRequestScore` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.20 | Approval Comments - System shall allow approvers to add comments to approval decisions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.21 | Approval Rejection Reasons - System shall require rejection reasons when approvals are denied. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.57 | Digital Signature Support - System shall support digital signatures for sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.59 | Approval Authentication - System shall require authentication before approval actions are executed. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.60 | MFA-Protected Approvals - System shall support MFA requirements for sensitive approval actions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision view includes a business context/evidence viewer (e.g. payment information, any logged customer complaint) and an approval timeline showing when the request was initiated and when each stage was completed or is pending. *(client request · MoM 8 Sep 2026, 4.15 Execution & Decision Management · DI-728)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-367` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-367`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 6: Works in Approval Request Detail → Approval Request Detail

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-367?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-368` AI Decision Support

**AI Decision Support**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-368 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `approvalRequestId` (navigation) |
| Route | `/venue-operations/ai-decision-support-bo-368` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-021): AI Decision Support used evaluateApprovalRequirement (whether approval is required) where the AI context is the request's score, getApprovalRequestScore …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI context for an approver: risk band, priority and suggested escalation for the request. The AI never suggests approve or reject.

**Fixed on main** (the package already carries these; draw what it says): Uses evaluateApprovalRequirement instead of getApprovalRequestScore. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**AI context** (detail panel, from `getApprovalRequestScore`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Approval request | the name it points at, never the id | — |
| Trigger | chip: Submitted, Resubmitted, Sla tick, Escalated | — |
| Risk score | 1,234 | — |
| Risk band | chip: Low, Medium, High, Critical | Design 5.6: a risk score and band, never a probability. |
| Priority score | 1,234 | For ordering work in an inbox; higher first. |
| Escalation suggestion | grouped details | A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy. |
| Action | chip: Escalate, Add backup approver, None | — |
| Reason | text | — |
| Signals | list or chips (count when long) | — |
| Code | text | e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate` … |
| Contribution | 1,234.5 | — |
| Detail | text | — |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Decision record | the name it points at, never the id | — |
| Scored at | 1 Oct 2026, 14:30 | — |

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **AI context**: Labelled as context only, with the factors it used; no approve/reject recommendation. *(source: contracts/satellite/ai.yaml#getApprovalRequestScore)*

**Data it reads**: `listApprovalRequests` (onLoad, Requests with their AI context (aiAssessment: risk …); `getApprovalRequestScore` (onLoad, Risk band, priority and suggested escalation for the …)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The decision support list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the decision support untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No decision support yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the decision support are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listApprovalRequests (ApprovalRequest):
- kind: standard
  rerouteOnNoApprover: true
  allowEmailApproval: true
  status: active
  summary: Guest charged twice at Main Gate Till 3
  amount: AED 1,250.00
  justification: Guest charged twice at Main Gate Till 3
- kind: standard
  rerouteOnNoApprover: false
  allowEmailApproval: false
  status: pending
  summary: Group of 40 from Desert Gate Tours
  amount: AED 48,000.00
  justification: Group of 40 from Desert Gate Tours
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `getApprovalRequestScore` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-368` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-368`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 8: Works in AI Decision Support → AI Decision Support

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-368?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-369` High Priority & Risk Queue

**Create a dedicated operational screen for approvals requiring immediate attention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-369 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `approvalRequestId` (navigation) |
| Route | `/venue-operations/high-priority-risk-queue-bo-369` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Approvals needing immediate attention: high risk, high value, close to or past SLA, sorted by breach time.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `listApprovalRequests` (onLoad, High priority and risk); `getApprovalRequestScore` (onLoad, Risk band, priority and suggested escalation for the …)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The high priority risk list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the high priority risk untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No high priority risk yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the high priority risk are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- request: APR-2026-004755
  kind: Refund above threshold
  amount: AED 7,800.00
  risk: High
  sla: Breached 25 min ago
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `getApprovalRequestScore` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-369` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-369`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 10: Works in High Priority & Risk Queue → Create a dedicated operational screen for approvals requiring immediate attention.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-369?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-370` Escalated Approval Center

**Manage requests that were escalated because of SLA breaches, risk conditions, unavailable approvers or configured escalation rules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-370 |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `requestId` (navigation) |
| Route | `/venue-operations/escalated-approval-center-bo-370` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Requests escalated by SLA breach, risk or unavailable approver: original and current approver, level, reason, time waiting. Escalation adds an approver; the original remains in the chain.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 8 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workflow | text field | — | — | `listSlaEscalationBottleneck` ?workflow |
| Risk | text field | — | — | `listSlaEscalationBottleneck` ?risk |
| Escalation level | text field | — | — | `listSlaEscalationBottleneck` ?escalationLevel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every escalated approval** (data table)

| Shows | Format | Notes |
|---|---|---|
| Original approver | text | not in the schema: `Original approver` |
| Current approver | text | not in the schema: `Current approver` |
| Escalation level | text | not in the schema: `Escalation level` |
| Escalation reason | text | not in the schema: `Escalation reason` |
| Time waiting | text | not in the schema: `Time waiting` |
| SLA status | text | not in the schema: `SLA status` |
| Previous actions | text | not in the schema: `Previous actions` |
| Next escalation level | text | not in the schema: `Next escalation level` |

**The selected escalated approval** (detail panel): The pack groups this record's detail under its own headings: “Escalation Timeline”.

| Shows | Format | Notes |
|---|---|---|
| Original approver | text | not in the schema: `Original approver` |
| Current approver | text | not in the schema: `Current approver` |
| Escalation level | text | not in the schema: `Escalation level` |
| Escalation reason | text | not in the schema: `Escalation reason` |
| Time waiting | text | not in the schema: `Time waiting` |
| SLA status | text | not in the schema: `SLA status` |
| Previous actions | text | not in the schema: `Previous actions` |
| Next escalation level | text | not in the schema: `Next escalation level` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Chain**: Both the original and the added approver shown; "who was asked and did not answer" is the point. *(source: contracts/spine/approvals.yaml#escalateApprovalRequest)*

**Data it reads**: `listSlaEscalationBottleneck` (onLoad, What escalated and why)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The escalated approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the escalated approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No escalated approval yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the escalated approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_REQUEST for escalateApprovalRequest. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#escalateApprovalRequest)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every escalated approval:
- Original approver: Rahul Menon
  Current approver: Rahul Menon
  Escalation level: 128
  Escalation reason: 46
  Time waiting: 3 h 20 min
  SLA status: 42 min
  Previous actions: 128
  Next escalation level: 233
- Original approver: Fatima Al Mansoori
  Current approver: Fatima Al Mansoori
  Escalation level: 46
  Escalation reason: 312
  Time waiting: 42 min
  SLA status: 1.8 s
  Previous actions: 46
  Next escalation level: 57
- Original approver: Omar Haddad
  Current approver: Omar Haddad
  Escalation level: 312
  Escalation reason: 74
  Time waiting: 1.8 s
  SLA status: 3 h 20 min
  Previous actions: 312
  Next escalation level: 11
```

#### Permissions

- `listSlaEscalationBottleneck` → `APPROVAL_VIEW` (read) · staff
- `escalateApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.47 | Multi-Level Escalation - System shall support escalation through multiple organizational levels. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |
| 11.1.48 | Escalation History - System shall maintain complete escalation history. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-370` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-370`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 12: Works in Escalated Approval Center → Manage requests that were escalated because of SLA breaches, risk conditions, unavailable approvers or configured escalation rules.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-370?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-371` Completed Approval History

**Provide searchable historical records of completed approval decisions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-371 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/completed-approval-history-bo-371` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Searchable history of completed approvals with outcome, decider, comment and duration.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search completed approval history | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by request id, transaction, customer, requester, approver, venue and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; - Publishing white-label … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Approval amount)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listApprovalRequests` (onLoad, Completed history)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The completed approval history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the completed approval history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No completed approval history yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the completed approval history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- request: APR-2026-004101
  kind: Discount override
  outcome: approved
  decidedBy: Fatima Al Mansoori
  comment: Repeat school group
  took: 6 min
```

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-371` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-371`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 14: Works in Completed Approval History → Provide searchable historical records of completed approval decisions.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-371?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-372` Approval SLA & Workload Monitor

**Give managers visibility into operational performance before approvals become bottlenecks.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-372 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/approval-sla-workload-monitor-bo-372` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** SLA health of approvals: within SLA, at risk, breached and average time, by team and kind.

**Fixed on main** (the package already carries these; draw what it says): Tile labels carry fixed values ("Within SLA — 92%"). (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Within SLA** (metric tile, from `listSlaEscalationReminder`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Policy code, the same key setApprovalSlaPolicy upserts by |
| Sla type | chip: Response sla, Approval sla, Task sla, Resolution sla, System action timeout | Which clock this policy governs |
| Calendar basis | chip: Calendar hours, Business hours, Working days, Venue calendar, Holiday calendar | How elapsed time is counted |
| Escalation actions | list or chips (count when long) | What happens on escalation |
| Channels type | chip: Email, Push, In app, SMS where appropriate | Vocabulary listed under Reminder Channels. |
| Target minutes | 1,234 | SLA target in minutes |
| On breach | chip: Notify only, Escalate, Auto approve, Auto reject | Outcome at breach; auto outcomes only where explicitly permitted |
| Auto action allowed | yes / no (icon or chip) | Auto-approve or auto-reject on breach is explicitly permitted; default false |
| First reminder at percent | 1,234 | Percent of target at which the first reminder goes |
| Second reminder at percent | 1,234 | Percent of target at which the second reminder goes |
| Escalate at percent | 1,234 | Percent of target at which the request escalates |

**At Risk** (metric tile, from `listSlaEscalationReminder`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Policy code, the same key setApprovalSlaPolicy upserts by |
| Sla type | chip: Response sla, Approval sla, Task sla, Resolution sla, System action timeout | Which clock this policy governs |
| Calendar basis | chip: Calendar hours, Business hours, Working days, Venue calendar, Holiday calendar | How elapsed time is counted |
| Escalation actions | list or chips (count when long) | What happens on escalation |
| Channels type | chip: Email, Push, In app, SMS where appropriate | Vocabulary listed under Reminder Channels. |
| Target minutes | 1,234 | SLA target in minutes |
| On breach | chip: Notify only, Escalate, Auto approve, Auto reject | Outcome at breach; auto outcomes only where explicitly permitted |
| Auto action allowed | yes / no (icon or chip) | Auto-approve or auto-reject on breach is explicitly permitted; default false |
| First reminder at percent | 1,234 | Percent of target at which the first reminder goes |
| Second reminder at percent | 1,234 | Percent of target at which the second reminder goes |
| Escalate at percent | 1,234 | Percent of target at which the request escalates |

**Breached** (metric tile, from `listSlaEscalationReminder`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Policy code, the same key setApprovalSlaPolicy upserts by |
| Sla type | chip: Response sla, Approval sla, Task sla, Resolution sla, System action timeout | Which clock this policy governs |
| Calendar basis | chip: Calendar hours, Business hours, Working days, Venue calendar, Holiday calendar | How elapsed time is counted |
| Escalation actions | list or chips (count when long) | What happens on escalation |
| Channels type | chip: Email, Push, In app, SMS where appropriate | Vocabulary listed under Reminder Channels. |
| Target minutes | 1,234 | SLA target in minutes |
| On breach | chip: Notify only, Escalate, Auto approve, Auto reject | Outcome at breach; auto outcomes only where explicitly permitted |
| Auto action allowed | yes / no (icon or chip) | Auto-approve or auto-reject on breach is explicitly permitted; default false |
| First reminder at percent | 1,234 | Percent of target at which the first reminder goes |
| Second reminder at percent | 1,234 | Percent of target at which the second reminder goes |
| Escalate at percent | 1,234 | Percent of target at which the request escalates |

**Average Approval** (metric tile, from `listSlaEscalationReminder`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Policy code, the same key setApprovalSlaPolicy upserts by |
| Sla type | chip: Response sla, Approval sla, Task sla, Resolution sla, System action timeout | Which clock this policy governs |
| Calendar basis | chip: Calendar hours, Business hours, Working days, Venue calendar, Holiday calendar | How elapsed time is counted |
| Escalation actions | list or chips (count when long) | What happens on escalation |
| Channels type | chip: Email, Push, In app, SMS where appropriate | Vocabulary listed under Reminder Channels. |
| Target minutes | 1,234 | SLA target in minutes |
| On breach | chip: Notify only, Escalate, Auto approve, Auto reject | Outcome at breach; auto outcomes only where explicitly permitted |
| Auto action allowed | yes / no (icon or chip) | Auto-approve or auto-reject on breach is explicitly permitted; default false |
| First reminder at percent | 1,234 | Percent of target at which the first reminder goes |
| Second reminder at percent | 1,234 | Percent of target at which the second reminder goes |
| Escalate at percent | 1,234 | Percent of target at which the request escalates |

**Data it reads**: `listSlaEscalationReminder` (onLoad, SLA and workload); `getApprovalAnalytics` (onLoad, Where the time goes)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval sla workload list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval sla workload untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval sla workload are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Within SLA — 92%: 94%
  At Risk — 17: 0
  Breached — 6: 5
  Average Approval — 34 min: 3 h 20 min
```

#### Permissions

- `listSlaEscalationReminder` → `APPROVAL_VIEW` (read) · staff
- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval analytics shows how long each request took and overall turnaround across all logged requests. *(client request · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-734)*
- SLA reminders notify the approver (e.g. by email) as the deadline approaches; a workload view shows how many pending requests each approver currently carries. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-731)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-372` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-372`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 16: Works in Approval SLA & Workload Monitor → Give managers visibility into operational performance before approvals become bottlenecks.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-372?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-373` Approval Activity & Notification Center

**Provide a unified chronological feed of important approval events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | Block B · task VM-BO-373 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/approval-activity-notification-center-bo-373` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A chronological feed of approval events (raised, decided, escalated, delegated, expired) for the approver's scope.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workflow instance | text field | — | — | `listWorkflowInstanceProcess` ?workflowInstance |
| Source module | text field | — | — | `listWorkflowInstanceProcess` ?sourceModule |
| Current status | text field | — | — | `listWorkflowInstanceProcess` ?currentStatus |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listWorkflowInstanceProcess` (onLoad, Activity across workflows)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Back to Approval Command Center Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval activity notification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval activity notification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval activity notification yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval activity notification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
feed:
- 10:12 Omar Haddad approved APR-2026-004812 (Level 1)
- 09:58 APR-2026-004755 escalated to Fatima Al Mansoori (SLA breached)
```

#### Permissions

- `listWorkflowInstanceProcess` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-373` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS30 Approval Workflows and Governance Board 1.dc.html#bo-373`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 1
- Flow F123 *Approval Workflows and Governance board 1: Approval Command Center Dashboard*, step 18: Works in Approval Activity & Notification Center → Provide a unified chronological feed of important approval events.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-373?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

### In P08 · Venue Operations

- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"decideApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/decide","contract":"approvals","summary":"Approve, reject, return or ask for information","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"escalateApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/escalate","contract":"approvals","summary":"Move it up a level","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"getApprovalAnalytics": {"method":"GET","path":"/approval-analytics","contract":"approvals","summary":"Volumes, times, rejections and bottlenecks","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ApprovalAnalytics"},
"getApprovalRequestScore": {"method":"GET","path":"/approval-requests/{approvalRequestId}/score","contract":"ai","summary":"The latest context score of an approval request","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiApprovalRequestScore"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaEscalationBottleneck": {"method":"GET","path":"/sla-escalation-bottleneck","contract":"approvals","summary":"SLA, Escalation & Bottleneck Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflow","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"escalationLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaEscalationReminder": {"method":"GET","path":"/sla-escalation-reminder","contract":"approvals","summary":"SLA, Escalation, Reminder & Timeout Rules","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SlaEscalationReminderTimeoutRulesView"},
"listWorkflowInstanceProcess": {"method":"GET","path":"/workflow-instance-process","contract":"approvals","summary":"Workflow Instance Monitor & Process Timeline","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflowInstance","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":"currentStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiApprovalRequestScore": {"type":"object","x-ticvai-persistence":"ai.approval_request_score","description":"**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).","required":["approvalRequestId","riskScore","riskBand","priorityScore","escalationSuggestion"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"approvalRequestId":{"type":"string","format":"uuid","x-ticvai-references":"approvals.request"},"trigger":{"type":"string","enum":["submitted","resubmitted","slaTick","escalated"]},"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"],"description":"Design 5.6: a risk score and band, never a probability."},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"description":"For ordering work in an inbox; higher first."},"escalationSuggestion":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}},"description":"A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."},"signals":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","description":"e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"scoredAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"ApprovalAnalytics": {"type":"object","x-ticvai-persistence":"none — aggregated from approvals.request","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string","description":"The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it.","enum":["kind","approver","venue","day","week"]},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"raised":{"type":"integer"},"approved":{"type":"integer"},"rejected":{"type":"integer"},"withdrawn":{"type":"integer"},"expired":{"type":"integer","description":"**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"},"escalated":{"type":"integer"},"slaBreached":{"type":"integer"},"medianMinutes":{"type":"number"},"p95Minutes":{"type":"number"}}}}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SlaEscalationBottleneckMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance, whose SLA and reminder timestamps it lists (data model for the agreed operations, 29 September)","description":"**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflow":{"type":"string","description":"Workflow"},"instance":{"type":"string","description":"Instance"},"currentStep":{"type":"string","description":"Current Step"},"owner":{"type":"string","description":"Owner"},"started":{"type":"string","format":"date-time","description":"Started"},"target":{"type":"string","format":"date-time","description":"SLA deadline"},"timeRemaining":{"type":"integer","description":"Minutes until breach; negative once breached"},"risk":{"type":"string","description":"Risk"},"escalationLevel":{"type":"string","description":"Escalation Level"},"firstReminder":{"type":"string","format":"date-time","description":"First Reminder"},"secondReminder":{"type":"string","format":"date-time","description":"Second Reminder"},"managerEscalation":{"type":"string","format":"date-time","description":"Manager Escalation"},"executiveEscalation":{"type":"string","format":"date-time","description":"Executive Escalation"},"finalOutcome":{"type":"string","description":"Final Outcome"}},"required":["instance"]},
"SlaEscalationBottleneckMonitorViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"withinSla":{"type":"integer","description":"Within SLA"},"atRisk":{"type":"integer","description":"At Risk"},"breached":{"type":"integer","description":"Breached"},"escalated":{"type":"integer","description":"Escalated"},"averageProcessingTime":{"type":"integer","description":"Minutes"},"averageApprovalTime":{"type":"integer","description":"Minutes"},"longestWaitingStep":{"type":"string","description":"Longest Waiting Step"}}},
"SlaEscalationReminderTimeoutRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.sla_policy (schema ApprovalSlaPolicy), including its reminder-percentage columns (data model for the agreed operations, 29 September)","description":"**What SLA, Escalation, Reminder & Timeout Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"code":{"type":"string","description":"Policy code, the same key setApprovalSlaPolicy upserts by"},"slaType":{"type":"string","enum":["responseSla","approvalSla","taskSla","resolutionSla","systemActionTimeout"],"description":"Which clock this policy governs"},"calendarBasis":{"type":"string","enum":["calendarHours","businessHours","workingDays","venueCalendar","holidayCalendar"],"description":"How elapsed time is counted"},"escalationActions":{"type":"array","items":{"type":"string","enum":["notify","reassign","escalate","addApprover","createTask","raisePriority","triggerBackupWorkflow"]},"description":"What happens on escalation"},"channelsType":{"type":"string","enum":["email","push","inApp","smsWhereAppropriate"],"description":"Vocabulary listed under Reminder Channels."},"targetMinutes":{"type":"integer","description":"SLA target in minutes"},"onBreach":{"type":"string","enum":["notifyOnly","escalate","autoApprove","autoReject"],"description":"Outcome at breach; auto outcomes only where explicitly permitted"},"autoActionAllowed":{"type":"boolean","description":"Auto-approve or auto-reject on breach is explicitly permitted; default false"},"firstReminderAtPercent":{"type":"integer","description":"Percent of target at which the first reminder goes"},"secondReminderAtPercent":{"type":"integer","description":"Percent of target at which the second reminder goes"},"escalateAtPercent":{"type":"integer","description":"Percent of target at which the request escalates"}},"required":["code"]},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"WorkflowInstanceMonitorProcessTimelineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance and approvals.workflow_step_execution (data model for the agreed operations, 29 September)","description":"**What Workflow Instance Monitor & Process Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowInstance":{"type":"string","description":"Workflow Instance"},"workflowName":{"type":"string","description":"Workflow Name"},"version":{"type":"string","description":"Version"},"sourceModule":{"type":"string","description":"Source Module"},"businessObject":{"type":"string","description":"Business Object"},"initiatedBy":{"type":"string","description":"Initiated By"},"startTime":{"type":"string","format":"date-time","description":"Start Time"},"currentStatus":{"type":"string","enum":["running","waitingApproval","waitingTask","waitingSystem","escalated","failed","completed","cancelled"],"description":"Current Status"},"currentStep":{"type":"string","description":"Current Step"},"sla":{"type":"string","description":"SLA"},"step":{"type":"string","description":"Step"},"type":{"type":"string","description":"Type"},"started":{"type":"string","format":"date-time","description":"Started"},"completed":{"type":"string","format":"date-time","description":"Completed"},"assignedTo":{"type":"string","description":"Assigned To"},"input":{"type":"string","description":"Input"},"output":{"type":"string","description":"Output"},"decision":{"type":"string","description":"Decision"},"duration":{"type":"integer","description":"Seconds"},"status":{"type":"string","description":"Status"},"ruleEvaluations":{"type":"integer","description":"Rule evaluations"},"assignments":{"type":"integer","description":"Assignments"},"approvals":{"type":"integer","description":"Approvals"},"rejections":{"type":"integer","description":"Rejections"},"escalations":{"type":"integer","description":"Escalations"},"notifications":{"type":"integer","description":"Notifications"},"apiCalls":{"type":"integer","description":"API calls"},"systemActions":{"type":"integer","description":"System actions"},"errors":{"type":"integer","description":"Errors"}},"required":["workflowInstance"]}
}
```
