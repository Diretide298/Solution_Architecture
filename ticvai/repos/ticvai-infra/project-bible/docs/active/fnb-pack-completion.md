# The F&B pack — what is done, and the one thing that is not

**As of 24 August 2026.** Every operation the client F&B hi-fi pack names is accounted for. One
join is not, and this says why it is not being automated.

---

## Done

**Operations — 210 of 210.** 74 exist in the contracts, 37 resolve to an operation under another
name, 99 are panels mapped to a real read. `fnb` grew from 50 operations to 96.

**Tables — 13 added.** Temperature logs, corrective actions, cold chain, combos and slots, sub
bills, kitchen exceptions, 86 events, count lines, substitution rules, production plans, and the
two suggestion tables.

**States — `corrective-action` written.** `actioned` is deliberately not terminal, because the
obvious model closes at *action taken* and produces a year of unsigned entries nobody notices until
an inspection.

**Flows — four.** Food safety (F28), table service (F29), stock counting (F30), menu lifecycle
(F31). `fnb` operations named by a flow went from 11% to 33%.

**Screens — 78% of `fnb` operations reach one**, up from 49%. The gap was not missing screens; it
was that **the contract grew this week and the screens had not caught up.**

---

## Not done: no frame maps to a screen

The pack draws **62 frames**. The package has **46 screens on the `fnb` module** plus F&B panels
living on P08, P16, P02 and P04 by the placement rule.

**`board-panel-map.json` maps operations. Nothing maps `FNB-3A` to `KIT-001`.**

### Why this is not being derived

**It was tried and it produces plausible nonsense.** Matching frames to screens by shared
operations resolves 37 of 62, and the matches are unreliable in exactly the way that is hardest to
notice: `FNB-1B Outlet Management` matches `KIT-001 Kitchen Operations Command Center` on one
shared operation out of four. **A reader who trusts that table is worse off than one who has no
table.**

Two earlier attempts failed the same way. Matching screen names gave *Table & Seating Configuration
→ Auto-Scaling Configuration* at 0.84 similarity. Matching on operations let `getDashboard` link a
kitchen board to a security console — **98 operations appear on eight or more screens and cannot
carry a match.**

**The pattern is consistent enough to state as a rule: a mapping between two human-authored
artefacts cannot be derived from their overlap.** The overlap is real and it is not evidence.

### What it needs instead

**A person reading the pack beside the screens, one board at a time.** Six boards, ten frames each,
and the judgement is quick per frame — *this is BO-045 improved*, *this is new*, *this is three
panels of ANL-004*. It is an hour of work and it cannot be an algorithm.

**Do it board by board and record the verdict per frame**, the same shape as
`board-operation-aliases.json`. That file exists because seven times in four days a board operation
looked missing and was not, and the frame mapping will have the same property.

---

## What a frontend team can do today without it

**Everything except pick a screen.** For any frame:

- The traceability block on the frame names its operations
- `board-operation-aliases.json` resolves any that look missing
- `board-panel-map.json` gives the shape and the real operation for every read
- The screen files carry `requiresModule`, `entryState` and the states

**What is missing is the sentence *this frame is that screen*** — and until somebody writes it, a
developer starting from a frame has to find the screen by reading both.

---

## One open question from F31

**What happens to a scheduled menu publish when its draft is edited before the date?**

The obvious answer is that the schedule carries the version rather than the menu, so a later edit
makes a new draft and leaves the schedule alone. **It is not stated anywhere**, and a venue that
edits a scheduled draft expecting the change to land is a venue publishing something it never
reviewed.
