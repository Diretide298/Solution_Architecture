# Answers — the two decisions

**8 September 2026.** Checked against the repo rather than argued from the options.

---

## 1 · `wireframe.status` versus the boards

### The field is already out of contract

`screens/_schema.yaml` line 218 declares:

```yaml
wireframe:
  type: object
  properties:
    status: { type: string, enum: [notStarted, inProgress, review, approved] }
    figmaNodeId: { type: string }
    owner: { type: string }
```

**`designed` and `generated` are not in that enum.** Grepping all 15 platform files for the four
legal values returns `notStarted` and nothing else — `inProgress`, `review` and `approved` appear
on zero screens across 1,091. So every non-`notStarted` value in the package is illegal under its
own schema, and `check-package` passes, which means nothing validates this block at all.

`wireframe.board` and `wireframe.workshopBoard` are not declared properties either. The 590
`workshopBoard` refs and every `board:` anchor the boards depend on are undeclared fields on a
declared object.

**That is the reason 90 screens drifted without anyone noticing.** Not a missing check on the
join — a missing check on the field.

### It is four numbers from one field, not two

| Tool | Rule | Yields |
|---|---|---|
| `derive-platform-deployment.py:36` | `status == "designed"` | 133 |
| `audit-links.py:194` | `status == "designed"` | "133 of 1091" |
| `derive-platform.py:152` | `status != "notStarted"` | counts `generated` as drawn |
| `build-wireframes.py:446` | `status == "approved"` | **permanently 0** — nothing sets it |

Two derivers already disagree about what *drawn* means from the same field, and one counts a value
the package never writes. The 133-vs-275 gap is the visible part.

### Answer

**Option 3, in two steps, and the schema fix comes first.**

1. **Make `_schema.yaml` describe reality, and make `check-package` enforce this block.** Declare
   `board` and `workshopBoard`; set `status`'s enum to values that exist. Until this lands, any
   fix to the join is a fix on top of a field no one is checking — which is how we got here.
2. **Then replace the coverage flag with the join.** `board-data.js` copied into
   `handoff/board-index.json` on each drop.

**On the dependency you asked about: yes, and it is not the `/tmp/reads.json` problem.** That file
failed because it was scratch, machine-local and unversioned. `board-data.js` is a maintained file
under version control that a person owns; copying it into `handoff/` per drop is the same
arrangement `ref-tais.docx` and `TICVAI_Schema_Reference.xlsx` already have in that folder. The
convention the package objects to is *inputs that do not survive the machine*, not *inputs owned
elsewhere*.

**On the cost you flagged — losing the ability to mark a screen designed before a board exists:**
the enum already carries `inProgress` and `review` for exactly that, and nothing uses them. So keep
`status` for **intent** on its legal enum, and derive **coverage** from the join as a separate
field. One field carrying both intent and fact is what drifted for 90 screens.

---

## 2 · `handoff/board-panel-map.json`

### What generated `/tmp/reads.json`

It supplied one thing: `panel name → the board frames it appears on`. Every piece of judgement in
the artefact — shape, `servedBy`, the note — is the `MAP` dict **inside
`tools/derive-board-panel-map.py`**, roughly 110 entries, in the package and under version control.

So the scratch file was a panel-to-frame extract taken off the client F&B board files, and **it is
reproducible: the boards are the source.** Nothing irreplaceable was in `/tmp`.

### Whether anything reads the map

**Nothing in `tools/`.** The deriver's own line 238 reads the existing map into a local `boards`
and never uses it — dead code, and the reason the freeze looks deliberate.

Two documents cite it as a deliverable:

- `docs/active/fnb-pack-completion.md`: "`board-panel-map.json` gives the shape and the real
  operation for every read"
- `docs/active/design-pack-ingestion-audit.md`: defines **Panel-mapped** by reference to it

The consumer is a person reading the handoff pack — a frontend team with four operation names on a
board and no way to know which endpoint serves each. **So option 3 is out.**

### Answer

**Option 1, and it is smaller than it looks.** Re-extract panel→frames from the F&B boards into
`sources/board-reads.json`, point the deriver at it, delete the `/tmp` branch and the dead
`boards` read. No judgement has to be reconstructed.

### Three things found while checking

- **`"generated": "24 August 2026"` is a hardcoded literal in the output.** Even a successful run
  stamps 24 August. The artefact's own date has been unreliable independently of the freeze —
  option 2 would have written an honest note next to a dishonest field.
- **The docstring says five `build` panels; the dict has four** — `verifyAllergens`,
  `setSubstitutionRules`, `buildProductionPlan`, `releaseProductionPlan`. The `shapes` note in the
  output says four. One of the two is wrong in the deliverable.
- **`releaseProductionPlan` corrects my own §5.** `notes/ops-review-2026-09-08.md` filed it as a
  `release`-means-let-go-of-a-hold false positive. The map is explicit that it is *"a plan becomes
  production runs… separate from building it because a plan is edited before it is released"* —
  which is a publish. **Real gates are 35, not 34**, and BO-136 needs `publishGate`. It also
  strengthens the recommendation there: `release` now demonstrably means both things in one
  package, so the eleven hold-releasing operations should be renamed rather than pattern-excluded.

---

# Phase A verification — answers to the three open items

**8 September 2026, later.** Settled from the documents first, then **measured against the patched
source** once the folder was linked (§6). Where the two differ the measurement wins, including
against my own §3 figure.

## 3 · The gate: BP-001 is **335**. Both documents are stale, and so was my first answer.

`build-plan.md:60` says the boards read BP-001 at 331. They do — and that figure is downstream of
the hand count, not independent of it:

```js
// pattern-data.js
BP-001: { screenCount: 331 }
FOLDED_FROM_BP010 = { screenCount: 17 }   // "The 17 screens BP-010 held before the fold"
```

314 + 17 = 331. `phase4-patch.md:66` says the same thing for the same reason. Both descend from the
hand count, so neither is independent of it. The three-screen gap is exactly `BO-020`, `BO-021` and
`BO-045` — the ids the first count missed by looking at three modules instead of the platform.

**But 334 was wrong too, and it was mine.** It is 314 + 20, and **the base measures 315**, not 314.
Counting the BP-001 signature — `template: split` carrying `dataTable`, `detailPanel` and
`searchField` — across the pre-patch snapshot returns 315, and across the patched source **335**,
with 20 added and none removed. So the figure the regeneration is checked against is measured, not
derived: **335**. `build-plan.md:60` and `atlas-handoff.md:50` should both be corrected to it.

**Corrected expectation. Exactly two numbers move:**

| | Before | After |
|---|---|---|
| `BP-001.screenCount` | 331 | **335** |
| `FOLDED_FROM_BP010.screenCount` | 17 | **20** |
| pattern count | 43 | **43** |
| P08 | 362 of 363 | **363 of 363** |
| P08 `BP-001` share | — | **192** |

**The pattern count stays 43.** `atlas-handoff.md:28` says 44 → 41, but 41 assumes `BP-023` and
`BP-024` dissolve when `scanTarget` is corrected — that is §2.6, which was not applied. **If the
regeneration reports 41, §2.6 landed and should not have.** Any third number moving is a failed
edit, which is the check working.

## 4 · Coverage is published against the 23-board set.

The repo's 157 boards cannot carry a coverage number. Every one of the 1,091 `wireframe.board`
refs resolving to a real anchor inside them is **referential integrity, not coverage** — the
anchors and the refs were generated from each other, so 100% is true by construction and would
still read 100% if not one frame had ever been drawn. A number that cannot fall is not a measure.

So: **assert it in CI as an integrity check that must stay at 100%, and call it that.** Coverage
means *a person can open a drawn frame for this screen*, and only the 23-board set answers that.
Publish 25% against the 23 boards, with the two named so they cannot be read as the same field
again — the repo set stays the `wireframe.board` resolution check, the join from `board-data.js`
publishes the coverage figure.

This is the last thing retiring the coverage flag was waiting on. §1 above is otherwise satisfied
by what landed: the schema now describes reality and `status` is intent only.

## 5 · `wireframe.provenance` collides with a field that already exists.

`provenance` is already in use one nesting level up, on **128 screens**, meaning *why this screen
exists and where its spec came from*:

```
client board, specified ......................................... 72
client board, named only ........................................ 33
parity gap found 24 August — the web could not do what the app could  11
MoM 10 August 2026 §4.9 .......................................... 5
gap found 24 August — no counter-service F&B on any till ......... 4
MoM 10 August 2026 §4.1 / §4.8 / none — see CF-92 ................ 3
```

`screen.provenance` is the origin of the **specification**; the new `wireframe.provenance` is the
origin of the **drawing**. Two fields with one name, two levels apart, in the same file — and
`P08-venue-back-office.yaml:11642` already carries both. Recommend renaming the new one
`wireframe.origin`. Cheap now, and it is the same class of mistake as one `status` field carrying
intent and fact.

**The 958/133 split reproduces exactly** from the pre-patch snapshot in `handoff/screens/`
(958 `generated`, 133 `designed`, summed per platform), so the preservation claim holds from this
side independently.

---

# 6 · Measured against the patched source

Folder linked as `adam/ticvai/screens`; the fifteen platform files, `_components.yaml` and
`_schema.yaml` are copied to `sources/atlas-verify/` so the checks are re-runnable. Every §2.1–§2.5
claim reproduces.

| Claim | Measured |
|---|---|
| §2.1 fold, 20 screens | **20 added, 0 removed** — `BO-020`, `BO-021`, `BO-045`, `BO-074`–`BO-090`, ids exact |
| §2.1 "114 existing BP-001 screens" | P08 signature now **134** = 114 + 20 ✓ |
| §2.2 `publishGate` on two screens | **`BO-094`, `BO-153` only**, package-wide |
| §2.3 `emptyNoEvents` on 11 | **exactly the 11**, and `emptyFirstRun` is gone from each — key and copy replaced together, as stated |
| §2.4 venue-map trio | `BO-092` list · `BO-093` form + `fileUpload` + `progressIndicator` · `BO-094` **canvas** + `publishGate` ✓ |
| §2.5 re-signatures | `BO-235` carries `dataTable` + `searchField` + `primaryButton`; P08 closes **363 of 363** |
| P08 mislabels corrected | `split` **192** — the prediction lands to the screen |
| `provenance` preserved | **958 generated / 133 designed**, and `wireframe.status` is **notStarted on all 1,091** — every value legal for the first time |
| Schema | all seven `wireframe` fields declared under `additionalProperties: false`; `source`, `note`, `derivedFrom` included, so nothing breaks on strict |

## The CI check needs tightening before it enforces

My own wording — *`template: list` carrying a `detailPanel`* — does not survive the fix it
checks:

- **On P08 it now returns zero.** The 20 screens are `split`, so the query's subject is gone. It
  reproduced the hand list exactly *before* the patch and can never fail again after it. As a
  regression test on the fold it is dead.
- **Package-wide it returns 17 screens, and 15 are not the pattern.** `WEB-036`, `POS-024`,
  `ANL-010` and twelve others are `cardList` + `detailPanel` — a card list with a detail view, not
  `listDetailSplit`. `ACC-006` is a `detailPanel` with **no list component at all**.
- **Tightened to `list` + `dataTable` + `detailPanel` it returns exactly 2**: `WEB-031` and
  `WEB-032`, both genuine, both P01. So **CI check one is not empty on enforce** — P01 is in the
  enforcing set and would fail on these two. Either fold them or warn on P01.

## Two screens carry the §2.1 defect one platform over

One P09 and one P13 screen are `split` + `dataTable` + `detailPanel` with **no `searchField`** —
the same *list with no way to find a row* that §2.1 fixed for twelve of the seventeen. Same
treatment takes BP-001 to 337. Flagging, not applying: outside Phase A's five files.

## §5 sharpens

The collision is now asymmetric. `wireframe.provenance` is declared and **enforced** under
`additionalProperties: false`; `screen.provenance` is undeclared, unenforced, and carries eight
free-text values on 128 screens. Two fields, one name, one validated and one not — a reader cannot
tell which. `wireframe.origin` still the recommendation.

## Unchanged and still to apply

`BO-136` carries `searchField` + `dataTable` and no `publishGate`, so §2 above stands: real gates
are 35, and it is the missing one.

## The extra screen is `ADM-041`

Diffing the regenerated groups against the old ones, the delta is exactly four: `BO-020`,
`BO-021`, `BO-045` — the three the module-scoped count missed — and **`ADM-041 System
Transactional Template Registry`**. Every one of the old 331 still matches the signature, so
nothing was wrong in the file; `ADM-041` was simply never a member of it. `Pattern Boards` cites it
as BP-001's *other reference frame*, which is how it went uncounted: it was read as the example
rather than as one of the screens. That is the 315-not-314 discrepancy, in one id.

## Regenerated

`pattern-data.js`: `BP-001` **335** across P08 · P09 · P10 · P12 · P13, twelve groups, 335 group
entries rebuilt from the source rather than appended to; `FOLDED_FROM_BP010` **20**, now with a
fourth group — `P08 · Food & Beverage`, holding the three missed ids. Pattern count unchanged at
43. Stale prose figures corrected on `Pattern Boards`, `Vocabulary Corrections`, `HANDOFF.md`
(362 → 363 of 363), `build-plan.md` and `phase4-patch.md`.

## Next

Phase 3 ops review on the corrected counts: 35 real gates, `BO-136` the missing one, nine
contract gaps, and the eleven `relinquish*` renames.

---

# Re-checked against the source, later on 8 September

Fresh copy of `atlas/ticvai/screens` into `sources/atlas-recheck/`. **13 of 17 files byte-identical;
four changed.**

## What changed: `publishGate` was applied

+160 lines across P06, P08, P09, P13. **The component is now declared on 34 screens** — exactly
the 35 the operation-keyed rule returns, minus `PTR-010 Cart & Quote`. Zero screens outside the
list. So the two I flagged for confirmation were both decided: `PTR-010` excluded, `CMS-006`
kept. `BO-136` and `BO-066` are both in, which closes the 34-vs-35 question in the source.

Each addition carries `impliedBy` naming the operation that required it —
`publishAnnouncement` ×6, `publishBundle` ×4, `deployConfigurationProfile` ×4,
`publishSupportNotice` ×4, `publishTenantConfig` ×3, `promoteRelease` ×2, and the rest
one-of-a-kind. **The rule reproduced from the declared operation, not the title**, which is what
§5 of the ops review asked for.

Only `PTR-010` remains without the component, and by decision.

## BP-001 is still 335. The reconciliation is not outstanding.

| | |
|---|---|
| BP-001 signature, my 8 September copy | **335** |
| BP-001 signature, fresh copy | **335** |
| Screens added | **none** |

**331 vs 334 was settled on 8 September and both figures were wrong.** 331 was 314 + the
seventeen-screen hand count; 334 was 314 + the corrected twenty. The base measures **315**, so
the answer is **315 + 20 = 335**, and the extra screen has a name — `ADM-041`, which
`Pattern Boards` cited as BP-001's *other reference frame* and was therefore never counted as one
of its screens.

`pattern-data.js` was regenerated to 335 the same day: twelve groups, 335 entries rebuilt from
the source rather than appended, `FOLDED_FROM_BP010` at 20 with a fourth group
(`P08 · Food & Beverage`), pattern count held at 43. `build-plan.md:60`, `phase4-patch.md`,
`Pattern Boards`, `Vocabulary Corrections` and `HANDOFF.md` were all corrected off 331/17/362.
**The regeneration has been checkable against 335 since then, and the fresh source agrees.**

## Still open, unchanged by this pass

- **`wireframe.origin` not renamed.** `wireframe.provenance` still collides with the
  screen-level `provenance` on 128 screens — one enforced under
  `additionalProperties: false`, one undeclared.
- **`_schema.yaml` id pattern is still `^[A-Z]{3}-[0-9]{3}$`**, which every one of the 363
  `BO-` screens fails. Two letters, not three.
- **The two `searchField` gaps are `ADM-240` and `CMS-044`** — and they are two of the five
  §2.5 re-signatures, the two `pattern-data.js` itself says "match BP-001 once BP-010 is folded".
  They are `split` + `dataTable` + `detailPanel` with no `searchField`, so they are routed to
  BP-001 while missing its third component. Adding it takes BP-001 to **337**.
