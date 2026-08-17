# TICVAI

Generated 17 August 2026

**737 operations · 278 tables · 364 screens · 45 state models · 26 events · 18 ADRs**

**Conflicts: 79 raised, 0 blocking.** See `conflict-status.md`.

---

## Start here

| | |
|---|---|
| **`COVERAGE.md`** | What is here and what is not, against the whole build |
| **`conflict-status.md`** | Every conflict and its state, one line each |
| **`wireframes/TICVAI Wireframe Boards.dc.html`** | 12 boards, 364 screens. Open in a browser |
| **`handoff/platforms-and-apps.md`** | Twelve platforms, ten apps, named by who operates them |
| **`handoff/build-order.md`** | Which apps can be built, and in what order |
| **`handoff/TICVAI_Schema_Reference.xlsx`** | 278 tables, 2,025 columns, nine sheets |
| **`handoff/services-and-procedures.md`** | Where each operation gets its data. 23 services, ten procedures |
| **`docs/active/ai-scope-for-confirmation.md`** | AI scope, for the client to confirm |

## Folders

| | |
|---|---|
| `contracts/` | **737 operations** across 25 files — 246 spine, 443 satellite |
| `screens/` | 347 definitions across 12 platforms |
| `frontend/` | 10 app manifests, with build readiness |
| `states/` · `events/` | 45 state models · 26 events, cross-checked |
| `flows/` | 15 user journeys with their unhappy paths |
| `wireframes/` | 12 platform boards, linked to the definitions both ways |
| `handoff/` | Schema workbook · lineage · storage design · registers · tooltips |
| `docs/` | 18 ADRs, conflict register, decisions |
| `tools/` | **Seven validators** and two generators |
| `repos/` | The six git repositories |

    python3 tools/check-screens.py    check-frontend      check-flows
    python3 tools/check-states.py     check-config-scope  check-wireframes
    python3 tools/check-package.py    # the layers against each other
    python3 tools/build-cf-index.py   link-screens-contracts

---

## Naming

**Platforms and apps are named by who operates them.** `guest-*` is what a visitor touches,
`venue-*` is what venue staff run, `ticvai-web` is the only one we operate. That is the
question that matters at 9pm on a Saturday, because it answers who is supposed to fix it.

Ten platforms map to one app each. Two apps serve two platforms and say so.

## Two levels of done

**Every screen is defined — 347 of 347.** Purpose, route, navigation, enough to draw.

**All 347 have their states written.** That is what a developer builds from, and it is why only two
apps — `venue-scanner` and `venue-pos` — currently clear the bar.

---

## No migrations, deliberately

The SQL was removed. **The schema workbook is the working artefact** while the design settles.
Writing DDL against a moving design produces migrations that must be rewritten, and a
forward-only migration cannot be rewritten. What the six migrations held beyond the column
list is in `handoff/storage-design.md`.

---

## State

| | Done | Total |
|---|---|---|
| **API operations** | **707** | — |
| API data lineage resolved | 707 | 707 |
| Requirements with a contract | 2,778 | 2,990 |
| Configuration levels decided | 321 | 321 |
| Tables designed | 266 | — |
| Tables written | 0 | deliberate |
| **Screens defined** | **364** | 364 |
| **Screens specified** | **364** | 364 |
| Screens with operations | 290 | 347 |
| Operations reaching a screen | 567 | 707 |
| Flows | 15 | ~60 |
| Sprint 0 | 0 | 11 |

**Nothing has been executed.** No build, no `psql`, no pipeline.
