# Products module: first module through the new way of working (plan, 19 October 2026)

Status: plan only. Nothing built, sent or reassigned yet.

Inputs: MOM 16 October (ticketing configuration review, prepared by Chitrangi), MOM 19 October (module timelines), the
reviewed wireframe `Refactored TICVAI ticketing UI` (file dated 9 October: the version Allam reviewed on Friday, before his
feedback), Sprint 1 and 2 tickets with their pulled screen records, `rebuild-assessment-19-october.md`.

## What the wireframe is
- One file, `TICVAI Ticketing Product Configuration.html`: dashboard, product list, create options, and a 12-step product
  form (Basics, Ticket type and variants, Validity, Schedule and capacity, What's included, Who can buy, Groups and
  memberships, Add-ons and bundles, After-sale rules, Price/channels/delivery, Review and submit, Publishing and versions).
- It is keyed to the client's board numbers, 121 screens B1-S01 to B12-S10. None of these IDs are in our package; our
  back office (P08) has its own 1,663 generated screens. So this wireframe has never been mapped to our operations and tables.
- It is the start of the "one connected back-office wireframe" the client asked for on 19 October.

## What the 16 October MOM changes (13 decisions, all in the product module)
1. No "special products" category; one "All products" list with a filter by type.
2. Ticket types cut to six: open dated, dated (takes special day and multi-day), time slot (takes camp and recurring),
   pass and membership, voucher, add-on.
3. Categories and tags are user-defined master data, picked from a drop-down; tags are separate and drive promotions.
4. Venue scope leaves the Basics step; replaced by "who can sell": global, site, operating area (channel), workstation,
   role, user, each allow or deny. Admin rights can be limited per venue.
5. Product ID is system generated with a naming convention (convention still to agree); barcodes only for merchandise and
   F&B, generated when the supplier has none; ticket media IDs are made at sale.
6. Languages are configurable (any language code), not fixed English and Arabic.
7. Only the tabs for the selected ticket type are enabled.
8. Variants carry quantities (2 adults + 2 children), which decide how many credentials are issued and how entry counts.
9. Renewal is a flag under monthly or annual, not its own behaviour; validity starts from sale, a fixed date range, or
   first scan within a window.
10. Reservation owner and ticket owner come from a configurable field set (data mask: text, drop-down, radio, check box)
    linked to the product; a ticket owner only where the ticket needs one.
11. Events and performances get their own screens; capacity at event level, inherited by performances; the product only
    flags "requires performance selection". Time slots generated from start, end, interval, duration, entry window.
12. Creation options: blank, template, copy, then import (template only, check, preview, confirm) and AI last.
13. AI creation never skips a required question; "configure later" must be accepted and shows on the review screen.

Our package is far from these: it still has the nine old types (special day, camp, recurring in hundreds of files),
venue scope in 21 files, and no sale-permission, product-tag or performance-selection concept at all.

## Who is free if back-office frontend is held
Sprint 1 and 2 frontend tasks, split by whether the task's screen is client-approved:

| Person | Can still build | Held |
|---|---|---|
| Pallavi Sawant | 0 | 92 (moves to wireframes full time) |
| Pradnya Yeram | 13 (POS, guest app) | 71 |
| Chinmay Patkar | 52 (guest web and app) | 23 |
| Chitrangi Mestry | 40 (guest web and app) | 35 |
| Sanket Keluskar | 0 | 52 (also has 62 backend) |
| Surendra Loke | 0 | 50 (also has 9 backend) |
| "Surendra" (second PMS account?) | 0 | 21 |

Lead's ruling (19 October, evening):
- Pradnya, Chinmay Patkar and Chitrangi keep all their tasks, held ones included, and build them, not from our generated
  wireframes. Pradnya's tasks go to no one else: she manages POS and the guest app.
- "Surendra" and "Surendra Loke" are the same person (two PMS accounts; 71 tasks in all).
- Free for new work: Sanket and Surendra Loke.
- Pallavi's 92 held tasks are not reassigned: they stay held and are re-cut into module slices when each module is signed.
- No client plan e-mail from us: today's meeting already covered it.

## Plan by day
**Tue 20 (holiday): preparation, nothing goes out**
- Change list: each MOM decision mapped to the wireframe steps and screens it changes, for Pallavi.
- Mapping: the 121 board screens to our operations, fields and tables, and what in today's package each decision contradicts.
- Wave 1 task drafts (below), each run through the dry run.
- Blockers, steps 1 and 2 (below): recover the walk's findings and sort them.

**Wed 21**
- Pallavi applies the change list (with or without Claude Design in small batches) and starts events and performances.
- Review call with the client on the revised product screens.
- Wave 1 goes out to Sanket and Surendra Loke once it passes the dry run.

**Thu 22**
- Client feedback on products. Events and performances wireframe sent (the client's Thursday date).

**Fri 23 (before Chinmay travels on the 24th)**
- Products signed off (one-day buffer). Spec for the product module generated from the signed wireframe, dry-run gated.
- Wave 2 tickets out as one testable slice.

**Week of 26 October**
- Products built as a slice. Events and performances: feedback and sign-off. Seat assignment wireframe next.

## Wave 1: settled by the MOM, safe to start before sign-off
Database, backend and screen together, small group:
1. Categories master data (user-defined, used from the product drop-down).
2. Tags master data (shared with the POS tags; promotions by tag come later).
3. Languages: the venue's language list by code, and translatable product texts per channel.
4. Field sets (data masks): custom fields, linked to a product; reservation owner and ticket owner from them.
5. Sale permissions: who can sell, with allow and deny at each level; per-venue admin rights.
6. Back-office shell: which venue you are in, navigation, dashboard counts (active, draft, pending, approved), needs
   attention, "All products" with the type filter.

Not in wave 1: product ID convention (not agreed), barcode generation (retail module), the product form itself (wave 2).

## Wave 2: after sign-off
The product form for the six types, with type-driven tabs; variants with quantities; pass and membership rules; the
"requires performance selection" flag; creation options including import preview and AI with "configure later"; review,
approval and publishing. Delivered migrations change by forward migration only.

## Proposed group (to confirm)
- Sanket: categories, tags and field sets (backend and screens), and the sale-permission backend.
- Surendra Loke: back-office shell, dashboard, product list, languages and sale-permission screens.
- Hrushikant: the migrations for wave 1 and wave 2.

## Blockers the walk found: clear what stays, keep the rest as checklists
The walk (stopped at 488 of 881 Sprint 1 and 2 tickets) drafted 2,548 gaps. None were challenged yet (the pilot kept about
3 in 4). The texts are in the walk agents' transcripts, so nothing has to be walked again to recover them.

| Bucket | Tickets | Gaps | What we do |
|---|---|---|---|
| Stable backend: identity, approvals, foundation, tenancy, subscription, digital, orders, public, payments, wallet, admission | ~107 | ~580 | Clear now |
| Kept frontend (Pradnya, Chinmay Patkar, Chitrangi) | 90 | 477 | Clear now |
| Test, DevOps, AI, database, onboarding | 63 | 378 | Clear the ones on stable modules |
| Back-office configuration backend (venue setup, ticketing, seating) | 89 | 432 | Checklist for the module rebuild |
| Held frontend | 100 | 408 | Checklist for the module rebuild |
| White Label backend | 53 | 297 | Park until White Label is scheduled |

Steps:
1. Recover all 2,548 gap texts into one file with ticket, module, kind and evidence (script, no agents).
2. Sort them into the buckets above.
3. Group "clear now" by cause. The same few causes repeat (contradictions 29%, undefined rules 23%, screen promises with
   no API 12%), so fix each cause once at its source (one source of truth per fact, every promise a rule or a decision),
   not one change request per gap. Check each cause on a sample instead of three challengers per gap.
4. Ship the fixes in one release (r8, together with lane H's CR-170, 171 and 172 work), not a stream of small ones.
5. The 393 tickets never walked: walk only those on stable modules still being built, when the lead says so.

## Decisions needed
1. Who applies the MOM changes: Pallavi by hand from the change list, or Claude Design in small batches with Pallavi checking.
2. Start wave 1 before the client signs off (only MOM-settled items, some redo risk), or wait for Friday.
3. The group above.
4. r8 timing: before the lead travels on the 24th, or after (only the lead's session tags and deploys).

## Apps, platforms and wireframes (lead's answers, 19 October night)
| Client's app | Our platforms | State | Who |
|---|---|---|---|
| Guest Web | P01 | Client-approved | (built by Chinmay Patkar, Chitrangi) |
| Guest App | P02 | Client-approved, including the 20 we recorded as only designed | (building) |
| POS | P04 | Client-approved, including the 23 we recorded as only designed | Pradnya |
| Kitchen Display | P15 | To design and build | Pradnya |
| Kiosk | P05 | To design, from the approved guest web | Us (local) |
| Venue Management | P08 + CMS P13 + analytics P16 + support console P12 + accreditation | To design, module by module | Pallavi + Chinmay (local) |
| Employee App | P06 + scanner P07 (flying POS, ticket check) | After the main modules; client session first | Later |
| B2B | P10 | With the UAE Pass work | Later |
| TICVAI Portal (TICVAI staff for now) | P09 | With the UAE Pass work | Later |
| Developer Portal | P14 | With the UAE Pass work | Later |
| TICVAI main website | not in the package | With the UAE Pass work | Later |

Record fix (r8): the 20 guest app and 23 POS screens become client-verified (the client approved them).

### Venue Management by the client's modules and workshop boards (not our 1,663 generated screens)
The workshop boards are already in `handoff/design-batches/WS*` (195 boards, ~1,850 screen rows, each with a brief).
| Order | Module | Boards | Rows | Who |
|---|---|---|---|---|
| 1 | Products (ticketing product configuration, membership, groups, ticket media) | Pallavi's B1-B12 + WS43-44, WS27-30, WS59-61 | ~210 | Pallavi (Claude Design), MOM 16 Oct applied |
| 2 | Events and performances | WS125-133 | 35 | Pallavi |
| 3 | Seat assignment and venue mapping | WS165-177 | 128 | Local (first module, the pilot) |
| 4 | Pricing, promotions, bundles, upsell | WS34-40, WS45-54, WS180-185 | 229 | Local |
| 5 | Resource management | WS155-164 | 99 | Local |
| 6 | F&B, retail and inventory | WS134 + our F&B, retail, inventory boards | ~200 | Local |
| core | Admin, access control, approvals, rules, sales channels | WS01-20, WS55-58 | ~240 | Local, alongside |
| 7 | Finance: payments, wallet, finance | WS147-154, WS186-195, WS178-179 | ~180 | Local |
| 8 | CRM and marketing, communications, privacy | WS135-146, WS24, WS41-42 | ~150 | Local |
| later | Orders, resale, upgrades, games and rides, rentals, accreditation, customer service, CMS, analytics | the rest of WS | ~600 | Local |

Each module: wireframe sent, client feedback the next day, finalised the day after (19 Oct meeting).

### How the local modules are made
- Pallavi's file is the template: same shell, design system (Nocturne), shared demo data store, screen registry and
  rendering per board screen. Each module is added to the one back-office wireframe, so the client sees one connected file.
- Made with Claude Code (with the ui-ux-pro-max skill for design quality), one agent per board batch of about 10 screens,
  from the module's workshop-board briefs and the meeting decisions. Small batches, because big ones cut corners.
- Pallavi's own modules stay in Claude Design; local modules are separate module files built into the one file, so neither
  side overwrites the other. When Pallavi exports a new version, it becomes the shell.
- Checks before the client sees a module: every board row drawn, no spec text on screen, MOM rules applied, cross-screen
  effects work in the shared store. Pallavi checks each module for consistency with hers.

## In r8 (lead, 20 October 00:15: ships with r8, not after)
### Faster database tickets (ADAM backend setup)
Today a [DB] ticket's agent rebuilds every migration from an empty database, reasons about effects by itself, and runs
`dotnet build` plus the whole `dotnet test` suite, because the starter's general rule says so. Change:
1. Apply only the ticket's new file to a local template database at the previous state (`CREATE DATABASE t TEMPLATE base`),
   then a second run that must change nothing.
2. ADAM ships the expected end state of the ticket's tables (from the package) in the ticket folder; one command compares
   the database with it (columns, keys, indexes, row security). A match is the evidence.
3. No `dotnet build`/`dotnet test` on a ticket that touches no C#.
4. The full from-empty apply and the full suite run once a day or in the pipeline on each merge request.
5. Migration tickets grouped per module so one verification covers several tables.

### Client note: everything waiting on the client, each tied to its board
One note for the client after the merge: each item names the screen, the approved frame or workshop board it sits on
(`wireframe.board` / prototype `view` of the screen record, or the WS board), what we propose and what we build meanwhile.
Sources: list C of the r8 decision sheet (15), the screens lane's parked wording (lane-screens-pending-ui.json: GPS-C09,
GPS-C02, ORDERS-MONEY-C02, WHITE-C03, WHITE-C23, DEV-001), the "How many seats" stepper on GST-049 and WEB-007, the
GST-001 "Your upcoming tickets" list, and offline sign-in wording on tills and handhelds (turnstiles and scanners get it in r9).
Approved wording changes are applied with lane-screens-apply-pending.py plus an approved-ui-changes.yaml entry naming the approval.
