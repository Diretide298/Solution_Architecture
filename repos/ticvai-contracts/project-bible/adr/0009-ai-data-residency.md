# ADR-0009: AI Data Residency

**Status:** Accepted
**Date:** 13 August 2026
**Closes:** CF-20
**Supersedes:** the working assumption that UAE law mandates domestic AI data storage

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
| Shared-tier tenants use `pgvector` | Dedicated and isolated tiers use Qdrant in-cell |

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
