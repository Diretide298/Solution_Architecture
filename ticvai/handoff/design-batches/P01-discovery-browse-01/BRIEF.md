# P01-discovery-browse-01 — P01 · Discovery & Browse

**4 screens · 8 operations · 23 schemas · 2 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## What to build

**A working surface, not a drawing of one.** The reference is `sources/designs/TICVAI_POS_Terminal_client_approved.html` — a Claude Design
build from these same sources, and the one the client responded to. Open it and match its depth:
real state, seeded data, controls that do something. Do not describe it, read it.

## What is in this folder

| file | what it is |
|---|---|
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PRODUCT_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **6 of these operations work offline**: getProduct, getTenantAppStatus, getWaitTimes, listPerformances, listProducts, searchCatalogue
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `WEB-001` | Home / Landing | listDetail | 3 | 0 | — |
| `WEB-002` | Event & Attraction Listing | listDetail | 4 | 0 | — |
| `WEB-003` | Search Results | listDetail | 2 | 0 | — |
| `WEB-004` | Attraction Details | listDetail | 4 | 0 | — |

## Thin screens in this batch

**WEB-003 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.
