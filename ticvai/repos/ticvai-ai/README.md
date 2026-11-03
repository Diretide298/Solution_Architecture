<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/ticvai-ai.md: edit that file, not this one. -->

# ticvai-ai

Python 3.12 / FastAPI. The AI runtime: a separate runtime, scaling profile and compliance boundary from the .NET core.
It belongs to the AI engineers, with its vector store, its schema migrations and its API.

## What is here

| Path | What it holds |
|---|---|
| `src/ticvai_ai/` | The service |
| `pyproject.toml` | The package and its dependencies |
| `.gitlab-ci.yml` | The pipeline |
| `project-bible/` | The TICVAI knowledge base, copied in: never edit it here |

## Start here

1. [AGENTS.md](AGENTS.md): what to read first, and the hard rules.
2. [project-bible/repos/ai.md](project-bible/repos/ai.md): the rules specific to this repository.
3. [project-bible/setup/quickstart.md](project-bible/setup/quickstart.md), then the setup standards indexed in
   [project-bible/setup/README.md](project-bible/setup/README.md) (`llm-conventions.md` for an AI engineer).

The specification is served by ADAM at the release tag: pull a ticket with `/ticket <id>`.
