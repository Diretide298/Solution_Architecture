# ADR-0063: Encryption and keys, and biometric templates stay with the biometric vendor

**Status:** Proposed · waiting on the client's data protection officer (where face templates may be stored, and the biometric retention floor) and on the client naming its facial-reader vendor
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab and the client (the client's DPO decides where templates live and the retention floor; both are make-or-break) · **Consulted:** Dinesh (infrastructure)
**Finding:** SD-058 (medium)
**Related:** ADR-0023 (PII apart from the ledger) · ADR-0043 (control plane split on personal data) · ADR-0047 (retention and erasure) · ADR-0042 (pinned instances) · ADR-0049 (Qdrant and its token key) · ADR-0057 (broker, proposed) · CF-35 (biometrics under PDPL)

---

## What is open, and who answers

| Question | Who | Decisions Register |
|---|---|---|
| May face templates be held by the biometric vendor, with TICVAI keeping only a reference and a deletion receipt (Option A below)? Or must they be held elsewhere? | The client's DPO | **No.** In the client email of 30 September, item 4 ("where face templates may be stored"), but not in the register |
| The legal retention floor for Face Pass, Face Tag and failed captures | The client's DPO | Yes ("Biometric retention by law") |
| Which facial-reader vendor is contracted (it sets the SDK, the template format and where the templates are processed) | The client | Yes ("Facial-reader vendor") |
| Face capture for guests under 18 | The client's DPO | Yes ("Biometrics for children"); not offered until answered |

The encryption half of this ADR (platform-managed keys, CMK on pinned instances, field-level
encryption) is ours and does not wait on these answers.

---

## Context

**Nothing decides how tenant data is encrypted or who holds the keys.**

- No ADR or architecture document covers encryption at rest, field-level encryption or customer-managed keys for tenant data.
- `docs/architecture/ai-credentials.md` covers bring-your-own-key for **model provider** keys only.

**Nothing says where a face template lives.**

- `pii.subject_biometric` (`010-pii.sql:37`) has `kind` (`facePass`, `faceTag`), consent, guardian, `expires_at` and `is_active`. It has no template and no template reference.
- `enrolFaceTag` (`access.yaml`) is in the Block A slice on POS-005.
- `setBiometricLifecycleRetention` (`access.yaml`) and `setDataRetentionSetting` (`tenancy.yaml`) carry the make-or-break retention floor.
- Biometric data is sensitive personal data under the UAE PDPL. When the client's DPO asks where the template is, who holds the key and how it is erased, there is no answer today.

**One platform fact shapes the key choice.** On Azure Database for PostgreSQL Flexible Server, a
customer-managed key applies to the whole server, not to one database. It is set when the server is
created (check whether it can be switched on later).

**Two key facts were settled on 30 September** (ADR-0049's amendment, `infra-answers-30-september.md`):
the Qdrant token key is an HS256 secret (the admin API key), held in Key Vault as a *secret*, because Key
Vault keys cannot do HMAC signing; and Key Vault Premium's HSM-backed keys are justified by the
per-tenant keys below, not by Qdrant (about $1.32 per tenant per month).

---

## Decision

**Proposed: platform-managed encryption by default, customer-managed keys only on a pinned
instance, application-level encryption for identity-document numbers, and no biometric templates in
TICVAI. The template location and the retention floor need the client's yes.**

### Encryption

1. **At rest, by default:** platform-managed keys on every store: PostgreSQL and its backups, Blob (including the Qdrant snapshots and the nightly dumps), Azure Managed Redis, the Qdrant nodes' managed disks, and the event broker. The broker is RabbitMQ or Kafka, the client's choice (ADR-0057): on our AKS its persistent disks are encrypted like any managed disk; on a managed service (CloudAMQP, Event Hubs) encryption at rest is the provider's, and is part of the residency check before signing.
2. **In transit:** TLS everywhere, including pgbouncer to PostgreSQL, service to Redis, the retrieval client to Qdrant (an API key over plain HTTP is not acceptable, ADR-0049) and every client to the broker.
3. **Customer-managed key (optional):** only for a tenant on a pinned, dedicated instance. The key lives in the tenant's or our Key Vault in the region. This is part of what a dedicated client buys (ADR-0042).
4. **Field-level:** identity-document numbers (Emirates ID, passport) and any field classed as sensitive are encrypted by the application: a data key per tenant, wrapped by an HSM-backed Key Vault key. Where lookup is needed, a keyed hash (blind index) sits beside the ciphertext. **Not `pgcrypto`**: its keys pass through SQL text and logs (it is installed but called nowhere today).
5. **Secrets that sign rather than encrypt** (the Qdrant API key) are Key Vault secrets, read only by their issuer (ADR-0049).

### Biometric templates

6. **TICVAI never stores a template.** The biometric vendor's system holds it. `pii.subject_biometric` gains `vendor` and `vendor_template_ref`.
7. **Enrolment** (`enrolFaceTag`) sends the capture to the vendor and stores only the reference. The image is not kept.
8. **Offline gates** match on the vendor's own edge appliance at the venue. Templates are never in our offline package.
9. **The vendor** must process in the UAE under a data processing agreement that covers deletion on request.
10. **Erasure:** `eraseSubject` and the expiry job call the vendor's delete API and store its deletion receipt. A failed call retries and alerts; it is never dead-lettered silently (ADR-0033's DSAR rule, amended by ADR-0058 for the relay only).

---

## Options Considered (templates)

### Option A: The vendor holds templates; TICVAI keeps a reference (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Low for us. A reference column and a vendor adapter |
| Cost | Inside the vendor's licence |
| Scalability | The vendor's |
| Team familiarity | High. An integration like any other |
| Time to Block A | Fits: POS-005 enrols through the adapter |

**Pros:** The most sensitive data never enters our databases, backups or logs. Erasure is one call with a receipt.
**Cons:** Depends on the vendor's residency and deletion guarantees. The vendor is not yet chosen.

### Option B: TICVAI stores encrypted templates in `pii`

| Dimension | Assessment |
|---|---|
| Complexity | High. Field encryption, key rotation, template format per vendor |
| Cost | Build and a larger compliance burden |
| Scalability | Fine |
| Team familiarity | Low |
| Time to Block A | Slow |

**Pros:** Vendor-independent; could change vendors without re-enrolment.
**Cons:** Makes TICVAI the holder of biometric data, in every backup and every restore drill.

### Option C: Templates only on edge devices at the venue

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Sync to each device, erasure on each device |
| Cost | Device storage and management |
| Scalability | Poor across many gates |
| Team familiarity | Low |
| Time to Block A | Slow |

**Pros:** No central store.
**Cons:** Erasure must reach every device, including one that was offline.

---

## Options Considered (keys)

| | Platform-managed keys everywhere | CMK on pinned instances only (recommended) | CMK for every tenant |
|---|---|---|---|
| Complexity | Low | Medium | High: needs one instance per tenant |
| Cost | None | Only for dedicated clients | A dedicated instance for every tenant |
| Scalability | Fine | Fine | Breaks the shared instance model (ADR-0038, amended by ADR-0040) |
| Team familiarity | High | Medium | Medium |
| Time to Block A | None | None for Block A | Not feasible |

---

## Trade-off Analysis

For templates, A puts the most sensitive data with the party whose product it is, and makes our
erasure one call. B makes us a biometric data holder in every backup. C spreads it over devices. For
keys, a customer-managed key per database does not exist on the platform, so it follows the instance:
offer it where the instance is the client's.

---

## Consequences

**Easier:** a clear answer to the DPO; erasure with a receipt; one encryption rule for every store, whichever broker the client picks.
**Harder:** the vendor choice now carries residency and deletion terms; field encryption adds a kernel component; Key Vault Premium cost grows with tenants.
**Revisit:** if the client insists on holding templates itself, Option B with a customer-managed key on a pinned instance.

---

## Action Items

**Before Monday 5 October 2026**

1. [ ] None blocking. Keep POS-005's Face Tag enrolment behind a flag until the client answers.
2. [ ] Add "Where may face templates be stored?" to the Decisions Register (the retention floor, the vendor and under-18s are there).

**Before POS-005 is built (sprint 2 at the latest)**

3. [ ] The client's yes on template location and the retention floor; the facial-reader vendor named.
4. [ ] Package: `vendor` and `vendor_template_ref` on `pii.subject_biometric`; the vendor delete call in the erasure path; classify sensitive fields. Re-derive, mirrors, check. (3 pts, the finding's estimate)
5. [ ] **BIO-ADAPTER**: vendor adapter interface and mock; enrol and delete with receipt. (3 pts)
6. [ ] **KERNEL-FIELD-ENC**: per-tenant data keys wrapped in Key Vault; blind index helper. (5 pts)

**Before production instances are created**

7. [ ] Dinesh: confirm how a customer-managed key is set on Flexible Server (at creation or later) and include the option in the Terraform `cell` module.
8. [ ] If the client picks a managed broker: confirm its encryption at rest and that its data stays in UAE North (ADR-0057's amendment asks the same of CloudAMQP).
