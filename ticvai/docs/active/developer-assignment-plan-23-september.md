# Developer tasks, assignment and timelines — plan (23 September)

Decided with Chinmay on 23 September. **OpenProject stays the only plan (CF-124).** This produces its
input, and any dates go into OpenProject through propose-then-confirm. This file never holds dates.

## Team and ownership

| Person | Owns | Stack |
|---|---|---|
| Pradnya Yeram | **POS** (P04). Eligible for Guest App — Mobile tasks when her load allows | React Native / React (4) |
| Chitrangi Mestry | **Guest App — Mobile** (P02), including all 5 and 8 point mobile screens | React Native (React 3) |
| Chinmay Patkar | **Guest App — Web** (P01), plus **Guest App — Mobile screens of 3 points or less**, to help Chitrangi (React Native rated 2) | React / Next.js (4) |
| Sanket Keluskar | **Guest App — Web** (P01) and **White Labelling CMS** (23 screens), taking it off Pradnya | React (4), .NET 3 |
| Pallavi Sawant | **Venue Management.** In this plan: **the Back Office setup screens** (the `APP-SETUP` epic, 39 screens, slice only). Also rotates as maker-checker | React / Next.js, Java |
| Hrushikant Patkar | **DevOps** (CI, database and migrations, environments) and .NET backend services | .NET 4, Docker/AWS/Azure 3 |
| Pranay Shinde | .NET backend services | .NET 4, SQL Server 4 |
| Tanmay Dukhande | .NET backend services | .NET 3, PostgreSQL 3 |
| Kalpita Mejari | AI. **Nothing assigned**; no AI work is in the first release | — |
| Deep Khanvilkar | **Easier backend tasks (1 and 2 points)** inside services owned by Hrushikant, Pranay and Tanmay, who review his work | .NET 2, PostgreSQL 2 |

**Reviews:** rotating peers in the same stack. ADAM already enforces that the tester is not the maker.

**Settled 23 September:** DevOps goes to Hrushikant. White Labelling went to Pradnya first, then to Sanket, with Chinmay Patkar sharing mobile, so the four frontend developers carry about 150 points each. The assignments are read from `docs/active/team.json`: edit that file and re-run `tools/build-service-docs.py`, not the task sheet.

**Matrix data issue:** Pallavi's React rating is 5 on a 0–4 scale.

**Later, not in this plan:** Pallavi moves on to Venue Management as a whole. What already exists there has to be checked before it is planned.

## Setup

`adam-connector-setup.zip` already gives each developer their environment: the .NET 10 clean-architecture skeleton or the Nx workspace (React Native apps and a web app), git, `CLAUDE.md`, role standards, and the ADAM connection with `/board`, `/ticket` and `/done`. The setup epic therefore covers:
- **One task per developer:** run `setup.cmd` and pass the connection test (1 point).
- **Shared tasks the zip does not cover:**
  - CI per repository
  - PostgreSQL and a migration runner that applies `backend/tenant/*.sql`. This is the first execution the DDL has ever had
  - **Seed data:** a demo venue with products, prices, events, tills, staff, roles and the UAE denominations. This lets POS and the guest apps be built and tested before Pallavi's setup screens exist
  - API client generation from `contracts/`
  - A working sign-in (Identity)
  - Logging and monitoring basics

## Complexity, not hours

Every task gets **1, 2, 3, 5 or 8 points**, computed from the spec by one formula:
- **Service task:** operations, fields, tables written, cross-service reads, and locks, offline or step-up behaviour.
- **Screen task:** operations called, components, states and navigation edges.

**Assignment rule:** 5 and 8 point tasks go only to someone rated 3 or 4 in that stack. 1 and 2 point tasks go to anyone in the stack. Load is balanced.

## Calibration fortnight

- Each developer gets about **15 points**, mixed 1/2/3/5, in their own area, from Setup and Wave 1. **No due dates.**
- Time is logged per task in OpenProject. ADAM's costing already reads those hours.
- From week 3, **hours per point per developer** comes from the actuals. Each estimate is points × that rate. A dependency-ordered schedule then proposes dates into OpenProject for confirmation. The rates are recalculated every fortnight.

## To build

1. A complexity scorer in `tools/build-service-docs.py`, adding a points column to `tasks.csv`.
2. The setup epic and the per-developer onboarding tasks.
3. An assignment pass: an assignee per task, from the table above plus the skills matrix.
4. Extend ADAM's OpenProject bridge to send the assignee. `create()` sends only the subject, description, type and parent today.
5. After the fortnight: a rates-and-schedule script that proposes dates, never writes them.

## Changes, 23 September (afternoon)

**Decided by Chinmay:**
- **Pallavi Sawant is full stack.** She starts Venue Management after her setup screens.
- **Venue Management epic.** It covers the wave 1-2 back-office screens whose every operation is agreed and specified (113 screens), with the backend they need beyond the first release (225 operations, 18 migrations). Provisional and wave-3 screens wait.
  - **First batch (15 points):** BO-100 Venue Home, BO-021 Order Search, BO-039 Shift Directory, BO-040 Variance Approval.
  - Nothing of Venue Management exists in code: `apps/backoffice` is an empty stub.
- **Her backend moves to the backend team.** The Venue Management backend (395 points) goes to each service's first-release owner, who reviews it.
- **Chinmay Patkar and Sanket Keluskar are full stack** and take easier backend tasks, as Deep does:
  - Sanket up to 3 points (.NET 3).
  - Chinmay up to 2 points (.NET 0, Node.js 4).
  - Deep stays at 2.
  - A task moves from its owner to a helper only while the helper's whole load, frontend included, stays below the owner's. Helper work is shared among the three.
- **Chronology.** Every task has a `sequence`: first release before Venue Management, then wave, then dependency depth, then database before backend before frontend. Every task also has a `queue`, its place in its assignee's own list. Screens are assigned in that order rather than largest first, so everyone moves through the waves together.
- **Frontend and backend are marked in OpenProject.** Every subject starts with [FE], [BE], [DB], [DevOps], [Onboarding] or [FE+BE], and `tasks.csv` has a `track` column.
- **Database migrations.** One per schema, in dependency order: the MIG epic, 30 tasks. Service tasks wait only for the migrations of the tables they use.

**Allocation after these changes (points):**

| Person | Points | Of which |
|---|---:|---|
| Pallavi Sawant | 482 | Venue Management screens 428, setup screens 53 |
| Hrushikant Patkar | 386 | backend 228, Venue Management backend 129, DevOps 28 |
| Tanmay Dukhande | 327 | backend 236, Venue Management backend 90 |
| Pranay Shinde | 324 | backend 256, Venue Management backend 67 |
| Sanket Keluskar | 278 | Web 77, White Labelling 73, backend 73, Venue Management backend 54 |
| Chinmay Patkar | 212 | Mobile 77, Web 75, backend 31, Venue Management backend 28 |
| Pradnya Yeram | 156 | POS 155 |
| Chitrangi Mestry | 153 | Mobile 152 |
| Deep Khanvilkar | 61 | backend 33, Venue Management backend 27 |

**Still open:**
- **Pallavi is at 482 points, all Venue Management screens.** It is a backlog, not a plan: at 15 points a fortnight it is over a year. Some screens could go to Pradnya and Chitrangi, who are at about 155.
- **Hrushikant is the heaviest backend developer** because he also carries DevOps.
- **Nothing is in OpenProject yet.**
  - TICVAI there holds only the 14 Greenleaf `test:` tickets: flat, with no versions and no categories.
  - The preview of the full tree is `handoff/service-docs/pms-preview.md`: 24 epics, 131 features and 640 tasks, with dependencies as *follows* relations.
  - Pushing waits for Chinmay.
  - Wave versions and Frontend/Backend categories would need a project admin.

## Changes, 23 September (evening)

**Decided by Chinmay:**
- **Sanket Keluskar joins Pallavi on the Venue Management screens.** Pallavi leads the epic, and screens go to whichever of the two is less loaded. Sanket keeps his backend helper tasks, up to 3 points each.
- **Sanket's Guest App web and White Labelling screens move** to Chinmay Patkar and Chitrangi Mestry.
- **The client Development Plan now has a section "Also built: parts of Venue Management".** It covers the 42 setup screens and the 113 wave 1-2 screens by area. There are no names or points in it.

**Allocation (points; backend includes database migrations; the last column is DevOps and onboarding):**

| Person | Frontend tasks | Frontend points | Backend tasks | Backend points | DevOps / onboarding | Total |
|---|---:|---:|---:|---:|---:|---:|
| Hrushikant Patkar | 0 | 0 | 63 | 357 | 29 | 386 |
| Pranay Shinde | 0 | 0 | 59 | 329 | 1 | 330 |
| Tanmay Dukhande | 0 | 0 | 63 | 329 | 1 | 330 |
| Sanket Keluskar | 48 | 183 | 40 | 119 | 1 | 303 |
| Pallavi Sawant | 107 | 298 | 0 | 0 | 1 | 299 |
| Chinmay Patkar | 69 | 217 | 37 | 59 | 1 | 277 |
| Chitrangi Mestry | 64 | 214 | 0 | 0 | 1 | 215 |
| Pradnya Yeram | 37 | 178 | 0 | 0 | 1 | 179 |
| Deep Khanvilkar | 0 | 0 | 37 | 59 | 1 | 60 |

Venue Management screens are shared between Pallavi and Sanket after his backend helper work is counted, so the two end level.

## Timeline decided, 23 September (night)

**Decided by Chinmay:**
- **Six months for everything.** The first 2 months are for the current Development Plan (Block A). The next 4 months are for the rest (Block B), in order of use. For now the focus is Block A.
- **The team codes with AI assistance.** Points stay as they are, because they measure size, not time. What changes is the pace: the calibration sprint measures it.
- **Kitchen Display is part of POS.** In `tools/derive-delivery-slice.py`, POS is P04 + P15. The first release is now 465 operations and POS has 40 screens.
- **Scanner: one app.** The flying scanner is the turnstile app with peripheral control off: it confirms entry but opens no turnstile. That is a setting, not separate screens.
- **The apps:**
  - Guest App (mobile, web, kiosk)
  - POS (with Kitchen Display)
  - Scanner (turnstile and flying)
  - Staff App
  - Venue Management (with White Labelling, Analytics and the Support console)
  - TICVAI main controller (Platform Console, Sign-up, Developer Portal)
- Suggested and not yet confirmed: the Partner portal goes in the Guest App family, and Accreditation splits into applicant and reviewer sides.

**Block A:**

| Month | Contents | Points |
|---|---|---:|
| 1 | Setup, POS Wave 1, Guest Web and Mobile Wave 1, first-release setup screens, and the backend they need | ~1,075 |
| 2 | POS Wave 2 with Kitchen Display, Guest Web and Mobile Waves 2-3, White Labelling, and the Venue Management parts | ~1,380 |

Block A needs roughly 65 points per person per sprint, about four times a hand-coded pace. That is also about 12 tickets a day across the team in month 1 and 19 in month 2.

**Fallback if Sprint 1 measures under about 60 points per person per sprint:** POS, Guest Web and Mobile Waves 1-2 and White Labelling stay in the 2 months, and the Venue Management parts move to month 3.

**Recommended and not yet applied:**
- Mock-first frontend.
- Backend levelling: DevOps off Hrushikant, Pallavi as a backend helper, Deep up to 3 points, Kalpita on the AI service.
- Pull the Scanner into Block A.

The Development Plan carries the two-month timeline in client terms, with no points.
