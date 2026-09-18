# Validating the developer team's Change Log

> **Owner:** Chinmay · **Written:** 18 September 2026 · **Status:** complete, feeds the response document
>
> Their workbook `TICVAI_16_Services_AND_Tables_UPDATED (1).xlsx` carries a **Change Log** sheet that
> was not read during the first three identity passes. This validates every claim in it against both
> workbooks — theirs, and the reference we sent them.

---

## Method

Three questions, each answered mechanically rather than by reading:

1. **Is the log internally true?** Does every change it records actually appear in their own sheets?
2. **Is it about our schema?** Does each renamed-from column exist in the reference we sent?
3. **What do the two models share?** Table-level correspondence, allowing every declared rename.

**The five schema-prefix renames must be normalised before any of this**, or the log appears to fail
on 64 rows that are simply recorded under their pre-rename names. That normalisation is the
difference between accusing them of sloppiness and reading their file correctly.

| their prefix | ours |
|---|---|
| `branding.*` | `whitelabel.*` |
| `ticketing.*` | `catalogue.*` |
| `tenancy.*` | `platform.*` |
| `crosscell.*` | `sync.*` |
| `venue_map.*` | `venuemap.*` |

---

## 1. The log is internally accurate — zero errors

| check | result |
|---|---|
| 654 column renames applied in their workbook | **654 verified, 0 failed** |
| 12 table renames landed | **12 verified, 0 failed** |
| 28 `Table Added` present in their sheets | **28 verified, 0 failed** |

**Say this back to them.** A changelog of 743 rows with no drift against its own artefact is careful
work, and it is the reason the rest of this analysis is possible at all.

## 2. But only 22% of it describes our schema

**143 of the 654 renamed columns trace to a column in the reference we sent. 511 do not.**

The untraceable ones rename tables we never had — `ai.activity`, `ai.action_request`,
`ai.indexing_job`, `ai.knowledge_group`. Worst-affected schemas: marketing 79, identity 63,
workforce 61, access 44, venue 34.

### This answers clarification 2.2 without them

The response document asks: *"is this the schema we sent with your changes applied, or your own
model with our naming annotated onto it?"*

**It is their own model.** Three independent measures agree:

| measure | value |
|---|---|
| renamed columns traceable to our reference | **22%** (143 of 654) |
| their tables corresponding to one of ours | **106 of 323** (exact or prefix-stem) |
| our tables absent from their workbook | **268 of 374** |

**One of the three blocking clarifications is now closed by evidence rather than by asking.** It
also reframes the whole exercise: this is a reconciliation of two schemas sharing about a third of
their surface, not a merge of ours with edits applied.

## 3. One convention is two thirds of the file

**They prefixed every column with its table name.** `code` → `access_point_code`, `status` →
`accreditation_status`, `content` → `message_content`, and `id` → `<table>_id` on 193 tables.

**436 of the 654 column renames are this one rule.** Add `scope_id` → `tenancy_scope_id` (24) and
the FK renames (92) and almost nothing is left unexplained.

**Answering it once resolves 436 rows.** We do not prefix — `access.access_point.code` is already
unambiguous, and `access.access_point.access_point_code` says the same thing three times.

## 4. They moved 43 tables onto our names unprompted

| theirs → ours | tables |
|---|---|
| `branding.*` → `whitelabel.*` | 15 |
| `ticketing.*` → `catalogue.*` | 13 |
| `tenancy.*` → `platform.*` | 8 |
| `crosscell.*` → `sync.*` | 4 |
| `venue_map.*` → `venuemap.*` | 3 |

Every one lands on our name, verified against `handoff/schema-reference.json`. **The response
document credits this nowhere and should.**

## 5. Seven renames the log does not declare

Found by stripping their redundant table prefix; the stem is our exact table, so these are certain:

`approvals.approval_matrix` · `approval_rule` · `approval_request` · `approval_decision` ·
`approval_delegation` · `approval_escalation` → **`approvals.*`**, plus
`resources.resource_booking` → `resources.booking`.

Same habit as the column prefixing, one level up. **It is the same conversation, so ask it once.**

---

## `Table Added` means added *this round*

**This trap cost a wrong correction on 18 September.** Reading the 28-row `Table Added` list as *the
tables they hold and we do not* produced the claim that membership and accreditation were absent
from their file. **Both are in it**, verified by reading their sheets:

| cluster | their tables | |
|---|---|---|
| **membership** | 7 | `catalogue.membership_plan` (12 cols) · `membership_program` · `membership_benefit` · `plan_benefit` · **`identity.customer_membership` (12 cols)** · `identity.membership_history` · `orders.membership_renewal` |
| **accreditation** | 6 | **`access.accreditation` (29 cols)** · `accreditation_type` · `accreditation_credential` · `accreditation_document` · `accreditation_access` · `accreditation_status_history` |

`identity.customer_membership` is **the exact table whose absence blocked `membership_renewal`**
during Phase 1. The gap closes by taking their cluster.

---

## Why the automated matcher cannot finish this

A column-overlap matcher was run over all 323 of their tables. **It fails in both directions**, and
both failures were observed rather than predicted:

- **Loose** — `min()` denominator: `orders.deposit` → `orders.order_discount` scored **100%**,
  because both are two-column stubs and any two columns overlap completely
- **Tight** — Jaccard with a five-column floor: called `identity.otp` **new**, when the Change Log
  *declares* it as `identity.otp_challenge` → `identity.otp`

**Step 3 stays human.** This is the third independent confirmation of the rule already in
[phase0-identity-pass-all-clusters.md](phase0-identity-pass-all-clusters.md). The ~23 surviving
mid-confidence candidates — `fnb.sold_out_item` ↔ `fnb.eighty_six_event` at 88%,
`platform.cash_denomination` ↔ `platform.denomination`, `inventory.stock_movement` ↔
`inventory.movement` — are a worklist for a person, not a result.

---

## What changes in `TICVAI_Schema_Merge_Response.docx`

**Not yet applied.** The document as sent is at the workspace root; this is the delta it needs.

| section | change |
|---|---|
| **§2.2** *What is this workbook* | **Question becomes a finding.** We answer it ourselves — their own model. Replace the numbers *165 / 246 / 158 correspond* with the measured **217 / 268 / 106** |
| **§1.3** *New tables — 165 with no counterpart* | Both numbers are true and measure different things. **28 added this round; 217 with no name counterpart overall.** Say both, and say which is which. Membership corrects from 4 tables to **7** |
| **§2.4** *Two renames point in opposite directions* | **Answered — drop the question.** Their sheets hold `whitelabel.*` = 15 and `branding.*` = 0. The two `whitelabel.banner → branding.banner` rows are stale entries that never applied |
| **§2.7** *Half-applied rename* | **Confirmed exactly as written** — `scope_id` on 31 tables, `tenancy_scope_id` on 32. No change |
| **§1.2** *Naming* | **Needs the largest new subsection.** The table-name prefixing convention is 436 of 654 renames. One position from us resolves two thirds of their changelog |
| **new, in §1** | **Credit the 43 schema-prefix renames.** They adopted our names unprompted and the draft says nothing about it |
| **new, in §1 or §2** | The seven undeclared `approvals.approval_*` renames |

**The scope compromise in §4 is unaffected** — Options A, B and C stand, and C remains the
recommendation.
