# TICVAI

Generated 17 August 2026

**776 operations · 287 tables · 376 screens · 80 state models · 29 events · 24 flows · 25 ADRs**

**Conflicts: 92 raised, 0 blocking.** See `conflict-status.md`.

---

**New here? Read [docs/principles.md](docs/principles.md) first.** The design principles, with
provenance and what each one rules out — including the six that were wrong first.

## Start here

| | |
|---|---|
| **`COVERAGE.md`** | What is here and what is not, against the whole build |
| **`conflict-status.md`** | Every conflict and its state, one line each |
| **`wireframes/TICVAI Wireframe Boards.dc.html`** | 12 boards, 376 screens. Open in a browser |
| **`handoff/platforms-and-apps.md`** | Twelve platforms, ten apps, named by who operates them |
| **`handoff/build-order.md`** | Which apps can be built, and in what order |
| **`handoff/TICVAI_Schema_Reference.xlsx`** | 287 tables, 2,025 columns, nine sheets |
| **`handoff/ai-index.md`** | Where every AI artefact lives |
| **`docs/active/workshop-packs.md`** | The three blocked domains, prepared |

## Folders

| | |
|---|---|
| `contracts/` | **776 operations** across 25 files — 267 spine, 470 satellite |
| `screens/` | 364 definitions across 12 platforms, all specified |
| `frontend/` | 10 app manifests, with build readiness |
| `states/` · `events/` | 80 state models · 29 events, cross-checked |
| `flows/` | 23 user journeys with 137 unhappy paths |
| `handoff/` | Registers, indexes and the schema workbook |
| `docs/` | Architecture, 25 ADRs, the conflict register |
| `tools/` | **7 validators** and two generators |
| `wireframes/` | 12 boards from Claude Code, linked to every definition |
| `sources/` | The matrix, the minutes, the client design references |

## Validating

    cd ticvai-full
    python3 tools/check-screens.py        check-frontend      check-flows
    python3 tools/check-states.py         check-config-scope  check-wireframes
    python3 tools/check-package.py        # the layers against each other

Six report zero warnings. `check-states` reports a backlog of lifecycles declared inline on a
property with no state model — **found on 17 August when the checker's own blind spot was
fixed**, and they are under-specified rather than wrong.

## What this is

A design package. **776 operations, 287 tables and 376 screens are specified and none of it
has been executed** — no SQL is written, no code is built, and every number above is an
assertion until something runs.

The fastest way to test that is `venue-scanner`: 376 screens, fully specified, offline-mandatory,
and one flow with eight branches.
