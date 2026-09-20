# TICVAI

A multi-tenant platform for ticketing, access control, point of sale and venue operations.
**This package is the design of it** — the contracts, the data model, the screens, the
journeys through them, and the reasoning behind every decision that was not obvious.

**2068 operations · 32 contracts · 625 tables · 2427 screens · 125 state models · 96 flows · 48 ADRs**

**Design 91% · Build 33%.**

---

## What this is for

**A contract-first package that refuses to contradict itself.** Nine validators run on
every change: a screen cannot call an operation that does not exist, an operation cannot
name a table stored nowhere, a state model cannot anchor on a schema with no values, a
flow cannot step through a screen that was deleted.

**Nothing holds a copy of anything else's truth.** A screen names an operation; the
operation resolves against the contracts; the contract resolves against the schema; the
schema resolves against the relationship graph. Four hops, no duplication.

**Every artefact is derived where it can be.** The boards are generated from the screens,
the schema reference from the contracts, the relationship graph from both, the repo
mirrors from the root. **A hand-maintained copy is a copy that goes stale**, and this
package has been bitten by that three times.

---

## Where it stands

| | | |
|---|---:|---|
| Requirements contracted | **2,647** of 3,184 | **95% of what is in scope** |
| Operations reaching a screen | 1798 of 2068 | 87% |
| Screens reachable from an entry point | 2426 of 2427 | 100% |
| Screens drawn on a board | 2427 of 2427 | 100% |
| Screens in a journey | 2126 of 2427 | 88% |
| Conflicts | 157 closed | 9 open, none blocking |
| **Tables written** | **0** of 625 | **build has not started** |

---

## Start here

| | |
|---|---|
| **`docs/principles.md`** | The design principles, with what each one rules out — including the six that were wrong first |
| **`conflict-status.md`** | Every conflict and its state, one line each |
| **`handoff/TICVAI_Schema_Reference.xlsx`** | The data model as a workbook |
| **`handoff/schema-roots.md`** | Which table each schema is about, and how the rest hang off it |
| **`COVERAGE.md`** | What is here and what is not |
| **`docs/adr/`** | Why the platform is shaped this way |

**Running the viewer** renders all of it as five linked layers:

```
cd viewer && npm start        →  http://localhost:4173
```

---

## The 16 platforms

| | | | |
|---|---|---|---:|
| `P01` | Guest Web — Storefront | guest | 46 |
| `P02` | Guest App — Mobile | guest | 71 |
| `P04` | Venue POS — Terminal and Tablet | staff | 30 |
| `P05` | Guest Kiosk — Self-Service | guest | 17 |
| `P06` | Venue Staff App — Operations | staff | 96 |
| `P07` | Venue Scanner — Access Control | staff | 11 |
| `P08` | Venue Management — Back Office | staff | 1182 |
| `P09` | TICVAI Web — Platform Console | platformAdmin | 676 |
| `P10` | Partner Web — Reseller Portal | partner | 51 |
| `P11` | Accreditation Web — Applications | public | 8 |
| `P12` | Venue Support — Agent Console | staff | 28 |
| `P13` | Venue CMS — White Label | staff | 100 |
| `P14` | Developer Portal | partner | 8 |
| `P15` | Kitchen Display — Pass and Stations | staff | 10 |
| `P16` | Venue Analytics — Cross-Domain Reporting | staff | 69 |
| `P17` | TICVAI Sign-up — Onboarding & Purchase | public | 24 |

---

## Folders

| | |
|---|---|
| `contracts/` | The OpenAPI files. **Spine and satellite** — a spine contract is one others depend on and cannot be removed |
| `screens/` | **The specification for everything visual.** Boards are generated from these |
| `flows/` | Journeys through the screens, with their branches and who resolves each |
| `states/` | Lifecycles, one per entity that has one |
| `events/` | What the platform publishes, and which consumers are critical |
| `docs/adr/` | Decisions, with the alternatives and why they lost |
| `docs/registers/` | Conflicts, traceability, the backlog |
| `handoff/` | Derived artefacts — the schema reference, the lineage, the graph |
| `tools/` | Nine validators and eight derivers. `bash tools/refresh.sh` runs everything |
| `repos/` | Mirrors of this package for each build repository. Also generated |

---

## What is not done

**Put last on purpose.** A landing page that only lists what exists is a landing page that misleads.

**Build is 0%.** 625 tables are designed and none is written. No migration has run, no service is scaffolded, and nothing has executed. **The design is 95% of in-scope requirements and the gap to build is the entire remaining risk.**

**96 journeys of a target 60.** Seventeen contracts have exactly one — `subscription` has one over 2068 operations. **Every journey written so far has found a defect**, which is the argument for writing more.

**2427 screens cannot be reached** from their platform's entry point, and navigation is still inferred rather than designed on most of the estate.

**9 conflicts are open.** None blocks build; four need an email and one needs a workshop.

- **CF-171** — Chinmay + Qossai **Re-measured 20 September: 577 of 2068 operations, 28%** — the figures above are 577 of 1,626 and 35%. **The absolute number has not moved by one, and all 577 still have a `summary` that is verbatim the title of a screen in their own `x-ticvai-consumed-by`.** It reads better only because the denominator grew by 2068 operations that were specified properly. **A measurement that drifts in our own favour is the one nobody re-runs**, which is the whole argument of this row restated against itself. Concentrated in `access` (146), `catalogue` (108), `promotions` (96), `orders` (89), `marketing-crm` (68), `subscription` (50) and `approvals` (20).
- **CF-170** — Chinmay + Dinesh
- **CF-169** — Chinmay + Dinesh
- **CF-162** — Dinesh
- **CF-165** — Allam
- **CF-140** — Chinmay + Qossai
- **CF-133** — Qossai + finance
- **CF-127** — Qossai
- **CF-35** — Allam + counsel

---

*Generated by `tools/derive-overview.py` from the package itself. **Do not hand-edit** — a landing page with typed numbers is a landing page that is wrong within a day, and this one claimed twelve platforms and 92 conflicts on a package that had fifteen and 166.*
