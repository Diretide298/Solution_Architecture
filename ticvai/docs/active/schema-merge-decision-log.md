# Schema merge — the decision log

> **What this is.** The eleven open decisions from
> [schema-merge-decisions-20-september.md](schema-merge-decisions-20-september.md), answered one
> at a time with the evidence that decided each. **This is the input to the final report** — the
> response document and the shared doc are written from here, not from memory.

## The rubric

**This is not ours against theirs.** Where their shape is better we take it, where ours is better
we keep it, and where each has half of it we combine. Every decision below is scored on four
things and nothing else:

| | the question it asks |
|---|---|
| **Maintainability** | how many places a change has to be made, and how many ways to get it wrong |
| **Readability** | does the name tell a developer what the rows are, without the schema doc open |
| **Optimised access** | does the query a screen actually runs stay inside one schema, on narrow rows |
| **DB strain** | contention, row width, update churn, and what shares a hot table with what |

**The fourth one carries more weight than it looks.** It is the same argument that gave F&B and
Retail their own product and price tables: a flash sale on retail stock must not contend with
ticket inventory. Anything that puts a second workload on `catalogue` or `orders` is paying that
cost again.

| # | Decision | Call | Date |
|---|---|---|---|
| 1 | Rental domain | **keep `rental.*` and take their agreement** | 20 Sep |
| 2 | Payments domain | — | |
| 3 | Subscription domain | — | |
| 4 | `venue` schema | — | |
| 5 | `pricing` schema | — | |
| 6 | Payroll and HR scope | — | |
| 7 | Where a customer lives | — | |
| 8 | Loyalty: one rules table or four | — | |
| 9 | Membership hierarchy | — | |
| 10 | Cross-cell guest link | — | |
| 11 | The DSAR duplicate | — | |

---

## 1 · Rental domain — **keep the schema, take their agreement**

**Their proposal:** ten tables across `catalogue` (4), `resources` (5) and `maintenance` (1).
**Ours:** one `rental` schema, 21 tables.

**The answer is neither side whole.** The schema boundary is ours; one of their tables is a
record we do not have and should.

### Scored

| | verdict | why |
|---|---|---|
| **Maintainability** | **ours** | a rental change touches one schema. Theirs touches `catalogue`, `resources` and `maintenance` — and `rental_rate` in `catalogue` means a pricing change lands in the ticket team's schema |
| **Readability** | **ours** | `rental.inspection` against `resources.rental_inspection`. Their prefix exists *because* of the placement — the name is carrying the schema's job |
| **Optimised access** | **ours** | a checkout reads booking, agreement, items, inspection, participant and pricing together. In ours that is one schema. In theirs it joins across three |
| **DB strain** | **ours, decisively** | **`catalogue.rental_rate` puts rental pricing inside the hottest table set in the system.** That is the flash-sale contention argument that gave F&B and Retail their own price tables, reintroduced |

**The fourth line is their own principle used against their own layout**, and it is the one to
lead with — not "the cost falls on you". The cost asymmetry is real (187 change points against a
schema rename) but it is an argument about effort, not about what is better.

### What is genuinely better on their side — **take it**

**We hold `agreement_rules` and `agreement_signature`, and no agreement.**

    rental.agreement_rules        agreement_required, e_signature_required, agreement_version, …
    rental.agreement_signature    participant_id, agreement_version, signatory_name, signed_at, …
    rental.participant            name, date_of_birth, has_signed_waiver, …   ← no booking reference

**The signature references a participant and a version string.** It signs a version *number*, not
a document instance, and the participant it names is attached to nothing — `rental.participant`
carries no booking or agreement column at all. Their `resources.rental_agreement` is exactly the
record both of ours are reaching for.

**Scored, taking it wins on all four:**

- **Maintainability** — a signature that points at a real row cannot be orphaned. Today it can
- **Readability** — `rental.agreement` beside `agreement_rules` and `agreement_signature` finally
  reads as a set
- **Optimised access** — a booking list does not need handover and return columns. Splitting
  narrows the row the busy query scans
- **DB strain** — **this is the real gain.** `rental.booking` carries the reservation *and* the
  fulfilment, so every row is updated at least twice more after creation: once at checkout, once
  at return, again on late accrual. Wide rows updated repeatedly means row versions and bloat on
  the table that every availability check reads. Move the churn to the agreement and `booking`
  goes stable-after-insert

**So: `rental.booking` keeps the commercial reservation, `rental.agreement` carries the
operational contract.** That is the split our own two tables already implied.

**And their `rental_agreement_item` merges with our `rental.equipment_assignment`** — their
per-item status and quantity path for things that are not serialised, our `asset_id`,
`serial_number`, `scanned_code` and `returned_at`. One table doing both jobs.

### What else we move — ours, not theirs

**`rental.category` leaves `rental`.** It is the asset-category master for the whole venue:

    maintenance.asset.category_id                    -> rental.category
    maintenance.maintenance_plan.asset_category_id   -> rental.category
    maintenance.inspection_template.applies_to_…     -> rental.category
    resources.resource_category.parent_category_id   -> rental.category
    resources.resource_requirement.category_id       -> rental.category

**A forklift that is never rented has its category defined in `rental`.** On maintainability and
readability alone it belongs in `maintenance` or `resources`. Their split is what surfaced it.

### The counter-argument, stated fairly

Rental equipment genuinely is a maintenance asset — seven real edges, against 14 that stay inside
rental. The domains interpenetrate and anyone arguing the other way is not being unreasonable.
It loses on **optimised access** and **DB strain**, not on ownership.

### A defect found on the way — evidence for nobody

**Five of the twelve `rental → maintenance` edges are wrong.**

    rental.category.icon_asset_id                    -> maintenance.asset    an icon
    rental.product.image_asset_id                    -> maintenance.asset    an image
    rental.agreement_rules.terms_document_asset_id   -> maintenance.asset    a PDF
    rental.agreement_signature.signature_asset_id    -> maintenance.asset    a signature scan
    rental.agreement_signature.document_asset_id     -> maintenance.asset    a signature scan

All five belong to `assets.media_asset`. **`derive-relationships` saw `*_asset_id` and reached for
`maintenance.asset`**, inflating the coupling by 70%.

**Open:** the same rule will have done this wherever a `*_asset_id` column names media. Not swept.

### Correction to carry into the report

**We do have dynamic pricing, on one table.** `rental.pricing_profile` holds `dynamic_enabled`,
`dynamic_max_increase_percent` and `dynamic_max_decrease_percent`. Those are **bounds, not an
engine** — there are no rules, no conditions, no actions, and nothing at all for tickets, F&B or
retail. The claim "no dynamic pricing at all" is stated in the response document and the shared
doc and is **overstated**; it has to read "guardrails on one table and no rules engine" before
decision 5 is argued.
