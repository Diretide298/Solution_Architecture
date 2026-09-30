# How the Block A tickets are structured, ordered and linked, and how new tickets join them

> **For:** Chinmay and the leads · **Date:** 30 September 2026
> **The live map of every link** is `TICKET-LINKS.md` in this folder (generated on every refresh). This page is
> the rules behind it and the procedure for new tickets.

## 1. The shape of a ticket

| Level | What it is | Example | Count now |
|---|---|---|---:|
| Epic | One service's first-release slice, one app's screens, or one platform area | `SVC-ORDER` OrderService: first-release slice | 27 |
| Feature | A group inside the epic: a service's operation group, a screen module | `SVC-ORDER-PAYMENT` | 164 |
| Task | The unit a person is assigned, sized in points, with a build order | `SVC-ORDER-PAYMENT-1` (up to 4 operations) | 870 |
| Sub-task | The steps inside a task, made when the task is pushed | see below | about 2,800 |

Sub-tasks are made by `tools/push-openproject.py`, never by hand:

- **Backend task:** one sub-task per operation (`[BE] createPayment: POST /payments`): 950.
- **Database task:** one per table (`[DB] orders.sales_order`): 548.
- **Screen task:** three: *build with all states* (against the mock API), *connect to API*, *tests*: 1,296.

Every task description carries, near its end: **Build order #n** (its place in the plan), **Planned: Block A
week n**, its **checker** for that week, and **Follows:** (the tasks it waits on). The OpenProject field
**Priority_No.** holds the same build order as a number, and the version **Block A · Week n** holds the week.

## 2. The build order

`tools/build-service-docs.py` gives every task a number, in this order of keys:

1. **Phase:** the first release before Venue Management.
2. **Wave:** 1 before 2 before 3.
3. **Step:** how many tasks stand in front of it along its longest chain of waits.
4. **Track:** setup, then database, then backend and AI, then screens.

Each person's **queue** is the same order restricted to their own tasks, so a board read top to bottom is the order
to work in. ADAM's board shows it that way since 30 September: started work first, then build order, the same every
time.

## 3. The links (who waits on whom)

A link is a hard "cannot be finished before". It becomes a **follows** relation in OpenProject.

| Rule | Since |
|---|---|
| Setup: CI and environments first; the database, hosts and Qdrant after them; every migration after the database | 23 Sep |
| Every migration after the migration baseline; a migration after the schemas its keys point into | 23 Sep |
| A service task after the migrations of the tables it reads and writes | 23 Sep |
| A screen task after the typed API clients (SETUP-CLIENTS) and the service tasks for the operations it calls. For screens this is **soft**: the screen is built against the mock API and only *connected* once the service lands | 23 Sep, soft 30 Sep |
| **Every service task after the platform kernel** (tenant routing, scope, auth) | 30 Sep |
| **A service task that writes after idempotency; one that publishes events after the outbox** | 30 Sep |
| **A read-only service task after the tasks that write what it reads** (reports, dashboards, exports) | 30 Sep |
| **A report that produces figures after every task that writes orders, money, catalogue, admissions, food and drink, stock, retail and wallets** | 30 Sep |
| AI engine: gateway after CI and environments; Qdrant work after the Qdrant cluster; the rest after the gateway | 30 Sep |

**Hard and soft, in the schedule** (decided 30 September). Every link above is a follows link in OpenProject: a
ticket is never *finished* before what it waits on. For *starting*, the Block A schedule
(`tools/derive-block-a-schedule.py`) treats some waits as soft, so nobody sits idle behind a finished interface:

| Wait | Start | Finish |
|---|---|---|
| A screen on its services | any time, against the mock server | after the services land |
| A service on the platform kernel, idempotency, the outbox | from day 3, against the interfaces published in week 1 | after the platform task |
| The kernel on sign-in setup | any time | after sign-in setup |
| A read-only or report task on the services whose data it reads | any time, against seeded data | after those services |
| Setup, migrations, the AI engine's setup | after them | after them |

A person whose next ticket is still waiting takes their next ticket that is ready, as ADAM's board shows it.

Links a longer chain already implies (A waits on C when A waits on B and B on C) are not sent to OpenProject: the
order is the same and OpenProject 10 is slow with large graphs.

## 4. The order of services: before and after 30 September

Until 30 September the build order had no rule putting one service before another beyond the links above, and most
services do not link to each other. So a service's first task came up by wave and chain length alone:

| Build order starts | Service | Phase in the proposal below |
|---|---|---|
| #171, #179 | Tenancy, Identity | 1 Foundation |
| #183 to #207 | Platform, VenueOps, Reporting, WhiteLabel, AI | 5, 3, 5, 5, 4 |
| #239 to #363 | Wallet, Catalogue, Ledger, Inventory, Order, Access | 2 Commerce (Inventory 3) |
| #378 to #507 | Marketing, F&B, Retail | 4, 3, 3 |

That puts reporting, white label and AI ahead of the sale path, against the 23 October checkpoint (one web purchase
end to end).

**Decided 30 September (Chinmay): the services are built in phases, from Block A to the end of the six months,**
following the package's own reasoning. White label and platform control sit in phase 1 because Block A's
storefront screens and tenant provisioning need them; reporting is last because it reports on everything else:

| Phase | Services | Why |
|---|---|---|
| 0 Plumbing | setup, platform kernel, auth, migration runner | Nothing runs without a scope (row-level security reads it on every connection) |
| 1 Foundation | Tenancy, Identity, Platform (control), WhiteLabel | Everything reads them; Block A's storefront and provisioning need the last two |
| 2 Commerce | Catalogue, Order, Ledger, Access, Wallet | The sale path; order, payment, entitlement and ledger commit in one transaction (ADR-0055) |
| 3 Operations | VenueOps, F&B, Inventory, Retail | Licensed per module; they plug in after commerce |
| 4 Engagement | Marketing, AI | Nothing that takes money depends on them |
| 5 Reporting | Reporting, CrossRegion | They report on, and replicate, everything else |

How it works: in the tickets (`build-service-docs.py`), the phase is a sort key after the release and before the
wave, applied as an ordered topological sort, so a task never comes before anything it waits on. A screen task
takes the phase of the service it calls most; the extras it also touches connect as their service lands. After
Block A (`build-plan-deck.py`), every module has the same phase and B1 to B3 work runs in that order.

## 5. New tickets: how they join the tickets already in OpenProject

2,862 tickets are in OpenProject (project 153). The plan now has 286 keys that are not, plus sub-tasks, and today's
rules add links and change build-order numbers for tickets that are already there. The procedure, in order; nothing
reaches OpenProject before Chinmay's go on the review workbook.

| Step | What happens | Tool | Status |
|---|---|---|---|
| 1 | Regenerate the plan: tasks, build order, links, schedule | `tools/refresh.sh` | ready |
| 2 | Review workbook: rewrites, retitles, new tickets, tickets leaving the plan | `op-descriptions.py`, `push-openproject.py --export`, `op-review.py` | ready |
| 3 | **Chinmay's go** | | waiting |
| 4 | Make the new tickets under their parents, with assignee, accountable, week version and Priority_No. | `op-create.rb` on the server, then `op-created-merge.py` into `pms-map.json` | ready |
| 5 | Rewrite descriptions and titles of tickets not started; a comment with the new text on started ones | `op-descriptions.rb MODE=status` on the server | ready |
| 6 | **Renumber Priority_No. on every ticket** to the new build order (a number, not content, so started tickets get it too) | `op-order-sync.py` here, `op-order-sync.rb` on the server | ready (30 Sep) |
| 7 | **Remove the links the plan no longer has, then add the new ones.** Only direct links between two plan tasks whose order the plan no longer has, even through a chain; every removal is listed in the dry run | `op-order-sync.rb` removes (same run as step 6); `op-bulk-links.py` + `op-bulk-links.rb` add | ready (30 Sep) |
| 8 | Move tickets that left the plan out of it, with the reason as a comment | `op-retire.py` | ready |
| 9 | ADAM links for the new tickets (contract, tables, screens on every pull) | `adam-links.py`, `load_links.py` on the ADAM server | ready |
| 10 | ADAM's board reads the build order from **Priority_No.** (found by name in the project's schema), falling back to the description, so a started ticket still sorts by the new order | ADAM, live after the deploy | ready (30 Sep) |
| 11 | Re-audit a sample by pulling tickets as a developer would | audit kit | after 4-10 |

Steps 6, 7 and 10 were the gaps until 30 September: without them, tickets already in OpenProject kept yesterday's
order numbers next to new tickets numbered today, and links the plan dropped stayed in place.

## 6. Keeping it right for the next change

- Change the plan only through its inputs (`docs/active/team.json`, `docs/active/block-a-extra-tasks.json`, the
  screens and contracts) and run `tools/refresh.sh`. Never edit `tasks.csv` or ticket order by hand.
- `TICKET-LINKS.md` shows the result; its last section must only list setup and onboarding.
- Push only through the steps in section 5, dry run first, database backup first
  (`OPENPROJECT-PUSH.md` has the server commands).
