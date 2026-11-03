# TICVAI repositories

What the package keeps for each repository developers work in: its project documents and `project-bible/`, the
TICVAI knowledge base, all written by `tools/derive-mirrors.py` (never edit them inside a repository). **No application
code is kept here** (the lead, 3 November 2026: "Retire the code trees"; CHG-R14J-002): the backend, frontend and AI
code lives in the team's GitLab repositories, started from ADAM's starters. The contracts repository keeps its
publishing scripts and the infrastructure repository its Terraform, the package's own sources for both.

| Repository | What it holds |
|---|---|
| [ticvai-backend](ticvai-backend/README.md) | The .NET modular monolith's rules page (`CLAUDE.md`, from ADAM's backend starter); the code is in GitLab |
| [ticvai-ai](ticvai-ai/README.md) | The Python 3.12 / FastAPI AI runtime's rules page, owned by the AI engineers; the code is in GitLab |
| [ticvai-contracts](ticvai-contracts/README.md) | The OpenAPI specs (`openapi/`, a copy of the package's `contracts/`), the standards and the scripts that generate and publish the clients |
| [ticvai-frontend](ticvai-frontend/README.md) | The front-end workspace's rules page (`CLAUDE.md`, from ADAM's frontend starter); one GitLab repository per app |
| [ticvai-infra](ticvai-infra/README.md) | Terraform: the cell module, the environments, the runbooks |
| [ticvai-docs](ticvai-docs/README.md) | The documentation repository: the package's mirrored folders and the setup standards |

Setting up a machine starts at [ticvai-docs/setup/quickstart.md](ticvai-docs/setup/quickstart.md); the setup
standards are indexed in [ticvai-docs/setup/README.md](ticvai-docs/setup/README.md).
