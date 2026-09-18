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

### Now

- [ ] **Send the response document** to the developer team — the three clarifications gate everything
- [ ] **Decide the five payroll tables** — `payroll_run`, `payroll_line`, `payslip`, `salary`,
      `salary_component` have no requirement behind them, and matrix 1.2.3 contemplates *integrating*
      with a workforce system rather than becoming one
- [ ] **Per-domain product catalogues** — they duplicate `product`/`price`/`category` into `fnb` and
      `retail`. This is a fifth architectural divergence and belongs in the response document
- [ ] **`marketing.data_subject_request` vs our `platform.dsar_request`** — one has to go
- [ ] **Phase 1, payments** — author the 14 new orders tables into `orders.yaml`, plus `cash_count`
      into `shift.yaml` and `membership_renewal` into `subscription.yaml`

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
