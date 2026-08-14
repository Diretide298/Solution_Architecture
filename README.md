# TICVAI

Generated 14 August 2026

**587 API operations · 213 tables designed, 27 written · 102 screens defined · 5 flows**

---

## Folders

| | |
|---|---|
| **`contracts/`** | 587 operations across 22 OpenAPI files. `spine/`, `satellite/`, `shared/` |
| **`backend/`** | 4 SQL migrations, 27 tables. `MIGRATIONS.md` explains the conventions |
| **`screens/`** | 102 screen definitions across 5 platforms, plus the schema and component library |
| **`flows/`** | 5 user flows, each traced across screens with its unhappy paths |
| **`frontend/`** | Per-app route and screen manifests, generated from the screens |
| **`docs/`** | 16 ADRs, registers, architecture, the client agenda |
| **`handoff/`** | API list, page inventory, schema reference workbook, deployment view |
| **`tools/`** | Five validators. Run them |
| **`sources/`** | Client documents — 7 MoMs, the matrix, designs |
| **`repos/`** | The six git repositories. This is what gets pushed |

---

## Run the validators

    python3 tools/check-migrations.py          # DDL conventions, RLS, level typing
    python3 tools/check-screens.py             # component vocabulary, operationIds, states
    python3 tools/check-frontend.py            # apps, routes, component paths
    python3 tools/check-flows.py               # flows against screens and contracts
    python3 tools/link-screens-contracts.py    # rebuild the two-way linkage

They expect to run from the repo root. Each has found something real — between them they
caught nine defects on 14 August that had all previously reported clean.

---

## What changed on 14 August

| | |
|---|---|
| **Three duplicate operationIds** | `getAsset`, `updateAsset`, `listBundles`. Media moved to `/media` — in a venue "asset" means a ride, not a JPEG |
| **`platform.outlet`** | Referenced nine times by F&B, retail and games. Defined nowhere |
| **`platform.tenant`** | A cell could not resolve its own tenant without a cross-database call it is not permitted to make |
| **`marketing.guest_device`** | Push notifications had nowhere to land |
| **Level-typed scope FKs** | `venue_id` was a bare uuid on 48 tables. Nothing stopped it pointing at a workstation |
| **`platform.outbox` RLS** | Carried venue event payloads with no policy |
| **Navigation** | 10 screens had it. Now 102 |
| **F02 corrected** | The seated flow skipped guest details |
| **Conflict register rebuilt** | CF-27 appeared twice, two open items were filed as closed, and six were never written in — including CF-37 |

---

## State

| | Done | Total |
|---|---|---|
| Requirements mapped | 3,184 | 3,184 |
| **API operations** | **587** | — |
| Tables designed | 213 | — |
| **Tables written as DDL** | **27** | 213 |
| Screens inventoried | 305 | — |
| Screens defined | 102 | 305 |
| Flows | 5 | ~60 |
| Sprint 0 | 0 | 11 |

**Nothing has been executed.** No `dotnet build`, no `psql`, no `pnpm install`, no pipeline
run. Everything validates structurally. The first real run will find things — every check
added today found something the previous one had missed.

**Blocking conflicts: 0.** Open: 14, of which 7 need a client decision. `docs/registers/conflicts.md`.
