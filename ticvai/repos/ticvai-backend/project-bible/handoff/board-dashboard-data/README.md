# board-dashboard-data

Machine-readable output of the board and dashboard requirements run, 22 September 2026.
Written here so the work does not have to be repeated — re-deriving `extracted.jsonl`
means visually reading 48 board pages again.

The prose summary is `../board-dashboard-requirements.md`.
The spreadsheet is `../TICVAI_Board_Dashboard_Requirements.xlsx`.

## Files

| File | Rows | Size | What it is |
|---|---|---|---|
| `extracted.jsonl` | 7,819 | 5.8 MB | **The expensive one.** Every requirement read from the 27 MoMs, 2 dashboard specs and 7 board packs, with a verbatim evidence quote, source, section/page, category, surface, persona, module and confidence. |
| `verdicts-blind.jsonl` | 7,019 | 2.4 MB | The blind adjudication: verdict, matrix ids, rationale, gap severity, reviewer note. `pass` says whether a row came from the first adjudication or the full-text re-judgement. |
| `matrix.jsonl` | 3,184 | 1.0 MB | The client matrix parsed from `Ticvai_matrix_20260621_2.xlsx`, Functionality sheet, one object per row. |
| `matrix-full.txt` | 3,184 | 0.6 MB | The same matrix as one greppable tab-separated file, full text, nothing trimmed. Use this to search the matrix. |
| `candidates.jsonl` | 7,819 | 15 MB | TF-IDF candidate matches, top 6 matrix rows per requirement. **Regenerable in seconds** — delete it if the size is a nuisance and rebuild with `scripts/match.py`. |
| `findings.jsonl` | 25 | 25 KB | The verified source and matrix defects, each with what was found, why it matters and a suggested action. |
| `pack-coverage-claims.jsonl` | 12 | 10 KB | The Ticket Types pack's own "Matrix Coverage:" header claims, expanded and checked. |
| `board-inventory.txt` | ~1,058 | 57 KB | Every named board, dashboard and screen found, with source file and page. |

## Field notes

`extracted.jsonl` — `uid` is the join key used everywhere (`MOM-0001` … `MOM-7819`).
`bd_scope` is `Direct` / `Indirect` / `Not` — board or dashboard bearing. `confidence`
matters only for rows from the image-only packs, where it records how legibly the label
could be read; **no label was invented**, so `Low` means the surrounding requirement was
recorded without the illegible detail.

`verdicts-blind.jsonl` — join on `uid`. `verdict` is `Covered` / `Partial` / `Absent` /
`Not a requirement`. The 800 rows with `bd_scope = Not` are absent from this file by
design: they were not assessed.

## Two things to know before using the verdicts

**These verdicts understate coverage.** Two causes, both measured:

1. The first adjudication pass saw matrix text trimmed to 260 characters, which hid the
   tails of 213 long rows — mostly "Required Reports" lists. 1,000 affected rows were
   re-judged against full text; 52 changed and **every one moved upward**. Those rows have
   `pass = re-judged-full-text`.
2. TF-IDF retrieval is weak here because both corpora share vocabulary. True matches
   sometimes scored near zero while false friends ranked first. Adjudicators compensated
   where they could and left a `adjudicator_note`.

So `Absent` means *not evidenced by this method*, not *proven absent*. Verify by hand
before quoting any individual Absent row to a client.

**The two sides are different units.** The board packs yielded UI atoms — a column, a
filter, a button. The matrix is a capability-level contract. One matrix row can legitimately
oblige dozens of atoms, which is why `Partial` dominates and why a low `Covered` percentage
is partly an artefact of the comparison rather than a finding about the contract.

## Rebuilding

`scripts/` holds every script used, in pipeline order. They were written for this run and
use no project tooling. `specs/` holds the instructions each agent group was given — these
are the substance of the method, more than the scripts are.

```
extract.py      MoM .docx  -> text
extract_pdf.py  spec .pdf  -> text
render.py       board .pdf -> PNG at 170 dpi          (the 5 packs with no text layer)
dump_matrix.py  matrix .xlsx -> matrix.jsonl
merge.py        agent outputs -> extracted.jsonl
match.py        extracted + matrix -> candidates.jsonl
chunk.py        candidates -> adjudication chunks
recheck.py      rebuild truncated rows with full text
claims.py       check the packs' own coverage claims
build_excel.py  everything -> the workbook
```

Counts to check a rebuild against: **7,819** extracted, **7,019** adjudicated, **3,184**
matrix rows, **1,000** re-judged, **52** changed.

The agent work is not reproducible from the scripts alone — it took 43 agent runs (13 blind
extraction, 24 adjudication, 6 re-judgement) driven by the prompts in `specs/`.
