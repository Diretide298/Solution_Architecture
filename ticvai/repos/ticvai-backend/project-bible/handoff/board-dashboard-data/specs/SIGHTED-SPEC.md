# Sighted re-check — full access, no restrictions

An earlier pass judged these rows **blind**: it saw only the extracted requirement and the
five matrix rows a lexical search proposed. That search was weak, so the blind pass
produced false gaps. Your job is to find them.

**You have full access.** Read the whole matrix, the repository, the design packs, the
contracts, the screens, any handoff note. Grep freely. Nothing is off limits.

## Your input

One JSONL file. Each row is a requirement the blind pass scored **Absent**, or scored
**Partial with High severity**. Each carries `blind_verdict`, `blind_rationale` and
`blind_matrix_ids` so you can see what it concluded and why.

## The two questions, kept separate

**Question 1 — does the matrix actually require this?**

The blind pass only ever saw five candidate rows. You can see all 3,184. Search properly:

- `scratchpad/sighted/matrix-full.txt` — every matrix requirement, full text, one per
  line, tab-separated `id / domain / sub-domain / text`. Grep it hard.
- Search by **concept and synonym**, not by the requirement's own wording. If the row is
  about "re-entry cooldown", grep for `re-entry`, `anti-pass`, `passback`, `cooldown`,
  `time elapse`, `exit`. The matrix rarely uses the same words as the design packs.
- Long matrix rows bury things. Many are lists — "Required Reports" followed by twenty
  names. Read the whole line.

**Question 2 — is it covered anywhere else in the project?**

Even where the matrix is silent, the thing may already be designed or contracted. The
repository root is `D:\Chinmay\adam\ticvai`. Useful places: `contracts/`, `screens/`,
`flows/`, `events/`, `states/`, `handoff/`, `docs/`. If you find it, say where, with a path.

This matters because a gap the matrix misses but the build already covers is a
**traceability** problem, not a scope problem, and they cost very different amounts to fix.

## Judge at the right altitude

The blind pass extracted UI atoms from design packs — a table column, a filter, a button,
a status chip. The matrix is a contract written at capability level. **One matrix row can
legitimately oblige dozens of UI atoms.** "System shall provide procurement dashboards"
reasonably covers the existence of a column on one of them.

So do not demand that the matrix name the atom. Ask whether a tester holding the matrix
would check the thing the requirement asks for. If a matrix row makes the capability
testable and the atom is an ordinary consequence of it, that is **Covered**, not Partial.

Be equally firm the other way: shared vocabulary is not coverage. A row about onboarding
does not cover a board. A row about QR codes refreshing every 30 seconds does not cover a
dashboard refreshing every 30 seconds.

## Output — one JSON object per input row, same order

```
uid                  copy through unchanged
blind_verdict        copy through unchanged
verdict              Covered | Partial | Absent | Not a requirement
matrix_req_ids       comma-separated real matrix ids, "" if none
where_else           path(s) in the repo that cover it, "" if none or not checked
evidence             the matrix text or file content that justifies your verdict, <= 300 chars,
                     quoted. This is the point of the exercise - show the thing you found.
rationale            ONE sentence saying why the verdict is what it is
gap_severity         High | Medium | Low | ""   (blank when Covered / Not a requirement)
changed              "yes" if your verdict differs from blind_verdict, else "no"
searched             what you actually grepped for, briefly - so a human can judge the search
```

## Rules

1. **Never cite a matrix id you have not read the full text of.** Every id you write must
   be one you looked up in `matrix-full.txt`.
2. Quote real text in `evidence`. An assertion without the quote is not usable.
3. Work every row. No sampling.
4. If after a genuine search nothing covers it, `Absent` is the right answer and a valuable
   one — it is now an Absent somebody actually looked for.

## Final message back to your caller

Rows processed, how many changed and in which direction, how many you resolved via the
repository rather than the matrix, and the three or four most consequential finds with
their matrix ids or file paths. Nothing else.
