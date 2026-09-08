# Phase 4 — apply checklist

**7 September 2026.** Five defects, five files, no schema change. Board side is done;
this is the source side. Full reasoning and the patch blocks are on
`Vocabulary Corrections.dc.html`.

Apply in this order — the vocabulary entries first, so the screen edits validate.

---

## 1 · `screens/_components.yaml` — two additions

**`components:`** add `publishGate`.

```yaml
- kind: publishGate
  description: >
    Making a draft live, with what it will affect named before it happens.
  states: [draft, validating, blocked, publishable, publishing, published, overridden]
  requiredWhen: the screen calls an operation that publishes, deploys or activates
  notes: >
    `blocked` names what is wrong and what to do — a disabled Publish with no reason is
    the state operators escalate. `overridden` is a publish that went past a warning; it
    is recorded, because the person who authorised it is the whole value of the record.
    Saving is not publishing. A gate that shares its button with save will be pressed by
    somebody who meant to save.
```

**`screenStates:`** add `emptyNoEvents`.

```yaml
- key: emptyNoEvents
  required: false
  requiredWhen: the screen renders a timeline it does not write to
  description: >
    The record is complete and nothing has happened yet. No action, and saying so is the
    point: an audit trail that offers to create its first entry is offering to author
    evidence.
```

Name taken from the frame at `Pattern Boards.dc.html#bp-006`, which drew the state before
the defect was found.

**Decision — recommendation, 8 September.** Measured across all 1,091 screens
(`notes/ops-review-2026-09-08.md` §5): the `requiredWhen` as worded fires on **45 screens**,
of which 34 are real gates (none declaring the component yet) and 11 are `release`-meaning-
*let go of a hold*. **Ship it warning**, and reword `requiredWhen` to key off the declared
operation rather than the screen's subject: *"the screen declares an operation that publishes,
deploys, promotes or activates"*, excluding `release*`. Flip to enforcing once the 34 are
declared.

---

## 2 · `P08-venue-back-office.yaml`

### 2a — BP-010 fold, 17 screens

`layout.template: list` → `split`, and add a `searchField` to `contentBody.components`.

```
BO-074  BO-075  BO-076  BO-077  BO-089  BO-090      orders & money
BO-078  BO-079  BO-080  BO-081  BO-082  BO-083      stock & supply
BO-084  BO-085  BO-086  BO-087  BO-088              people & access rights
```

Result: BP-010 ceases to exist, BP-001 goes 314 → 331, pattern count 44 → 43.

### 2b — the three venue-map screens

`layout` opens straight into `regions` on all three; add the missing key.

| Screen | | Also |
|---|---|---|
| BO-092 Venue Maps | `template: list` | — |
| BO-093 Map Import & Labelling | `template: form` | add `fileUpload`, `progressIndicator` |
| BO-094 Map Editor & Publish | `template: canvas` | add `publishGate` |

Does not answer `CF-146`. Raise `graphFinding` separately — BO-094's own notes carry two
findings (unreachable point, step-only route) with no component to declare them.

### 2c — publish screens, add `publishGate`

**Revised 8 September — apply to `BO-153` and `BO-094` only.**

Of the seven originally listed, six declare no publish-shaped operation: BO-173
`listCredentialSecurity`, BO-193 `listBiometric`, BO-213 `listEdgeSecurityDeployment`,
BO-223 `listJourneys`, BO-343 `listVirtualTicketArchitecture`, ADM-227
`listGovernanceRiskLaunch`. Only BO-153 declares `publishTopologyValidation`. All seven are
BP-006 screens, so the list was read off their titles — the evidence CI check 1 rejects.

Hold those six. They join the contract-gap list with BO-233 and CMS-033: either they publish
and an operation is missing, or they do not and the titles are wrong. Nine screens, not two.

The 34 screens across the package that *do* declare a publish, deploy, promote or activate
operation are the real work list for this component; none declares it today.

### 2d — audit trails, replace the empty state

`BO-233` `BO-302` `BO-362`: drop `emptyFirstRun`, add `emptyNoEvents`.

### 2e — re-signature

`BO-235 Access Attribute Catalog` → `list` · dataTable · searchField · primaryButton.
Declared operation is `listAccessAttributeCatalog` on load. It is a data dictionary.

---

## 3 · `P09-platform-admin-console.yaml`

**Re-signature, each from its one declared operation:**

| Screen | Operation | Becomes |
|---|---|---|
| ADM-121 Bulk Product Creation & Catalogue Import | `createBulkProductCatalogue` | `form` · fileUpload · progressIndicator · dataTable · banner |
| ADM-240 Conditions, Decision Logic & Decision Tables | `listConditionDecisionLogic` | `split` · dataTable · detailPanel |
| ADM-260 Product & Catalogue Assignment | `setProductCatalogue` | `split` · treeNav · multiSelect · confirmDialog |

ADM-121 also loses `error: Configuration service unavailable` — it uploads a file.

**`publishGate`:** ADM-227.

**`emptyNoEvents`:** ADM-136, ADM-147, ADM-275, ADM-296.

---

## 4 · `P12-support-agent-console.yaml`

**`emptyNoEvents`:** SUP-011.

---

## 5 · `P13-white-label-cms.yaml`

**Re-signature:** `CMS-044 Dynamic Fields, Questions & Conditional Logic` →
`split` · dataTable · detailPanel · selectField. Operation is `listDynamicFieldQuestion`.

**`emptyNoEvents`:** CMS-033, CMS-039, CMS-058.

---

## 6 · Then regenerate

`pattern-data.js` and the derived frame inventory. The board copy already reads 43
patterns, so a regeneration should change numbers nowhere on the index — if it does, one
of the edits above did not land.

---

## Two open items, not blocking

**BO-233 and CMS-033 declare operations they cannot work from.** BO-233 is a shift
handover whose only operation is `listShiftHandoverSummary`; CMS-033 manages withdrawals
with only `listConsentEvidenceWithdrawal`. The screens their titles promise cannot be
built from what they declare. Missing operations, not layout defects — raise against the
contracts.

**The generator default outlives this pass.** All 23 BP-006 screens carried one stamped
layout and the same generator wrote the other 793. The operation names are the titles
camel-cased, so the API and the layout agreeing means nothing. Two CI checks: a screen
whose only operation is `list…` cannot claim a verb in its title, and an unauthored
layout should fail rather than default.
