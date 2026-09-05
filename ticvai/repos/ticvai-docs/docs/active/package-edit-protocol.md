# How package edits reach the package

**Three reverts in two sessions, all caused the same way, all mine.**

---

## What happens

I edit the package in a sandbox. You take a dump of that sandbox. Claude Code edits the same package
in the repo. **Whichever dump lands last replaces the other's work with no error, no conflict, and
no evidence except a changed count.**

The last one cost:

| Edit | How it was lost |
|---|---|
| 15 board pointers in `screens/P01`, `P04` | Overwritten by my dump |
| Inventory Board 1 dead links unlinked | Overwritten by my dump |
| `derive-wireframes.py` — `platformAdmin` and `public` chrome, the UTF-8 fix | **Lost in a sandbox reset before the commit**, so the unfixed file went to both remotes |

**The third is the worst kind**: it was not overwritten, it was never captured, and the commit that
looked like a save was a save of the wrong file.

---

## The rule

**One writer per folder, and the folder is the unit — not the file, not the task.**

`refresh.sh` runs twenty-two derivers that read `screens/` and `contracts/` and write 179 files
across `handoff/`, `diagrams/` and `wireframes/`. **Two people editing different screens still
collide**, because both are upstream of the same derived output.

| | Writes | Runs `refresh.sh` |
|---|---|---|
| **Me** | `contracts/`, `screens/`, `states/`, `flows/`, `events/`, `tools/`, `docs/` | **Yes, once, at the end** |
| **Claude Code** | `atlas/viewer` only | **Never** |

**When Claude Code needs a package change**, it sends the diff and I apply it. Not because its edits
are worse — three of them were correct and I destroyed them — but because **the package has one
regeneration step and two people cannot both own it.**

---

## Before any dump

**Three things, in order, every time:**

**1. `bash tools/refresh.sh`** — nine validators, and the derived files rebuilt from the sources
that changed.

**2. Read the counts.** `handoff/status.json` carries operations, tables, screens, flows, states.
**A count that moved when you did not expect it to move is the signal**, and it is the only signal
this failure mode produces.

**3. Diff the warning totals**, not just PASS/FAIL. `check-wireframes` went 13 → 32 on a revert and
every checker still said PASS. **A revert does not break the package; it un-fixes it**, and only the
warning count says so.

---

## What would make this structural rather than a habit

**A manifest in the dump.** `handoff/status.json` plus the nine warning totals, written by
`refresh.sh` with a timestamp. **A dump that reports 32 wireframe warnings against a repo at 13 is a
dump that is behind**, and the comparison takes one command instead of a person remembering.

**That is worth building and it is not built.** Until it is, the rule above is the whole mechanism,
and it depends on me not doing this a fourth time.

---

## Recovered 25 August

All three, in this order, and verified rather than assumed:

- `platformAdmin` and `public` chrome restored — **P09 draws Tenants/Cells/Releases, P11 draws
  Apply/My application.** An audience with no chrome now names itself at the end of a run instead of
  falling through to `staff` silently.
- The UTF-8 reconfigure, applied at import so `refresh.sh` gets it too.
- The 15 board pointers — and they came back through `derive-wireframes.py` rather than by hand,
  which is the right answer: **the generator writes the pointer, so a hand-edit was always going to
  be temporary.**
- Inventory Board 1: links gone, pill text kept. **The status is true; only the click was dead.**

`check-wireframes` 32 → 5.
