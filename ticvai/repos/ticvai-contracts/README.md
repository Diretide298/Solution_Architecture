<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/ticvai-contracts.md: edit that file, not this one. -->

# ticvai-contracts

OpenAPI specs, event schemas and generated clients: the coordination artefact every other repository consumes.

## What is here

| Path | What it holds |
|---|---|
| `openapi/` | The package's `contracts/` (spine, satellite, shared), copied by `tools/derive-mirrors.py`: never edit it here |
| `standards/` | API design, coding standards, nomenclature and AI authorship |
| `scripts/generate-clients.sh`, `scripts/breaking-change-check.sh` | Client generation and the breaking-change check |
| `Makefile` | The targets that run them |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [AGENTS.md](AGENTS.md): what to read first, and the hard rules.
2. [project-bible/repos/contracts.md](project-bible/repos/contracts.md): the rules specific to this repository.
3. [openapi/README.md](openapi/README.md): the contracts' own index.
4. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md).
