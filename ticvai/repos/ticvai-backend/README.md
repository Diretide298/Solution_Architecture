<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/ticvai-backend.md: edit that file, not this one. -->

# ticvai-backend

.NET 10 (LTS). A modular monolith: one solution, its modules deployed as five units (ADR-0055). One deployment serves
many tenants, each in its own database, routed per request by tenant id (ADR-0038).

## Where the code is

**Not here.** The team's repository is GitLab `ticvai/ticvai-backend`; a new one starts from ADAM's backend starter
(`viewer/mcp/setup/starters/backend/`), which the setup zip uses when the team repository is empty. The package keeps no
copy of the code (the lead, 3 November 2026: "Retire the code trees"; CHG-R14J-002): a copy nothing kept in step was
the code a reviewer read, and it was not the code developers got.

## What is here

| Path | What it holds |
|---|---|
| `CLAUDE.md` | The repository's rules as the backend starter gives them to every clone, copied from ADAM's starter |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [CLAUDE.md](CLAUDE.md): the layout, the rules and how a ticket is worked through ADAM.
2. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md) (`backend-patterns.md`, `quality-gates.md`).

The specification (contracts, tables, screens) is served by ADAM at the release tag: pull a ticket with `/ticket <id>`.
