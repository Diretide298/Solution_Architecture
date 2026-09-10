# Wiring the September pack boards, and collapsing one duplicate

**Decision, 9 September 2026.** Not a derivation — there was nothing to derive from, and this file
exists so that is on the record rather than inferred later from the edges.

## What was wrong

140 screens arrived with the September pack ingest carrying **no navigation whatsoever** — no
`exitTo`, no `entryFrom` — and **no operations**. All wave 3. Every reachability warning in the
package traced to them:

| platform | module | stranded | reachable siblings in that module |
|---|---|---|---|
| P08 Venue Management | Venue Operations | 30 | 15 |
| P09 TICVAI Web | Platform | 50 | 30 |
| P16 Venue Analytics | Analytics | 60 | 10 |

They came from exactly two packs — `Approval_Workflows_and_Governance` (80) and
`Unified_BI_Reporting_and_AI_Analytics` (60).

**They were not screens that had lost their links.** Nothing ever gave them any. On P16 the
stranded outnumbered the wired six to one.

## What could not be used

- **The packs carry no navigation.** A pack entry has `board`, `area`, `number`, `page`,
  `purpose`, `acceptance`, `terms`. There are no edges in it, anywhere.
- **The flows do not reach them.** 10 of the 140 appear in a flow and none of those yielded an
  edge — the 94 flows were written before these packs landed.
- **The module says where they belong but not what they hang off.** Every one sits in a module
  that has reachable siblings, which is why the answer is not "delete them", but a module is not
  a parent.

## What was decided

**The board is the unit.** The 140 fall into 14 board groups of 10, each led by a Command Center,
a Library or a Workspace — the screen the board was drawn around.

1. That lead screen is the **hub**.
2. The hub hangs off the **platform's home screen** — `BO-100 Venue Home`, `ADM-002 Platform
   Dashboard`, `ANL-001 Executive Command Center` — each a real home with 8–9 existing exits.
3. **Children hang off the hub and go back to it**, so a board is navigable rather than a one-way
   list.

139 edges. **This is a convention, not evidence.** A new product area being reachable from the
platform's home screen is the most honest guess available; dressing it as a flow citation would
have been worse than labelling it as what it is.

## The collapse

**`ANL-011 Executive Command Center` was removed, not wired.**

It is name-identical to `ANL-001`, which is P16's entry point. The two are not comparable:

| | `ANL-001` | `ANL-011` |
|---|---|---|
| operations | 4 | 0 |
| exits | 9 | 0 |
| purpose | "across F&B, retail, ticketing and frontline, **filtered by domain**" | "an immediate consolidated view of overall organizational performance" |

The BI pack redrew a screen the platform already had, and the redraw is the poorer of the two. Its
9 siblings attach to `ANL-001` instead. **Its `purpose` and its gap were carried onto `ANL-001`**
as `purposeNote` rather than deleted — the same carry rule the generators follow, for the same
reason: the pack said something the screen did not, and a collapse is not a licence to lose it.

Screen count goes 1,231 → 1,230.

## Left for a person

**`ADM-321 Visual Workflow Designer` duplicates `ADM-241`.** It was wired, not collapsed: unlike
`ANL-011` it is a child rather than a hub, and which of the two should survive is a question about
the workflow designer, not about navigation.

The other known name collisions are untouched and unchanged: `BO-020`/`BO-047`
(*F&B Order Management*) and `BO-031`/`BO-069` (*Asset Register*).

**None of the 140 has a single operation.** They are navigable now and still not buildable — a
screen with no `apis[]` binds to nothing. That is the next thing these need, and it is a larger
piece of work than this one.
