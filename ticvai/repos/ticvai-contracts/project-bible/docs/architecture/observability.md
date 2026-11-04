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
| Aggregation | Central, cross-region | Cell as a first-class dimension |

Central aggregation is a control-plane function. Metrics and traces are operational telemetry, not personal data — but see compliance/data-residency: logs must be PII-free **by construction**, not by filtering, if they leave the jurisdiction.

## Credentials in requests

**Decided 3 November 2026, Chinmay** ("All four, one release", on the r13 system review's finding C-13; CHG-R14H-005).
Some credentials travel in the request itself: a payment link's and an invitation's token and a gift or game card's
code in the path (`/payment-links/{token}`, `/gift-cards/{cardCode}`), an order access token, a consent key, an
admission token and the till's supervisor PIN in a header (`X-Order-Access-Token`, `X-Consent-Key`,
`X-Admission-Token`, `X-Supervisor-Pin`). Standard ingress, WAF and tracing record full paths and often headers, so
"never PII" is not enough: these are credentials. Each such parameter is marked `x-ticvai-secret: bearer` in its
contract (`tools/check-contract-shapes.py` C-SECRET-PARAM fails one that is not), and:

| Where | Rule |
|---|---|
| Application logs and traces | Record the route template (`http.route` = `/payment-links/{token}`), never the raw path: `url.path`, `url.full` and `http.target` are dropped or rewritten to the template for every operation with a `bearer` path parameter. No request header is logged unless it is on an allow-list; `Authorization`, `X-Api-Key` and every `bearer` header are never on it |
| The edge (Front Door, WAF, ingress) | Access logs for a route with a `bearer` path parameter record the route template, or are scrubbed of the path; request headers are not logged. A WAF match on such a route logs the rule, never the matched value |
| Errors and problem bodies | A `bearer` value is never echoed in `detail`, `instance` or a validation message |
| Retention | Anything that slipped through is a security incident, not a log line: purge it and record it |

**Long enough not to be guessed** means at least 128 bits from a cryptographic random source (22 or more base64url
characters) for a payment link's and an invitation's token. Gift and game card codes are printed and typed, so their
strength is the rate limit and lockout on the reads that take them, not their length.

## Per-venue attribution

A hot venue degrades within its tenant and is invisible to every other tenant. Diagnosing that requires venue-level attribution on every signal — otherwise the only visible symptom is aggregate latency.

## What to alert on

**Thresholds are proposed defaults, client to confirm** (the lead, 20 October 2026, cause FOUNDATION-AI-C25: take
the proposal; correct them from the first weeks of real traffic). A window means the condition holds for that long
before the alert fires. *Page* wakes the on-call person; *ticket* raises a ticket for the next working day.

| Signal | Why | Threshold (proposed, client to confirm) | Window | Severity | Built in |
|---|---|---|---|---|---|
| Error rate | A broken release or dependency shows here first | 5xx responses above 1 percent of requests, per service and cell. `402` and `409` refusals are answers, not errors, and do not count | 5 minutes | page | PLATFORM-OBSERVE |
| Operation latency | Slow is the first sign of saturation | p95 above the operation's `x-ticvai-latency-budget-ms` (1,000 ms where an operation declares none) | 10 minutes | ticket; page when on the sale path (createOrder, createPayment, validateAccess) | PLATFORM-OBSERVE |
| Outbox backlog depth per device | The leading indicator of a sync problem | above 1,000 rows, or the oldest row older than 5 minutes | 5 minutes | ticket; page when 10 or more devices of one venue are over it | PLATFORM-OBSERVE |
| Replication lag per cell | Gate validation reads primary, but everything else degrades | above 30 seconds | 5 minutes | page | PLATFORM-OBSERVE |
| PgBouncer pool saturation (one tenant's share of its pool) | Connection exhaustion fails as a total outage, not a slowdown | server connections in use (`sv_active` + `sv_used`) above 60 percent of the tenant database's `pool_size`; a second signal when clients wait (`cl_waiting` > 0) | 5 minutes | page | **OBS-TENANT-POOL** (one alert, not two: PLATFORM-OBSERVE does not build its own) |
| Instance connections | The pool caps hold per tenant; the instance has one limit | `pg_stat_activity` count above 80 percent of `max_connections` | 5 minutes | page | OBS-TENANT-POOL |
| Capacity counter divergence (Redis vs Postgres) | Overselling | any difference that lasts | 2 minutes | page | PLATFORM-OBSERVE |
| Venue edge node heartbeat | A site is offline | no heartbeat | 2 minutes | page | PLATFORM-OBSERVE |
| Migration version drift across cells | Cells running different schema versions | any cell on a different version after a release finishes | 30 minutes | ticket | PLATFORM-MIGRATE |
| AI token spend per tenant | Cost containment; feeds AI-65 | above the tenant's monthly AI budget share for the day | 1 hour | ticket | AI tickets |

**The pooler is Azure's built-in PgBouncer** (the lead, 20 October 2026, cause FOUNDATION-AI-C53: take the
recommendation). Terraform turns it on for the Flexible Server (`pgbouncer.enabled`, port 6432); its statistics
(`SHOW POOLS`, `SHOW DATABASES`) are read through PgBouncer's admin console on 6432 by a monitoring role with no
data access, and scraped into the metrics of SETUP-OBS. No self-run PgBouncer pair is deployed in Block A
(ADR-0060's pair is the fallback if the built-in one cannot give the numbers above). The per-tenant pool alert is
the PgBouncer saturation alert of this table: OBS-TENANT-POOL builds it and the scrape; PLATFORM-OBSERVE does not
build a second one.

## What not to log

Guest names, emails, phone numbers, document numbers, card data, biometric templates. Reference the opaque subject ID instead.

A log line that helps debugging and breaches PDPL is not a good trade.
