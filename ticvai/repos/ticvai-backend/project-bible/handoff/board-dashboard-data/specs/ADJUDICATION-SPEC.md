# Adjudication — does the requirements matrix already cover this?

The blind stage is over. You are now the *checker*. You are given requirements that were
extracted from meeting minutes and board/dashboard design packs, each paired with the
handful of matrix rows a lexical search thought were closest. You decide, row by row,
whether the client's requirements matrix already covers it.

## What you are given

One JSONL chunk file. Each line:

```
uid             our id for the extracted requirement
requirement     the extracted requirement sentence
module/surface  where it belongs
category        what kind of requirement it is
bd_scope        Direct | Indirect | Not  (board/dashboard bearing)
source_file     which meeting or board pack it came from
evidence_quote  the verbatim source text behind it
candidates[]    up to 6 matrix rows: matrix_req_id, domain, subdomain, text, score
```

`score` is raw lexical overlap. **It is a hint, not an answer.** A high score can pair two
unrelated requirements that share vocabulary; a low score can sit on a genuine match worded
differently. Judge the meaning, never the number.

## The verdict

- `Covered`      — a candidate matrix row requires substantially the same thing. The
                   matrix would make a tester check what this requirement asks for.
- `Partial`      — the matrix gestures at the area but omits the specific thing being
                   asked. Typical: the matrix says "provide a dashboard", the source
                   specifies the eight tiles on it. **This is the most common honest
                   verdict for board and dashboard detail — do not round it up to
                   Covered, and do not round it down to Absent.**
- `Absent`       — nothing in the candidates covers it, and from what you can see of the
                   matrix's shape, nothing plausibly would.
- `Not a requirement` — on review the extracted row is a process note, a pleasantry or an
                   artefact of extraction, and should not be scored at all.

## Fields to write, one JSON object per line

```
uid              copy through, unchanged
verdict          Covered | Partial | Absent | Not a requirement
matrix_req_ids   comma-separated matrix Requirement IDs you matched, e.g. "8.7.3, 8.9.1"
                 ("" for Absent / Not a requirement)
matrix_domain    the domain of the best match, "" if none
rationale        ONE sentence. For Covered, say which candidate and why it suffices.
                 For Partial, say precisely what the matrix leaves out.
                 For Absent, say what kind of requirement is missing.
gap_severity     High | Medium | Low | ""  (blank when Covered or Not a requirement)
                 High   = a board/dashboard cannot be built or signed off without it,
                          or it implies architecture (data, refresh, retention, access).
                 Medium = real scope the matrix does not oblige, buildable late.
                 Low    = detail, cosmetic, or safely inferred from a covered row.
adjudicator_note "" unless something needs flagging to a human — a matrix row that
                 contradicts the source, a duplicate matrix reference, an ambiguity
                 worth raising at sign-off.
```

## Rules

1. Decide on the text in front of you. **Do not go looking at the repository, the matrix
   file, the source documents, or the web.** Everything you need is in your chunk file.
2. Never mark `Covered` on the strength of a shared word. A matrix row about "onboarding"
   does not cover a requirement about "a board".
3. A matrix row may legitimately cover several extracted rows. Reuse ids freely.
4. Be exact with `matrix_req_ids` — they are the traceability the client will audit.
5. Work through **every** line of your chunk. No sampling, no "and so on".

## Final message back to your caller

The chunk you processed, rows written, the verdict split, the gap_severity split, and up
to five rows you found genuinely hard to call. Nothing else.
