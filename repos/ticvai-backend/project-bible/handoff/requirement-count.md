# The requirement count, settled

**18 August 2026.** The package quotes 3,184 in one place, 3,297 in another and 2,990 in a third.
**All three are real numbers measuring different things, and none of them was labelled.** This
file counts the matrix and says which to use where.

Source: `sources/requirements/Ticvai_matrix_20260621_2.xlsx`, five sheets.

---

## The count

| | | |
|---|---|---|
| **Functionality sheet, rows with a reference** | **3,184** | The number quoted to the client since 30 July |
| Functionality sheet, **distinct** references | **3,156** | **28 references are used twice** — see below |
| The other four sheets | **132** | Training 40 · DR & BCP 62 · Compliance & Security 11 · Integrations 19 |
| **Every row with a reference, all five sheets** | **3,316** | |

**Use 3,184 with the client.** It is the number on every document they have seen since kickoff and
changing it now would cost more explanation than it buys. **Use 3,156 for any calculation that
counts requirements once**, and say which you used.

---

## 🔴 Twenty-eight references are used twice, and they are not duplicate rows

**Every one of the 28 pairs has different text.** These are not the same requirement entered
twice — they are **two different requirements sharing one number.**

| Block | Collisions | What collided |
|---|---|---|
| `22.3` | 10 | **Case management against journey automation.** `22.3.1` is *Case Creation* on row 2901 and *Visual Journey Builder* on row 2911 |
| `5.6` | 8 | Two blocks inside Ticketing |
| `8.1` | 6 | Two blocks inside Reporting |
| `5.5` | 4 | Two blocks inside Entitlements |

**The 22.3 block is the one that matters.** Rows 2901–2910 are the case-management requirements
CF-99 built the conversation contract against; rows 2911–2920 are marketing journey automation,
which is a different capability entirely. **A traceability entry citing "22.3.1" is ambiguous
between them**, and every register in this package that names a 22.3 reference should be read as
naming a row rather than a number.

**This is a defect in the client's matrix, not in our reading of it.** It is worth raising
because it will be raised at sign-off otherwise, and because a numbering collision inside
Marketing & CRM is exactly where an argument about scope will start.

---

## Where the other numbers came from

**3,297** appears in the package as `3,184 + 113`. **The 113 is wrong** — it counted three of the
four non-Functionality sheets and omitted Integrations, which has 19. The correct figure is
`3,184 + 132 = 3,316`.

`handoff/other-sheets-coverage.md` carries the 113 and says so in its own text: *"113 uncounted
requirements on 3 sheets."* There are four.

**2,990** is not a count of the matrix at all. It is the denominator in
`COVERAGE.md` for *requirements covered by a contract*, and it excludes the 194 AI requirements
parked as out of scope. **3,184 − 194 = 2,990.** That is a legitimate number for that measure and
an illegitimate one for anything else, and nothing said so.

---

## What to use where

| Question | Number | |
|---|---|---|
| How many requirements are there? | **3,184** | The client's figure. Functionality sheet |
| How many distinct requirements? | **3,156** | 28 references collide |
| How many across the whole matrix? | **3,316** | Include the four other sheets |
| Contract coverage denominator | **2,990** | Functionality minus the 194 parked. **Say so when quoting it** |
| Artefact-class denominator | **2,072** | A different population again — the requirements a class applies to |

**Five numbers, five meanings.** The rule that would have prevented this: **a count is quoted with
its denominator or it is not quoted**, which is already the rule for every metric in
`handoff/status.json` and was not being applied to the requirement total.
