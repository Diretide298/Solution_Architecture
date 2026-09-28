# Status words: what "open", "live", "active" and "settled" mean

> **Purpose:** the one-page table the client asked for in audit R095
> **Owner:** Chinmay
> **Status:** Proposed, 28 September 2026. Client product to correct.

**The state models in `states/*.yaml` are the rule (decided 28 September, audit R095).** An action that is not allowed from an entity's current status is refused. It is not accepted and then fixed up later. The contracts, screens and filters use the four words below, and this table pins each word to the statuses it covers, entity by entity. A correction to this table becomes a change to the state model and the filters that use it.

| Entity | All statuses | "Open" | "Live" / "active" | "Settled" / finished |
| --- | --- | --- | --- | --- |
| Order (`OrderStatus`) | pending, held, partiallyPaid, paid, completed, partiallyRefunded, refunded, voided, failed | pending, held, partiallyPaid: money still owed | — (an order is never "live") | paid, completed, partiallyRefunded: paid in full. voided, refunded and failed are **closed**, not settled |
| Shift (`ShiftStatus`) | pendingApproval, open, suspended, pendingClosure, pendingVariance, closed, autoClosed | open, suspended, pendingClosure, pendingVariance: the till still holds the shift's cash | open: the only status that can take sales | closed, autoClosed. closed can be reopened with a supervisor's PIN (audit R144); autoClosed cannot |
| Promotion (`PromotionStatus`) | draft, scheduled, live, paused, expired, ended | draft, scheduled, paused: can still be edited or resumed | live: the only status the cart evaluates | expired, ended |
| Tenant (`TenantStatus`) | onboarding, active, suspended, terminating, terminated | onboarding | active: can trade. suspended keeps its data and cannot trade | terminated. terminating is still amendable only through the termination steps |
| Work order (`WorkOrderStatus`) | open, assigned, inProgress, paused, awaitingParts, completed, verified, cancelled, closed | open, assigned, inProgress, paused, awaitingParts | inProgress | verified, closed. cancelled is closed without work. completed waits for a supervisor other than the technician to verify it (audit R106) |
| Seat hold (`SeatHold.status`) | held, converted, released, expired | held | held: counts against capacity (audit R101) | converted (sold), released, expired |

**Where the words appear.** A list filter such as `status=open` or "open orders" means exactly the "Open" column. "Active" in a count or KPI means the "Live / active" column. "Settled" in finance and reports means the "Settled" column. Voided and failed orders are never counted as settled.
