# ticvai-contracts

Single source of truth for every interface between TICVAI services and clients.
Nothing in this repo is generated. Everything downstream is.

## Rules

1. **Spec-first.** Hand-author the OpenAPI. Never generate the spec from code —
   that reinstates the serialisation the hybrid repo model exists to avoid.
2. **Breaking changes require a major bump.** `oasdiff` runs on every PR and fails
   the build on an unapproved break.
3. **N-3 minor versions supported.** Guest apps ship through store review and lag
   the backend by weeks. See Project Direction §3.4.9.
4. **Every schema carries tenant scope.** No endpoint is tenant-ambiguous.

## Publishing

| Target   | Artefact              | Registry       |
|----------|-----------------------|----------------|
| .NET     | `Ticvai.Contracts`    | Private NuGet  |
| TS       | `@ticvai/api-client`  | Private npm    |
| Python   | `ticvai-contracts`    | Private PyPI   |
| Testing  | Prism mock image      | Container reg. |

`make generate` regenerates all three. `make mock` runs Prism locally on :4010.

## Layout

    openapi/shared/    common.yaml    errors, pagination, money, tenant scope
    openapi/spine/     identity, tenancy, catalogue, orders, access, sync
    openapi/satellite/ per-module contracts, added in Phase 4
    events/            domain + sync event JSON Schemas
