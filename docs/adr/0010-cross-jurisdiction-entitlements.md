# ADR-0010: Cross-Jurisdiction Entitlements

**Status:** Accepted
**Date:** 13 August 2026
**Closes:** CF-31
**Constrains:** ADR-0001 cells · Product & Entitlement spine · Order & Payment spine · Finance & Ledger

---

## Context

A cell serves one tenant in one jurisdiction (ADR-0001). CF-31 asked whether a guest-app's
entitlements, wallet, membership and identity are confined to one cell, or span them.

Four features depend on the answer:

- A multi-venue pass whose venues sit in different countries
- A membership valid across a tenant's whole estate
- A wallet balance spendable at any venue
- One guest-app account across all channels and venues

**Client decision: yes, these cross jurisdictions.**

This is the more expensive answer. It is also the commercially correct one — a tenant
selling a portfolio pass cannot sell a pass that stops at a border their guests do not
perceive.

It is legally workable. Cross-border transfer is permitted under PDPL Article 22 with
adequacy, or Article 23 with contractual safeguards or explicit consent (ADR-0009). The
constraint is that every transfer needs a documented mechanism — not that transfer is
prohibited.

---

## Decision

**Home-cell ownership with delegated redemption.** No shared database, no distributed
transaction, and no personal data crossing a border without a basis.

### 1. Guest Link Registry — Control Plane, pseudonymous only

A global registry mapping a stable pseudonymous `guestLinkId` to the cells holding a local
record for that guest-app.

```
GuestLink {
  guestLinkId    ULID          // pseudonymous. Not derived from any personal data
  homeCellId                   // cell of first registration. Authoritative for wallet
  linkedCells    [ cellId ]
  consentVersion               // Article 23 consent basis for cross-border linkage
  linkedAt
}
```

**What crosses the border: the link ID and nothing else.** No name, email, phone, document
number, date of birth or biometric template. Each cell holds its own `Subject` record with
its own PII, referenced locally.

A guest-app who has never transacted across jurisdictions never acquires a link.

### 2. Linking is explicit and consented

Creating a link is a **guest-app action with recorded consent**, not a silent side effect of
buying a cross-border product. The consent record is the Article 23 basis and carries the
version of the notice shown.

Withdrawing consent severs the link. Existing entitlements already redeemed are unaffected;
un-redeemed cross-cell rights are revoked and refunded per policy.

### 3. Entitlements: issued once, replicated as redemption rights

The **selling cell owns the order and the entitlement.** Consuming cells receive a
*redemption right* — a narrow projection carrying only what a gate needs:

```
RedemptionRight {
  rightId, guestLinkId, ticketId
  validFrom, validTo, admissionProfileId
  entriesAllowed, entriesConsumed
  issuingCellId
}
```

No PII. Redemption is **authoritative in the consuming cell** — the gate must work when the
inter-cell link is down, which is the same reason venue edge nodes exist. Consumption is
reported back and reconciled.

This is the offline sync pattern applied across cells rather than across a WAN gap. The
problem shape is identical: local authority, eventual reconciliation, idempotent replay.

### 4. Wallet: single authoritative balance, never split

Split balances double-spend. The home cell holds the authoritative balance.

| Path | Mechanism |
|---|---|
| Spend in home cell | Local, synchronous |
| Spend in a linked cell, link up | **Synchronous authorisation** against the home cell — the card-authorisation pattern. Hold, capture, release |
| Spend in a linked cell, link down | Draw against a **pre-authorised allocation** the consuming cell holds. Bounded, so exposure is capped |
| Reconciliation | Continuous. Allocation topped up or clawed back |

The allocation cap is a tenant configuration. Set to zero, wallet spend simply fails when
the link is down — which some tenants will prefer.

### 5. Orders never span cells

An order is created, paid and posted in **one** cell. What propagates is the redemption
right, not the order.

This avoids a distributed transaction entirely. The order + payment + entitlement + ledger
transaction stays atomic within its cell, which was the reason for schema-per-service in the
first place.

### 6. Revenue allocation crosses legal entities

12 Aug §16 already requires revenue split by percentage or fixed amount per venue. Where
venues sit in different countries, that split now crosses **legal entities in different tax
jurisdictions**.

| Consequence | |
|---|---|
| Inter-company positions | The selling entity owes the consuming entity for redemption |
| Settlement | Periodic inter-company settlement, not per-transaction |
| Tax | Each entity accounts under its own regime. The split is a transfer, not a sale, in the consuming entity |
| Currency | Split across regions with different currencies and scales. FX policy required |
| Recognition | Deferred until redemption in the consuming entity, not at sale |

**This is the largest downstream consequence of the decision** and it lands in Finance &
Ledger, not in the entitlement model.

### 7. DSAR and erasure fan out

A guest-app linked across cells exists in both. Access, rectification and erasure are
orchestrated from the Control Plane by `guestLinkId`, fanning out to each linked cell.

Erasure deletes each cell's PII record. The link is severed. Ledger entries retain their
opaque subject reference and stay intact.

---

## Consequences

| | Detail |
|---|---|
| **New component** | Guest Link Registry in the Control Plane |
| **New component** | Inter-cell redemption propagation and reconciliation |
| **New component** | Cross-cell wallet authorisation with allocation fallback |
| **Compliance** | Article 23 consent basis per link. Transfer register. DPIA |
| **Finance** | Inter-company settlement, transfer pricing, cross-currency allocation |
| **Availability** | A linked-cell spend depends on the home cell, unless allocation covers it |
| **Latency** | Cross-cell wallet authorisation adds a round trip. Entitlement redemption does not — it is local |
| **Testing** | The reference fixture must include a two-cell tenant with a linked guest-app |

### What does *not* change

- Cells stay isolated. No shared database, no cross-cell query
- Orders stay atomic within a cell
- Gate validation stays local and offline-capable
- No PII crosses a border

---

## Alternatives

| Rejected | Why |
|---|---|
| Entitlements confined to one jurisdiction | Simplest, and the client has ruled it out. A portfolio pass that stops at a border is not the product |
| Shared global entitlement database | Puts entitlement data — and by association guest-app data — outside every jurisdiction. Fails residency |
| Full guest-app replication across cells | PII crossing borders continuously. Maximum compliance exposure for minimal gain |
| Distributed transaction across cells | Two-phase commit across regions, over the public internet, in the sale path. Unacceptable latency and failure modes |
| **Home-cell ownership with delegated redemption** | **Accepted.** No PII crosses, no distributed transaction, gates stay offline-capable |

---

## Open Items Arising

| # | Question | Owner |
|---|---|---|
| 1 | Default wallet allocation cap when the inter-cell link is down. Zero, fixed, or percentage of balance? | Qossai |
| 2 | Inter-company settlement frequency and the transfer pricing basis | Finance — TICVAI |
| 3 | FX policy for allocation splits across currencies. Rate at sale, at redemption, or at settlement? | Finance — TICVAI |
| 4 | Does a membership grant cross-jurisdiction benefits automatically, or is that a separate product attribute? | Qossai |

Item 3 affects the ledger and should be settled before Finance & Ledger contracts are
drafted.
