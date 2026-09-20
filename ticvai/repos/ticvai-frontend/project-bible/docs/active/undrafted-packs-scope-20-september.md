# The 26 undrafted packs — what is in them and what they would cost

> **Owner:** Chinmay · **Written:** 20 September 2026 · **Status:** scoping only. Nothing here was drafted.
>
> Answers the larger half of **CF-171**: 17 packs carry 577 provisional operations and the other 26
> carry none. This measures the 26 rather than estimating them.

---

## The four numbers

| | |
|---|---:|
| Packs scoped | **26** |
| Pages, measured with `pypdf` | **2,172** |
| Boards found | **148** |
| Screens found | **1,475** |
| Screens an existing operation already serves | **837** |
| **Estimated new operations** | **638** |

**CF-171 says 1,323 undrafted pages and the real figure is 2,172.** Every page count in
`sources/packs-index.json` is correct — all 43 agree with a fresh `pypdf` read, page for page — so
the error is in the row's arithmetic, not in the index. The drafted side of its comparison, 1,058
pages, is right.

### How the operation estimate is derived

**`draft-pack-operations.py` writes exactly one operation per unserved screen.** Its own docstring
records the ratio: 590 pack screens, 13 matched to operations that already existed, **577 drafted**
— and 577 is what the contracts cite today (`([A-Z][^\n]{6,70}?),\s*page\s+\d+` over
`contracts/*/*.yaml` returns 577 citations across exactly 17 distinct packs).

So **estimated new operations = measured screens − screens an existing operation already serves**.
Screens served is read from the `apis` list on each screen in `screens/P*.yaml` whose
`source.pack` names the pack.

**584 operations carry `x-ticvai-provisional: true` and only 577 cite a pack.** Seven provisional
operations name no origin. Small, but it means the citation count and the provisional count are not
interchangeable.

---

## `drafted: false` does not mean unserved, and that is the finding

**`index-packs.py` sets `drafted` from whether any operation cites `<pack>, page N`** — line 294,
`"drafted": bool(ops)`, fed by `signal_a()`. Only operations that `draft-pack-operations.py` wrote
carry that citation. **A pack whose screens were specified by hand therefore reports as undrafted.**

`ACCREDITATION.pdf` is the clearest case: **79 declared screens, 79 of them served, 43 distinct
operations, `accreditation` owning 69 of the bindings** — and `drafted: false`. The same holds for
Approval Workflows, Marketing CRM Configuration, Seat Management Venue Mapping, Wallet
Configuration and Upsell/Cross-Sell.

**The 26 are not one pile.** They are four:

| | packs | screens | est. new ops |
|---|---:|---:|---:|
| Already specified by hand — fuller wording of what exists | 7 | 649 | **4** |
| Renders of boards specified in another pack on this list | 6 | — | **0** |
| Existing contract, real remainder still unspecified | 9 | 699 | **527** |
| Genuinely new scope | 4 | 127 | **107** |

---

## 1 · Already specified — 7 packs, 4 operations outstanding

These were read and built against without `draft-pack-operations.py` touching them. **Opening them
to draft would duplicate work already done.**

| pack | pages | boards | screens | served | contracts touched | est. new |
|---|---:|---:|---:|---:|---|---:|
| ACCREDITATION.pdf | 74 | 8 | 80 | 79 | `accreditation` 69, `marketing-crm` 4, `approvals` 3, `access` 3 | 1 |
| Approval_Workflows_and_Governance_Reference.pdf | 81 | 8 | 80 | 79 | `approvals` 87, `identity` 4, `promotions` 2 | 1 |
| Marketing_CRM_Configuration_Reference v1.0.pdf | 61 | 12 | 120 | 120 | `marketing-crm` 152, `white-label` 8, `promotions` 3 | 0 |
| Payment_Payment_Orchestration.pdf | 190 | 8 | 80 | 79 | `payments` 67, `orders` 19, `finance` 8, `tenancy` 5 | 1 |
| Seat_Management_Venue_Mapping_Reference v1.0.pdf | 57 | 13 | 129 | 128 | `seating` 135, `public-api` 9, `catalogue` 8, `tenancy` 8 | 1 |
| Upsell,CrossSellEngine.pdf | 183 | 6 | 60 | 60 | `promotions` 69, `orders` 4 | 0 |
| Wallet_Configuration_Backend_Structure_v1.0.pdf | 129 | 10 | 100 | 100 | `wallet` 125, `orders` 2, `payments` 1 | 0 |

**Marketing CRM Configuration puts 120 screens on 61 pages** — two per page. The parse reconciles
to twelve ten-screen boards, so the density is the document's, not the parser's.

**Seat Management Venue Mapping is the one pack that does not follow ten-per-board**: 13 boards,
129 screens, one board short by one. It parsed that way on 8 September and has been served that way
since.

---

## 2 · Renders — 6 packs, no new scope

**Zero extractable text, one full-page image per page.** These are pictures of boards whose written
specification is another pack in this same list.

| pack | pages | chars of text | images | the text book it renders |
|---|---:|---:|---:|---|
| F&B Dashboard Screens v1.0.pdf | 6 | 5 | 6 | F&B_Backend_Structure (§3) |
| Marketing_CRM_Dashboard_Screens v1.0.pdf | 12 | 11 | 12 | Marketing_CRM_Configuration (§1) |
| Seat_Management_Dashboard_Screens_Reference.pdf | 13 | 12 | 13 | Seat_Management_Venue_Mapping (§1) |
| TICVAI_POS_Frontline_Dashboard Screens Reference v1.0.pdf | 6 | 5 | 6 | — see below |
| TICVAI_Resource_Management_All_Screens v1.0.pdf | 11 | 10 | 11 | Resource_Management_Configuration (§3) |
| TICVAI_FnB_POS_Visual_Reference_Revised.pdf | 8 | 1,492 | 64 | P04 point-of-sale, 30 screens |

**Four of the six are byte-duplicates of files in `sources/boards/`**, where they hold `authority:
board` — `packs-index.json` records both copies. Their place is the visual reference for a board
already written down, and that is how `sources/README.md` ranks them.

**These six cannot be scoped by reading.** 56 pages of rendered screenshots; a count of the boards
in them needs a person or OCR, and neither produces an operation.

---

## 3 · Existing contract, real remainder — 9 packs, 527 operations

**The contract exists and is a fraction of what the pack specifies.** This is the bulk of the
estimate and the part worth planning.

| pack | pages | boards | screens | served | contract today | est. new |
|---|---:|---:|---:|---:|---|---:|
| TICVAI_Ticket_Types_Product_Configuration_Scope_of_Work_v1.0.pdf | 46 | 12 | 120 | 0 | `catalogue` 199 ops / 238 screens | **120** |
| TICVAI_Inventory_and_Procurement_Backend_Structure_Sample v1.0.pdf | 175 | 7 | 70 | 0 | `inventory` 51 ops / 37 screens | **70** |
| TICVAI Finance Backend Structure Reference v1.0.pdf | 123 | 7 | 70 | 2 | `finance` 56 ops / 33 screens | **68** |
| Event_Management_Configuration_Backend_Structure_v1.0.pdf | 91 | 10 | 100 | 33 | `catalogue` 33 bindings, `workforce` 3 | **67** |
| Retail_Backend_Structure_Module_Reference_v1.0.pdf | 202 | 6 | 60 | 0 | `retail` 25 ops / 21 screens | **60** |
| F&B_Backend_Structure_Module Sample Reference v1.0.pdf | 130 | 6 | 60 | 7 | `fnb` 102 ops / 72 screens | **53** |
| Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf | 136 | 10 | 100 | 58 | `reporting` 78 bindings | **42** |
| Virtual_Queue.pdf | 17 | 4 | 36 | 0 | `queue` 21 ops / 26 screens | **36** |
| Resource_Management_Configuration_Reference.pdf | 169 | 10 | 100 | 89 | `resources` 96, `workforce` 25, `rental` 12, `maintenance` 6 | **11** |

### Ticket Types is the largest single number and the cheapest to check

**The pack states its own scope on its cover: *"12 Boards | 120 Configuration Screens"*, and the
measurement agrees** — 12 `BOARD n` headings, 120 `PAGE n —` headings in the body. Its board titles
are all already-contracted domains: Product Catalogue, Ticket Types & Variants, Validity & Usage
Rules, Scheduling & Timeslots, Capacity, Entitlements & Access Rights, Eligibility, Group & Corporate
Products, Bundles & Add-ons, Upgrade/Exchange/Transfer, Media & Pricing & Promotion.

**No operation anywhere is named for a ticket type** — a case-insensitive scan of every
`operationId` for `tickettype` returns nothing, and the five matches for `ticket` are kitchen
tickets and one booking setter. `catalogue` models products and SKUs. So 120 is the honest estimate
until somebody reads whether a ticket type is a product in this model or a thing beside it.
**That question is worth one afternoon and it moves the total by up to 120.**

### Retail and Inventory parse to zero through the existing parser, and they are not unreadable

`parse-workshop-pack.py` handles three numbering conventions. **These two use a fourth**:
`TICVAI RETAIL — BOARD 1` followed by `PAGE 1 — Retail Command Center`. Both routes in the parser —
table of contents and body fallback — return zero screens, which is why they hold no records in
`pack.json` despite 143,766 and 179,488 characters of clean extractable text.

Counted directly from the headings, **both reconcile exactly**: Retail, 6 boards and 60 screens in
the contents and 60 in the body; Inventory & Procurement, 7 boards and 70 in each. **The
ten-per-board convention holds for both.**

Board titles, which is what makes the attribution:

```
Retail     1 Retail Store & Operational Configuration      -> retail, tenancy
           2 Product, Catalog, Pricing & Merchandising     -> catalogue, promotions
           3 Retail POS, Sales, Returns & Fulfilment       -> retail, orders, payments
           4 Store Stock, Transfers & Operational Inventory-> inventory
           5 Promotions, Omnichannel & Guest Engagement    -> promotions, marketing-crm
           6 Retail Intelligence, Analytics, Forecasting   -> reporting, ai

Inventory  1 Inventory Master & Stock Control              -> inventory
           2 Warehouse, Location & Fulfilment Operations   -> inventory
           3 Transfers, Stock Counts, Adjustments          -> inventory
           4 Supplier, Purchase Request & Procurement      -> inventory (none exists)
           5 Procurement Intelligence Loop                 -> ai, reporting
           6 Receiving, GRN, Invoice Matching & Closure    -> inventory, finance
           7 Planning, Analytics, AI Optimization          -> reporting, ai
```

**Attributing Retail's 60 screens to `retail` would be the seating mistake at pack scale**, which
is exactly what `scope-pack-to-contracts.py`'s docstring warns about: board 4 is stock transfers
and `inventory` has 51 operations serving them; board 2 is catalogue and pricing; board 5 is
`promotions`. **`retail` is one board of six.**

### Finance and F&B are under-parsed rather than unparsed

`TICVAI Finance Backend Structure Reference v1.0.pdf` holds **7 boards and 70 body headings, and
`pack.json` has two records for it.** `F&B_Backend_Structure` holds **6 boards and 60 unique body
headings, and `pack.json` has 20 across 2.** Both use the `PAGE n —` convention; the parser caught
the fragment that happened to match. **A number that says 2 where the document says 70 is the kind
somebody plans against**, and the parse tool says so itself.

### Event Management loses two thirds of its screens the same way

**10 boards and 100 body headings; `pack.json` holds 33 across 9 boards**, all 33 declared and
served, `catalogue` taking 33 of the bindings. The 67 unparsed screens are the estimate.

### Unified BI is missing four boards, not forty screens

**10 boards in the PDF, 100 screens; `screens/P16-venue-analytics.yaml` declares 59 of them, from
boards 1, 2, 3, 4, 9 and 10.** Boards 5 to 8 were never declared. `reporting` already carries 78
bindings from this pack, so the shape is agreed and the middle of the book was skipped.

### Virtual Queue does not use boards or screens

**It numbers `1.1` to `4.10` — 4 boards, 36 named sections**, and says so itself: *"This document
explains the four TICVAI Virtual Queue boards."* Sections 5 to 9 are end-to-end narrative, not
screens. `queue` has 21 operations against 26 screens and none of them cite this pack.

### Resource Management is the smallest remainder and the best-attributed

`scope-pack-to-contracts.py` ran on it. **Board 8 is the only one that needs authoring** — 9 of 10
screens unserved, 7 with no candidate anywhere, the two that do score landing on
`catalogue.listDemandBookingCurve` and `access.listCredentialReplacementReissue`. Board 7 has one.
**Everything else is served, and the served bindings prove the docstring's point**: `resources` 96,
`workforce` 25, `rental` 12, `maintenance` 6. **Four contracts, not one.**

---

## 4 · Genuinely new scope — 4 packs, 107 operations

**Nothing contracted serves these and the term matcher finds no home for most of them.**

| pack | pages | boards | screens | served | est. new |
|---|---:|---:|---:|---:|---:|
| AI_Governance_Reference.pdf | 105 | 4 | 40 | 1 | **39** |
| AI_Configuration_Assistant_Reference.pdf | 63 | 3 | 30 | 2 | **28** |
| AI_Forecasting_and_Predictive_Intelligence_Reference.pdf | 56 | 2 | 20 | 0 | **20** |
| Entitlement Lifecycle.pdf | 28 | 2 | 20 | 0 | **20** |

**The three AI packs arrived on 18 September, after `ai.yaml` was written.** `ai` holds 31
operations against 26 screens and not one of them serves a screen in these books.
`scope-pack-to-contracts.py` returns **AUTHOR — nothing covers it** for five of their nine boards,
and for the rest the best candidates are borrowed from elsewhere and read wrong:
`ADM-520 AI Capability Registry & Ownership` scoring 0.48 against
`access.listMediaTypeCredential`, `ADM-550 AI Risk Register` against
`payments.listB2bCreditAccounts`. **A 0.48 between an AI capability registry and a media-type
credential is the matcher finding two words, not a join.**

Where a candidate is real it is worth keeping: `ADM-547 AI Audit Record & Evidence Package` scores
0.70 against `approvals.createApprovalEvidencePackage`, and `ADM-489 AI Configuration Readiness
Center` scores 1.00 against `subscription.runGoLiveValidation`. **AI governance approval routing
belongs in `approvals`, not in a new contract**, on that evidence.

**Entitlement Lifecycle board 1 is `Portfolio, Ownership & Entitlement Management` and the package
has no portfolio.** A scan of every `operationId` for `portfolio` returns zero. Entitlement itself
is spread over six contracts — `access` 11, `catalogue` 5, `cross-region` 4, `orders` 4,
`subscription` 3, `games` 2 — so **the pack's second board is a fuller specification of something
scattered, and its first is new.** It parsed to 20 titles with no body: its section vocabulary is
not one `parse-workshop-pack.py` knows.

---

## What could not be read, and what was used instead

**Six packs, 56 pages, have no extractable text.** Listed in §2 with their character counts. No
board or screen count is offered for them; the render/source pairing is taken from
`packs-index.json`'s `copies` and `authority` fields, not from the content.

**`tools/scope-pack-to-contracts.py` ran and covers 15 of the 26.** It reads `sources/workshop/
pack.json` and cross-references `screens/P*.yaml`, so **a pack with no records in `pack.json` is
invisible to it** — that is 11 of the 26, including Retail, Inventory & Procurement and Ticket
Types, the three largest estimates in this document. It reported on the 15 that are there. Its
verdicts for the fully-served packs read `MIXED — read it` with zero unserved, which is the tool
having nothing to say rather than a finding.

**`tools/parse-workshop-pack.py` could not be invoked directly.** The sandbox refused it under
*Modify Shared Resources* — it takes `--apply` to write and writes nothing without it, but that is
not visible from the command line. Its parsing functions were imported into a read-only counting
script in the scratchpad instead, which calls `page_texts`, `toc_block`, `parse_toc`,
`body_screens`, `spec_for` and `sections` and prints counts. **No file in the package was written
by it.** Where that parser returned zero, the counts in this document come from a direct regex over
`pypdf` text for `BOARD n` and `PAGE|SCREEN n —`, stated per pack above.

**Nothing in `contracts/`, `handoff/` or `docs/registers/` was touched.**

---

## What to do with it

**Read Ticket Types first.** 46 pages, the smallest of the four largest estimates, and the answer to
one question — is a ticket type a `catalogue` product or a thing beside it — decides whether the
number is 120 or near zero.

**Fix `index-packs.py`'s `drafted` before it is quoted again.** Seven packs report undrafted while
their screens are fully served by hand-written operations. The flag answers *"did
`draft-pack-operations.py` touch this"* and it is read as *"is this unused"*. Those are different
questions and the second one's answer is 15 packs, not 26.

**Teach `parse-workshop-pack.py` the `PAGE n —` convention.** It costs one pattern and recovers
Retail, Inventory & Procurement, Finance, F&B Backend, Event Management and Ticket Types — **500 of
the 638 estimated operations** — into structured records that `scope-pack-to-contracts.py` can then
attribute board by board. Scoping them by regex, as this document did, is a worse version of what
that tool already does properly.

**Do not schedule a workshop for these.** CF-171's own 20 September note settles it: the F&B,
Retail, Procurement and Inventory workshop ran on 18 and 19 August. **Nobody has to be scheduled;
somebody has to read them.**
