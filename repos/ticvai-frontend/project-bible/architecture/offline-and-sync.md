# Offline & Sync

> **Purpose:** How devices work without a network  
> **Owner:** Backend + Frontend  
> **Status:** Settled — design Week 2


Offline is not a feature. It is a layer every write path passes through.

## Which surfaces

| Surface | Offline | Notes |
|---|---|---|
| POS thick client | **Full** | Installable, local SQLite |
| Mobile / Flying POS | **Full, mandatory** | Roaming, may be off-site |
| Dedicated scanner app | **Full, mandatory** | Native. Explicitly not web |
| Employee app | Partial | Validity lookup, not full scanning |
| Kiosk | Full | Unattended |
| Guest app | Partial | Cached tickets |
| Back office, B2C web | **None** | Config-heavy, always connected |

## Guarantees

| Concern | Rule |
|---|---|
| **Ordering** | Strictly sequential per device. A void arriving before the sale it voids is rejected and retried forever |
| **Idempotency** | Client-generated ULID, sent as `Idempotency-Key`. Server deduplicates. Replay after a crash is a no-op |
| **Timestamps** | Both `recorded_at` (device) and `synced_at` (server) retained. Reporting on the wrong one misstates revenue by trading day |
| **Conflict policy** | Declared **per entity** at the call site. No global default |
| **Capacity products** | Blocked offline. Client-enforced, server re-validated |
| **Retail** | Blocked offline — real-time inventory depletion |
| **Payment** | Cash only offline |
| **Mode detection** | Automatic on connectivity loss, automatic restore and flush |

### Conflict policies

| Policy | Applies to | Behaviour |
|---|---|---|
| `append` | Sales, scans | Never conflict. The server appends |
| `serverWins` | Configuration | Local change discarded |
| `manual` | Rare | Surfaced in the UI, never resolved silently |

## One implementation

`offline-core` in `ticvai-frontend`. **Six copies of a sync engine is six divergent bug surfaces**, which is why the frontend is a monorepo while the runtimes are not. Apps are lint-blocked from importing a SQLite driver directly.

| Component | Responsibility |
|---|---|
| `Outbox` | Durable queue, per-device sequence, status, attempt counting, crash recovery |
| `SyncOrchestrator` | Drain with backpressure, mode switching, failure classification, jittered backoff |
| `sqlite` | Driver boundary — swappable in one place |
| `ulid` | ID generation matching the backend's generator |

## Drain behaviour

- **Halts the batch on transient failure.** Skipping to keep moving breaks ordering.
- **4xx that retrying cannot fix → rejected**, surfaced to the operator. Retrying forever behind an "all synced" indicator hides a real problem.
- **Backoff is jittered** — otherwise every terminal in a venue retries in lockstep after a blip and recreates the outage.
- **In-flight entries recovered on start.** Safe to replay; the server deduplicates.

## Venue edge

A lightweight node per site with local SQLite, replicating access rules down and scan events up. Survives total WAN loss.

This is what makes offline architectural rather than aspirational — and it removes gate scanning, the highest-frequency operation on a busy day, from the primary database entirely.

## Read-after-write

A ticket sold at the front gate, scanned 20 metres later, must not be refused by a lagging replica. Writes return a WAL LSN as `X-Consistency-Token`; subsequent reads carry it. **Access validation reads the primary unconditionally** — low volume, non-negotiable correctness.

## Testing

Not provable on a bench. Requires a **pilot venue** and deliberate WAN severing mid-transaction. See [delivery/environments](../delivery/environments.md).
