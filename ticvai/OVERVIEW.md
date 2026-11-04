# TICVAI

A multi-tenant platform for ticketing, access control, point of sale and venue operations.
**This package is the design of it** — the contracts, the data model, the screens, the
journeys through them, and the reasoning behind every decision that was not obvious.

**2873 operations · 33 contracts · 1178 tables · 2453 screens · 210 state models · 98 authored flows · 72 ADRs**

**Design 95% · Build 32%** (handoff/status.json).

---

## What this is for

**A contract-first package that refuses to contradict itself.** 117 checks run on
every refresh, 111 of them gating: a screen cannot call an operation that does not exist, an operation cannot
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
| Requirements contracted | **3,154** of 3,184 | **100% of what is in scope** |
| Operations reaching a screen | 2583 of 2873 | 90% |
| Screens reachable from an entry point | 2453 of 2453 | 100% |
| Screens drawn on a board | 2453 of 2453 | 100% |
| Screens in an authored journey | 265 of 2453 | 11% |
| Screens on any flow, board-derived routes included | 2108 of 2453 | 86% |
| Conflicts | 158 closed | 8 open, 0 blocking |
| Tables in the DDL | 1,123 of 1,178 | 95% |

---

## Start here

| | |
|---|---|
| **`docs/principles.md`** | The design principles, with what each one rules out — including the six that were wrong first |
| **`conflict-status.md`** | Every conflict and its state, one line each |
| **`handoff/TICVAI_Schema_Reference.xlsx`** | The data model as a workbook |
| **`handoff/schema-roots.md`** | Which table each schema is about, and how the rest hang off it |
| **`COVERAGE.md`** | The account of 17 August 2026 of what was here and what was not (historical) |
| **`docs/adr/`** | Why the platform is shaped this way |

**Running the viewer** renders all of it as five linked layers:

```
cd viewer && npm start        →  http://localhost:4173
```

---

## The 16 platforms

| | | | |
|---|---|---|---:|
| `P01` | Guest Web — Storefront | guest | 50 |
| `P02` | Guest App — Mobile | guest | 77 |
| `P04` | Venue POS — Terminal and Tablet | staff | 32 |
| `P05` | Guest Kiosk — Self-Service | guest | 17 |
| `P06` | Venue Staff App — Operations | staff | 96 |
| `P07` | Venue Scanner — Access Control | staff | 11 |
| `P08` | Venue Management — Back Office | staff | 1663 |
| `P09` | TICVAI Web — Platform Console | platformAdmin | 211 |
| `P10` | Partner Web — Reseller Portal | partner | 43 |
| `P11` | Accreditation Web — Applications | public | 8 |
| `P12` | Venue Support — Agent Console | staff | 28 |
| `P13` | Venue CMS — White Label | staff | 104 |
| `P14` | Developer Portal | partner | 8 |
| `P15` | Kitchen Display — Pass and Stations | staff | 10 |
| `P16` | Venue Analytics — Cross-Domain Reporting | staff | 71 |
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
| `tools/` | 117 checks (tools/run-checks.py) and 43 derivers. `bash tools/refresh.sh` runs everything |
| `repos/` | Each repository's project documents (its README, its CLAUDE.md from ADAM's starter) and `project-bible/`, a mirror of this package; no code. Also generated |

---

## What is not done

**Put last on purpose.** A landing page that only lists what exists is a landing page that misleads.

**Build is 32%** by the package's own measure (handoff/status.json). **The design is 100% of in-scope requirements and the gap to build is the remaining risk.**

**98 authored journeys of a target 120**, beside 193 routes derived from the client boards. 3 of 33 contracts have no operation in an authored journey (`payments`, `rental`, `transport`). **Every journey written so far has found a defect**, which is the argument for writing more.

**0 screens cannot be reached** from their platform's entry point, and navigation is still inferred rather than designed on most of the estate.

**8 conflicts are open**, 0 of them blocking. Each is listed with who answers it:

- **CF-171** — Chinmay + Qossai **Re-measured 20 September: 577 of 2,056 operations, 28%** — the figures above are 577 of 1,626 and 35%. **The absolute number has not moved by one, and all 577 still have a `summary` that is verbatim the title of a screen in their own `x-ticvai-consumed-by`.** It reads better only because the denominator grew by 430 operations that were specified properly. **A measurement that drifts in our own favour is the one nobody re-runs**, which is the whole argument of this row restated against itself. Concentrated in `access` (146), `catalogue` (108), `promotions` (96), `orders` (89), `marketing-crm` (68), `subscription` (50) and `approvals` (20).
- **CF-170** — Chinmay + Dinesh
- **CF-169** — Chinmay + Dinesh
- **CF-162** — Dinesh
- **CF-165** — Allam
- **CF-140** — Chinmay + Qossai
- **CF-133** — Qossai + finance
- **CF-35** — Allam + counsel

---

*Generated by `tools/derive-overview.py` from the package itself. **Do not hand-edit** — a landing page with typed numbers is a landing page that is wrong within a day, and this one claimed twelve platforms and 92 conflicts on a package that had fifteen and 166.*
