# Distribution

> **Purpose:** OTAs, resellers, channel management  
> **Owner:** Backend  
> **Status:** **Wave 3**


## Three B2B models (05 Aug 2026)

| Model | Mechanism |
|---|---|
| **1 — API consumption** | Partner consumes TICVAI APIs directly. The contract *is* the deliverable |
| **2 — B2B portal** | Partner logs in, buys against allocation and credit limit |
| **3 — Bulk QR** | Batch issuance for pre-negotiated volume |

## Named partners

Viator · Klook · Headout · GetYourGuide · BookMyShow · Platinum List · Ticketmaster

Each has its own onboarding. **Sequence by commercial priority**, not alphabetically.

## Design implications

- Allocation and quota per partner, per product, per period
- Credit limits with supervisor-level override and authorisation (2.7.39)
- Child accounts under a partner admin (07 Aug §11)
- Alternative codes for third-party product identifiers — partners use their own SKUs
- Rate limiting per partner at the gateway
- Contract versioning matters here: a partner integration pinned to v1.4 must keep working
