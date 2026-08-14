# TICVAI

Six repositories. **`ticvai-docs` is the project bible** — copied into every other repo as
`project-bible/`.

| Repo | Runtime | Cadence |
|---|---|---|
| `ticvai-docs` | Markdown | Living. **The source** |
| `ticvai-contracts` | OpenAPI + codegen | On change, semver |
| `ticvai-backend` | .NET 8 | Continuous |
| `ticvai-frontend` | TypeScript / RN / React | Web continuous, mobile per store cycle |
| `ticvai-ai` | Python 3.12 / FastAPI | Continuous |
| `ticvai-infra` | Terraform / K8s | On change |

## Updating the bible

Edit `ticvai-docs/`, then from this directory:

    ./update-bible.sh

Commit the `project-bible/` change in each repo. **Never edit `project-bible/` inside a
code repo** — it is overwritten on the next run. CI warns if a PR touches it.

`project-bible/.synced-at` records when each copy was taken.

## Habit worth keeping

**Closing a conflict should be followed by a sync.** Otherwise developers keep reading a
settled question as open — `registers/conflicts.md` is the page most likely to go stale.

## Start here

Each repo's `CLAUDE.md` / `AGENTS.md`: reading order, repo-specific rules, and the hard
rules that apply everywhere.
