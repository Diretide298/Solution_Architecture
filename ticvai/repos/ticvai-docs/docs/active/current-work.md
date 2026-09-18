# Current work

> **Owner:** Chinmay · **Updated:** 18 September 2026 · **Status:** living — update it, don't fork it
>
> What is in flight, what is next, and what must stay true while it happens. **One file.** The 73
> other documents in this folder are records of work that finished; this one is the work that has not.

---

## In flight: merging the developer team's schema

They returned `TICVAI_16_Services_AND_Tables_UPDATED` against the schema reference we sent. A deep
audit — matching by column content rather than by name — is in
[schema-merge-audit-18-september.md](schema-merge-audit-18-september.md), and the response document
for them is `TICVAI_Schema_Merge_Response.docx` at the workspace root.

**The shape of the job.** Everything downstream is derived from `contracts/`. The whole chain —
schema, lineage, relationships, DDL, burst scope, sizing, table notes, schema roots, frontend,
board-panel map, diagrams, both workbooks, wireframes, workshop boards, id register,
screen-contract links, platform, deployment, audience, backlog, clusters, overview, counts,
mirrors — **is one command.** So this is a contract-authoring job with a small number of human
gates, not twenty-four jobs.

**Scale:** ~100 tables and 1,099 columns, mapped to 13 services. **No table crosses a schema
boundary**, so ADR-0028 holds without exception — the best single fact in the audit for sequencing.

### Blocked on the client, not on us

| | |
|---|---|
| Four architectural conflicts | scope (path vs FK) · venue (tree vs entity) · PII (separate schema vs inline) · actor (principal vs user+customer) |
| Three clarifications | any SQL Server code already written · what the workbook *is* · the undeclared `wallet` / `venue` / `pricing` schemas |

**None of this blocks Phase 1.** The ~100 tables being merged do not change whichever way the four
land — that was the point of separating them.

---

## Phases

### Phase 0 — establish identity, then the four fields

**Identity first, and this was the lesson.** The plan said Phase 0 was *assign service, audience,
scope, persistence*. Running it on the orders cluster revealed a step in front: **working out which
of their tables are actually new.** Three passes were needed and the first two were wrong —
165 "new", then 138, then fewer again once a person read the column lists. In orders alone, **six
"new" tables were renames of tables we already have**, and creating them would have produced six
duplicate pairs that no check would have caught.

**Column overlap cannot settle identity once both sides have restructured.** Budget a person's
afternoon per cluster for this, ahead of any contract authoring.

Then the four fields, none of which derivation can produce:

1. **Service per operation** — `derive-lineage --apply` is additive and never revises an existing
   entry. A wrong assignment is permanent until someone rebuilds the lineage by hand.
2. **Audience** — `check-screens` **fails** a guest-callable operation with no guest screen.
   Declaring `guest` casually commits us to screens.
3. **Scope level** — decides RLS and, through ADR-0044, partitioning.
4. **`x-ticvai-persistence` and store** — `derive-ddl` only creates a table for a schema that
   declares one; `check-package` rule 28 fails a SQL table whose store is not Postgres.

### Phase 1 — author the contracts, cluster by cluster

Payments (OrderService) → catalogue and rentals → identity and tenancy → marketing → the tail.
Payments first because it is self-contained, it is their strongest material, and it feeds the money
path in the build plan.

### Phase 2 — screens, before anything reads them

`refresh.sh` says it plainly: *"The screens are authored before anything reads them… running them
later would publish an index of the previous run's screens."* **Decide the screen count here, not
after the run.**

### Phase 3 — one command

`bash tools/refresh.sh`. **Two things it does not do and this merge needs:**

- `python3 tools/derive-services.py --apply` — otherwise the 16 skeletons never see the new tables.
  This caught us on 17 September.
- `python3 tools/derive-mirrors.py` — refresh runs it, but it is the stage that fails loudest when
  something upstream half-ran, so check its output rather than the exit code.

### Phase 4 — hold the baselines

| check | must stay at |
|---|---|
| `check-package` | **9 errors** — 7 `release*` lineage, `p09-commercial`, `audit-2026-09-07` |
| `check-screens` | PASS |
| `check-flows` | PASS |
| `check-migrations` | PASS |
| `audit-links` | every link resolves |

Anything above 9 on `check-package` is ours, and it gets fixed before the next cluster starts.

---

## Todo

### Now — renames first, then Phase 1

**Sequencing changed 18 September.** Phase 1 was authored and then **reverted on purpose**: adding
new tables on top of unresolved renames means renaming tables that new code already references.
**Renames land first.** See *Phase 1, reverted* below for how to bring it back.

### The workbook has a Change Log sheet, and it changes the whole picture

**Read it before any more inference.** `TICVAI_16_Services_AND_Tables_UPDATED (1).xlsx` carries a
**Change Log** sheet, 743 rows, with an explicit `Change Type` column. It was not read during the
first three identity passes, and it is authoritative in a way column-overlap matching never is.

| change type | rows | |
|---|---|---|
| **Column Renamed** | 645 | |
| Table Added | **28** | |
| Column Attributes Changed | 23 | |
| Column Added | 17 | |
| Table Renamed | 12 | |
| Column Renamed & Attributes Changed | 9 | |
| Schema Prefix Renamed | 5 | **covering 43 tables** |
| Proposed then Rejected | 3 | they added it, then pulled it |
| Column Removed | 1 | |

**671 of 743 changes are renames — 90%.** Twenty-eight tables were added.

**This corrects the headline number in
[phase0-identity-pass-all-clusters.md](phase0-identity-pass-all-clusters.md).** That document says
*165 → 138 → ~110 genuinely new*. **The workbook declares 28 table additions**, of which 27 are new
to us. The three passes were inferring from names and columns what the sheet states outright.

### One convention explains two thirds of the file

**They prefixed every column with its table name.** `code` → `access_point_code`, `status` →
`accreditation_status`, `content` → `message_content`, and `id` → `<table>_id` on 193 tables.
**436 of the 654 column renames are this one rule applied mechanically** — 67%. Add
`scope_id` → `tenancy_scope_id` (24) and the FK renames (92) and almost nothing is left.

**This is a position to take, not a merge detail.** We do not prefix; `access.access_point.code` is
already unambiguous and `access.access_point.access_point_code` says the same thing three times.
**Decide it once, tell them once**, and 654 of their 743 changes resolve in that single answer.

### The 43 schema-prefix renames are them adopting our names

| theirs → ours | tables |
|---|---|
| `branding.*` → `whitelabel.*` | 15 |
| `ticketing.*` → `catalogue.*` | 13 |
| `tenancy.*` → `platform.*` | 8 |
| `crosscell.*` → `sync.*` | 4 |
| `venue_map.*` → `venuemap.*` | 3 |

**Every one of these lands on our name**, confirmed against `schema-reference.json`. No work on our
side, and worth acknowledging back to them — they moved 43 tables to our convention unprompted.

### Seven renames the Change Log does not declare

Found by stripping their redundant table prefix. **These are certain** — the stem is our exact table:

`approvals.approval_matrix` · `approval_rule` · `approval_request` · `approval_decision` ·
`approval_delegation` · `approval_escalation` → **`approvals.matrix` / `rule` / `request` /
`decision` / `delegation` / `escalation`**, plus `resources.resource_booking` →
`resources.booking`.

**Same redundant-prefix habit as the column renames**, one level up. It is the same conversation.

### What still needs a person, and why the matcher cannot finish it

A column-overlap matcher was run over all 323 of their tables. **It cannot settle table identity**,
and both failure directions were observed:

- **Scored too loose**, `min()` denominator: `orders.deposit` → `orders.order_discount` at 100%,
  because both are two-column stubs and any two columns overlap completely
- **Scored too tight**, Jaccard with a five-column floor: called `identity.otp` *new* — when the
  Change Log **declares** it as `identity.otp_challenge` → `identity.otp`

**This is the lesson already in the phase-0 doc, confirmed from a third direction: step 3 must be
human.** The ~23 surviving mid-confidence candidates (`fnb.sold_out_item` ↔ `fnb.eighty_six_event`
at 88%, `platform.cash_denomination` ↔ `platform.denomination`, `inventory.stock_movement` ↔
`inventory.movement`) are a worklist for a person, not a result.

- [ ] **Three table renames the Change Log proves we owe** — resolved by normalising their schema
      prefixes and checking each side against our package:
      `sync.rejection` → `sync.cross_cell_rejection` · `identity.otp_challenge` → `identity.otp` ·
      `marketing.segment` → `marketing.customer_segment`.
      Of the other nine declared table renames, four are **already our name** and five are their
      own internal churn between two names we do not use
- [ ] **The five renames from the earlier by-hand pass** — these came from column reading rather
      than the Change Log, so they stand until someone reconciles the two lists. Blast radius
      measured against `handoff/schema-reference.json`, not guessed:

      | ours → theirs | inbound FK | contract files | note |
      |---|---|---|---|
      | `orders.shift` → `orders.pos_shift` | **6** | 3 | The only expensive one. `retail.sale`, `orders.sales_order`, `cash_movement`, `deposit_box` and two more point at it |
      | `reporting.execution` → `reporting.report_execution` | 1 | 1 | `reporting.export.execution_id` |
      | `orders.payment_provider` → `orders.payment_gateway` | 0 | 1 | free |
      | `orders.payment_routing` → `orders.payment_route` | 0 | 1 | free |
      | `marketing.journey_entrant` → `marketing.journey_enrollment` | 0 | 1 | free |

      **Four of the five are free.** Do those, then `orders.shift` on its own with its six FKs.

- [ ] **Four renames to decline, in writing** — `orders.sales_order` (`ORDER` is reserved),
      `catalogue.variant` (pairs with `variant_dimension`), `reporting.report_parameter`
      ("parameter" is the domain word), `ai.policy` (26 columns against their 17)
- [ ] **One rename nobody cares about** — `whitelabel.config_version` vs `brand_version`. Either.
      Concede it; it costs nothing and it is worth spending on the four above
- [ ] **Two stubs to replace wholesale, not rename** — `orders.order_discount` (2 columns) and
      `approvals.escalation` (2 columns). **Keep our names, take their bodies.** Zero inbound FKs on
      both, so this is the cheapest real work in the list
- [ ] **Two to union, no rename** — `approvals.request` (**8 inbound FKs**, both sides rich) and
      `approvals.rule` (1 inbound). Column union only
- [ ] **Send the response document** to the developer team — the three clarifications gate everything
- [ ] **Decide the five payroll tables** — `payroll_run`, `payroll_line`, `payslip`, `salary`,
      `salary_component` have no requirement behind them, and matrix 1.2.3 contemplates *integrating*
      with a workforce system rather than becoming one
- [ ] **Per-domain product catalogues** — they duplicate `product`/`price`/`category` into `fnb` and
      `retail`. This is a fifth architectural divergence and belongs in the response document
- [ ] **`marketing.data_subject_request` vs our `platform.dsar_request`** — one has to go
### Phase 1, reverted — how to bring it back

**It was written, it worked, and it was rolled back for sequencing.** All fourteen schemas were
authored and derived clean; `check-package` held at the 9-error baseline the whole way. Nothing was
wrong with it. It sits behind the renames.

| | |
|---|---|
| **Backup** | `scratchpad/phase1-backup/` — `phase1-full.patch` (988 lines) plus whole copies of the three contract files |
| **Restore** | `git apply` the patch from the repo root, then `derive-schema` → `derive-ddl --apply` → `derive-relationships` → `derive-diagrams` → `derive-mirrors` |
| **Covered** | 12 schemas into `orders.yaml`, `CashCount` into `shift.yaml`, `MembershipRenewal` into `subscription.yaml`, and the `CURRENCY_OK` entry in `check-package.py` |
| **Not covered** | **Operations — 0 of 14 were ever written.** Every table was unreachable through the API |

**Decisions baked into the patch, so they do not need retaking:** `orders.deposit` →
`security_deposit`; `Upgrade` → `OrderUpgrade`; `subjectId` and `*PrincipalId` throughout;
`orders.currency_rule` exempted from the ADR-0018 currency rule with its reason written into
`check-package.py`; no `currencyCode` anywhere else in the cluster.

**`derive-schema` merges, it does not rebuild.** Reverting `contracts/` alone left all fourteen
tables standing in `handoff/schema-reference.json` — the count went *up*, to 407. `handoff/` had to
be checked out to HEAD as well before re-deriving. **A contract revert is a two-part revert.**
Baseline is **393 tables**, confirmed after the re-derive.

### Blocked on a decision: there is no membership cluster

Writing `membership_renewal` exposed it. **No `customer_membership`, no `membership_product`, no
`membership_tier` — no membership table of any kind.** Against that, `subscription.yaml` carries
**13 membership operations** and ~30 `Membership*View` schemas each declaring itself *"a projection
over subscription state, assembled at read time from tables that already exist."* They do not exist.

The three name matches are false friends: `control.subscription` is the tenant's SaaS plan,
`marketing.subscription` is a mailing list, `orders.wallet_pass` is an Apple/Google pass.

**`orders.membership_renewal` cannot be migrated until `orders.customer_membership` lands.**

**They have already specified it**, which changes the answer: the merge audit lists
`membership_plan`, `membership_program`, `membership_benefit` and `plan_benefit` among their 165,
plus ~15 identity-cluster tables described as *membership instances*. **This is not new design work,
it is another additive cluster** — author it with the rest of the additive pass and
`membership_renewal` stops dangling.

### Additive — what to take, in cost order

**The cheapest and best change in their whole file, first:**

- [ ] **`created_at` on 83 tables and `updated_at` on 66.** The package largely lacks both.
      **Adopt wholesale, not table by table** — it is one mechanical pass and it is right
- [ ] **`is_active` on 39 tables** — a soft-state convention where the package has none
- [ ] **Settle `kind` vs `type` once.** They drop 22 of our `kind` columns and add 17 `type`.
      **Either is fine; both is not.** Pick one and apply it in the same pass as the renames

**Column unions into tables we already have** (orders cluster, from
[phase0-orders-cluster.md](phase0-orders-cluster.md)):

| table | what they add | call |
|---|---|---|
| `orders.payment` | gateway_id, method_id, terminal_id, link_id, client_reference, failure_code/message, paid_at, updated_at | **Union.** Ours is tender-oriented (what happened at the till), theirs gateway-oriented (what happened at the provider). Both are needed |
| `orders.payment_link` | amount, url, provider_id, provider_link_reference, timestamps | **Union.** Ours is *send a guest a link*; theirs is *a provider-hosted page* |
| `orders.order_line` | product_code/name, item_source, source_item_id, parent_order_line_id, relation_type, recommendation_id, discount_amount, unit_price | **Take.** `item_source` is *one cart across ticketing, F&B and retail* written as a column — a rule we have carried since 14 August with no way to express it. **ASK what `relation_type` enumerates** |
| `orders.cart_line` | as above, plus `seat_hold_id` | **Take.** `seat_hold_id` ties a cart line to the hold reserving it |
| `orders.cash_count_line` | denomination_id, denomination_value, line_total | Straight union |
| `orders.cash_movement`, `refund`, `refund_policy`, `cart` | small additions | Straight unions |

**The 27 tables actually added**, from the Change Log's own `Table Added` list, normalised and
checked against our package. One of the 28, `orders.payment_link`, we already hold.

| cluster | tables | |
|---|---|---|
| **orders — payments** | 10 | `payment_method` · `payment_method_config` · `payment_policy` · `payment_eligibility_rule` · `payment_fee_rule` · `payment_terminal` · `currency_rule` · `order_fee` · `deposit` · `deposit_activity` — **all ten already written in the reverted Phase 1 patch** |
| resources — rentals | 5 | `rental_agreement` · `rental_agreement_item` · `rental_inspection` · `rental_inspection_item` · `rental_product_mapping` |
| catalogue — rentals | 4 | `rental_product_config` · `rental_rate` · `rental_requirement` · `rental_rule` |
| platform — subscription tiers | 4 | `subscription_tier` · `tenant_subscription` · `tier_allowance` · `tier_module` |
| identity — custom fields | 3 | `customer_extra_field` · `customer_extra_option` · `customer_extra_value` |
| maintenance | 1 | `rental_damage_assessment` |

**Nine of the 27 are the rental cluster**, matching the 9 September workshop almost row for row.
**Ten are the payment cluster and are already authored.** The real additive backlog is **17
tables**, not ~110.

**Two claims made earlier in this file do not survive the Change Log, and are withdrawn:**

- **The membership cluster is not in the added list.** The claim that the developer team had
  specified it came from the merge audit's prose, not from the Change Log. **The membership gap is
  still ours to close** and the decision is still open
- **Accreditation is not in the added list either.** The earlier note that *"they appear to have
  specified it"* and that reading it may close CF-21 rests on their sheet carrying `access.
  accreditation` with 29 columns — which is true — but the Change Log does not record it as added
  in this round. **Worth reading before the workshop regardless**; CF-21 still calls it the only
  blocked work on the project. Treat it as a lead, not a delivery

### Decided today, ready to apply

- [x] Orders cluster identity — 14 new, 5 renames, 5 column merges
      ([phase0-orders-cluster.md](phase0-orders-cluster.md))
- [x] All six orders ASKs answered — no client input was needed for any of them
- [x] **Identity pass across all sixteen schemas**
      ([phase0-identity-pass-all-clusters.md](phase0-identity-pass-all-clusters.md)).
      **165 → 138 → ~110 genuinely new. Fourteen renames caught**, each of which would have become
      a duplicate table no check would have flagged
- [ ] Take `orders.order_discount` and `approvals.escalation` **from them wholesale** — ours hold
      two columns each and theirs carry the actual domain
- [ ] Take `marketing.waiver_template` and `waiver_signature` — we have **no waiver table at all**,
      against 321 contract mentions, a client design pack and a workshop board
- [ ] `PAYMENT_CONFIGURE` — the one new permission, following the `*_CONFIGURE` family.
      `SHIFT_CLOSE`, `OVERSHORT_ACCEPT` and `PAYMENT_VOID` already exist
- [ ] Rename their `orders.deposit` to `security_deposit` — ours is a physical cash box
- [ ] Push back on `orders.order`: **`ORDER` is a reserved word**, and `orders."order"` would need
      quoting at every use site

### Waiting on the developer team

- [ ] Is any DDL, EF model or migration already written against SQL Server?
- [ ] Is the workbook our schema merged, or their own model annotated?
- [ ] `wallet`, `venue`, `pricing` — new schemas, or renames of ours?
- [ ] A position on the four conflicts, scope first
- [ ] What the accreditation tables were modelled from — **may close CF-21**

### Build, on the critical path

- [x] **ADR-0044 signed off** — full partitioning rule, 32 tables qualify
- [x] **V0001__baseline.sql written** — RLS with `FORCE`, scope tree, partition helper, outbox,
      `platform.schema_version`. `check-migrations` PASS
- [ ] **B5 migration orchestrator** — 10 days, critical path, fans out per region, every migration
      needs a tested `-- ROLLBACK`
- [ ] **B1 tenant resolution + RLS policies** across 73 scoped tables
- [ ] **C1 audit the existing 20% against ADR-0002** — one day now, a sprint at integration

### Also open, not forgotten

- [ ] Three MoMs read but not diffed into the contracts — none of the 8 September approval decisions
      (N-of-M, amount thresholds, substitute approver) and none of the 10 September licensing model
      (VSI, tier thresholds, minimum guarantee, per-ticket) exist in the contracts
- [ ] The design handoff's gaps — 3D seat view, at-venue wayfinding, passkeys, the configuration
      panel, seat-hold countdown, waitlist, availability bands
- [ ] `conflict-status.md` is 51 conflicts stale; four entries sit under Open while their own text
      says Closed
- [ ] The forward-direction identity-resolution operation ADR-0045 names as owed

---

## Traps, learned the hard way

**`sync-counts` rewrites any "N tables" phrase to the package total.** 383 → 483 will silently
rewrite prose elsewhere in the package. Phrase counts so it cannot match them.

**`derive-lineage --apply` is additive.** A wrong audience set in Phase 0 survives every subsequent
run, forever, until someone rebuilds by hand.

**`backend/` is derived** — but only `0*.sql` and `9*.sql` are deleted on regeneration, which is why
`V0001__baseline.sql` survives. It lives in `src/Ticvai.Migrations/Scripts/` regardless, because a
`V*.sql` file in `backend/` sorts after the numeric series and would apply last.

**Never trust a name match, and never trust column overlap alone.** Read both column lists.
