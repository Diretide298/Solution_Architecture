# Gap coverage — do the backlog entries list every row they answer?

**Written 18 August 2026 after the requirement walk closed, in response to a challenge that
*675 gap references exist, 326 have a backlog entry and 349 do not*.**

## The count is right and the conclusion is the opposite of how it reads

| | |
|---|---:|
| Gap rows in `traceability.json` | **677** |
| Gap rows whose reference appears in some entry's `refs` array | 323 |
| Gap rows whose reference does **not** appear in any `refs` array | **354** |
| Gap rows carrying **no** `backlog` and **no** `cf` field | **0** |

**Every gap row is routed. None is orphaned.** `check-traceability.py` check 6 enforces exactly
this and passes clean — it fails any `GAP_CONTRACT` or `CONTRACTED_PARTIAL` row without a queued
edit, on the stated grounds that *a gap with no queued edit is a gap that gets lost*.

**The 349 is a different measurement.** It compares gap rows against the `refs` arrays *inside*
backlog entries, and those arrays were written as **illustrative citations, not exhaustive**
**indexes**. The routing lives on the traceability row (`"backlog": "BL-053"`), not in the
entry's `refs` list.

## Why the two numbers diverge so far

The widest entries cite far more rows than they list:

| Entry | Rows citing it | Refs listed | Ratio |
|---|---:|---:|---:|
| BL-053 | 75 | 3 | 25× |
| BL-110 | 43 | 9 | 4× |
| BL-143 | 40 | 5 | 8× |
| BL-052 | 38 | 2 | 19× |
| BL-156 | 36 | 8 | 4× |
| BL-013 | 35 | 1 | 35× |
| BL-101 | 34 | 11 | 3× |
| BL-141 | 30 | 9 | 3× |
| BL-040 | 27 | 8 | 3× |
| BL-041 | 25 | 3 | 8× |
| BL-062 | 22 | 2 | 11× |
| BL-063 | 21 | 1 | 21× |

`BL-053` is cited by 75 rows and lists 3. `BL-013` is cited by 35 and lists 1. **The entry is**
**correct and its `refs` array is a sample.**

## Why this still matters

**Reading the backlog alone understates the work by roughly half.** Anyone scoping from
`contract-backlog.md` sees `BL-013` listing one reference and may size it as one requirement;
it answers 35. That is a real estimation hazard, and it is why the clustering pass reports
**row citations rather than entry counts** — CL-02 is 2 entries and 115 row citations.

**The fix is mechanical, not investigative.** The routing already exists on every row, so the
`refs` arrays can be back-filled from `traceability.json` without any judgement. Until that is
done, treat `refs` as *examples* and `traceability.json` as the index.

## What was done about it — 18 August

1. **`refs` back-filled from `traceability.json` on 96 entries.** Unlisted gap rows fell from
   **354 to 17**, and those 17 are correct: each is routed by a `cf` field with no contract edit
   to queue, because the answer is a client decision rather than an artefact change — CF-14,
   CF-51, CF-64, CF-69, CF-83, CF-130, CF-138.
2. **`check-backlog.py` gained `check_refs_complete`.** It fails any entry whose `refs` array
   omits rows that cite it. Verified by truncating `BL-013` to one ref: *refs array omits 34
   row(s) that cite it*. **This class of drift was invisible because both artefacts stayed
   individually valid** — the traceability row named its entry, the entry named some refs, and
   neither was wrong on its own terms.
3. **Row citations, not entry counts,** remain the figure to quote to a client or a planner.

## The unlisted rows, by entry

| Entry | Unlisted gap rows |
|---|---:|
| BL-110 | 31 |
| BL-013 | 23 |
| BL-101 | 23 |
| BL-041 | 22 |
| (cf only) | 17 |
| BL-040 | 17 |
| BL-155 | 14 |
| BL-170 | 13 |
| BL-156 | 12 |
| BL-057 | 11 |
| BL-152 | 10 |
| BL-157 | 10 |
| BL-054 | 9 |
| BL-171 | 9 |
| BL-062 | 8 |
| BL-058 | 8 |
| BL-052 | 8 |
| BL-160 | 8 |
| BL-173 | 8 |
| BL-027 | 7 |
| BL-175 | 7 |
| BL-039 | 6 |
| BL-080 | 6 |
| BL-063 | 5 |
| BL-141 | 5 |
| BL-029 | 3 |
| BL-012 | 3 |
| BL-072 | 3 |
| BL-081 | 3 |
| BL-035 | 3 |
| BL-076 | 3 |
| BL-121 | 3 |
| BL-140 | 3 |
| BL-150 | 3 |
| BL-166 | 3 |
| BL-100 | 2 |
| BL-114 | 2 |
| BL-073 | 2 |
| BL-177 | 2 |
| BL-016 | 1 |
| BL-070 | 1 |
| BL-103 | 1 |
| BL-075 | 1 |
| BL-066 | 1 |
| BL-129 | 1 |
| BL-034 | 1 |
| BL-134 | 1 |
| BL-118 | 1 |
| BL-091 | 1 |
| BL-116 | 1 |
| BL-102 | 1 |
| BL-122 | 1 |
| BL-135 | 1 |
| BL-146 | 1 |
| BL-123 | 1 |
| BL-042 | 1 |
| BL-133 | 1 |
| BL-172 | 1 |

**354 rows across 58 entries.** All routed; none lost.
