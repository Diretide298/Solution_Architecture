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

## Not yet done

The new screens exist in `sources/workshop/pack.json` and **are not wired into anything**.
`derive-pack-screens.py`, `derive-pack-linkage.py` and the refresh chain still have to run, and
1,024 new screens against a package of 1,110 is a large enough jump to look at the diff before
publishing it.
