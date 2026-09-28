# Dependencies

> **Purpose:** Adding a package is a decision  
> **Owner:** Chinmay  
> **Status:** **Draft: proposed, client to approve (audit R038)**


## Before adding

1. Does an approved package already do this?
2. What licence? Permissive only — MIT, Apache-2.0, BSD. **GPL and AGPL are blocked** in a commercial client deliverable
3. Maintenance signal — last release, open issue count, single-maintainer risk
4. Transitive weight — what does it pull in?
5. Does it need to exist, or is it fifty lines?

## Rules

- **Contract packages are pinned, never floating.** `@ticvai/api-client`, `Ticvai.Contracts`, `ticvai-contracts` — exact versions, bumped deliberately
- Renovate raises bump PRs; humans review them
- Security scanning in CI, blocking on high severity
- A generated dependency — one an AI tool suggested — gets the same licence review as any other. See [llm-conventions](llm-conventions.md)
- Adding a dependency to `Shared.Kernel` or `offline-core` needs architecture sign-off. Those propagate everywhere

## Approved by runtime

**Proposed, client to approve (audit R038, decided 28 September).** Drafted from what the starters already ship. Anything not on this list needs sign-off from **one named approver on the client side: [client to name]** (client IT / architecture), recorded in the PR that adds it. Until that person is named, Chinmay approves provisionally and the addition is listed for the client at the next review.

Versions are the starters' baseline; Renovate raises bumps within a major version, and a major bump is a new approval.

### Backend (.NET 10, `ticvai-backend`)

| Package | Purpose | Starter baseline |
|---|---|---|
| `Microsoft.AspNetCore.OpenApi`, `Microsoft.OpenApi` | OpenAPI document from the API | 10.0.x, 2.x |
| `Microsoft.Extensions.*` (DependencyInjection, Configuration, Options, Diagnostics.HealthChecks) | Hosting, configuration, `/health` | 10.0.x (framework) |
| `Serilog.AspNetCore`, `Serilog.Sinks.Console` | Structured logging | 10.0.x, 6.x |
| `OpenTelemetry.Extensions.Hosting`, `OpenTelemetry.Instrumentation.AspNetCore`, `OpenTelemetry.Instrumentation.Http` | Traces | 1.17.x |
| `OpenTelemetry.Exporter.OpenTelemetryProtocol` | Export to the OTLP endpoint (not yet in the starter; approved for SETUP-OBS) | 1.17.x |
| `FluentValidation`, `FluentValidation.DependencyInjectionExtensions` | Request validation | 12.x |
| `Microsoft.EntityFrameworkCore`, `Microsoft.EntityFrameworkCore.Design`, `Npgsql.EntityFrameworkCore.PostgreSQL` | Persistence on PostgreSQL | 10.0.x |
| `Microsoft.CodeAnalysis.BannedApiAnalyzers` | Compile-time banned symbols (`BannedSymbols.txt`) | 3.3.x |
| `xunit`, `xunit.runner.visualstudio`, `Microsoft.NET.Test.Sdk`, `coverlet.collector` | Tests and coverage (test projects only) | 2.9.x, 3.1.x, 17.x, 6.x |

### Frontend (Nx + pnpm, `ticvai-frontend`)

| Package | Purpose | Starter baseline |
|---|---|---|
| `nx`, `@nx/js`, `@nx/react`, `@nx/react-native`, `@nx/vite`, `@nx/eslint`, `@nx/eslint-plugin` | Monorepo build, module boundaries | 20.x |
| `typescript` | Language | 5.6+ |
| `vitest` | Tests | 2.x |
| `eslint`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin` | Lint, including `enforce-module-boundaries` | 8.x |
| pnpm | Package manager (`packageManager: pnpm@9`) | 9.x |

**Banned in apps by the lint rule:** `expo-sqlite`, `react-native-sqlite-storage`, `@op-engineering/op-sqlite`. Local storage goes through `offline-core` only.

### Infrastructure and CI (`ticvai-infra`)

No infra starter ships yet, so this list follows the platform decision (audit R057: Azure in a UAE region, GitHub Actions).

| Item | Purpose |
|---|---|
| Terraform with the `hashicorp/azurerm` provider | Cells, databases, key vaults |
| GitHub Actions, using `actions/*` and `pnpm/action-setup` only, pinned to a major version | CI for every repository |
| Azure Key Vault | Per-cell secrets (see config-and-secrets) |

A third-party GitHub Action is a dependency like any other and needs the named approver.

### AI (`ticvai-ai`, Python)

No starter ships yet. FastAPI is the stated framework (quickstart); every other package waits for the named approver.
