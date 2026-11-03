# TICVAI repositories

The package's copies of the repositories developers work in. Each carries `project-bible/`, the TICVAI knowledge base
copied in by `tools/derive-mirrors.py` (never edit it inside a repository).

| Repository | What it holds |
|---|---|
| [ticvai-backend](ticvai-backend/README.md) | .NET modular monolith: the modules, the API host, the migrations and their tests |
| [ticvai-ai](ticvai-ai/README.md) | The Python 3.12 / FastAPI AI runtime, owned by the AI engineers |
| [ticvai-contracts](ticvai-contracts/README.md) | The OpenAPI specs (`openapi/`, a copy of the package's `contracts/`), the standards and the client generation scripts |
| [ticvai-frontend](ticvai-frontend/README.md) | The front-end workspace: apps and shared packages |
| [ticvai-infra](ticvai-infra/README.md) | Terraform: the cell module, the environments, the runbooks |
| [ticvai-docs](ticvai-docs/README.md) | The documentation repository: the package's mirrored folders and the setup standards |

Setting up a machine starts at [ticvai-docs/setup/quickstart.md](ticvai-docs/setup/quickstart.md); the setup
standards are indexed in [ticvai-docs/setup/README.md](ticvai-docs/setup/README.md).
