# TICVAI

A multi-tenant platform for ticketing, access control, point of sale and venue operations.
**This package is the design of it** — the contracts, the data model, the screens, the
journeys through them, and the reasoning behind every decision that was not obvious.

**1023 operations · 28 contracts · 379 tables · 492 screens · 122 state models · 94 flows · 30 ADRs**

**Design 93% · Build 0%.**

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
| Operations reaching a screen | 758 of 1023 | 74% |
| Screens reachable from an entry point | 419 of 492 | 85% |
| Screens drawn on a board | 492 of 492 | 100% |
| Screens in a journey | 262 of 492 | 53% |
| Conflicts | 148 closed | 12 open, none blocking |
| **Tables written** | **0** of 379 | **build has not started** |

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

## The 15 platforms

| | | | |
|---|---|---|---:|
| `P01` | Guest Web — Storefront | guest | 46 |
| `P02` | Guest App — Mobile | guest | 63 |
| `P04` | Venue POS — Terminal and Tablet | staff | 24 |
| `P05` | Guest Kiosk — Self-Service | guest | 17 |
| `P06` | Venue Staff App — Operations | staff | 66 |
| `P07` | Venue Scanner — Access Control | staff | 11 |
| `P08` | Venue Management — Back Office | staff | 143 |
| `P09` | TICVAI Web — Platform Console | platformAdmin | 37 |
| `P10` | Partner Web — Reseller Portal | partner | 21 |
| `P11` | Accreditation Web — Applications | public | 8 |
| `P12` | Venue Support — Agent Console | staff | 8 |
| `P13` | Venue CMS — White Label | staff | 20 |
| `P14` | Developer Portal | partner | 8 |
| `P15` | Kitchen Display — Pass and Stations | staff | 10 |
| `P16` | Venue Analytics — Cross-Domain Reporting | staff | 10 |

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

**Build is 0%.** 379 tables are designed and none is written. No migration has run, no service is scaffolded, and nothing has executed. **The design is 95% of in-scope requirements and the gap to build is the entire remaining risk.**

**94 journeys of a target 60.** Seventeen contracts have exactly one — `subscription` has one over 55 operations. **Every journey written so far has found a defect**, which is the argument for writing more.

**73 screens cannot be reached** from their platform's entry point, and navigation is still inferred rather than designed on most of the estate.

**12 conflicts are open.** None blocks build; four need an email and one needs a workshop.

- **CF-161** — Dinesh + Chinmay
- **CF-162** — Dinesh
- **CF-163** — Chinmay
- **CF-164** — Chinmay + Allam
- **CF-165** — Allam
- **CF-166** — ?
- **CF-64** — Dinesh + Qossai
- **CF-140** — Chinmay + Qossai
- **CF-133** — Qossai + finance
- **CF-127** — Qossai
- **CF-35** — Allam + counsel
- **CF-21** — Chinmay — schedule

---

*Generated by `tools/derive-overview.py` from the package itself. **Do not hand-edit** — a landing page with typed numbers is a landing page that is wrong within a day, and this one claimed twelve platforms and 92 conflicts on a package that had fifteen and 160.*
