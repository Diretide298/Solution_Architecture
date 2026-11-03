# TICVAI backend

.NET 10 API in clean-architecture layers: Api, Application, Contracts, Domain, Infrastructure.

## Run it

Requires the .NET 10 SDK and PostgreSQL.

```
dotnet build TICVAI-Backend.slnx
dotnet test TICVAI-Backend.slnx
```

One process serves every tenant of a cell, each on its own database (ADR-0038): the request's host
picks the tenant. To run the API, list at least one tenant outside source control, for example:

```
dotnet user-secrets --project src/TICVAI.Api init
dotnet user-secrets --project src/TICVAI.Api set "Tenants:Entries:0:TenantId" "01920000-0000-7000-8000-000000000001"
dotnet user-secrets --project src/TICVAI.Api set "Tenants:Entries:0:Hosts:0" "localhost"
dotnet user-secrets --project src/TICVAI.Api set "Tenants:Entries:0:RootScopePath" "t_ref"
dotnet user-secrets --project src/TICVAI.Api set "Tenants:Entries:0:ConnectionString" "Host=localhost;Database=ticvai;Username=dev;Password=dev"
dotnet run --project src/TICVAI.Api
```

Then `GET http://localhost:5042/health` (503 until every listed tenant database answers). Tokens are
verified with the cell's public key (`Authentication:Issuer`, `Audiences`, `SigningKeys`).

## The pipeline

`.gitlab-ci.yml` builds with warnings as errors and runs every test project on each push and merge
request, the integration tests against a PostgreSQL 16 service (`TICVAI_TEST_DATABASE`; with
`TICVAI_REQUIRE_DATABASE=1` a missing database fails instead of skipping). A test project that runs
no tests, or a skipped test, fails the job. Locally the row-security test skips unless you set
`TICVAI_TEST_DATABASE` to a PostgreSQL superuser connection string.

## Working with Claude Code

`CLAUDE.md` tells Claude how this repository is laid out and how to work a ticket through ADAM.
The team's coding standards are in `project-bible/setup/`.
