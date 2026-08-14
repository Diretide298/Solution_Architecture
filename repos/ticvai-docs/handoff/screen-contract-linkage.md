# Screen ↔ contract linkage

**64 of 581 operations are consumed by a specified screen.**

The link is written once — screens declare which operations they call — and derived both
ways by `tools/link-screens-contracts.py`. Contracts carry `x-ticvai-consumed-by` per
operation; screens carry `contract` per API entry. They cannot disagree, because only one
side is hand-written.

## Why the number is low

Only 5 of 9 platforms have screen definitions, and within those most screens are still
structural. The 203 screens on platforms with UI/UX boards have no definitions yet at all.

**An uncovered operation is not automatically wrong.** It is one of three things:

| | |
|---|---|
| A screen that exists but is not yet specified | Most of them |
| A back-office or Control Plane surface with no screen definition | Finance, reporting, platform-ops |
| An endpoint nothing will ever call | The one worth finding |

The third is why this report exists. An endpoint no screen consumes, on a platform whose
screens *are* specified, is a candidate for deletion — and cheaper to delete now than to
build, test and maintain first.

## Coverage by contract

| Contract | Ops | Linked | Coverage |
|---|---|---|---|
| `marketing-crm` | 43 | 14 | 33% |
| `subscription` | 28 | 10 | 36% |
| `orders` | 31 | 9 | 29% |
| `catalogue` | 45 | 8 | 18% |
| `identity` | 38 | 7 | 18% |
| `white-label` | 41 | 5 | 12% |
| `seating` | 29 | 4 | 14% |
| `promotions` | 27 | 3 | 11% |
| `retail` | 23 | 2 | 9% |
| `reporting` | 23 | 1 | 4% |
| `finance` | 37 | 1 | 3% |
| `assets` | 10 | 0 | 0% |
| `fnb` | 30 | 0 | 0% |
| `games` | 13 | 0 | 0% |
| `inventory` | 34 | 0 | 0% |
| `maintenance` | 28 | 0 | 0% |
| `platform-ops` | 21 | 0 | 0% |
| `queue` | 20 | 0 | 0% |
| `access` | 19 | 0 | 0% |
| `cross-cell` | 16 | 0 | 0% |
| `shift` | 10 | 0 | 0% |
| `tenancy` | 15 | 0 | 0% |

## Fully uncovered contracts

No operation in these is consumed by any specified screen. In every case the reason is a
missing screen definition rather than a missing purpose.

- **`access`** (19 ops) — P07 Access Handheld — no screen definitions yet
- **`assets`** (10 ops) — P13 White-Label CMS — no screen definitions yet
- **`cross-cell`** (16 ops) — Cell-to-cell. No screen consumes these, by design
- **`fnb`** (30 ops) — P04 POS and P06 Staff Ops — no screen definitions yet
- **`games`** (13 ops) — P04 POS and game readers — no screen definitions yet
- **`inventory`** (34 ops) — P06 Staff Ops — no screen definitions yet
- **`maintenance`** (28 ops) — P06 Staff Ops — no screen definitions yet
- **`platform-ops`** (21 ops) — P09 — screens exist but the contract postdates them; re-run the linker after mapping
- **`queue`** (20 ops) — P02 Guest App and signage — no screen definitions yet
- **`shift`** (10 ops) — P04 POS — no screen definitions yet
- **`tenancy`** (15 ops) — P08 Back Office — no screen definitions yet

## Operations with no consuming screen

517 operations. Grouped by contract; full list in the workbook.

