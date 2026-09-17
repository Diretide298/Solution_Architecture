# TICVAI — API Design Standard

**Version:** 1.0
**Scope:** Every contract in `openapi/`. Binding.

---

## 1. Contract-First, Never Code-First

Specs are hand-authored. Servers and clients are generated from them.

Code-first generation means the contract only exists after the backend does, which
reinstates the serialisation that the whole delivery model exists to avoid. Frontend and
AI must be able to build against a mock before any backend code is written.

---

## 2. The Five Contracts

OpenAPI alone is insufficient here. Five artefacts are versioned together:

| # | Artefact | Format | Consumers |
|---|---|---|---|
| 1 | REST API | OpenAPI 3.1 | Frontend, AI, partners |
| 2 | Event schemas | JSON Schema | Every module, reporting, warehouse |
| 3 | Sync protocol | OpenAPI + state machine spec | POS, scanner, employee apps |
| 4 | Error taxonomy | Enumerated codes + RFC 9457 | Frontend, AI, partners |
| 5 | Permission vocabulary | Enumerated strings | Frontend nav, backend authz, AI scoping |

Artefact 5 is the one most often skipped. The frontend filters navigation on the same
strings the backend enforces. If they diverge, a supervisor sees a button that returns
403 — invisible in code review, obvious in production. Generate both from one enum.

---

## 3. Required Extensions

Every operation declares six things. Each maps to a settled architectural decision.

```yaml
/orders:
  post:
    operationId: createOrder
    x-ticvai-permission: ORDER_CREATE
    x-ticvai-scope-level: venue
    x-ticvai-offline-capable: true
    x-ticvai-conflict-policy: append
    parameters:
      - $ref: '../shared/common.yaml#/components/parameters/IdempotencyKey'
    responses:
      '201':
        headers:
          X-Consistency-Token:
            schema: { type: string }
```

| Extension | Settled by | Breaks without it |
|---|---|---|
| `x-ticvai-permission` | User/role-driven authz | Frontend and backend diverge |
| `x-ticvai-scope-level` | *No cross-venue access unless permitted* | Leakage found at pen-test, not design |
| `x-ticvai-offline-capable` | Offline architecture, 31 Jul | Apps guess; capacity products sold offline |
| `x-ticvai-conflict-policy` | Sync design | Each app invents its own conflict handling |
| `Idempotency-Key` | Outbox replay | Duplicate sales on reconnect |
| `X-Consistency-Token` | Replication lag | Ticket sold at the gate refused 20s later |

Redocly rules reject any operation missing the first four.

---

## 4. Type Rules

| Concept | Rule |
|---|---|
| Money | `{ amount: string, currency: string, scale: int }`. Never a float. Never fixed 2dp — OMR is 3dp |
| Scope | `ScopeRef` with level, id and ltree path |
| Errors | RFC 9457 problem details, enumerated `type` URI |
| Pagination | Cursor-based. Never offset — it drifts under concurrent writes |
| Timestamps | RFC 3339, UTC, always `timestamptz` semantics |
| Enums | Closed. Clients must handle unknown values gracefully |
| IDs | ULID for edge-created entities, UUID for configuration |

---

## 5. Resource Conventions

- Collections plural kebab-case: `/sales-orders`
- Sub-resources over actions: `POST /orders/{id}/refunds`, not `/orders/{id}/refund`
- Actions only where genuinely not a resource: `/sessions/{id}/force-logout`
- `operationId` camelCase verbNoun: `createSalesOrder`
- Every 4xx and 5xx documented with its problem `type`

---

## 6. Versioning

| Change | Version | Process |
|---|---|---|
| Add optional field, endpoint, or enum value | Patch | Merge |
| Add required request field, remove response field, narrow a type | **Major** | `contract:major` label, deprecation window, tenant impact report |
| Change a permission string | **Major** | Frontend nav breaks silently otherwise |
| Change event schema shape | **Major** | Consumers break silently |
| New error code | Minor | Clients handle unknown codes gracefully |

**N-3 minor versions supported.** Mobile apps ship through store review and tenants
publish their own binaries, so a live app can be three minors behind. The Control Plane
tracks contract version per tenant per platform.

`oasdiff` gates every PR.

---

## 7. Gates

**Gate 1 — contract review.** Three questions:
1. Can the frontend build every page in this context against it?
2. Can the backend implement it without needing a field that is not there?
3. Does every operation declare permission, scope, offline and conflict policy?

**Gate 2 — mock-proven.** One end-to-end flow runs against the Prism mock with zero
backend code. If it cannot, the contract is wrong, and finding out now costs a day
instead of a sprint.

**After Gate 2 the contract is frozen for the context.** Changes need a version bump and
review. This is what stops contract-first collapsing into code-first with extra steps.
