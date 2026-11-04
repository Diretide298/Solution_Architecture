# ticvai-contracts

OpenAPI specs, event schemas, generated clients. The coordination artefact every other repo consumes.

## Read this first

`project-bible/` is the whole TICVAI knowledge base, copied in.

| Read | Path | Why |
|---|---|---|
| **1** | `project-bible/overview.md` | Source-of-truth hierarchy and settled positions. **Where anything conflicts with this, it wins** |
| **2** | `project-bible/glossary.md` | Canonical terms. Do not invent synonyms |
| **3** | `project-bible/gotchas.md` | The traps, symptom first |
| **4** | `project-bible/repos/contracts.md` | **Rules specific to this repository** |
| **5** | `project-bible/setup/naming-and-style.md` | Case per layer, identifiers, money, time, banned words |
| **6** | `project-bible/setup/git-and-mrs.md` | Commits, trailers, review checklist |
| **7** | `project-bible/setup/llm-conventions.md` | Attribution, accountability, elevated-review areas |
| **8** | `project-bible/docs/adr/README.md` | Why decisions were made |

Then as needed: `project-bible/docs/architecture/` · `docs/registers/` · `product/modules/` ·
`sources/` for the client documents everything derives from.

## project-bible is a copy

The package's `tools/derive-mirrors.py` writes it at every refresh, from the package and from ADAM's
starters (`setup/`). **Do not edit it here**: the next refresh overwrites it. A change goes into the package
(served by ADAM at the release tag) or, for `setup/`, into ADAM's starter docs.

## Hard rules

- **Money is `Money`** — never a float, never fixed 2dp. OMR is 3dp, AED is 2dp
- **Timestamps are UTC.** Distinguish `recorded_at` (device) from `synced_at` (server) from `created_at` (row)
- **Permission strings come from the generated enum.** Never hand-typed — divergence gives a supervisor a button that 403s
- **Tenant scope is enforced on every data path**, at the data layer, not only in services
- **Authorisation is user-driven.** Workstation determines presentation, hardware, till identity and reporting — never authorisation
- **The committer owns the code.** Verify every external API against real documentation

## When something is unclear

Check the bible. If it is not there, it is a **question, not an assumption**.
Open questions: `project-bible/docs/registers/conflicts.md`.

Anything tagged `REF` or `DESIGN` is not a build item until promoted to `MATRIX` or `MOM`.
