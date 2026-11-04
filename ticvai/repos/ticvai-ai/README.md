<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/ticvai-ai.md: edit that file, not this one. -->

# ticvai-ai

Python 3.12 / FastAPI. The AI runtime: a separate runtime, scaling profile and compliance boundary from the .NET core.
It belongs to the AI engineers, with its vector store, its schema migrations and its API.

## Where the code is

**Not here.** The team's repository is GitLab `ticvai/ticvai-ai`; an AI engineer's folder is a clone of it with ADAM's
files added by the setup zip. The package keeps no copy of the code (the lead, 3 November 2026: "Retire the code
trees"; CHG-R14J-002).

## What is here

| Path | What it holds |
|---|---|
| `CLAUDE.md` | The rules the setup zip gives an AI engineer's folder, copied from ADAM's starter |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [CLAUDE.md](CLAUDE.md): what to read first, and how a ticket is worked through ADAM.
2. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md) (`llm-conventions.md` for an AI engineer).

The specification is served by ADAM at the release tag: pull a ticket with `/ticket <id>`.
