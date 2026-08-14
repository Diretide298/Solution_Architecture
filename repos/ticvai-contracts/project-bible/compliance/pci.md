# PCI Scope

> **Purpose:** Payment card boundary  
> **Owner:** Chinmay  
> **Status:** **Week 2**


Compliance sheet requires PCI-DSS alignment. The objective is to **keep card data out of the platform entirely**.

## Boundary

| Component | In scope | Approach |
|---|---|---|
| Payment terminals | Yes | P2PE where available; the terminal handles PAN, the platform never sees it |
| Gateway integration | Yes | Tokenised. Store the token, never the PAN |
| Order and ledger | **No** | Reference the token; no card data at rest |
| Logs and traces | **No** | PAN, CVV and track data are never logged. Enforced by construction |
| Backups | **No** | Follows from the above |

## Rules

- No card data at rest, in logs, in traces, in analytics or in the warehouse
- Encryption in transit throughout; TLS 1.2 minimum
- Access to payment configuration is a distinct permission, audited
- **Backups are encrypted** (Compliance sheet #2)
- Gateway credentials live in the per-cell key vault, never in source

## Open

Confirm the SAQ level applicable per gateway and per venue configuration. This depends on whether terminals are P2PE-validated, which depends on the outstanding hardware model list.
