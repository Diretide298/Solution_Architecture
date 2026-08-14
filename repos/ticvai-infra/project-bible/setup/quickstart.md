# Quickstart

> **Purpose:** Running locally  
> **Owner:** Backend  
> **Status:** **Week 1**


**Done when:** a new engineer clones, runs, and hits a mocked endpoint from the frontend without asking anyone a question.

## The six repos

| Repo | What it is |
|---|---|
| `ticvai-contracts` | OpenAPI, event schemas, generated clients. **Everything downstream reads from here** |
| `ticvai-backend` | .NET 8, one cell |
| `ticvai-frontend` | Nx monorepo — 6 apps, 4 shared packages |
| `ticvai-ai` | Python / FastAPI |
| `ticvai-infra` | Terraform, K8s, cell provisioning |
| `ticvai-docs` | This |

## Steps

1. **Registry auth** — private NuGet, npm, PyPI. Credentials from the team vault, never committed.
2. **Backend stack** — `docker compose up -d` in `ticvai-backend`. Brings up Postgres 16, PgBouncer (transaction mode), Redis, Jaeger.
3. **Seed the reference fixture** — two brands, three regions across two countries, AED and OMR. **Never develop against a single-venue fixture.**
4. **Run migrations** — `dotnet run --project src/Ticvai.Migrations`.
5. **Mock server** — `make mock` in `ticvai-contracts`. Prism on :4010.
6. **Frontend** — `pnpm install && pnpm nx serve backoffice`. Points at the mock by default.
7. **Verify** — architecture tests must pass: `dotnet test tests/Ticvai.ArchitectureTests`. If they fail on a clean clone, something is wrong with the environment, not your code.

## Read next

[naming-and-style](naming-and-style.md) before writing anything · [git-and-mrs](git-and-mrs.md) before the first commit · [gotchas](../gotchas.md) before you hit them.
