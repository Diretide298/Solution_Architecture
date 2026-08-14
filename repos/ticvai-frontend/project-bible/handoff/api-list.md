# API List

> **Purpose:** Every endpoint, its status, and who consumes it
> **Owner:** Chinmay
> **Status:** **581 published** — 211 spine, 346 satellite · **every unblocked module complete**

One third of the build handoff. See [page-inventory](page-inventory.md) and [schema](schema.md).

**Status key:** ✅ published in OpenAPI · 🟡 specified, contract not written · ⬜ not specified

---

## 1. Identity & Session — `identity.yaml`

| Status | Method | Path | Permission | Offline | Consumers |
|---|---|---|---|---|---|
| ✅ | POST | `/auth/login` | — | ✗ | all |
| ✅ | POST | `/auth/select-role` | — | ✗ | all |
| ✅ | POST | `/auth/refresh` | — | ✗ | all |
| ✅ | POST | `/auth/logout` | — | ✓ | all |
| ✅ | GET | `/auth/session` | — | ✓ | all |
| ✅ | POST | `/auth/sessions/{id}/force-logout` | `SESSION_FORCE_LOGOUT` | ✗ | pos, backoffice |
| 🟡 | POST | `/auth/guest` | — | ✗ | guest, webb2c |
| 🟡 | POST | `/auth/guest/otp` | — | ✗ | guest, webb2c |
| 🟡 | POST | `/auth/guest/social` | — | ✗ | guest, webb2c |
| 🟡 | GET/POST | `/principals` | `USER_MANAGE` | ✗ | backoffice |
| 🟡 | GET/PATCH | `/principals/{id}` | `USER_MANAGE` | ✗ | backoffice |
| 🟡 | GET/POST | `/roles` | `ROLE_MANAGE` | ✗ | backoffice |
| 🟡 | GET/POST/DELETE | `/grants` | `PERMISSION_GRANT` | ✗ | backoffice |
| 🟡 | POST | `/permissions/resolve` | `PERMISSION_VIEW` | ✗ | backoffice |
| 🟡 | GET/PUT | `/password-policy` | `USER_MANAGE` | ✗ | backoffice |

**6 published · ~20 total**

---

## 2. Tenancy & Organisation — `tenancy.yaml`

| Status | Method | Path | Permission | Offline | Consumers |
|---|---|---|---|---|---|
| ✅ | GET/POST | `/scope-nodes` | `SCOPE_VIEW` / `SCOPE_MANAGE` | ✗ | backoffice |
| ✅ | GET/PATCH | `/scope-nodes/{id}` | `SCOPE_VIEW` / `SCOPE_MANAGE` | ✗ | backoffice |
| ✅ | GET/PUT | `/regions/{id}/settings` | `SCOPE_VIEW` / `REGION_CONFIGURE` | ✓ read | all |
| ✅ | GET | `/workstations` | `SCOPE_VIEW` | ✗ | backoffice |
| ✅ | GET/PUT | `/workstations/{id}` | `SCOPE_VIEW` / `WORKSTATION_CONFIGURE` | ✓ read | pos, scanner |
| 🟡 | GET/POST | `/sale-boards` | `WORKSTATION_CONFIGURE` | ✓ read | backoffice, pos |
| 🟡 | GET/POST | `/devices` | `DEVICE_CONFIGURE` | ✗ | backoffice |

**9 published · ~12 total**

---

## 3. Shift & Till — `shift.yaml`

| Status | Method | Path | Permission | Offline | Consumers |
|---|---|---|---|---|---|
| ✅ | GET/POST | `/shifts` | `REPORT_VIEW_WORKSTATION` / `SHIFT_OPEN` | ✓ | pos |
| ✅ | GET | `/shifts/current` | `SHIFT_OPEN` | ✓ | pos |
| ✅ | GET | `/shifts/{id}` | `REPORT_VIEW_WORKSTATION` | ✓ | pos, backoffice |
| ✅ | POST | `/shifts/{id}/suspend` | `SHIFT_SUSPEND` | ✓ | pos |
| ✅ | POST | `/shifts/{id}/resume` | `SHIFT_OPEN` | ✓ | pos |
| ✅ | POST | `/shifts/{id}/close` | `SHIFT_CLOSE` | ✓ | pos |
| ✅ | POST | `/shifts/{id}/accept-variance` | `OVERSHORT_ACCEPT` | ✗ | pos |
| ✅ | GET/POST | `/shifts/{id}/cash-movements` | `CASH_LIFT` | ✓ | pos |

**10 published — context complete**

---

## 4. Access Control — `access.yaml`

| Status | Method | Path | Permission | Offline | Consumers |
|---|---|---|---|---|---|
| ✅ | POST | `/access/validate` | `ACCESS_VALIDATE` | ✓ | scanner, pos |
| ✅ | POST | `/access/override` | `ACCESS_OVERRIDE` | ✓ | scanner |
| ✅ | GET | `/access/lookup` | `TICKET_LOOKUP` | ✓ | scanner, employee |
| ✅ | GET/POST | `/access/scans` | `ACCESS_VALIDATE` | ✗ | scanner |
| ✅ | GET | `/access/offline-package` | `ACCESS_VALIDATE` | ✗ | scanner, edge |
| ✅ | PUT | `/access-points/{id}/mode` | `TURNSTILE_MODE_SET` | ✓ | scanner |
| 🟡 | GET/POST | `/access-points` | `ACCESS_POINT_CONFIGURE` | ✗ | backoffice |
| 🟡 | GET/POST | `/admission-profiles` | `ACCESS_POINT_CONFIGURE` | ✗ | backoffice |
| 🟡 | GET/POST/DELETE | `/blacklist` | `ACCESS_POINT_CONFIGURE` | ✗ | backoffice |

**7 published · ~20 total**

---

## 5. Catalogue & Entitlement — `catalogue.yaml` · ✅ 26 published

| Status | Method | Path | Permission | Offline | Notes |
|---|---|---|---|---|---|
| ✅ | GET/POST | `/products` | `PRODUCT_CONFIGURE` | ✓ read | Local-first read on POS |
| GET/PATCH | `/products/{id}` | `PRODUCT_CONFIGURE` | ✓ read | |
| GET/POST | `/products/{id}/components` | `PRODUCT_CONFIGURE` | ✗ | |
| GET/POST | `/attributes` | `PRODUCT_CONFIGURE` | ✗ | Axes generating variants |
| POST | `/products/{id}/regenerate-variants` | `PRODUCT_CONFIGURE` | ✗ | Materialised variant table |
| GET/POST | `/price-lists` | `PRICE_CONFIGURE` | ✓ read | |
| GET/POST | `/price-lists/{id}/prices` | `PRICE_CONFIGURE` | ✓ read | |
| GET/POST | `/events` | `EVENT_CONFIGURE` | ✓ read | |
| GET/POST | `/events/{id}/performances` | `PERFORMANCE_CONFIGURE` | ✓ read | |
| GET/POST | `/envelopes` | `CAPACITY_CONFIGURE` | ✗ | Capacity allocation |
| GET | `/availability` | `PRODUCT_VIEW` | ✗ | Live counts |
| **POST** | **`/catalogue/bundles`** | `PRODUCT_CONFIGURE` | ✗ | **C102 — sign, version, publish** |
| **GET** | **`/catalogue/bundles/latest`** | `PRODUCT_VIEW` | ✗ | **Terminal pull, ETag** |
| **GET** | **`/catalogue/bundles/{v}/delta/{from}`** | `PRODUCT_VIEW` | ✗ | **Delta apply** |
| **POST** | **`/leases`** | `ORDER_CREATE` | ✗ | **C103 — acquire** |
| **POST** | **`/leases/{id}/renew`** | `ORDER_CREATE` | ✗ | **TTL extension** |
| **DELETE** | **`/leases/{id}`** | `ORDER_CREATE` | ✗ | **Return unsold** |
| **GET** | **`/leases`** | `PRODUCT_VIEW` | ✗ | **Monitor, stranded detection** |
| GET/POST | `/data-masks` | `PRODUCT_CONFIGURE` | ✓ read | JSONB + field registry |
| GET | `/entitlements/{id}` | `ORDER_VIEW` | ✓ | |
| GET/POST | `/tickets` | `ORDER_VIEW` | ✓ | |
| POST | `/tickets/{id}/media` | `ORDER_MODIFY` | ✗ | Re-link. Ticket ID unchanged |

*~22 shown of ~45. Remainder: product lifecycle, portfolio, resale, alternative codes.*

---

## 6. Order & Payment — 🟡 ~40 ops beyond shift

| Method | Path | Permission | Offline | Notes |
|---|---|---|---|---|
| POST | `/orders` | `ORDER_CREATE` | ✓ | **Server re-prices every line on ingest** |
| GET | `/orders` | `ORDER_VIEW` | ✓ | |
| GET | `/orders/{id}` | `ORDER_VIEW` | ✓ | |
| POST | `/orders/{id}/refunds` | `ORDER_REFUND` | ✗ | **CF-36 — threshold shape open** |
| POST | `/orders/{id}/voids` | `ORDER_VOID` | ✓ | |
| POST | `/orders/{id}/exchanges` | `ORDER_EXCHANGE` | ✗ | |
| POST | `/orders/{id}/reprints` | `ORDER_REPRINT` | ✓ | |
| POST | `/refunds/bulk` | `ORDER_REFUND_BULK` | ✗ | Event or date level |
| POST | `/refund-requests` | — *(guest)* | ✗ | A34 → ops queue |
| GET/POST | `/payments` | — | ✓ cash | |
| POST | `/payments/{id}/inquiry` | — | ✗ | **Status recovery. 12 Aug §12** |
| POST | `/payments/{id}/capture` | — | ✗ | |
| GET/POST | `/reservations` | `ORDER_CREATE` | ✗ | Unpaid, expires |
| POST | `/sync/orders` | `ORDER_CREATE` | ✗ | Ordered batch replay |
| GET | `/sync/rejections` | `ORDER_VIEW` | ✗ | Operator reconciliation |

---

## 7. Cross-Cell — 🟡 ~15 ops · **Wave 1 per ADR-0014**

| Method | Path | Where | Notes |
|---|---|---|---|
| POST | `/guest-links` | Control Plane | **Explicit consent required** |
| GET | `/guest-links/{linkId}` | Control Plane | Pseudonymous only. No PII |
| DELETE | `/guest-links/{linkId}` | Control Plane | Consent withdrawal |
| POST | `/redemption-rights` | Cell → cell | Propagate from issuing cell |
| POST | `/redemption-rights/{id}/consume` | Consuming cell | **Locally authoritative** |
| POST | `/redemption-rights/reconcile` | Cell → cell | Report consumption back |
| POST | `/wallet-authorisations` | Home cell | Hold. Card-auth pattern |
| POST | `/wallet-authorisations/{id}/capture` | Home cell | |
| POST | `/wallet-authorisations/{id}/release` | Home cell | |
| GET/PUT | `/wallet-allocations` | Home cell | Bounded fallback for link-down |
| POST | `/dsar/requests` | Control Plane | Fan-out across linked cells |

---

## 8. Finance & Ledger — 🟡 ~40 ops · blocked on CF-36/37/38

| Method | Path | Notes |
|---|---|---|
| GET/POST | `/accounts` | Chart of accounts, native + ERP mapping |
| GET/POST | `/tax-codes` | Per line, compound, multi-country |
| GET/POST | `/recognition-schedules` | Immediate, redemption, straight-line, breakage |
| GET/POST | `/allocation-splits` | % or fixed. **Cross-entity per ADR-0010** |
| GET/POST | `/journal-entries` | Post → review → approve |
| POST | `/journal-entries/{id}/approve` | Finance manager |
| GET | `/ledger/entries` | Append-only |
| GET | `/ledger/trial-balance` | |
| GET/POST | `/settlements` | 5-step, monthly file |
| POST | `/settlements/{id}/reconcile` | |
| GET/POST | `/legal-entities` | By country, currency |
| GET/POST | `/fiscal-periods` | Close to lock postings |
| GET | `/reports/financial` | P&L, balance sheet, cash flow |
| GET | `/price-variances` | **CF-38 — new** |
| GET/POST | `/intercompany-settlements` | **New per ADR-0010** |

---

## 9. Reporting — 🟡 ~15 ops

`/reports` · `/reports/{id}/run` · `/reports/schedules` · `/reports/subscriptions` ·
`/reports/sales-summary` · `/reports/admission-summary` · `/reports/exports`

Filterable by site, operating area, channel, workstation, user.

---

## Totals

| Context | Published | Total | Status |
|---|---|---|---|
| **Identity & AuthZ** | **38** | ~38 | **Complete.** Staff auth, guest auth, SSO, MFA, sessions, principals, roles, grants |
| **Tenancy & Org** | **15** | ~15 | **Complete.** Scope tree, regions, workstations, sale boards, devices |
| Shift & Till | **10** | 10 | **Complete** |
| **Access Control** | **19** | ~19 | **Complete.** Validation, override, group, offline package, access points, geofence |
| **Catalogue & Entitlement** | **45** | ~45 | **Complete.** Products, lifecycle, pricing, events, capacity, bundles, leases, entitlement templates |
| **Order & Payment** | **41** | ~41 | **Complete.** Orders, payments, refunds, modification, exchange, reschedule, transfer, statement, B2B credit |
| **Cross-Cell** | **16** | ~16 | **Complete** |
| **Finance & Ledger** | **37** | ~49 | **CF-36/38 closed.** ~12 FX ops need CF-37 |
| Reporting | 0 | ~15 | |
| **Spine** | **149** | **~208** | **72%** |
| Satellites | **346** | ~346 | **13 domains complete** |

---

## What a Team Needs Before Building an Endpoint

1. Path, method, permission, scope level
2. Offline-capable and conflict policy
3. Request and response schema
4. Error responses with enumerated types
5. Which pages consume it → [page-inventory](page-inventory.md)
6. Which tables it touches → [schema](schema.md)

Items 1–4 are the OpenAPI contract. Rows marked 🟡 have 1–2 but not 3–4, so they are
**estimable but not buildable**.
