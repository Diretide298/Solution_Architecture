# The cell module

One instance of this module is one cell: a region with a database per tenant (ADR-0038, ADR-0040). Tenants are rows in
the control database (ADR-0039), so no tenant id or slug is an input here.

| File | What it holds |
|---|---|
| `variables.tf` | The inputs, each with its description: `environment` (staging or production; dev has no cell), `cell` (the jurisdiction and a number, e.g. `ae1`), and the rest |
| `main.tf` | The cell's resources |
| `network.tf` | Its network |
| `outputs.tf` | What it gives the environments that use it |

The descriptions in `variables.tf` are the reference for the inputs; this page only lists the files.
