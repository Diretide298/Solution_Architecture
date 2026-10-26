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
| IDs | `format: uuid`, every one (ADR-0056). New ids are UUIDv7, minted by the server (`Id.New()`) or the device (`newId()`). Human codes people read or type (order numbers, ticket codes) are separate fields, never the id |

---

## 5. Resource Conventions

- Collections plural kebab-case: `/sales-orders`
- Sub-resources over actions: `POST /orders/{id}/refunds`, not `/orders/{id}/refund`
- Actions only where genuinely not a resource: `/sessions/{id}/force-logout`
- `operationId` camelCase verbNoun: `createSalesOrder`
- **Shared errors are implicit** (decided 24 September). Every operation may return the shared responses in `contracts/shared/common.yaml` without listing them: 400 `Problem` (validation), 401 `Unauthorized`, 403 `Forbidden`, 404 `NotFound` where it addresses a resource, and 429 and 5xx as `Problem`. A contract lists only the errors that belong to that operation (for example 409 when a purchase order is raised without an approved requisition), each with its problem `type`. **An operation that lists no errors is not missing any.**

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

---

## 8. Rules the r10 change requests settled (the build's defaults)

Forty-eight change requests of 21 to 24 October 2026 found gaps every build had passed (PROCESS-LOG P-30). Each rule
below is stated once here; a check fails a contract or screen that breaks it, a fixer writes the default where the
fix is mechanical, and the generators (`tools/contract_shapes.py`, CHG-R10GEN-007) write it into what they generate.
Run the fixer a check names; a second run writes nothing.

| # | Rule | Check | Fixer |
|---|---|---|---|
| a | **Money has a currency source.** An operation that answers or accepts common `Money` from a row that stores the amount only asks the currency of its owner: `x-ticvai-read-via` to `tenancy#venueSettingsRecords` (the venue's frozen trading currency) or `tenancy#regionSettingsRecords` (a row with only a region), unless the row or a parent row keeps a currency column. A platform billing row (`control.*`) has no venue: its schema stores `currencyCode`, the billing entity's `billingCurrency` copied when the row is written, and a platform answer computed from such rows reads `control.billing_entity` (CR-202). A row with no venue, and a computed answer, take the venue the operation acts at (naming-and-style 5.1, ADR-0018; CR-197, CR-202, CR-217, CR-234, CR-235). | `check-money-currency` | `tools/fix-money-currency.py` |
| b | **A list states its order, and the order is total.** Every list says how it is ordered; a key that can be null says where the rows without it go (default: after every row that has it, then `id`), and `id` breaks ties (CR-190, CR-206, CR-236). | `check-list-order` | `tools/fix-order-and-refusals.py` |
| c | **A refusal agrees with its state model.** An operation named in a `states/*.yaml` transition refuses (`409`) exactly the states the model does not move it from, and its words name no allowed state the model lacks (CR-237). | `check-state-refusals` | `tools/fix-order-and-refusals.py` (the rest are rulings) |
| d | **A screen value has a declared source.** Every `bindsTo`, state and entry value a screen shows is a field of an answer of an operation in its `apis` (or what the app shell preloads), and every write its text describes is an operation it declares (CR-186, CR-187, CR-220, CR-221, CR-233). | `check-screen-value-sources` | none: declare the read, or rebind |
| e | **Another module's fact is asked of its owner.** An operation whose words name another module's table, field or fact declares `x-ticvai-read-via` to the owner's query over that table (`in-process` within one deployable, `service` across); a read (GET) does so for what its own words name or its response says is worked out on read (ADR-0055 rule 2; CR-096, CR-218). | `check-cross-module-reads` XR-FACT | `tools/fix-read-routes.py` |
| f | **A public guest read of venue data names its venue.** A GET a guest calls without a session at venue scope takes the shared `GuestVenue` parameter (`X-Venue-Id`) and declares `400 venue-required`, unless its path or a required query already names the venue (CR-198). | `check-business-rules` BR-GUEST-VENUE | the generators write it |
| g | **A permission is evaluated per scope.** `x-ticvai-permission` holds at the scope the operation acts on or an ancestor, from the per-scope set (`Session.permissionsByScope`), never the flat `effectivePermissions`; a list reaches the scope paths where it holds (a filter outside them is `403`), and a tenant-level operation needs it at the tenant root (CR-189). | `check-business-rules` BR-SCOPE-AUTHZ | the generators write it |
