# ADR-0048: Guest recurring billing is commerce, not the Control Plane

**Status:** Accepted
**Date:** 21 September 2026
**Decides:** the boundary half of **BL-100**
**Relates to:** [ADR-0039](0039-control-plane-and-tenant-database-lifecycle.md), [ADR-0043](0043-the-control-plane-splits-on-personal-data.md), [ADR-0028](0028-service-decomposition.md)

---

## Context

**BL-100 argued the boundary and then the package drifted across it.** The entry's own words:

> `subscription` looks like the answer and is not. It is the Control Plane, running outside any
> cell because it provisions cells, and it bills **tenants** for the platform. A guest paying
> monthly for an annual pass is a different ledger, a different payer and a different failure mode.

That reasoning is correct. It is also what `subscription.yaml` now contradicts: **seventeen
membership operations sit in it**, including `setRenewalAutoMembership`, `listRenewalAuto` and
`listMembershipRenewalRetention` — guest membership billing, in the contract that provisions cells.

**All seventeen are `x-ticvai-provisional`.** They were read off a workshop pack and never
specified, which is how they arrived without the boundary being argued. **Nobody decided this; a
filename did.**

### Why it matters more than tidiness

**The Control Plane runs outside every cell, by design.** ADR-0039 puts it there because it creates
and drops tenant databases, and ADR-0043 splits it again on personal data. A guest's recurring
charge is the opposite shape:

| | Control Plane billing | Guest recurring billing |
|---|---|---|
| **Payer** | a tenant, under a contract | a guest, under a mandate |
| **Ledger** | platform revenue | venue revenue, in-cell |
| **Residency** | outside the cell | **inside it — the guest is personal data** |
| **Failure** | an invoice goes unpaid | a card declines and somebody is at a gate |

**The residency row is the one that is not negotiable.** A guest's payment history in a
control-plane table is personal data outside its jurisdiction, which is the thing the cell model
exists to prevent.

---

## Decision

**Guest recurring billing lives where the rest of the billing lives.**

    payments.yaml     the policy -- dunning, retry spacing, decline classification,
                      what happens when the attempts run out
    orders.yaml       the record -- a statement of what was charged, guest-facing,
                      computed from the ledger rather than stored beside it

**`subscription.yaml` keeps tenant billing and nothing else.** `generateInvoice`,
`listSubscriptionInvoices`, `recordInvoicePayment` and the dispute path are platform-to-tenant and
stay where they are.

### The seventeen provisional drafts are not moved yet, and that is deliberate

They are unreviewed workshop text awaiting one of the seven provisional-review sessions (CF-171).
**Relocating seventeen operations nobody has agreed would assert a home rather than record one** —
and the review exists precisely so that a pack's guess does not become the package's position by
being left alone.

**This ADR is the instruction to the session that reads them**: membership billing belongs in
`payments` and `orders`, and a draft that survives review moves there rather than being promoted
where it landed.

---

## Consequences

**Built the same day** (BL-100): `DunningPolicy`, `DunningCase`, `DeclineClass` and the dunning
queue in `payments.yaml`; `BillingStatement` in `orders.yaml`.

**Two constraints that came out of building it and belong here rather than only in a description:**

**Dunning retry and gateway retry are different axes and must never share a counter.**
`setPaymentFailoverPolicy` governs retry *inside* one attempt — seconds, a different provider, and
a decline is final there. Dunning governs retry *across days* — a fresh authorisation on a card
that may since have been replaced. **Both are called "retry", and treating one as the other is how
a guest is charged twice.**

**Dunning cannot revoke admission.** `terminalAction` stops at `suspendBilling` and `cancelRenewal`.
`graceDays` already governs how long a pass keeps working, and the case this separation protects is
a guest at a gate on a family day out, refused because a card expired and a retry ran at 3am.
**Ending somebody's access stays a staff decision with a name attached.**

**What this does not decide.** Stored-card scope and PCI boundaries, which BL-100 also warned about
and which arrived with the mandate model without being re-examined. That is a security review, not
a contract question, and it is not answered here.
