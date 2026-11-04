<!-- Written by tools/derive-mirrors.py from ticvai/docs/repos/rules/docs.md: edit that file, not this one. -->

# Docs Repo

`ticvai-docs` is a copy, not a source. The package (`ticvai/` in the ADAM repository, served by ADAM at each release
tag) is the source of every folder it shares with the package; `setup/` comes from ADAM's starter docs
(`viewer/mcp/setup/starters/docs/`), the same files the setup zip gives every repository as `project-bible/setup/`.
The package's `tools/derive-mirrors.py` writes all of it at every refresh: never edit it here.

## Placement rule

> **Anything mechanically enforced lives with the code that enforces it.
> Anything narrative lives here, and links to the enforcement.**

`BannedSymbols.txt` lives in `ticvai-backend` (from ADAM's backend starter); the lint configuration lives in each
frontend repository. `setup/naming-and-style.md` explains why and links to them.

## Project bible

Every repository's `project-bible/` is the same copy as this repository. A change to a bible page is a change to its
package source (or, for `setup/`, to ADAM's starter docs), released with the package.

## sources/

Client documents, read-only, organised by authority rank. **Reference-system material is
deliberately not held here** — rank 4, never scope, and storing it beside rank 1 and 2
invites reference behaviour quietly becoming an expectation.
