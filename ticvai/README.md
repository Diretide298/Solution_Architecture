# TICVAI

**2864 operations · 1173 tables · 2453 screens · 210 state models · 113 events · 98 flows · 72 ADRs**

**Conflicts:** every one and its state in `conflict-status.md`; the open ones, with who answers each, in [OVERVIEW.md](OVERVIEW.md). **Today's figures are in OVERVIEW.md**, derived on every refresh; the counts on this page are rewritten from `handoff/status.json` by `tools/sync-counts.py`, and it carries no other figure (r13 system review F-13).

---

**New here? Read [docs/principles.md](docs/principles.md) first.** The design principles, with
provenance and what each one rules out — including the six that were wrong first.

## Start here

| | |
|---|---|
| **`COVERAGE.md`** | What was here and what was not on 17 August 2026 (historical) |
| **`conflict-status.md`** | Every conflict and its state, one line each |
| **`wireframes/TICVAI Wireframe Boards.dc.html`** | 219 boards, 2453 screens. Open in a browser |
| **`handoff/platforms-and-apps.md`** | The platforms and the apps, named by who operates them |
| **`handoff/build-order.md`** | Which apps can be built, and in what order |
| **`handoff/TICVAI_Schema_Reference.xlsx`** | The data model as a workbook: 1173 tables |
| **`handoff/ai-index.md`** | Where every AI artefact lives |
| **`docs/active/workshop-packs.md`** | The three blocked domains, prepared |

## Folders

| | |
|---|---|
| `contracts/` | **2864 operations** in 33 contracts, spine and satellite |
| `screens/` | 2453 screens across 16 platforms |
| `frontend/` | 13 frontends, one derived manifest each, with build readiness |
| `states/` · `events/` | 210 state models · 113 events, cross-checked |
| `flows/` | 98 flows written as journeys, beside the routes derived from the client boards |
| `handoff/` | Registers, indexes and workbooks: the derived layer |
| `docs/` | Architecture, 72 ADRs, the conflict register |
| `tools/` | The checks, run as one gated pass by `tools/run-checks.py`, and the derivers |
| `wireframes/` | 219 boards from Claude Code, linked to every definition |
| `sources/` | The matrix, the minutes, the client design references |

## Validating

    bash tools/refresh.sh                 # every derived file, in order
    python3 tools/run-checks.py           # every check; the gate is tools/refresh-safe.sh

## What this is

The design package of the platform: the contracts, the data model, the screens, the journeys through them, and the
reasoning behind every decision that was not obvious. Developers build from it through ADAM at each release tag
(`repos/README.md` says where each repository lives); how far the build has come is in [OVERVIEW.md](OVERVIEW.md).
