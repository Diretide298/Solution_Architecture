# TICVAI — Delivery Package

Generated 13 August 2026

**534 API operations · 475 schemas · 103 permissions · 16 ADRs · 0 blocking conflicts**

---

## Vocabulary

Read this first — the words are used precisely throughout.

**Contract** — one hand-authored OpenAPI file covering one bounded context. It is the source
of truth: server code, client code and mock servers are generated from it, never the reverse.
If a field is not in a contract, it does not exist.

**Spine** — the eight contexts everything else depends on. Frozen first; a change needs a
formal change request because every satellite has pinned against them.

**Satellite** — a domain built on the spine that can move independently. Cheaper to change.

**Operation** — one method on one path. All 534 declare four TICVAI extensions:
`x-ticvai-permission`, `x-ticvai-scope-level`, `x-ticvai-offline-capable`,
`x-ticvai-conflict-policy`. Redocly rejects any that does not.

**API schema** — the shape of data on the wire. **Not a database table.** One API schema may
become three columns (`Money`) or five tables (`Order`); some have no table at all
(`ValidationResult`, `TrialBalance`). Roughly 70% of the DDL derives from these; the rest —
partitioning, RLS, the PII split — is storage design in the migration scripts.

**Capability** — a unit of behaviour traced to requirement IDs. 176 defined, covering all
3,184 matrix requirements.

**Cell** — one tenant in one region. The deployment unit.

Every contract carries this same guide in its own `description`, so a file opened cold
explains itself.

---

## Contract metadata

Each contract declares where it sits, in `info`:

```yaml
x-ticvai-tier: spine | satellite | shared
x-ticvai-module: "1 — Ticketing Catalogue"      # matrix domain
x-ticvai-requirements: 312
x-ticvai-capabilities: [C20, C79, ...]
x-ticvai-platforms: ["P04 POS", "P08 Venue Back Office", ...]
```

`x-ticvai-platforms` maps to the platform codes in the screen hierarchy — P01 Guest Web,
P02 Guest App, P03 Kiosk, P04 POS, P06 Staff Ops, P07 Access Handheld, P08 Back Office,
P09 Platform Admin, P10 Partner Portal, P12 Support Console, P13 White-Label CMS.

---

## Spine — 211 operations

| Contract | Ops | Schemas | Matrix domain |
|---|---|---|---|
| `catalogue` | 45 | 28 | 1 — Ticketing Catalogue |
| `identity` | 38 | 21 | 17 — Guest Mobile App & Branding (auth) + cross-cutting staff auth |
| `finance` | 37 | 32 | 5 — F&B & Guest Management (accounting and revenue recognition) |
| `orders` | 31 | 26 | 2 — Ticketing Sales |
| `access` | 19 | 16 | 3 — Admission and Access |
| `cross-cell` | 16 | 8 | Cross-cutting — multi-region |
| `tenancy` | 15 | 14 | Cross-cutting — organisation hierarchy |
| `shift` | 10 | 10 | 2 — Ticketing Sales (cash handling) |

## Satellite — 323 operations

| Contract | Ops | Schemas | Matrix domain |
|---|---|---|---|
| `white-label` | 41 | 34 | 17 — Guest Mobile App & Branding (builder) |
| `marketing-crm` | 40 | 37 | 20 — Marketing & CRM |
| `inventory` | 34 | 30 | 13 — Inventory Management |
| `fnb` | 30 | 25 | 7 — F&B POS  ·  5 — F&B & Guest Management (service) |
| `seating` | 29 | 33 | 19 — Seat Management & Venue Mapping |
| `maintenance` | 28 | 29 | 15 — Maintenance & Safety Management |
| `subscription` | 28 | 29 | 18 — Subscription & Licensing Management |
| `promotions` | 27 | 30 | 4 — Bundles and Promotions |
| `reporting` | 23 | 25 | 8 — Unified Operations Dashboard  ·  cross-cutting |
| `retail` | 23 | 22 | 6 — Retail POS |
| `queue` | 20 | 18 | 5 — F&B & Guest Management (Virtual Queue) |

## Shared

`common.yaml` — Money, ScopeRef, Problem, pagination, idempotency, **4 security schemes**
`permissions.yaml` — **103 permissions.** Every `x-ticvai-permission` validates against it in CI

---

## Package layout

    contracts/    the 534 operations, flat for direct reading
    docs/         16 ADRs · registers · architecture · sprint · client agenda
    handoff/      API list · page inventory · schema conventions
    sources/      client documents — MoMs, matrix, designs, diagram
    repos/        THE SIX REPOSITORIES — this is what gets pushed

`contracts/`, `docs/` and `handoff/` duplicate content inside `repos/`. The repositories are
authoritative.

---

## Authentication

| Scheme | Used by |
|---|---|
| `bearerAuth` | Staff sessions. Carries `sid`, validated against the session registry |
| `guestAuth` | Guest sessions. No workstation, no role selection, no single-session rule |
| `serviceAuth` | Cell-to-cell. mTLS plus a cell-identity token |
| `apiKeyAuth` | Partner and developer. Deferred pending the Developer & API workshop |

Authorisation is not expressed through OAuth scopes — permissions resolve at login against a
seven-level tree with deny-overrides-allow, which scopes cannot express. An empty `security`
array means "this scheme, no scopes", and is not the same as an absent one.

---

## State

| | Done | Total |
|---|---|---|
| Requirements → capability | 3,184 | 3,184 |
| **API operations** | **534** | ~546 |
| **API schemas** | **475** | — |
| **Database tables** | **8** | **~180** |
| Capability workflows | 0 | ~60 |
| Sprint 0 | 0 | 11 |

**Contracts are effectively done; database schema has barely started.** ~172 tables are
derivable from the 475 API schemas today. The migration orchestrator has been unowned since
30 July, and every table lands through a migration.

Awaiting others: CF-37 FX policy · lab rig in place of a pilot venue · payment sandbox
credentials · four domain workshops covering ~276 requirements.
See `docs/active/needs-discussion.md`.
