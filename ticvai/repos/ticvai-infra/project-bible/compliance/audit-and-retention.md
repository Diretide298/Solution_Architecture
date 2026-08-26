# Audit & Retention

> **Purpose:** Trails, retention periods, and what they are not  
> **Owner:** Chinmay  
> **Status:** **Week 2**


## Do not conflate these

| | Mechanism | Period |
|---|---|---|
| **Financial audit trail** | Append-only ledger. Nothing is deleted; corrections are new entries | **7 years** (31 Jul 2026) |
| **PITR backup retention** | WAL archive + base backups | 35 days |
| **Monthly archives** | Cold storage | 12 months |
| **Operational logs** | Structured, PII-free | 90 days |

The 7-year requirement is satisfied by the **ledger design**, not by backup retention. Retaining backups for seven years is expensive and does not produce an audit trail.

## What is audited

| Event | Retained |
|---|---|
| Every ledger posting and correction | 7 years |
| Supervisor overrides, with the authorising user | 7 years |
| Refunds and voids, with authorisation chain | 7 years |
| Shift open, close, cash lift, over/short | 7 years |
| Access grants and revocations | 7 years |
| Session force-logout, with reason | 7 years |
| AI prompts, responses and actions | Per AI-61; period TBC |
| Configuration changes | 7 years |

## Erasure

Erasure obligations and an append-only ledger coexist because **PII lives in a separate erasable store**, referenced by opaque subject ID. Erasing the PII record leaves the ledger intact with an orphaned but valid reference.

See [privacy-and-dsar](privacy-and-dsar.md).
