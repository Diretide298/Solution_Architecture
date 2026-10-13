# Quickstart

> **Purpose:** Running locally  
> **Owner:** Backend  
> **Status:** **Week 1**. Checked against the starters on 28 September. Steps 2 to 4 get shorter once SETUP-DB and SETUP-SEED land.


**Done when:** a new engineer clones, runs, and hits a mocked endpoint from the frontend without asking anyone a question.

## The repos

| Repo | What it is |
|---|---|
| `ticvai-contracts` | OpenAPI, event schemas, generated clients. **Everything downstream reads from here** |
| `ticvai-backend` | .NET 10, one cell. `TICVAI-Backend.slnx`: `TICVAI.Api`, `.Application`, `.Domain`, `.Infrastructure`, `.Contracts`, and three test projects |
| `ticvai-frontend/*` | One repository per app since 13 October 2026, in the GitLab group `ticvai-frontend`: `ticvai-venue-management`, `ticvai-guest-web`, `ticvai-employee-app`, `ticvai-kiosk`, `ticvai-guest-app`, `ticvai-pos`. Before that one Nx monorepo (13 apps, 4 shared packages: `api-client`, `design-tokens`, `offline-core`, `ui`), still ADAM's starter with `-UseStarter` |
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
6. **Frontend:** run ADAM's setup (it makes a frontend workspace), then clone your app's repository
   inside that workspace. Install and serve the app inside the repository's folder, as its README
   says (in the one-workspace starter: `pnpm install && pnpm nx serve <app>`). The ticket's screen
   names its platform and the package's app; the workspace's CLAUDE.md says which repository builds
   which platform. The package's app names:
   - guest: `guest-web`, `guest-app`
   - staff and venue: `venue-pos`, `venue-staff-app`, `venue-scanner`, `kitchen-display`, `venue-management-web`, `venue-support-web`
   - platform and partners: `ticvai-web`, `partner-web`, `accreditation-web`, `developer-portal-web`, `signup-web`

   In the starter, each app points at the mock by default; in an app repository, its README says how.
7. **Verify:** in `ticvai-backend`, run `dotnet build TICVAI-Backend.slnx`, then `dotnet test tests/TICVAI.ArchitectureTests`.
   - Warnings are errors, so a clean build means no warnings.
   - If either fails on a clean clone, something is wrong with the environment, not your code.

## Read next

[naming-and-style](naming-and-style.md) before writing anything · [git-and-mrs](git-and-mrs.md) before the first commit · [gotchas](../gotchas.md) before you hit them.
