# TICVAI

Generated 14 August 2026

**654 API operations · 230 tables designed · 347 screens · 39 state models · 16 events · 18 ADRs**

**Conflicts: 25 open, 41 closed, 0 blocking.**

---

## Start here

| | |
|---|---|
| **`COVERAGE.md`** | What is here and what is not, against the whole build. Every figure counted from the files |
| **`conflict-status.md`** | Every conflict and its state, one line each |
| **`wireframes/TICVAI Wireframe Boards.dc.html`** | **12 boards, 347 screens, one visual system.** Open in a browser |
| **`handoff/TICVAI_Schema_Reference.xlsx`** | 230 tables, 2,026 columns, eight sheets |
| **`handoff/screen-index.json`** | Every screen joined to its board, operations, service and tables |
| **`handoff/services-and-procedures.md`** | Where each operation gets its data, 22 services, ten stored procedures |
| **`handoff/storage-design.md`** | The 30% of a migration that does not derive from the contracts |
| **`docs/active/design-plan.md`** | Boards, forms, and what combines |

## Folders

| | |
|---|---|
| `contracts/` | 654 operations across 22 files |
| `wireframes/` | **12 platform boards, 347 screens** |
| `screens/` | 347 definitions across twelve platforms |
| `flows/` | 12 user journeys with their unhappy paths |
| `states/` · `events/` | 39 state models · 16 domain events, cross-checked |
| `handoff/` | Schema workbook · storage design · integration register · artefact audit · tooltips |
| `docs/` | 18 ADRs, registers, decisions |
| `tools/` | **Six validators** and two generators |
| `repos/` | The six git repositories |

    python3 tools/check-screens.py    check-frontend    check-flows
    python3 tools/check-states.py     check-config-scope   check-wireframes
    python3 tools/build-cf-index.py   link-screens-contracts

---

## Two levels of done

**Every screen inventoried is now defined — 347 of 347.** 167 arrived on 14 August,
extracted from the wireframe boards, which carry real purposes and real navigation.

**67 have their states written.** That is the number that matters. A screen with a
purpose and a route can be drawn; it cannot be built from. The states are where the behaviour
lives, and on the sixteen scanner screens — the surface where offline matters most — the
offline state is `TODO`.

The same distinction runs through the flows: 8 written of roughly sixty, and between them
they have found one missing screen, four missing operations and **one missing contract** —
a task, which the employee app's fifty screens are built around and which appears in none of
642 operations (CF-71).

---

## No migrations, deliberately

The SQL was removed. **The schema workbook is the working artefact** while the design settles.
Writing DDL against a moving design produces migrations that must be rewritten, and a
forward-only migration cannot be rewritten.

---

## State

| | Done | Total |
|---|---|---|
| **API operations** | **654** | — |
| Requirements covered | 2,842 | 3,184 |
| Configuration levels decided | 321 | 321 |
| Tables designed | 230 | — |
| Tables written | 0 | deliberate |
| **Screens defined** | **347** | **347** |
| **Screens specified** | **67** | 347 |
| Operations reaching a screen | 154 | 654 |
| Flows | 12 | ~60 |
| Sprint 0 | 0 | 11 |

**Nothing has been executed.** No build, no `psql`, no pipeline.
