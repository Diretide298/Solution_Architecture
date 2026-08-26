# Payment Integration

> **Purpose:** Gateways, terminals, recovery  
> **Owner:** Backend  
> **Status:** **Wave 1**


## The rule that differs from every other integration

The standard pattern — TICVAI exposes an inbound API and the client's third party feeds into it — **does not apply to payment**.

> **Payment gateways require full end-to-end integration consuming all relevant APIs, not just the happy path** (12 Aug §12).

## In scope (Integrations sheet)

| System | Type |
|---|---|
| Stripe gateway + Stripe payment device | Gateway + hardware |
| Network International N-Genius gateway + device | Gateway + hardware |
| DCT | Gateway |

Additional processors are supported through the **driver abstraction**, not pre-built. Adding one is a driver plus configuration.

## Recovery paths — the part that matters

| Failure | Handling |
|---|---|
| Terminal charged, success response never arrived | **Payment-status inquiry API.** Poll the gateway for the transaction outcome and reconcile the order |
| On-site terminal failure mid-transaction | Background reconciler sweeps unconfirmed transactions |
| Duplicate submission after retry | Idempotency key; the gateway must not be charged twice |
| Refund initiated, gateway unreachable | Six-step ledger-to-gateway sequencing; ledger entry precedes gateway call and is reconciled |

An integration that handles only the success path will produce orphaned charges and unhappy guests within the first week of live trading.

## Reconciliation

**Monthly, file-based** (12 Aug §17). Not per-transaction API comparison. Five steps: ingest, parse, match, classify, auto-resolve.

## Offline

Card payment is **not available offline**. Cash only. This is a product constraint, not a technical gap.

## Outstanding

Sandbox credentials for both gateways. Recovery flows are untestable without them.
