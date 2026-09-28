# TICVAI — build readiness

28 September 2026 · Chinmay Parab · follows the report of 21 September (`docs/reports/build-readiness-21-september.md`)

## Verdict

**The answer from 21 September stands: build the sale-and-entry path now, and not the back office.** Guest web, guest app, kiosk, POS, staff app, scanner and kitchen display are 99–100% ready. The back office is where it was, because it is waiting on the same thing: **577 operations nobody has agreed with the client.**

**What changed this week is the part of the package developers actually read.** Every Block A ticket was pulled the way a developer would pull it. That gave 9,976 findings, which were grouped into 293 root issues and checked against the source. The fixes then went into the connector, the starter, the ticket text and the package itself.

**A sample re-audit says the tooling fixes worked and the screen specifications still need work:**
- **Connector findings fell 52%, and starter findings 57%.**
- **Package findings fell 7%**, because what is left is mostly in screens.
- **Ticket-text findings rose 19%.** Screen tickets still have no acceptance criteria of their own.

|  | 21 Sep | 28 Sep |
| --- | --: | --: |
| Operations | 2,073 | 2,135 |
| Operations agreed and fully resolved | 1,429 | 1,494 |
| Operations not yet agreed (provisional) | 577 | 577 |
| Agreed operations with no lineage | 67 | 64 |
| Tables | 627 | 678 |
| Indexes | 734 | 1,468 |
| Screens naming an operation | 2,319 of 2,427 | 2,319 of 2,427 |
| Permission keys with no description | 72 | 70 |
| Conflicts open, blocking | 9, none | 9, none |
| Modules fully ready | — | 46 of 69 |

## What the audit changed

**Most of the growth in tables and operations is the audit's doing, and deliberately so.**
- **Tables (+51).** The fixes added tables that operations wrote to but no DDL created, such as `orders.refund_batch` and `orders.deposit_box_foreign_holding`, and foreign keys that were missing.
- **Indexes (doubled).** `910-indexes.sql` now indexes every foreign key.
- **Operations (+62).** They were added where screens called something that did not exist.
- **OpenProject.** The additions reached it on 28 September:
  - 2,701 ticket descriptions rewritten
  - 30 tickets retitled
  - one new migration ticket, `VM-MIG-ORDERS`
  - 38 new sub-tasks

**The re-audit sampled three tickets for each of the 269 root issues our fixes could have touched.** That was 294 tickets, and the table compares findings on those same tickets before and after.

| Owner | Findings before | After | Change | Roots gone / reduced / grew |
| --- | --: | --: | --: | --- |
| Connector (ADAM) | 666 | 322 | −52% | 8 / 9 / 5 |
| Starter (setup zip) | 586 | 250 | −57% | 3 / 7 / 2 |
| Package | 2,969 | 2,766 | −7% | 39 / 94 / 85 |
| Ticket generation | 368 | 437 | +19% | 1 / 11 / 12 |

**What is gone:**
- **Connector:** table-file paths that led nowhere (R004, 129 → 0), and a search that could not find operations (R005, 69 → 4).
- **Starter:**
  - app names the starter did not have (R249, 118 → 0)
  - standards documents describing a different codebase (R028, 73 → 4)
  - Done-when lines asking for tests the starter could not run (R027, 81 → 5)
- **Package:** list operations returning a bare array instead of a page (R076, 47 → 3), and guest operations demanding staff permissions (R072, 91 → 31).

**What grew is concentrated, and it tells us what to fix next.**
- **Screen specifications:**
  - generic UI states (R250, 94 → 137)
  - navigation guessed wrong (R251, 72 → 113)
  - data a screen needs that no operation supplies (R259, R275 and R280 together, 28 → 150)

  These screens were generated from names, not drawn. With the connector now showing developers the whole contract, the gaps are visible where before they were hidden.
- **Wireframes (R252, 109 → 198).** The drawn boards are back and linked, but no screen outside P01 has a frame in review, and none is client-verified.
- **Ticket text:**
  - screen tickets whose only acceptance line is "three sub-tasks" (R041, 62 → 111)
  - Done-when lines asking for 401/403 tests on operations that have no permission (R054, 11 → 48)
- **Expected until Setup lands:** predecessor tickets not in the repo (R050) and the empty api-client (R029). Both describe work not started, not a defect.

**Read the growth with one caution.** The new findings were matched to root issues by a fresh classifier, which assigns more generously than the grouping pass did. The direction is reliable; the exact counts are not.

## What 100% means

**A module is ready to build when all six of these hold.** The first two are what the 21 September score measured. The other four are what a developer hits on the day.

1. **Agreed:** every operation it calls is agreed, not provisional.
2. **Resolved:** every operation names the tables it reads and writes.
3. **Specified:** every screen names at least one operation.
4. **Permitted:** every permission key it checks has a description, so the grant screen can show it.
5. **Drawn:** every screen has a client-verified wireframe.
6. **Clean:** no open audit root issue on its tickets.

**No module meets all six today, because none has a client-verified wireframe.** On the first three, 46 of 69 modules are complete.

## What each platform needs

| Code | Platform | Ready | Not agreed | No lineage | Screens with no operation | Needs |
| --- | --- | --: | --: | --: | --: | --- |
| P09 | TICVAI Web | 44% | 282 | 12 | 88 | 2 client sessions and 1 scoping decision; lineage (us) |
| P13 | Venue CMS | 64% | 39 | 5 | 0 | 1 client session; `assets` lineage (us) |
| P12 | Venue Support | 65% | 19 | 0 | 0 | 1 client session |
| P08 | Venue Management | 72% | 269 | 37 | 10 | 1 client session (access); lineage and 10 screens (us) |
| P10 | Partner Web | 77% | 30 | 1 | 0 | 1 client session, with the commercial side |
| P17 | TICVAI Sign-up | 79% | 2 | 1 | 0 | closes with P09 and P10 |
| P16 | Venue Analytics | 91% | 2 | 3 | 1 | `reporting` lineage (us) |
| P04 | Venue POS | 99% | 1 | 0 | 0 | one `access` operation agreed |
| P06 | Venue Staff App | 99% | 0 | 2 | 2 | 2 `rental` lineages and 2 screens (us) |
| P01, P02, P05, P07, P11, P14, P15 | the rest | 100% | 0 | 0 | 7 | wireframes; P11's 4 screens |

**P13 fell from 68% to 64%.** The audit rewired its screens, so it calls 123 operations instead of 140, and five `assets` operations it now calls have no lineage. The client-side gap is unchanged.

### P09 TICVAI Web — 44%

- **Not agreed (282):**
  - `catalogue` 108
  - `promotions` 96
  - `orders` 42
  - `approvals` 20
  - `marketing-crm` 11
  - `subscription` 5
- **Client:**
  - a pricing and promotions session
  - a resale and approvals-engine session
  - **a scoping decision on the AI configuration assistant, forecasting and AI governance.** 67 of the 88 screens with no operation belong to them. If they are in this delivery, they need contracts written from scratch.
- **Us:** lineage for 12 operations (`payments` 6, `promotions` 3, `subscription` 3).

### P08 Venue Management — 72%

- **Not agreed (269):**
  - `access` 146
  - `orders` 49
  - `marketing-crm` 35
  - `subscription` 20
  - `catalogue` 9
  - `promotions` 6
- **Client:** the access control session. It is still the highest-leverage meeting on the list, and on its own it takes P08 to about 86%.
- **Us:**
  - lineage for 37 operations (`seating` 5, `rental` 5, `resources` 4, `games` 4 and others)
  - specifying the 10 screens that name no operation, all in Rentals

### P13 Venue CMS — 64%

- **Not agreed:** 39, all `marketing-crm`, from the consent, waiver and privacy packs.
- **Client:** one session on consent and waivers, taken together with **CF-127** (cookie consent) and **CF-165** (retention).
- **Us:** lineage for 5 `assets` operations (Media Library).

### P12 Venue Support — 65%

- **Not agreed:** 19, all `marketing-crm`, from the Customer Service pack.
- **Client:** taken in the consent and customer-service session (4). It is the smallest gap on the list.

### P10 Partner Web — 77%

- **Not agreed:** 30, all `subscription`, from the B2B, Reseller & OTA Partner pack. It is the whole of the Partners module, which stands at 0%.
- **Client:** one session on reseller credit terms and OTA allocation, with the commercial side present.
- **Us:** lineage for 1 `seating` operation.

### P16, P17, P04 and P06 — 79–99%

- **Mostly ours:**
  - lineage for 3 `reporting`, 2 `rental` and 1 `subscription` operation
  - 3 screens with no operation (1 on P16, 2 on P06)
- **Client:** P04's one `access` operation and P17's two provisional ones are agreed in the access and partner sessions above.

## The modules below 100%

**23 of 69 modules are not complete on the first three tests.** Five are the back office almost entirely:

| Module | Platforms | Ready | Not agreed | No lineage | Screens with no operation |
| --- | --- | --: | --: | --: | --: |
| Partners | P10 | 0% | 30 | 0 | 0 |
| Policy | P13 | 2% | 39 | 0 | 0 |
| Catalogue | P09 | 10% | 18 | 0 | 0 |
| Commercial | P09 | 24% | 230 | 9 | 1 |
| Platform | P09 | 34% | 35 | 0 | 67 |
| Support | P01, P02, P10, P12 | 41% | 19 | 0 | 0 |
| Access & Venue | P08 | 57% | 155 | 9 | 0 |
| Engagement & Support | P01, P02, P08 | 70% | 40 | 4 | 0 |
| Onboarding & Assessment | P17 | 75% | 1 | 0 | 0 |
| Package Builder | P17 | 80% | 0 | 1 | 0 |
| Orders & Money | P08 | 82% | 29 | 5 | 0 |
| Media Library | P13 | 83% | 0 | 5 | 0 |
| Purchase & Activation | P17 | 83% | 1 | 0 | 0 |
| Sell | P04, P05, P08 | 83% | 41 | 4 | 2 |
| Games & Rides | P08 | 86% | 3 | 4 | 0 |
| Rentals | P06, P08 | 87% | 6 | 15 | 10 |
| Tenants & Licensing | P09 | 88% | 5 | 3 | 0 |
| Analytics | P09, P16 | 91% | 2 | 3 | 21 |
| Venue Operations | P08 | 96% | 4 | 0 | 0 |
| Booking & Quotes | P10 | 97% | 0 | 1 | 0 |
| Operations | P06, P08 | 99% | 0 | 1 | 2 |
| Applicant Journey | P11 | 100% | 0 | 0 | 4 |
| System States | P01, P02 | 100% | 0 | 0 | 1 |

**Support spans P01, P02, P10 and P12.** Its 19 provisional operations are the Customer Service pack that P12 waits on, so it closes with session 4.

## The work to reach 100%

### From the client: five sessions and one decision

**Every provisional operation sits behind one of these six.** Each provisional operation cites the client pack and page it was drafted from.

| # | Session | Unblocks | Operations |
| --: | --- | --- | --: |
| 1 | Access control, with ticket media and credentials | P08, P04 | 147 |
| 2 | Pricing and promotions | P09 | 204 |
| 3 | Resale, orders and the approvals engine | P09, P08 | 111 |
| 4 | Consent, waivers, privacy and customer service, with CF-127 and CF-165 | P13, P12, P08 | 93 |
| 5 | Partner, reseller and membership terms, with the commercial side | P10, P17, P08 | 52 |
| 6 | **Decision:** are the AI configuration assistant, forecasting and AI governance in this delivery? | P09 | 67 screens |

Also for the client:
- **The audit's question pack:** 77 questions in `TICVAI_Client_Questions_Audit_2026-09-28.xlsx`. It includes the two state-model decisions the audit left open: whether cancelled media can be restored, and whether an expired subscription can be reactivated.
- **Wireframe verification:** POS first, then the guest app and web.

### From us, in the order it blocks something

1. **Screen tickets need acceptance criteria of their own** (R041). Every [FE] ticket should say what done looks like for that screen: its states, what it shows and what it calls. Today it says "three sub-tasks". This is the largest ticket-text finding and it is ours alone.
2. **Screens need the data their operations do not supply** (R259, R275, R280). Either add the lookup operations, or take the field off the screen. One decision per screen, about 150 findings.
3. **Screen states and navigation** (R250, R251). Generated from names, they read as boilerplate and guess exits wrong. Fix them screen by screen as each wireframe is verified, rather than twice.
4. **Lineage for 64 agreed operations.** The contracts are agreed; the tables they touch are not named.
5. **70 permission descriptions**, one line each. Until then the grant screen shows bare keys.
6. **The 4 tables described but not created:** `identity.session`, `identity.guest_session`, `inventory.stock_level`, `reporting.report_field`. Open since 21 September.
7. **The five ADR-0047 retention operations:** `eraseSubject`, archive, restore, the retention policy model and the expiry listing. Decided and still not written.
8. **Done-when lines that ask for 401/403 tests on operations with no permission** (R054). Generate the line from the operation's actual security.
9. **Specify the 108 screens that name no operation.** 67 are P09's Platform module: the AI assistant, forecasting and AI governance. They wait for decision 6. The rest are ours now.

### What is not a gap

- **Predecessor tickets missing from the repo** (R050) and **the empty api-client** (R029) describe Setup work that has not started. They go away as Block A is built.
- **282 operations no screen names.** Sync, webhook and job operations have none by design. This is a list to read, not a number to drive to zero.

## Where to start

**Unchanged: P01, P02, P04, P05, P06, P07 and P15.** Everything under them is agreed and resolved, and the connector and starter a developer uses to build them are now fixed. What they are missing is a wireframe a developer can trust, not a contract. **Guest [FE] tickets build the logic now and take the layout from the verified frame when it arrives.**

**Do not start with P09.** It is 44% ready, and a third of its screens wait on a scoping decision.

*Every figure here is read from `handoff/package-report.json` and `handoff/TICVAI_Build_Readiness.xlsx`, as refreshed on 28 September. The audit figures come from the re-audit sample's `compare.json`.*
