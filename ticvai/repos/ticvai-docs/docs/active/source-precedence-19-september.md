# Source precedence — which document wins, and what to build from when they are all silent

> **Owner:** Chinmay · **Decided:** 19 September 2026 · **Status:** governing
>
> Replaces six separate coverage reports with one rule. Today produced three lexical matchers —
> RFP, Ch03, and the pack triage — each with its own false positives, all answering the same
> question differently. **Three tools disagreeing is not three answers, it is none.**

---

## The rule

```
MoM  >  boards  >  specifications        and where all three are silent, the matrix
```

**MoM trumps all.** A minute is rank 1 and a later minute supersedes an earlier one. Where a MoM
has decided something, no board, specification or matrix row reopens it.

**Where the MoM is silent, the board decides** — it is the client's own screen-by-screen layout.

**Where both are silent, the specification decides** — the RFP is rank 2 and says what was asked
for.

**Where all three are silent, build from the matrix.** The matrix is 3,184 contracted requirements
and it is the only source that is exhaustive. A capability nobody drew a board for and no minute
discussed is still scope if the matrix carries it.

### What this settles that was open this morning

| question | answer under the rule |
|---|---|
| Access control vendors — RFP names five, MoM names two | **MoM.** HID and Suprema; the rest staged |
| Wallet screens — gaming pack built first, wallet pack arrived later | **MoM 27 Aug** backs the wallet pack; the five configuration screens are superseded |
| Seatmap Management, Gamification — named by RFP and Ch03, drawn by nothing | **matrix**, if no board and no minute covers them |
| Ch01–Ch09 | **not a source at all.** Ours, retired to `sources/legacy/` |

---

## The matrix route exists, and it is two hops rather than one

**Nothing builds a screen from a matrix row, and nothing needs to.** The path already runs through
the contracts:

```
matrix row  ->  handoff/traceability.json  ->  contract operation  ->  generate-screens-from-contracts.py
```

`check-traceability.py` walks all 3,184 rows and PASSes today:

| verdict | rows |
|---|---:|
| `CONTRACTED` | **2,647** |
| `PARKED` | 396 |
| `GAP_CONTRACT` | 93 |
| `CONTRACTED_PARTIAL` | 43 |
| `GAP_DECISION` | 5 |

So a matrix row that is `CONTRACTED` already names an operation that exists. **The fallback is
therefore bounded and countable**, not open-ended:

```
operations defined in contracts : 1,630
operations reached by a screen  : 1,386
operations reaching NO screen   :   244
```

**Those 244 are the matrix fallback.** They are contracted, traceable to a requirement, and no
screen calls them — which is the precise definition of *the matrix says build it and nothing has*.
The figure was 245 on 9 September, so it has not moved in ten days.

**136 rows cannot produce a screen by any route** — 93 `GAP_CONTRACT` and 43
`CONTRACTED_PARTIAL` have no operation or only part of one. Those are contract work before they are
screen work, and the rule does not reach them.

---

## What the rule does not decide

**It orders the sources; it does not say a screen exists.** Two screens can each cite a MoM and
still be the same screen, which is what step 2 of the ingestion runbook is for. Precedence answers
*whose version wins*, not *how many there are*.

**It does not make a lexical matcher right.** The three coverage reports stay useful as review
queues and none of them is a verdict. A capability reading as *thin* under a rare-word match may
simply be named differently.
