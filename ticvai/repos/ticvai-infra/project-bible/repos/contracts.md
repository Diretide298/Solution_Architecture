# Contract Rules

**Spec-first, never code-first.** Specs are hand-authored; servers and clients are generated.

Code-first means the contract only exists after the backend does, which reinstates the
serialisation the delivery model exists to avoid.

## Five contracts, versioned together

| # | Artefact | Consumers |
|---|---|---|
| 1 | REST API (OpenAPI 3.1) | Frontend, AI, partners |
| 2 | Event schemas (JSON Schema) | Every module, reporting, warehouse |
| 3 | Sync protocol | POS, scanner, employee apps |
| 4 | Error taxonomy (RFC 9457) | Frontend, AI, partners |
| 5 | **Permission vocabulary** | Frontend nav, backend authz, AI scoping |

Artefact 5 is the one most often skipped. Frontend filters navigation on the same strings
backend enforces. Divergence gives a supervisor a button that 403s.

## Required on every operation

```yaml
x-ticvai-permission: ORDER_CREATE       # authz, single source
x-ticvai-scope-level: venue             # hierarchy level required
x-ticvai-offline-capable: true          # queueable by offline clients
x-ticvai-conflict-policy: append        # sync semantics
```

Plus `Idempotency-Key` on every mutation, and `X-Consistency-Token` on write responses.

Redocly rejects any operation missing the first four.

## Types

Money `{amount: string, currency, scale}` — never a float, never fixed 2dp ·
`ScopeRef` with level, id and ltree path · errors RFC 9457 with enumerated `type` ·
**cursor pagination, never offset** — offset drifts under concurrent writes ·
ULID for edge-created entities, UUID for configuration.

## Versioning

| Change | Version |
|---|---|
| Add optional field / endpoint / enum value | Patch |
| Add required request field, remove response field, narrow a type | **Major** |
| Change a permission string | **Major** |
| Change event schema shape | **Major** |

**N-3 minor versions supported.** Mobile ships through store review and tenants publish
their own binaries, so a live app can be three minors behind.

`oasdiff` gates every PR. Breaking changes need the `contract:major` label.

## Gates

**Gate 1 —** can frontend build every page against it? Can backend implement it without a
missing field? Do all four extensions appear on every operation?

**Gate 2 —** one flow runs end to end on the Prism mock with **zero backend code**.
After Gate 2 the contract is **frozen** for the context.
