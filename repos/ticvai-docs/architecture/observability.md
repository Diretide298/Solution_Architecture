# Observability

> **Purpose:** Tracing, metrics, logging across cells  
> **Owner:** Dinesh  
> **Status:** **Week 1**


## The rule

**Every log, metric and span carries `tenant_id`, `region_id`, `venue_id`.**

Without it, *"the tenant is slow"* is unactionable — and with cells, *"which cell"* is the first question anyone asks.

## Layers

| Layer | Tool | Carries |
|---|---|---|
| Tracing | OpenTelemetry → OTLP | tenant, region, venue, cell, correlation ID, session ID |
| Metrics | Prometheus-compatible | Same dimensions, plus workstation for POS metrics |
| Logging | Structured, never concatenated | Same dimensions. **Never PII** |
| Aggregation | Central, cross-cell | Cell as a first-class dimension |

Central aggregation is a control-plane function. Metrics and traces are operational telemetry, not personal data — but see [compliance/data-residency](../compliance/data-residency.md): logs must be PII-free **by construction**, not by filtering, if they leave the jurisdiction.

## Per-venue attribution

A hot venue degrades within its tenant and is invisible to every other tenant. Diagnosing that requires venue-level attribution on every signal — otherwise the only visible symptom is aggregate latency.

## What to alert on

| Signal | Why |
|---|---|
| Outbox backlog depth per device | The leading indicator of a sync problem |
| Replication lag per cell | Gate validation reads primary, but everything else degrades |
| PgBouncer pool saturation | Connection exhaustion fails as a total outage, not a slowdown |
| Capacity counter divergence (Redis vs Postgres) | Overselling |
| Venue edge node heartbeat | A site is offline |
| Migration version drift across cells | Cells running different schema versions |
| AI token spend per tenant | Cost containment; feeds AI-65 |

## What not to log

Guest names, emails, phone numbers, document numbers, card data, biometric templates. Reference the opaque subject ID instead.

A log line that helps debugging and breaches PDPL is not a good trade.
