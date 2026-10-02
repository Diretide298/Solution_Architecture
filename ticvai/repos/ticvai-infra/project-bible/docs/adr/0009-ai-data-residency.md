# ADR-0009: AI Data Residency

**Status:** Accepted · section 2 amended by [ADR-0049](0049-vectors-live-in-qdrant-one-collection-per-tenant.md), 30 September 2026: Qdrant on every tier, one collection per tenant with a collection-scoped token; the shared tier no longer uses pgvector · sections 1 and 3 amended 2 October 2026 (Chinmay): **a residency class per tenant**, UAE-only by default through Core42 Compass (see the amendment below); the vendor terms are still to be had in writing
**Date:** 13 August 2026
**Closes:** CF-20
**Supersedes:** the working assumption that UAE law mandates domestic AI data storage

---

## Amended 2 October 2026: a residency class per tenant

**Decided by Chinmay, 2 October 2026** (DEC-539 and DEC-540 in `docs/registers/decisions-2-october.md`;
change entry CHG-DOC-003). Source: `docs/active/research/ai-ml-model-selection-2-october.md`, sections 2.1
and 2A. It amends AI-D02 and AI-D03 (`handoff/ai-decisions.json`).

**Why section 1 could not stand as written.** Section 1 keeps inference on an in-region endpoint, and the
design's default was Azure OpenAI in UAE North (AI-D02, AI-D03). The research found that **Azure UAE North
serves no chat or reasoning model in-region on pay-per-token**: it offers Global Standard (data at rest in
the UAE, processing anywhere) or Regional Provisioned throughput, whose minimum is about $8,450 a month for
the Small tier before the first tenant asks a question. UAE government and bank apps run on a sovereign
wrapper (G42/Core42 Compass); consumer and leisure apps, including our closest peer, make no residency
claim at all.

**The decision: every tenant has an AI residency class.**

| Residency class | Small tier | Strong tier | Fallback when the breaker opens |
|---|---|---|---|
| **UAE-only**: the default, and mandatory for government and semi-government, bank or payment, and health tenants | Core42 Compass GPT-4.1 mini (or GPT-4.1 Arabic, "Seraj", if it wins the Arabic golden set) | Compass GPT-5 (UAE region) | OpenAI's UAE region, then the in-cell open model (gpt-oss-120b, the same model Compass serves) |
| **Global allowed**: a private venue opts in under PDPL Art. 23 (vendor contract, DPIA, privacy notice) | Azure gpt-5-mini, Global Standard, or the tenant's BYOK provider | Azure gpt-6-sol, Global Standard | The UAE-only chain |
| **On-premise** (ADR-0046) | Qwen3.5 or gpt-oss | Qwen3.5-122B; Falcon-H1 Arabic or Jais 2 for Arabic-heavy tenants | None outside the site |

1. **Compass is reached through the existing `openaiCompatible` provider kind**, so no new adapter. It runs
   on Azure and is billed through Azure Marketplace; per-token billing per selected module (AI-D02) stands.
2. **The class is a per-tenant setting** that extends the region's `allowedAiResidencies`
   (`contracts/spine/tenancy.yaml`). The gateway resolves a provider from the class: **a UAE-only tenant can
   only resolve to an endpoint inside the UAE**, and a residency refusal is never failed over to a
   cross-border endpoint (ADR-0034).
3. **Section 3's transfer register lists every Global-allowed tenant**, with its Article 23 mechanism, the
   transfer risk assessment, the DPIA and the notice. **BYOK other than OpenAI's UAE region is a
   cross-border transfer**, so BYOK is available only to Global-allowed tenants (AI-D20, closed the same day).
4. **Embeddings, reranking, the guard model and PII detection stay self-hosted in the cell** for every
   class, and every prompt is scrubbed offline before it leaves, whatever the class (ADR-0020, amended the
   same day).
5. **Scale step.** When steady Small-tier traffic in a region nears about 100,000 calls a day, the UAE-only
   Small tier moves to Azure UAE North Regional Provisioned throughput (gpt-5-mini, 25 to 50 PTU) with
   spillover **off** (spillover can only target Global Standard).

**Before signing, in writing** (DEC-541, open: it needs the vendors and counsel; CHG-DOC-004): Core42
Compass's retention, logging and sub-processor terms, its minimum, and the in-UAE region of each model;
OpenAI's approval of the UAE region and of Modified Abuse Monitoring; Microsoft's PTU calculator figures at
our traffic mix; and legal advice on whether Miral and Dubai Holding count as government entities (which
would make their tenants UAE-only by law, not by default).

---

## Context

CF-20 was raised on the assumption that UAE regulation would require AI data — prompts,
embeddings, logs, vector stores — to remain physically in-country, and that a third-party
LLM API would therefore be non-compliant. The Qdrant selection was held pending a ruling.

Research shows the premise was wrong in one important respect and right in another.

### What the regulation actually says

<cite index="10-1">The cornerstone of onshore privacy regulation is the UAE Personal Data Protection Law (Federal Decree-Law No. 45 of 2021), in force since 2 January 2022. It applies to controllers and processors established in the UAE, and extraterritorially to entities outside the UAE processing personal data of individuals residing in the UAE.</cite>

<cite index="3-1">UAE law defines strict controls for personal data processing under Federal Decree Law No 45 of 2021, without mandating domestic storage.</cite>

Cross-border transfer is governed by two articles:

- <cite index="16-1">Article 22 permits transfer where the recipient country provides an adequate level of protection as determined by the UAE Data Office, or where a bilateral or multilateral agreement exists.</cite>
- <cite index="13-1">Where neither applies, alternative mechanisms include binding corporate rules, standard contractual clauses imposing UAE-level protections, explicit and informed consent, or necessity for contract performance. A transfer risk assessment must be conducted before initiating cross-border data flows, with documentation of all transfer mechanisms maintained.</cite>

<cite index="10-1">The UAE AI Office published the UAE Charter for the Development and Use of Artificial Intelligence on 30 July 2024, supplemented by an International Policy on AI in September 2024. Both are non-binding but inform sectoral rule-making and are commonly referenced in commercial contracts and procurement.</cite>

<cite index="10-1">DIFC's Regulation 10 on autonomous and semi-autonomous systems reaches full enforcement from January 2026.</cite>

### Why residency still matters architecturally

<cite index="5-1">There is no single AI residency rule. The obligation comes from the data-protection and sector regulations that already govern the data an AI feature touches, applied to the new processing path. The hard part is inference: when a prompt built from customer data is sent to a foundation model hosted elsewhere, that data has left the region regardless of where the application runs. The controls that decide residency are architectural — where the model runs, where prompts and logs are written, where embeddings are stored, and whether any sub-processor moves data across a border.</cite>

<cite index="9-1">Sovereignty applies to prompts, datasets, intermediate outputs and learned representations.</cite>

---

## Decision

**Residency is an architectural property, not a storage location.** TICVAI keeps the entire
AI processing path in-jurisdiction by default, and treats any cross-border path as an
Article 22/23 transfer requiring a documented mechanism.

### 1. In-jurisdiction by default

| Component | Placement |
|---|---|
| Vector store | **In-cell**, in the cell's jurisdiction |
| Prompt and response logs (AI-61) | In-cell |
| Embeddings and derived representations | In-cell |
| Retrieval indices | In-cell |
| **Inference** | **In-region endpoint** — regional cloud AI service or self-hosted model |

<cite index="5-1">Residency is met by deploying inference in-region, keeping prompts, logs and vector stores in-country, and contracting cross-border transfer out where the law requires it.</cite>

### 2. Qdrant is selected, deployed in-cell

> **Amended 30 September 2026 by ADR-0049.** Qdrant on **every** tier, shared included: self-hosted
> in Azure UAE North (3-node HA), a single node on-premise, one collection per tenant with a token that
> reaches only that collection. The `pgvector` default for the shared tier below no longer holds.

The abstraction with a `pgvector` fallback stays, but the residency objection dissolves:
a self-hosted vector store inside the cell is in-jurisdiction by construction. The choice
returns to being a technical one.

`pgvector` remains the default for the shared tier, where operating a separate vector
service per small tenant is not worth the cost.

### 3. Cross-border AI is possible but must be a documented decision

Where a tenant wants a model with no in-region endpoint, it is permitted **only** with:

- A recorded Article 22 adequacy basis, or an Article 23 mechanism — standard contractual
  clauses, binding corporate rules, or explicit informed consent
- A transfer risk assessment completed and retained
- A DPIA where the processing is high-risk
- The mechanism recorded per tenant in the Control Plane, surfaced in the AI governance
  view (AI-64)

This is a **per-tenant configuration with a compliance gate**, not a platform default.

### 4. Model provider abstraction is now load-bearing

Already built for portability. It is now also the compliance boundary — the point at which
a request either stays in-region or becomes a documented transfer.

### 5. Non-binding instruments are treated as binding for design

The UAE AI Charter and International Policy on AI are non-binding but are referenced in
commercial contracts and procurement. TICVAI's AI governance layer (AI-61 to AI-66) already
satisfies their substance: logging, explainability, human approval before execution, audit
trail, consent control.

Designing to them costs nothing extra and removes a procurement objection.

---

## Consequences

| Consequence | Detail |
|---|---|
| **CF-20 no longer blocks AI architecture** | The design was already correct; the constraint is confirmed rather than imposed |
| Inference endpoint becomes a cell attribute | Alongside database and vector store placement |
| A new compliance artefact is required | Transfer register per tenant, with mechanism and risk assessment |
| DIFC-located tenants carry an extra regime | Regulation 10 on autonomous systems, enforced from January 2026 |
| Shared-tier tenants use `pgvector` | Dedicated and isolated tiers use Qdrant in-cell (amended by ADR-0049: Qdrant on every tier, a collection per tenant) |

### New finding — biometric data

<cite index="14-1">Sensitive personal data under PDPL includes genetic or biometric data.</cite>

Face Pass, facial readers and fingerprint enrolment (C29, AI-54 adjacent) therefore attract
**heightened protection**: explicit consent, a DPIA, and stricter transfer rules than
ordinary personal data.

This was not previously flagged. Raised as **CF-35**.

---

## Alternatives

| Rejected | Why |
|---|---|
| Block all third-party LLM use | Over-reads the law. PDPL regulates transfer, it does not prohibit it |
| Assume no residency obligation and use any endpoint | Under-reads it. Inference is a transfer, and an undocumented transfer is a breach |
| Wait for a definitive ruling before designing | There is no single AI rule to wait for. The obligation is derived from PDPL and is already knowable |

---

## Caveat

This ADR is engineering guidance, not legal advice. The transfer mechanism, adequacy
position and DPIA scope for each tenant must be confirmed with counsel and, where required,
with the UAE Data Office. Enforcement practice is still developing and the Executive
Regulations continue to evolve.

**Action:** Allam to confirm the position with TICVAI's counsel and, for any DIFC-located
venue, assess Regulation 10 applicability.
