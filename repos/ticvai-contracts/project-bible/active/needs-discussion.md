# Needs Discussion — Client Agenda

> **Purpose:** Everything requiring TICVAI input, in priority order
> **Owner:** Chinmay
> **Status:** Living — updated 13 August 2026

**19 items.** Nine are decisions, five are deliverables, four are workshops, one is legal.

Nothing here blocks Sprint 1. Items 1–4 block work starting within two to four weeks.

---

## Suggested Session Split

| Session | Items | Attendees | Duration |
|---|---|---|---|
| **A — Finance** | 1 | Qossai, Allam, TICVAI Finance | 30 min |
| **B — Operations & scope** | 2, 3, 5, 6, 7, 8 | Qossai, Allam, Chinmay | 60 min |
| **C — Four domain workshops** | 13–16 | Per domain | 90 min each |
| **D — Commercial** | 9, 10, 11, 12 | Qossai | 45 min |
| **E — Legal & compliance** | 17, 18, 19 | Allam + counsel | 30 min |

Sessions A and B are the ones to hold this week.

---

# Priority 1 — Blocking within 2 weeks

## 1. FX policy for cross-region revenue splits — CF-37

**Decision · TICVAI Finance · email drafted**

A pass sold in one region and redeemed in another splits revenue across legal entities in
different currencies. At what rate, at what moment, and which entity carries the movement.

A pass sells for 100, split 60/40. Rate 10.00 at sale, 9.50 at redemption, 9.80 at
settlement. Entity B books **400, 380 or 392** depending on the answer. Same transaction,
5% spread.

**Recommendation:** daily published rate · convert at redemption · inter-company balance
denominated in the consuming entity's currency · movement to the selling entity's FX gain
and loss · open balances revalued at close · breakage recognises wholly in the selling
entity.

**Why now:** the ledger is append-only. Once cross-currency entries exist, a different
policy means posting corrections rather than restating.

**Blocks:** ~12 finance API operations, several ledger tables, and the period-close process.

---

## 2. Exact hardware models and reference numbers

**Deliverable · Qossai / Allam · outstanding since 12 August**

**The ask has changed shape.** Per ADR-0015, roughly nine of fourteen device classes have
real open standards — ESC/POS for printers and drawers, UnifiedPOS for POS peripherals,
OSDP for access readers. We are building to those now.

So the list is needed for **verification, procurement and acceptance**, not for design:

- Confirming each model implements its standard rather than an emulation with gaps
- Ordering the lab bench
- Acceptance testing

**Blocks:** lab procurement, which has lead time.

---

## 3. Turnstile SDK and specification

**Deliverable · Qossai / Allam · outstanding since 5 August**

OSDP standardises reader-to-controller. It does **not** standardise controller-to-application
— that layer is vendor-specific.

We have designed the driver interface to OSDP's command shape, so the vendor adaptor is a
translation rather than a redesign. The SDK now blocks **one adaptor**, not the interface.

**Blocks:** the access-control driver. Access Control is the largest sub-domain at 125
requirements.

---

## 4. Lab rig in place of a pilot venue

**Decision · Qossai / Allam / Dinesh**

There is no pilot venue, and Gate 4 as written is unprovable without one.

**Proposal — split the gate:**

| Gate | Where | Proves |
|---|---|---|
| **4a** | Lab rig with a severable network | The architecture is correct |
| **4b** | First real venue | The deployment is correct |

4a becomes the go/no-go for Wave 2. 4b becomes a per-venue acceptance step, which it should
have been anyway.

**Lab rig:** one turnstile and reader · one POS terminal with drawer, receipt printer,
ticket printer and customer display · one handheld · one payment terminal · **a managed
switch you can pull** · a throttled uplink to simulate 4G.

**Ask:** is **off-hours access to any operating venue** possible for 4b? Two nights before a
rollout is enough. Much smaller than a dedicated pilot site.

---

# Priority 2 — Scope confirmations

## 5. Two employee modules have no provenance — CF-40

**Decision · Qossai / Allam**

Two screens in the employee app design reference appear in **neither the requirement matrix
nor any of the seven MoMs**:

| | What it is |
|---|---|
| **Training & Knowledge Base** | SOP and manual library, videos, per-course progress, due dates, required vs optional |
| **Employee Recognition / Kudos** | Peer recognition with categories, message and recipient |

Design references are rank 3 — directional, not scope.

**Our split view:**

| | Recommendation |
|---|---|
| SOP repository | **Probably in.** The AI assistant grounds on SOPs and asset screens reference them. Small — a document store with search |
| Training management — courses, assignment, progress, due dates | **Probably out.** That is an LMS |
| Recognition / kudos | **Probably out.** No operational function |

**Question:** does TICVAI or the tenant already have an LMS? If so the answer is an
integration, not a build.

---

## 6. Five device classes absent from the Integrations sheet

**Decision · Qossai / Allam**

These appear in requirements but not on the Integrations sheet. Either it is incomplete or
they are out of scope. Both answers are fine; the ambiguity is not.

Parking and ANPR · queue and people-counting sensors · ticket-eater and game readers ·
electronic lockers · digital signage.

---

## 7. Reference modules and integration scope boundary

**Decision · Qossai / Allam**

**Integrations:** Tier 1 is the Integrations sheet, roughly 35 systems. Additional payment
processors and turnstile controllers are supported through driver extensibility rather than
pre-built. Confirming the tiering avoids a UAT dispute.

**Sub-domain naming:** the "Retail POS" domain's only sub-domain is "Wallet" (78
requirements). Worth confirming this is intended.

---

## 8. AI is a primary navigation tab in the employee app — CF-41

**Decision · Qossai + Chinmay**

The employee app's bottom navigation is Home · Tasks · Scan · **AI** · More.

AI-06 sits in Wave 2 of the phasing paper, but the app shell cannot ship without the tab
existing.

**Options:** move AI-06 to Wave 1 · ship the shell with a disabled tab · reorder the
navigation.

---

# Priority 3 — Commercial

## 9. AI Phase 1 scope — 15 of 67 applications

**Decision · Qossai / Allam · position paper drafted**

Conversational AI, natural-language reporting, and the six governance applications.
Forecasting, dynamic pricing, recommendations and fraud detection defer until operating data
exists.

**Also needed:** a view on AI Translation, which meets the same cold-start test and supports
the Arabic and English obligations.

## 10. Dynamic pricing guardrails

**Decision · Qossai**

46 requirements describe the pricing mechanism. **None define price floors, ceilings, or
maximum movement per period.**

Unbounded automated pricing on a large multi-venue operator is a commercial and reputational
exposure. Needed before design even though delivery is Phase 3.

## 11. Guest app distribution and publishing

**Decision · Qossai / Allam · options paper drafted**

Tiered distribution: branded native apps for dedicated tenants, PWA for shared tier,
universal app as a discovery surface only.

**Requires tenants to hold their own Apple and Google developer accounts** and grant TICVAI
App Manager access — Apple Guideline 4.2.6 rejects template apps submitted by the provider.

**D-U-N-S registration has lead time. Start it before it is on the critical path.**

## 12. Region placement and branded publishing as priced tiers

**Decision · Qossai**

Under cell-per-region, each region has an infrastructure cost floor. Branded app publishing
carries per-tenant operational cost.

Both need to be priced features in the licensing model rather than absorbed.

---

# Priority 4 — Workshops

**~276 requirements have never been discussed with the client — CF-21.** Four sessions.

| # | Domain | Reqs | Why it matters |
|---|---|---|---|
| **13** | **Accreditation & Credential Management** | 58 | **Accreditation validation appears on the employee scanner.** Not safely deferrable — the scanner shell needs it |
| **14** | **Developer & API Management** | 94 | Largest of the four. Sandbox, API keys, developer roles |
| **15** | **Device Management** | 60 | 100% hardware-dependent. Manages the lifecycle of every device in every other domain |
| **16** | **Rentals** *(inside F&B POS)* | ~64 | Check-out and check-in, deposits, serial tracking, overdue |

Also outstanding: **17 — AI concierge mechanism and token billing model (CF-14)**, and
**guest authentication**, which is 83 requirements — the largest single sub-domain in the
matrix — with one passing mention across seven MoMs.

---

# Priority 5 — Legal and compliance

## 17. PDPL transfer position

**Legal · Allam → counsel**

Per ADR-0009, residency is architectural. Cross-border AI inference is permitted under PDPL
Articles 22 and 23 with a documented mechanism, a transfer risk assessment, and a DPIA where
processing is high-risk.

**Needs counsel confirmation**, plus an assessment of DIFC Regulation 10 applicability for
any DIFC-located venue.

## 18. Biometric data is sensitive under PDPL — CF-35

**Decision · Allam + Chinmay**

Biometric data attracts heightened protection — explicit consent, DPIA, stricter transfer
rules.

This affects **Face Pass, facial readers and fingerprint enrolment**, and was not previously
flagged.

## 19. Payment gateway sandbox credentials

**Deliverable · Allam · in progress**

Stripe and Network International. Needed for the recovery paths — payment-status inquiry and
the background reconciler — which are untestable without a sandbox.

A terminal that charged a card and never received a response is the normal failure, not the
exotic one.

---

# Record Corrections

Not decisions, but the MoM record needs amending.

| # | Item |
|---|---|
| **R1** | **12 Aug party inversion** — decision bullets invert the parties relative to the body and every prior MoM. **Five action items have ambiguous ownership** |
| **R2** | **12 Aug self-contradiction** — one bullet says front-end selection is role-driven and not device-driven; another says it auto-loads from the workstation. Resolved by ADR-0002, but the record should say so |
| **R3** | **10 Aug §5.1 lost subject** — *"agreed this makes more sense and will be adopted"* names nobody. No owner for a decision since partially reversed |
| **R4** | **Matrix duplicate IDs** — requirement IDs 5.6.1 to 5.6.8 appear twice with different text. Citations to them are ambiguous. A full audit is advisable before the matrix is used as the acceptance baseline |

---

# Summary

| Priority | Items | Type |
|---|---|---|
| 1 — Blocking within 2 weeks | 4 | 1 decision, 2 deliverables, 1 proposal |
| 2 — Scope confirmations | 4 | Decisions |
| 3 — Commercial | 4 | Decisions |
| 4 — Workshops | 5 | ~276 requirements |
| 5 — Legal and compliance | 3 | 1 legal, 1 decision, 1 deliverable |
| Record corrections | 4 | Amendments |

**Item 1 is the only one holding contract work today.** Items 2, 3 and 4 hold hardware and
acceptance, which becomes critical in three to four weeks. Everything else can wait a
fortnight without cost.
