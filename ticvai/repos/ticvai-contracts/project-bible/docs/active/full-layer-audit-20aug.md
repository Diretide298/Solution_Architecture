# Full-layer audit — 20 August

Flows, screens, contracts, schema and the connections between them. **All nine validators pass.**
What follows is what the audit found that a validator does not fail on: judgements, not defects.

---

## Flows and journeys — clean

**27 flows. 0 broken screen references, 0 unknown operations, 0 unresolved branches, every one of
28 contracts touched by at least one flow.**

Nothing to fix. **The flow layer is the best-built artefact class in the package** and this audit
found nothing wrong with it.

**What is thin is coverage, not correctness.** 158 of 943 operations are named by a flow, and 106
of 476 screens appear in one. Seventeen contracts have exactly one flow — `subscription` has one
over 55 operations, `fnb` one over 50. **Every flow written so far has found a defect**, which is
the argument for writing more of them.

---

## The eighteen tables written by more than one contract

**Not a defect list.** A contract writing another's table is how a platform stays coherent — a till
that cannot post to the ledger is a till whose takings nobody can reconcile. **What matters is
whether each crossing is deliberate.**

### Correct, and would be wrong otherwise

| Table | Foreign writers | Why it is right |
|---|---|---|
| `ledger.entry`, `ledger.journal_entry` | orders, shift | **A sale and a till close both post to the ledger.** Routing them through `finance` would make every sale a two-hop write, and a ledger written only by finance is a ledger that lags the thing it records |
| `access.entitlement` | catalogue, orders | An order issues an entitlement; a catalogue change revalidates one. **Both are the moment the row's truth changes** |
| `pii.subject` | identity, marketing-crm | `identity` for registration and deletion, `marketing-crm` for `updateMyProfile` — **the one place a guest edits their own name.** ADR-0023 says one writer; this is one and a half, and it is worth confirming rather than assuming |
| `catalogue.inventory_lease` | orders | Leasing is what an order does to inventory. **The lease is `catalogue`'s row and only `orders` has a reason to take one** |
| `inventory.stock_level` | fnb, retail | A production run consumes stock and a collection releases a reservation. **Stock moves where the work happens** |
| `marketing.message_dispatch` | orders, public-api, workforce, identity | **Five writers, and every one is sending a message.** An order confirmation, a webhook, an evacuation notice and a verification email are all dispatches — a single writer would mean four contracts asking marketing to send things |

### Worth a second look

**`orders.sales_order` written by `identity`** — one operation, `linkGuestCheckout`. **A guest
registering after checking out attaches their new account to the order they just placed.** Correct
in intent, and it is the only write to a sales order from outside `orders`. **Worth confirming it
sets the subject and nothing else.**

**`ai.interaction` written by `reporting`** — `askReportingQuestion` and
`saveNaturalLanguageQuery`. **ADR-0020 says only the AI contract writes AI tables**, and this is
the exception the ADR itself names: the governed reporting pair. **It caught me three times in one
day when I tried to add a fourth.** Correct, and the reason it looks wrong is that the rule is
strict.

**`marketing.consent_record` written by `access` and `orders`** — `enrolFacePass` and
`storePaymentToken`. **Consent captured at the point it is given rather than routed through
marketing**, which is right: a guest consenting to biometric enrolment at a gate is not a marketing
interaction, and **a consent record written later is a consent record with the wrong timestamp.**

---

## The forty tables no operation touches

**28 are children** — reached through their parent's operations, which is correct and not
countable as a gap.

**Ten of the remaining twelve are infrastructure**, and the package already says so in their own
descriptions: default partitions (`access.scan_event_unassigned`,
`orders.sales_order_unassigned`), migration bookkeeping (`platform.schema_version`), the
authorisation layer's own audit trail (`identity.authz_audit`), a rotating hashed location code.
**These are written by the platform rather than by an API, and an operation touching them would be
the defect.**

### Two are real

**`orders.fraud_rule` — 6 columns, no operation.** BL-118 built the model and **nothing
configures a rule.** A fraud rule that cannot be added, edited or disabled is a fraud rule that
ships with whatever it was seeded with, forever.

**`orders.group_booking` — 10 columns, no operation.** A group with a leader and an attendee
manifest, and **no way to create one.** Built during Track 3 as part of CL-05 and never given an
operation surface.

**`platform.denomination` was the third** until this morning, when `POS-001` gained the cash-count
screen — it is now reached and is left here as the example of how these close.

---

## What the audit changed

**116 tables had no `id` column**, and the cause was one thing rather than 116: **the schema
reference derives table columns from API response schemas, and a response is not a table.**
`Subscription` returns tenant, plan and status — everything a caller needs and **not the row's own
identity.**

**32 had no key at all** — no id, no parent, no natural key. `marketing.guest_profile` among them:
**a row nothing could address, update or delete.** All 32 given a key at source, and
`check-package` now refuses a table without one.

**The fix took four attempts and three were wrong**, which is worth recording because each failure
was a different shape:

1. **A self-referencing parent key** — `navigation_item_id` on `navigation_item`, pointing at the
   row it sits on.
2. **A guard that dropped the row's own `id`** along with the false key — **turning a
   self-reference into a table with no key at all**, a worse defect than the one being fixed.
3. **A duplicate `id`**, three times, in contracts that already had one inline — caught each time
   by the duplicate-key check.
4. **And the check itself was wrong.** `navigation_item_id` on `navigation_item` **is** a primary
   key, by a convention half this package uses. It demanded literally `id`.

**Then the real bug.** `derive-schema` merged a derived table into the existing one only when the
derived set was at least as long — so **a contract adding a primary key lost to an arithmetic
comparison**, because the existing row already held two columns the relationship graph had
supplied. Now merged by column: contract-derived wins where they overlap, graph-derived is kept
where the contracts say nothing.
