# Parsing the packs nobody had parsed

> **Owner:** Chinmay · **Written:** 18 September 2026 · **Status:** in progress
>
> `sources/packs/` held 43 PDFs and only 19 had ever been through
> `tools/parse-workshop-pack.py`. **A pack becomes screens only if the parser is pointed at it**,
> and nothing ever pointed it at the other 24 — 1,955 pages.

---

## Why they were never parsed

The parser read `sources/workshop/` and nothing else. A document had to be *placed* there to be
read, and placement was manual. So the 2,172-page drafting backlog in
[pack-backlog-18-september.md](pack-backlog-18-september.md) had a cause underneath it: **nobody
declined to draft from these packs. The tooling never turned them into anything to draft from.**

Fixed with `--from DIR` and `--only SUBSTRING`, which read a pack where it lies. **Copying them
into `workshop/` is how the duplication started**, so that was not the fix.

## Three parser defects, each found by running it

**1 — the inline `Purpose:` form.** This family writes `Purpose: Executive and operational landing
screen.` The workshop family puts `Purpose` alone on a line with the prose beneath. Matched only by
the second form, the table-of-contents block never closed, ran to the last page, and every screen
parsed from its own index entry with an empty body. **The first run of `ACCREDITATION.pdf` reported
131 screens and 131 of them had no specification at all.**

**2 — inline labels must be a known section name.** Accepting any short `Word: value` line looked
correct and was not. Across the seventeen workshop packs it **invented 925 labels** out of table
cells and example rows — `Status: Active`, `Venue: Dubai`, `Remaining: 12` — while dissolving 275
real ones. **Total content was identical, so nothing failed**; the vocabulary simply became noise.
Caught only by diffing content rather than counts.

**3 — a partial run must merge.** The tool writes the whole file. `--only ACCREDITATION --apply`
would have replaced 1,110 screens with that document's 80 and printed a success line.

## The quality gate

**A title with no purpose and no sections is not a parsed screen, it is a line from a contents
list.** Four packs produce these in bulk, because their section vocabulary is not one the parser
knows yet. Kept, they become screens downstream with nothing behind them — counted, planned
against, and found hollow only by whoever tries to build them.

They are dropped and reported by document, so the gap is a worklist rather than a silent number.

## Result

| | screens |
|---|---|
| Before | 1,110 from 23 sources |
| After | **1,924 from 36 sources** |
| New | **814**, from 13 sources |
| Hollow records remaining | **0** |

Before the quality gate the same run produced 2,134 from 38 sources. **The extra 210 were titles
with no body** — the gate is the difference between 814 screens and 1,024 numbers.

**Zero drift on all 23 previously-parsed packs.** Nineteen of them were re-parsed from the
`sources/packs/` copy rather than the `workshop/` one and came out identical, which is a useful
incidental proof that the duplicated pairs really are the same document.

### Parsed well — full purpose and sections on every screen

```
129  Seat_Management_Venue_Mapping_Reference v1.0.pdf
120  Marketing_CRM_Configuration_Reference v1.0.pdf
100  Resource_Management_Configuration_Reference.pdf
100  Wallet_Configuration_Backend_Structure_v1.0.pdf
 80  ACCREDITATION.pdf                     ← 22 screens carry requirement-matrix ids
 80  Payment_Payment_Orchestration.pdf
 60  Upsell,CrossSellEngine.pdf
 40  AI_Governance_Reference.pdf           ← arrived 18 September
 30  AI_Configuration_Assistant_Reference.pdf
 20  AI_Forecasting_and_Predictive_Intelligence_Reference.pdf
```

### Accreditation carries something no workshop pack does

**Twenty-two of its eighty screens cite the requirement matrix directly** — `Key requirements:
12.1.8–12.1.15`, `12.1.38–12.1.42`, `12.1.1, 12.1.47`. Every other pack has to be traced to the
baseline by hand. **CF-21 calls accreditation the only blocked work left on the project**, and the
pack has been on disk since 8 September carrying its own traceability.

Reconciled against the document rather than trusted: 8 boards, 80 screens, ten per board, counted
from its headings.

## Still owed

**Four packs need their section vocabulary added** before they parse to anything. They yield screen
titles and no bodies:

| pack | titles dropped | kept |
|---|---|---|
| `TICVAI_Ticket_Types_Product_Configuration_Scope_of_Work_v1.0.pdf` | **120** | 0 — the whole pack |
| `Entitlement Lifecycle.pdf` | **20** | 0 — the whole pack |
| `Event_Management_Configuration_Backend_Structure_v1.0.pdf` | 58 | 33 |
| `TICVAI Finance Backend Structure Reference v1.0.pdf` | 12 | 2 |

`Ticket_Types` at 120 titles is the larger loss and the more tractable: it is a *Scope of Work*
document, so its headings are probably one substitution away from parsing like the rest.

**Nine packs parse to zero screens** — the parser finds no screen headings at all, so these use a
different structure again. Two are the largest undrafted packs in the package:

```
202pp  Retail_Backend_Structure_Module_Reference_v1.0.pdf
175pp  TICVAI_Inventory_and_Procurement_Backend_Structure_Sample v1.0.pdf
 17pp  Virtual_Queue.pdf
 13pp  Seat_Management_Dashboard_Screens_Reference.pdf
 12pp  Marketing_CRM_Dashboard_Screens v1.0.pdf
 11pp  TICVAI_Resource_Management_All_Screens v1.0.pdf
  8pp  TICVAI_FnB_POS_Visual_Reference_Revised.pdf
  6pp  TICVAI_POS_Frontline_Dashboard Screens Reference v1.0.pdf
  6pp  F&B Dashboard Screens v1.0.pdf
```

**The six small ones are dashboard-screen albums** — images of screens rather than specifications —
so zero is probably the right answer for them and they belong in `boards/`, not as parse input.
**Retail and Inventory are not**, at 202 and 175 pages of backend structure, and they are worth a
vocabulary probe of their own.

### Three parse ragged and need checking

`Event_Management` 91 screens across 9 boards · `Seat_Management_Venue_Mapping` 129 across 13 ·
`TICVAI Finance` 14 across 3. **Every well-formed pack is ten screens per board**, so these three
are either genuinely irregular or partly mis-parsed.

## Wired in — 19 September

`derive-pack-screens.py --apply` added **814 screens**. The package goes **1,629 → 2,443**.

| platform | was | now |
|---|---|---|
| P08 Venue Management — Back Office | 614 | **1,198** |
| P09 TICVAI Web — Platform Console | 446 | **676** |

**P08 and P09 now hold 77% of every screen in the package.** That is what the source material says
— these are configuration references and configuration is back-office work — but a back office of
1,198 screens is a navigation problem somebody has to answer, and it is worth answering before it
is built rather than after.

### The thirteen placements, and the three that were decided rather than derived

The placement table maps a module to one platform, a licensed module and a navigation section.
**For the 23 packs already placed by hand, `sources/packs-index.json` derives the same platforms
independently from the contracts** — including the splits, `Rental → P06,P08` and
`Subscription → P08,P09,P17`. The derivation agrees with every hand placement, which is why it can
be trusted where it fires. It cannot fire for these thirteen: they have no operations yet, so there
are no citations to follow.

Three were genuine decisions and are recorded as such:

**Accreditation goes to P08, not P11.** P11 is `audience: public` — landing page, registration
form, status tracking, badge. The pack's eight boards are every one a staff command centre. Putting
them on P11 would contradict its own declared audience. **Boards 3 and 4 overlap P11's existing
`ACC-006 Reviewer Queue` and `ACC-008 Credential Register`**, and that overlap is a reconciliation
item, not something placement should quietly settle. `accreditation` is already a `ModuleKey`, so
the domain was always meant to be licensable on its own.

**Payment orchestration is P09 and wallet is P08.** The line is who operates it: gateway
credentials, provider routing and settlement are platform-level, like Pricing and Sales Channel; a
wallet is a venue's own stored-value scheme its staff administer, like Access Control.

**Marketing CRM is P08.** Privacy and Waiver sit on P13 because they are content and policy the CMS
publishes. Campaigns, segments and journeys are worked by venue marketing staff.

### 1,291 pack screens carry no operation

**By design.** `derive-pack-screens.py` does not invent operations, and its docstring says why:
these screens imply roughly three thousand endpoints against 1,032 that exist, and *"authoring
three thousand endpoints from a PDF is not derivation, it is fabricating an API surface"*. The gap
is written to `docs/active/workshop-contract-gap.md` as named operations instead.

## Not yet done

`derive-pack-linkage.py` and the refresh chain. **`check-screens` must hold** — it fails a
guest-callable operation with no guest screen, and 814 new screens is the largest single change the
screen layer has taken.
