# Repos

> **Purpose:** Rules specific to each code repository  
> **Owner:** Chinmay  
> **Status:** Living

Each repository mounts this whole knowledge base at `project-bible/` as a git submodule.
Its `CLAUDE.md` points here for the runtime-specific rules.

| Repo | Page | Runtime |
|---|---|---|
| `ticvai-contracts` | [contracts](contracts.md) | OpenAPI, event schemas, codegen |
| `ticvai-backend` | [backend](backend.md) | .NET 8 |
| `ticvai-frontend` | [frontend](frontend.md) | TypeScript, React, React Native |
| `ticvai-ai` | [ai](ai.md) | Python 3.12, FastAPI |
| `ticvai-infra` | [infra](infra.md) | Terraform, Kubernetes |
| `ticvai-docs` | [docs](docs.md) | This repository |

Shared rules — glossary, nomenclature, gotchas, git conventions, LLM conventions, decisions —
are not duplicated here. They live once, in their own sections.
