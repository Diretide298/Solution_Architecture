# The pack backlog — what is sitting unread

> **Owner:** Chinmay · **Written:** 18 September 2026 · **Status:** live count, re-run it after any intake
>
> Re-measures the 8 September audit in `sources/packs/README.md` against the current package.
> **The gap has grown**, because three AI packs arrived on 18 September and nothing was drafted from
> the previous twenty-five either.

---

## The count

| | 8 Sept | before today | **18 Sept** |
|---|---|---|---|
| Packs held | **40** | 42 | **45** |
| Packs with at least one operation drafted | 17 | 17 | **17** |
| **Packs with nothing drafted** | **23** | 25 | **28** |
| Undrafted pages | — | 1,948 | **2,172** |

### `sources/packs/README.md` says 44, and there were never 44

Counted from git rather than from the prose:

```
a387a7a  8 Sept   40 packs   ← README written in this commit, claiming 44
78d71ba           42 packs   ← +Approval_Workflows, +Unified_BI
687bc44  18 Sept  45 packs   ← +3 AI packs
```

**The README overstated by four on the day it was written**, and its derived figures inherit the
error: *"17 of 44"* and *"27 of the 44 have no operation drafted"* should have read **17 of 40** and
**23 of 40**. The arithmetic is self-consistent against a number that was wrong.

**This document repeated it** — an earlier revision showed *44 → 45*, implying one net pack arrived
when three did. **Three docs in, three packs up, 42 → 45.** Count the directory, never the prose.

**584 provisional operations cite 17 packs. Twenty-eight packs are cited by nothing.**

Seventeen packs carried the whole drafting effort and the other twenty-eight have never been opened
by anyone writing a contract. **This is CF-164 and CF-125 seen from the source side.**

**The seventeen have not grown since 8 September.** Every pack added since — five of them — went
straight onto the undrafted pile.

## Nothing has been lost, it is just scattered

The client's OneDrive export holds **53 design books, and all 53 are in `sources/`.** None is
missing. They are spread across five directories, which is why a count of `packs/` alone understates
what we hold:

| directory | client design books |
|---|---|
| `sources/packs/` | 43 |
| `sources/boards/` | 7 |
| `sources/workshop/` | 4 — DAM, Game_and_Ride, Rental_Management, Subscription_Licensing |
| `sources/designs/` | 2 — Employee App UI, White Label Guest App UI |
| `sources/requirements/` | 1 — Ticketing Platform Native Dashboard |

**Eight design books sit outside `packs/` and are therefore invisible to the pack audit.** Four of
them — DAM, Game and Ride, Rental Management, Subscription and Licensing — are full reference books
with MoMs against them, filed as workshop material. **Worth deciding whether they belong in
`packs/`**, because as it stands no audit counts them either way.

## Arrived 18 September — the AI workshop

`Downloads/TICVAI_-_AI_Governance,_Config_Asst_&_Forecasting_-_Workshop.zip` held three packs, all
now in `sources/packs/`:

| pack | pages |
|---|---|
| `AI_Governance_Reference.pdf` | 105 |
| `AI_Configuration_Assistant_Reference.pdf` | 63 |
| `AI_Forecasting_and_Predictive_Intelligence_Reference.pdf` | 56 |

**224 pages of AI material and not one MoM against it.** `sources/mom/` holds 26 minutes covering
every other workshop from 28 July to 15 September; **there is no AI workshop MoM**. The two packs
were supplied directly rather than through a OneDrive export, which is why the usual pairing is
missing. **Ask for it** — the other packs were all read alongside their minutes, and the minutes are
where the decisions live.

## The undrafted 28, largest first

```
202pp  Retail_Backend_Structure_Module_Reference_v1.0.pdf
190pp  Payment_Payment_Orchestration.pdf
183pp  Upsell,CrossSellEngine.pdf
175pp  TICVAI_Inventory_and_Procurement_Backend_Structure_Sample v1.0.pdf
169pp  Resource_Management_Configuration_Reference.pdf
136pp  Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf
130pp  F&B_Backend_Structure_Module Sample Reference v1.0.pdf
129pp  Wallet_Configuration_Backend_Structure_v1.0.pdf
123pp  TICVAI Finance Backend Structure Reference v1.0.pdf
105pp  AI_Governance_Reference.pdf                          ← new
 91pp  Event_Management_Configuration_Backend_Structure_v1.0.pdf
 81pp  Approval_Workflows_and_Governance_Reference.pdf
 74pp  ACCREDITATION.pdf                                    ← CF-21
 63pp  AI_Configuration_Assistant_Reference.pdf              ← new
 61pp  Marketing_CRM_Configuration_Reference v1.0.pdf
 57pp  Seat_Management_Venue_Mapping_Reference v1.0.pdf
 56pp  AI_Forecasting_and_Predictive_Intelligence_Reference.pdf  ← new
 46pp  TICVAI_Ticket_Types_Product_Configuration_Scope_of_Work_v1.0.pdf
 28pp  Entitlement Lifecycle.pdf
 17pp  Virtual_Queue.pdf
 13pp  Seat_Management_Dashboard_Screens_Reference.pdf
 12pp  Marketing_CRM_Dashboard_Screens v1.0.pdf
 11pp  TICVAI_Resource_Management_All_Screens v1.0.pdf
  8pp  TICVAI_FnB_POS_Visual_Reference_Revised.pdf
  6pp  TICVAI_POS_Frontline_Dashboard Screens Reference v1.0.pdf
  6pp  F&B Dashboard Screens v1.0.pdf
```

Plus `Sample - Technical Product Sheet.xlsx` and `TICVAI_Ticketing_Configuration_Reference v1.0.jpeg`,
which are not PDFs and carry no page count.

## The 17 that were drafted from

```
116  Access Control Module_Reference
 96  Promotions & Bundles Management
 70  Pricing & Revenue Management
 30  B2B, Reseller & OTA Partner Management
 30  Ticket Resale Marketplace
 30  Ticket Media & Credential Management
 29  Order & Reservation Management
 20  Group Sales & Corporate Booking · Membership & Annual Pass · Rules/Workflow/Approval ·
     Sales Channel Management · Waiver, Consent & Digital Form
 19  Customer Service · Privacy, Consent & Preference Management
 18  Product Lifecycle & Catalogue Governance
 10  Communication & Notification Platform Services · Ticket Upgrade, Exchange & Conversion
```

## Where to start, and why

**`ACCREDITATION.pdf`, 74 pages.** CF-21 calls accreditation *"the only blocked work left on the
project"* — 58 requirements, no contract, a workshop still owed. **It has been sitting in
`sources/packs/` since 8 September, unread.** It pairs with
`sources/mom/TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue.docx`, also on disk, and
with the six accreditation tables the developer team turned out to have already modelled
(`access.accreditation` at 29 columns — see
[change-log-validation-18-september.md](change-log-validation-18-september.md)).

**Three independent sources on the same domain, all held, none reconciled.** That is the cheapest
blocked thing on the project to unblock.

`Virtual_Queue.pdf` at 17 pages is the same MoM's other half and is nearly free to do alongside it.
