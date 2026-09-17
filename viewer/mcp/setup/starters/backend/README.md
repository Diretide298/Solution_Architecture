# TICVAI backend

.NET 10 API in clean-architecture layers: Api, Application, Contracts, Domain, Infrastructure.

## Run it

Requires the .NET 10 SDK and PostgreSQL.

```
dotnet build TICVAI-Backend.slnx
dotnet test TICVAI-Backend.slnx
```

To run the API, set the connection string outside source control, for example:

```
dotnet user-secrets --project src/TICVAI.Api init
dotnet user-secrets --project src/TICVAI.Api set "Database:ConnectionString" "Host=localhost;Database=ticvai;Username=dev;Password=dev"
dotnet run --project src/TICVAI.Api
```

Then `GET http://localhost:5042/health`.

## Working with Claude Code

`CLAUDE.md` tells Claude how this repository is laid out and how to work a ticket through ADAM.
The team's coding standards are in `project-bible/setup/`.
