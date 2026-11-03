<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/ticvai-frontend.md: edit that file, not this one. -->

# ticvai-frontend

The front-end workspace (Nx): the apps under `apps/` and the shared packages under `packages/` (`api-client`,
`design-tokens`, `offline-core`, `ui`). The per-app repositories of the GitLab group ticvai-frontend, and the app each
one builds, are listed in [project-bible/docs/active/frontend-repos.yaml](project-bible/docs/active/frontend-repos.yaml).

## What is here

| Path | What it holds |
|---|---|
| `apps/` | One folder per app |
| `packages/` | The shared packages |
| `nx.json`, `package.json`, `tsconfig.base.json` | The workspace settings |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [AGENTS.md](AGENTS.md): what to read first, and the hard rules.
2. [project-bible/repos/frontend.md](project-bible/repos/frontend.md): the rules specific to this repository.
3. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md) (`frontend-patterns.md`).

Screens, their states and their bindings are served by ADAM at the release tag: pull a ticket with `/ticket <id>`.
