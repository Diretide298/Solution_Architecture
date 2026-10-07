# Quickstart

> **Purpose:** Running locally  
> **Owner:** Backend  
> **Status:** **Week 1**. Checked against the starters on 28 September. Steps 2 to 4 get shorter once SETUP-DB and SETUP-SEED land.


**Done when:** a new engineer clones, runs, and hits a mocked endpoint from the frontend without asking anyone a question.

## The six repos

| Repo | What it is |
|---|---|
| `ticvai-contracts` | OpenAPI, event schemas, generated clients. **Everything downstream reads from here** |
| `ticvai-backend` | .NET 10, one cell. `TICVAI-Backend.slnx`: `TICVAI.Api`, `.Application`, `.Domain`, `.Infrastructure`, `.Contracts`, and three test projects |
| `ticvai-frontend` | Nx monorepo: 13 apps, 4 shared packages (`api-client`, `design-tokens`, `offline-core`, `ui`) |
| `ticvai-ai` | Python / FastAPI |
| `ticvai-infra` | Terraform, K8s, cell provisioning (Azure, UAE region) |
| `ticvai-docs` | This |

## Steps

1. **Registry auth:** private NuGet, npm, PyPI. Credentials from the team vault, never committed.
2. **A local PostgreSQL 16.** There is no compose file in `ticvai-backend` yet; **SETUP-DB** adds one. Until then, run one container:
   `docker run -d --name ticvai-pg -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:16`
   Redis and Jaeger are not needed until **SETUP-OBS**.
3. **Apply the schema.** The schema is plain SQL migrations, not EF Core migrations, and there is no `Ticvai.Migrations` project.
   - `db/tenant` and `db/control` hold **our** migrations: one file per **[DB]** ticket, written from the package's numbered files (the reference; never copied in whole or run as they are). See `backend-patterns.md` §3.4.
   - Apply each with `SqlMigrationRunner` (`src/TICVAI.Infrastructure/Persistence/Migrations`):
     `await new SqlMigrationRunner(connectionString).ApplyAsync("db/tenant", ct);`
   - A second run applies nothing: that is the check every **[DB]** ticket uses.
   - **SETUP-DB** wraps this in a command.
4. **Seed the reference fixture:** two brands, three regions across two countries, AED and OMR. **SETUP-SEED** builds it. **Never develop against a single-venue fixture.**
5. **Mock server:** `make mock` in `ticvai-contracts` runs Prism on :4010. It serves the **identity** contract only. For another contract, bundle first (`make bundle`), then:
   `npx @stoplight/prism-cli mock dist/<contract>.yaml -p 4010 --dynamic`
6. **Frontend:** `pnpm install && pnpm nx serve <app>`. The app is the one your ticket names:
   - guest: `guest-web`, `guest-app`
   - staff and venue: `venue-pos`, `venue-staff-app`, `venue-scanner`, `kitchen-display`, `venue-management-web`, `venue-support-web`
   - platform and partners: `ticvai-web`, `partner-web`, `accreditation-web`, `developer-portal-web`, `signup-web`

   Each app points at the mock by default.
7. **Verify:** in `ticvai-backend`, run `dotnet build TICVAI-Backend.slnx`, then `dotnet test tests/TICVAI.ArchitectureTests`.
   - Warnings are errors, so a clean build means no warnings.
   - If either fails on a clean clone, something is wrong with the environment, not your code.

## Read next

[naming-and-style](naming-and-style.md) before writing anything · [git-and-mrs](git-and-mrs.md) before the first commit · [gotchas](../gotchas.md) before you hit them.
