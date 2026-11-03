<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/ticvai-backend.md: edit that file, not this one. -->

# ticvai-backend

.NET 10 (LTS). A modular monolith: one solution, its modules deployed as five units (ADR-0055). One deployment serves
many tenants, each in its own database, routed per request by tenant id (ADR-0038).

## What is here

| Path | What it holds |
|---|---|
| `src/` | The API host (`Ticvai.Api`), the Control Plane, the shared kernel, the modules (`Ticvai.Modules.*`) and `Ticvai.Migrations` |
| `tests/` | The architecture, integration and unit tests |
| `tools/check-migrations.py` | The migration check |
| `Ticvai.sln`, `Directory.Build.props`, `global.json`, `BannedSymbols.txt` | The solution, its build settings, the SDK pin and the banned APIs |
| `docker-compose.yml` | The local services for development |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [AGENTS.md](AGENTS.md): what to read first, and the hard rules.
2. [project-bible/repos/backend.md](project-bible/repos/backend.md): the rules specific to this repository.
3. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md).

The specification (contracts, tables, screens) is served by ADAM at the release tag: pull a ticket with `/ticket <id>`.
