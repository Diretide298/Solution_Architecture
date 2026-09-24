# Re-judgement — rows that were scored against truncated matrix text

Read `ADJUDICATION-SPEC.md` in this directory first. The verdict vocabulary, the field
list and the rules all carry over unchanged. This note explains what is different.

## Why these rows are back

The first pass showed each adjudicator at most 260 characters of a matrix requirement.
213 matrix rows are longer than that, and they are disproportionately the ones that
enumerate things — "Required Reports", followed by twenty report names; a capacity rule,
followed by the five levels it applies at. Cut at 260 characters, such a row reads as
though it stops before the item that actually matters.

Real examples of what the trim hid:

- `6.1.67` was cut at "Foreign Cu…". The full row lists **Foreign Currency Sales**.
- `4.3.2` was cut at "Dynamic C…". The full row lists **Dynamic Currency Conversion**.
- `1.1.135` was cut mid-list. The full row lists **Donation Transaction Details**.
- `1.1.10` was cut after "1) Sales Capacity…". The full row also defines **Admission Capacity**.

Every row in your file was previously scored **Partial or Absent** and had at least one
truncated candidate. So the error, if there is one, runs one way: the matrix may cover
more than the first pass could see.

## What is different in your input

Each row carries the usual fields plus:

```
candidates[].text           now the FULL matrix text, not a 260-character extract
candidates[].was_truncated  true if this candidate is one the first pass had cut
previous_verdict            what the first pass decided
previous_matrix_req_ids     what it traced to
previous_rationale          why it said so
```

## What to do

Judge the row again, from scratch, on the full text. Do not defer to the previous
verdict and do not assume it was wrong — most will be right. Read the parts of the
candidate that were previously hidden and ask only: does the matrix, in full, already
require this?

Expect a minority to change. A row changes to `Covered` when the hidden tail of a
candidate turns out to require exactly the thing. A row may also stay `Partial` with a
better matrix id, which is still an improvement worth recording.

## Output

Same seven fields as `ADJUDICATION-SPEC.md`, plus these two:

```
previous_verdict   copy through unchanged
changed            "yes" if your verdict differs from previous_verdict, else "no"
```

Write one object per input row, same order, to the path given in your task.

## Final message back to your caller

Rows processed, how many changed and in which direction (e.g. "31 Partial→Covered,
4 Absent→Partial"), and the two or three most consequential changes with their matrix
ids. Nothing else.
