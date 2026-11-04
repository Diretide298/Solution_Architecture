# Repository READMEs

Each file here is the authored source of one `README.md` under `repos/`. `tools/derive-mirrors.py` writes them at
every refresh (README_SOURCES), and `tools/check-repo-readmes.py` fails when a repository README is a copy of any
other package file. Edit the file here, never the README in `repos/`: the next refresh overwrites it.

| Source | Written to |
|---|---|
| [index.md](index.md) | `repos/README.md` |
| [ticvai-ai.md](ticvai-ai.md) | `repos/ticvai-ai/README.md` |
| [ticvai-backend.md](ticvai-backend.md) | `repos/ticvai-backend/README.md` |
| [ticvai-contracts.md](ticvai-contracts.md) | `repos/ticvai-contracts/README.md` |
| [ticvai-docs.md](ticvai-docs.md) | `repos/ticvai-docs/README.md` |
| [ticvai-frontend.md](ticvai-frontend.md) | `repos/ticvai-frontend/README.md` |
| [ticvai-infra.md](ticvai-infra.md) | `repos/ticvai-infra/README.md` |
| [ticvai-infra-cell.md](ticvai-infra-cell.md) | `repos/ticvai-infra/terraform/modules/cell/README.md` |

Every other README under `repos/` that is not a mirror of a package file (the setup standards' folder, the older
documentation folders, `ticvai-contracts/standards/`) is written by the same tool as an index of its folder's files.

`rules/` holds the authored source of three of the per-repository rules pages (`project-bible/repos/contracts.md`,
`infra.md`, `docs.md`); the other three (`backend.md`, `frontend.md`, `ai.md`) and each of those repositories'
`CLAUDE.md` are copies of ADAM's starter `CLAUDE.md` (`viewer/mcp/setup/starters/<role>/CLAUDE.md`), and every
`setup/` folder is a copy of ADAM's starter docs. tools/check-repo-trees.py fails when anything else is under
`repos/<repository>/`, or a copy differs from its source (CHG-R14J-002).
