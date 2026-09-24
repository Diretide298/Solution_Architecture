# Resolving "Partial" — does the build already specify it?

Every row in your file was judged **Partial**: the matrix obliges the capability, but not
the specific thing the source asks for — a named column, a status vocabulary, a scope
level, a tile, a threshold.

"Partial" on its own is not actionable. A project manager cannot tell from it whether to
open a ticket or file a note. **Your job is to split it into three.**

You have full access: the whole matrix, the repository, contracts, screens, states, flows,
docs. Grep freely.

## The three outcomes

**`Covered`** — on a proper reading, the matrix does oblige this after all. The blind pass
only ever saw five lexically retrieved candidate rows and routinely missed the right one.
Search the concept and its synonyms across `matrix-full.txt` before accepting the verdict
you were given. A capability-level row legitimately covers an ordinary consequence of it:
"provide procurement dashboards" covers a column existing on one.

**`Traceability`** — the matrix does not oblige the detail, **but the build already
specifies it**. The status vocabulary is an enum in a contract; the field is on a schema;
the override level is in a state machine; the screen exists with an ID. Nothing needs
building. What is needed is a register entry pointing the matrix row at the artefact.
**This is expected to be the largest group** — cite the exact path, and a line number or
schema/field name where you can.

**`Specification`** — neither the matrix nor the build pins it down. Somebody has to decide
the value set, the threshold, the scope or the field list before it can be built or tested.
This is real remaining work, so be strict: only choose it after you have actually searched
the repository and come up empty.

## Where to look

- `scratchpad/sighted/matrix-full.txt` — all 3,184 matrix rows, full text, greppable
- `D:\Chinmay\adam\ticvai\contracts\` — spine and satellite OpenAPI contracts. Enums,
  schemas and required fields live here; this is where most status vocabularies and field
  lists will be found.
- `D:\Chinmay\adam\ticvai\screens\` — screen definitions with IDs, and `_components.yaml`
  for platform-wide patterns (pagination, chart states, table behaviour)
- `D:\Chinmay\adam\ticvai\states\` — state machines and their allowed transitions
- `D:\Chinmay\adam\ticvai\flows\`, `events\`, `docs\architecture\`, `docs\adr\`

Search by **concept, not by the source's wording**. The design packs and the project use
different vocabulary — the packs say "store", the project says `Outlet`; the packs say
"86", the contract says `EightySixEvent`.

## Output — one JSON object per input row, same order

```
uid              copy through unchanged
outcome          Covered | Traceability | Specification
verdict          Covered | Partial      (Covered for the first, Partial for the other two)
matrix_req_ids   the matrix ids that oblige it, "" if none
build_path       file path, plus line/field where you can, "" if none
evidence         the matrix text, enum, schema or screen line that settles it, <= 300 chars,
                 quoted. An outcome without evidence is not usable.
rationale        ONE sentence.
remaining_work   for Specification only: what precisely has to be decided. "" otherwise.
gap_severity     High | Medium | Low | ""   (blank when outcome is Covered)
searched         briefly, what you grepped - so a human can judge the search
```

## Rules

1. Never cite a matrix id or a file path you have not opened and read.
2. `Traceability` requires a real path. If you cannot name one, it is `Specification`.
3. Rows in your file are grouped by module on purpose — open the relevant contract once and
   answer many rows from it, rather than searching per row.
4. Work every row. No sampling.

## Final message back to your caller

Rows processed, the Covered / Traceability / Specification split, the two or three contracts
or screens that resolved the most rows, and the handful of genuine `Specification` items
that a human should see. Nothing else.
