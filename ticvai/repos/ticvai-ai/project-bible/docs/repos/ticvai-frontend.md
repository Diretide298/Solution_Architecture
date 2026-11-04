# ticvai-frontend

The front end is six repositories in the GitLab group `ticvai-frontend`, one app each; the app each one builds is
listed in [project-bible/docs/active/frontend-repos.yaml](project-bible/docs/active/frontend-repos.yaml). The setup
zip makes a workspace holding ADAM's files, and the developer clones their app's repository inside it.

## Where the code is

**Not here.** Each app's code is in its own repository; the shared conventions and the workspace files come from
ADAM's frontend starter (`viewer/mcp/setup/starters/frontend/`). The package keeps no copy of the code (the lead,
3 November 2026: "Retire the code trees"; CHG-R14J-002).

## What is here

| Path | What it holds |
|---|---|
| `CLAUDE.md` | The rules the frontend starter gives every workspace, copied from ADAM's starter |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [CLAUDE.md](CLAUDE.md): the workspace, the rules and how a ticket is worked through ADAM.
2. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md) (`frontend-patterns.md`).

Screens, their states and their bindings are served by ADAM at the release tag: pull a ticket with `/ticket <id>`.
