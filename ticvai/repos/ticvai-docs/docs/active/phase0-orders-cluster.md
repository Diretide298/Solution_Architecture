# Phase 0 — the orders cluster, table by table

> **18 September 2026.** Identity, ownership and the four fields that derivation cannot produce.
> **This is a worksheet for review, not a decision already taken.** Every row below is a
> recommendation with its evidence; the ones marked **ASK** need someone who knows the intent.

---

## What Phase 0 turned out to be

The plan said Phase 0 was *assign service, audience, scope and persistence*. Running it revealed a
step in front of that one: **establishing which of their tables are actually new.**

Three passes were needed and the first two were wrong:

| pass | method | result |
|---|---|---|
| 1 | tables whose name has no match in ours | 165 "new" |
| 2 | ...minus those whose name does exist | 138 new, 27 column merges |
| 3 | ...minus renames, read by a person | **see below — far fewer again** |

In the orders cluster alone, six tables that pass 2 called *new* are renames of tables we already
have. **Creating them would have produced six duplicate pairs holding the same rows**, and no check
in the package would have caught it, because a table nothing references is not an error.

**Column overlap cannot settle identity once both sides have restructured.** The matcher scored
their `payment_link` as a 0.29 match for our `reservation` while our own `payment_link` sat there
unmatched — the two models of that table share only `id`, `order_id`, `status`, `expires_at` and
`paid_at`. A person reading both column lists sees it instantly. This is the step that has to be
human, and it has to happen before any contract is written.

---

## 1. Identity — their orders tables against ours

### Renames of tables we already have

| theirs | ours | evidence | recommendation |
|---|---|---|---|
| `orders.order` | `orders.sales_order` | both carry channel, status, gross_amount, refunded_amount, workstation_id, tax, order number | **Merge. Keep our name.** `order` is a reserved word in SQL and would need quoting at every use site — worth pushing back on rather than conceding. |
| `orders.pos_shift` | `orders.pos_shift` | both: workstation_id, status, opening_float, sales_total, refunds_total, opened_at, closed_at | **Merge, take their name.** `pos_shift` is clearer, and their change log already declares `till_shift → pos_shift`. |
| `orders.payment_gateway` | `payments.provider` | both: name, kind, supported_methods, supported_currencies, credential reference, is_active, supports_* flags | **Merge.** Name is a coin-toss; `gateway` is the more common industry term. |
| `orders.payment_route` | `orders.payment_routing` | both: priority, conditions, fallback provider | **Merge, take their name.** A row is one route. |
| `orders.discount` | `orders.order_discount` | ours holds `id` and `order_id` **and nothing else** | **Merge, take theirs wholesale.** Ours is a stub that was never filled in. Theirs has applied_amount, coupon_code, promotion_id, reason, type, value. |
| `orders.cash_count_line` | `orders.cash_count_line` | same name | **Merge.** They add denomination_id, denomination_value, line_total. |

### Column merges into an existing table

| table | they add | note |
|---|---|---|
| `orders.payment` | client_reference, currency_code, failure_code, failure_message, gateway_id, link_id, method_id, paid_at, terminal_id, updated_at | Ours is tender-oriented (tender, change, FX); theirs is gateway-oriented. **Both are needed** — ours describes what happened at the till, theirs what happened at the provider. Union them. |
| `orders.payment_link` | amount, currency_code, url, provider_id, provider_link_reference, created_at, updated_at | Ours models *send a guest a link to pay*; theirs models *a provider-hosted payment page*. Union. |
| `orders.order_line` | product_code, product_name, item_source, source_item_id, source_variant_id, parent_order_line_id, relation_type, recommendation_id, recommendation_source, discount_amount, entitlement_reference_id, unit_price | The parent/relation columns are a bundle model we lack. **ASK** what `relation_type` enumerates. |
| `orders.cart_line` | as above plus seat_hold_id, tax_amount | `seat_hold_id` is worth taking — it ties a cart line to the hold that reserves it. |
| `orders.cash_movement`, `orders.refund`, `orders.refund_policy`, `orders.cart` | small additions | Straight unions. |

### Genuinely new

`cash_count` · `currency_rule` · `deposit` · `deposit_activity` · `membership_renewal` ·
`order_fee` · `payment_eligibility_rule` · `payment_fee_rule` · `payment_method` ·
`payment_method_config` · `payment_policy` · `payment_terminal` · `recommendation_activity` ·
`upgrade`

**14 new tables, not the 18 the first pass claimed.**

---

## 2. The four fields, for the 14 new tables

Scope level and audience are the two that bite. `check-screens` **fails** a guest-callable
operation with no guest screen, so declaring `guest` commits us to a screen. Scope level decides
row-level security and, through ADR-0044, partitioning.

| table | scope | audience | permission | offline | note |
|---|---|---|---|---|---|
| `payment_method` | tenant | staff, guest | `TENANT_CONFIGURE` / `ORDER_VIEW` | read: yes | Master catalogue. A guest reads the list at checkout; only staff write it. |
| `payment_method_config` | venue | staff | `TENANT_CONFIGURE` | no | Which methods this venue offers. |
| `payment_policy` | tenant | staff | `TENANT_CONFIGURE` | no | Versioned. **ASK** whether a version is immutable once referenced. |
| `payment_eligibility_rule` | tenant | staff | `TENANT_CONFIGURE` | no | |
| `payment_fee_rule` | tenant | staff | `TENANT_CONFIGURE` | no | Carries money — `numeric(18,4)`, not their `decimal(18,2)`. |
| `payment_terminal` | **workstation** | staff, device | `TENANT_CONFIGURE` / `ORDER_VIEW` | **yes** | Has workstation_id and device_id. A till must know its own terminal offline. |
| `payment_gateway` *(merge)* | tenant | staff | `TENANT_CONFIGURE` | no | Credentials — must not be venue-readable. |
| `currency_rule` | tenant | staff | `REGION_CONFIGURE` | no | Touches ADR-0008 per-region scale. **ASK** how it relates to presentment currency. |
| `order_fee` | venue | staff, guest | `ORDER_VIEW` | yes | Guest sees fees at checkout. Written with the order. |
| `deposit` | venue | staff, guest | `ORDER_VIEW` / `ORDER_CREATE` | yes | Rental security deposits. Distinct from our `deposit_box`, which is physical cash. **Name them apart.** |
| `deposit_activity` | venue | staff | `ORDER_VIEW` | yes | Audit trail. Carries `created_by_user_id` — **§3.4 conflict**, becomes `principal_id`. |
| `cash_count` | **workstation** | staff | `SHIFT_CLOSE` *(new)* | **yes** | Already uses `approved_by_principal_id` / `counted_by_principal_id` — **their table, our convention.** Worth noting back to them. **ASK:** belongs in `shift.yaml` rather than `orders.yaml`? Schema says OrderService owns it; the contract may not. |
| `upgrade` | venue | staff, guest | `ORDER_EXCHANGE` | no | We have `ORDER_EXCHANGE` already. Carries `requested_by_user_id` — §3.4. |
| `membership_renewal` | tenant | staff, guest | `ORDER_CREATE` | no | **ASK** whether this is OrderService or a membership service — it references plan and customer_membership. |
| `recommendation_activity` | venue | staff | `ORDER_VIEW` | no | Analytics. **Candidate for `postgres-analytical`, not `postgres`.** |

**Store:** all `postgres` except `recommendation_activity`, which is a candidate for
`postgres-analytical` and should be decided rather than defaulted.

**Partitioning:** none of the 14 carries a `venue_id`, so under ADR-0044 **none of them partition**.
That is a consequence of §3.2 being unresolved, not a decision — if the venue question lands our
way, several of these should carry `venue_id` and partition.

---

## 3. The six ASKs — answered

All six were answerable from the package and their own workbook. None needs the client.

### 3.1  `orders.order` vs `orders.sales_order` — keep ours

**`ORDER` is a reserved word in SQL and in PostgreSQL.** `orders.order` has to be written
`orders."order"` at every use site — every join, every migration, every hand-written report query —
and the first person to forget the quotes gets a syntax error at the wrong moment. None of their
other table names collide: `discount`, `payment`, `upgrade`, `deposit`, `shift` are all clear.

**Keep `sales_order`.** This is the one rename to push back on, and it has a reason rather than a
preference behind it.

### 3.2  `relation_type` — take it, it is the 14 August rule made explicit

From their own descriptions:

- `relation_type` — cart: `PRIMARY`, `ADD_ON`, `CROSS_SELL`, `UPSELL`; order: those plus `UPGRADE`
- `item_source` — `CATALOGUE`, `FNB`, `RETAIL`
- `recommendation_source` — the service owning the recommendation rule

**`item_source` is *one cart, one order, one receipt across ticketing, F&B and retail* written as a
column.** The package has carried that rule since 14 August and never gave a line a way to say which
domain it came from. **Take all three.**

### 3.3  `cash_count` belongs in `shift.yaml` — and the precedent already exists

`shift.yaml` already declares persistence into `orders.cash_count_line`, `orders.pos_shift`,
`orders.cash_movement`, `orders.deposit_box` and `orders.no_sale_event`. **A contract file already
owns `orders.*` tables**, so schema ownership and contract ownership diverging is the established
pattern, not a new problem.

`cash_count` is the parent of `cash_count_line`, and `closeShift` and `acceptShiftVariance` are the
operations that write it. **It goes in `shift.yaml`. The schema stays `orders`, the service stays
OrderService.**

### 3.4  `membership_renewal` — describe it in `subscription.yaml`

Every membership operation lives in `contracts/satellite/subscription.yaml`. The table sits in the
`orders` schema and carries `renewal_order_id`, so a renewal produces an order.

**Same pattern as 3.3:** schema `orders`, service OrderService, described in `subscription.yaml`
beside the operations that use it.

### 3.5  `recommendation_activity` — `postgres-analytical`

It records impressions and outcomes against recommendation rules: high write volume, read by
reporting, never on a transaction path. That is exactly what `postgres-analytical` is for, and the
store map already holds five tables there. **Declaring it `postgres` by default would put analytics
traffic on the cell's transactional instance**, which ADR-0016 exists to prevent.

### 3.6  No new permissions — the vocabulary already covers it

The package has **127 permissions**, and the ones this cluster needs are already among them:

| need | existing permission |
|---|---|
| close a shift | **`SHIFT_CLOSE`** — already used twice in `shift.yaml` |
| accept a cash variance | **`OVERSHORT_ACCEPT`** — already exists, and is exactly this |
| void a payment | **`PAYMENT_VOID`** |

**One genuinely new permission: `PAYMENT_CONFIGURE`**, following the established `*_CONFIGURE`
family — `PRICE_CONFIGURE`, `TAX_CONFIGURE`, `DEVICE_CONFIGURE`, `WORKSTATION_CONFIGURE`,
`ACCOUNT_CONFIGURE`. `TENANT_CONFIGURE` is too broad for gateway credentials: a person who may
rename a venue should not thereby hold the merchant account reference.

### 3.7  One naming clash found while answering

**`orders.deposit_box` (ours) and `orders.deposit` (theirs) are different things.** Ours is a
physical cash box — `cashier_principal_id`, `opening_float`, `venue_id NOT NULL`. Theirs is a
refundable security deposit against a rental, with a lifecycle of `REQUIRED → AUTHORIZED → HELD →
RELEASED / FORFEITED`.

**Rename theirs `security_deposit`.** Two tables a letter apart, meaning unrelated things, is a
defect waiting to happen.

---

## 4. Method note, for the other clusters

**Do not trust a name match, and do not trust column overlap alone.** The sequence that worked:

1. exact name match → column merge
2. name absent → check our schema for a plausible rename **by reading both column lists**
3. only what survives both is new

Steps 1 and 2 are mechanical. **Step 3 is not, and skipping it would have created six duplicate
tables in this cluster alone.** Budget a person's afternoon per cluster for it, ahead of any
contract authoring.
