<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/ticvai-infra.md: edit that file, not this one. -->

# ticvai-infra

Terraform. One instance of the cell module is one cell: a region with a database per tenant (ADR-0038, ADR-0040).
Tenants are rows in the control database (ADR-0039).

## What is here

| Path | What it holds |
|---|---|
| `terraform/modules/cell/` | The cell module ([its README](terraform/modules/cell/README.md)) |
| `terraform/environments/` | The environments that use it |
| `runbooks/` | Operational runbooks (`restore-drill.md`) |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [AGENTS.md](AGENTS.md): what to read first, and the hard rules.
2. [project-bible/repos/infra.md](project-bible/repos/infra.md): the rules specific to this repository.
3. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md) (`config-and-secrets.md`).
