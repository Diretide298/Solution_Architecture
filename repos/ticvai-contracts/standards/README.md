# TICVAI Engineering Standards

Binding across all five repositories.

| Document | Covers |
|---|---|
| [`NOMENCLATURE.md`](NOMENCLATURE.md) | One concept, one name — glossary → contract → schema → code → UI. Canonical domain terms, case conventions, identifiers, banned words |
| [`CODING_STANDARDS.md`](CODING_STANDARDS.md) | C#, TypeScript, Python, SQL, Terraform. Testing, review, commits |
| [`API_DESIGN.md`](API_DESIGN.md) | Contract conventions, TICVAI extensions, versioning, error taxonomy |
| [`AI_AUTHORSHIP.md`](AI_AUTHORSHIP.md) | Provenance via git trailers, accountability, elevated-review areas |

## Why these live in `ticvai-contracts`

Under the hybrid repository model, this repo is the only artefact every other repo pins
and consumes. Standards versioned alongside the contract are standards every team already
has checked out. A separate standards repo is one more thing to remember to read.

## Enforcement

Standards a human must remember are standards that decay. Almost everything here is
enforced mechanically:

| Standard | Mechanism | Blocking |
|---|---|---|
| Banned types and members (C#) | `BannedSymbols.txt` + `BannedApiAnalyzers` | **Compile error** |
| Module boundaries (C#) | `Ticvai.ArchitectureTests` | **Build failure** |
| Module boundaries (TS) | `@nx/enforce-module-boundaries` | **CI** |
| Permission string drift | Generated enum, single source | **Compile error** |
| Contract breaking changes | `oasdiff` | **CI** |
| API naming | Redocly ruleset | **CI** |
| Case conventions | `.editorconfig`, ESLint, Ruff | **CI** |
| Type strictness | `TreatWarningsAsErrors`, `tsconfig strict`, mypy strict | **CI** |
| Terraform validity | `fmt` + `validate` | **CI** |
| Canonical domain terms | Glossary review | Gate 1 contract review |
| Commit trailers | `commit-msg` hook, non-blocking | Review |

## Changing a standard

PR to this directory, reviewed by Architecture. Where a standard is mechanically enforced,
the change includes the enforcement update in the same PR — a rule the tooling does not
know about is a suggestion.
