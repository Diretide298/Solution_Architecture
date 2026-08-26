# Waves

> **Purpose:** Context sequencing and rationale  
> **Owner:** Chinmay  
> **Status:** Settled


| Wave | Contexts | Reqs | Why here |
|---|---|---|---|
| **1 — Spine** | Tenancy & Org · Identity & AuthZ · Product & Entitlement · Order & Payment · Access Control | ~1,000 | Everything depends on them. Frozen before satellites start |
| **1b — Parallel** | **Finance & Ledger** | 327 | Orders write into the ledger from day one. Retrofitting a ledger under a live order module is expensive, and it is append-only so corrections are entries not edits |
| **2** | F&B · Retail · **Seating** · Guest Identity & Branding · Subscription & Licensing | ~600 | Highest volume, POS- and revenue-adjacent |
| **3** | Inventory & Procurement · Maintenance · Marketing/CRM · Resource Management · Virtual Queue | ~700 | Employee-app dependent |
| **4** | AI & Analytics · Accreditation · Device Management · Developer Platform · DAM · Rentals · Redemption | ~600 | Post-workshop. **Four have zero MoM coverage** |

## Placements worth explaining

**Finance runs parallel to the spine, not after it.** 327 requirements, and order + payment + entitlement + ledger must be one transaction. A ledger bolted on later is a rewrite of the order module.

**Seating is Wave 2, not later.** 112 requirements at zero coverage until recently, and seat categories, envelopes and capacity allocation are **entitlement concepts** — they constrain the Product & Entitlement spine rather than sitting on top of it.

**Guest Identity is Wave 2.** 83 requirements in Authentication & Login alone — the single largest sub-domain in the matrix, with one passing mention across seven MoMs.

**AI is Wave 4 for features, Wave 1 for governance.** AI-61 to AI-66 — logging, approval-before-execution, explainability, audit trail, usage analytics, consent — are preconditions. Nothing AI ships before them, and retrofitting an audit trail across sixty applications is not something you do twice. See [plan/ai-phasing](../plan/ai-phasing.md).

**Virtual Queue moved to Wave 3** pending [CF-33](../registers/conflicts.md). The Virtual **Waiting Room** (C98) is separate and is **Wave 1** — it is what keeps the platform standing at 15,000 concurrent during an on-sale.

## Blocked

| Context | Blocked on |
|---|---|
| Access Control | Turnstile SDK · hardware models · pilot venue |
| Device Management | Hardware models · domain workshop |
| Accreditation · Developer Platform · Rentals | Domain workshops (CF-21) |
| AI & Analytics | CF-20 residency ruling |
