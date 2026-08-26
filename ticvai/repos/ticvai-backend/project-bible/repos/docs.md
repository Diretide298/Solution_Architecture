# Docs Repo

This repository is the source. Everything else is generated from it.

## Placement rule

> **Anything mechanically enforced lives with the code that enforces it.
> Anything narrative lives here, and links to the enforcement.**

`BannedSymbols.txt` lives in `ticvai-backend`. `.eslintrc.json` lives in
`ticvai-frontend`. `setup/naming-and-style.md` explains why and links to them.

## Project bible sync

    ticvai-docs/project-bible/  --sync-->  <repo>/project-bible/

One-way. Generated files carry a `GENERATED - DO NOT EDIT` header with source path and
content hash. `make bible-check` fails CI on drift.

To change a bible page, change it here and re-run `./sync-bible.sh`.

## sources/

Client documents, read-only, organised by authority rank. **Reference-system material is
deliberately not held here** — rank 4, never scope, and storing it beside rank 1 and 2
invites reference behaviour quietly becoming an expectation.
