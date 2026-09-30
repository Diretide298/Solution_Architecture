# ADR-0061: Replica floors are set per deployable and per zone

**Status:** Accepted · 1 October 2026 · Chinmay Parab
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-044 (medium)
**Depends on:** ADR-0055 (five deployables)
**Related:** ADR-0032, pooling amended by ADR-0038 (autoscale triggers) · ADR-0035, amended 3 September (burst floors) · ADR-0060 (zones, proposed)

---

## Context

**The floors were computed per service.**

- `handoff/sizing.json`, normal cells: `replicasAtFloor` is **34 in every cell size** (17 services × a floor of 2). The small cell has a mean of 64.8 rps and a peak of 382 rps.
- Hosting cost for small tenants is dominated by idle floors.
- `rpsPerReplica` comes from ADR-0032's autoscale triggers and is *"a hypothesis until `tools/bench.py` runs"*.

**Since 30 September the package also sizes the five deployables** (ADR-0055). `sizing.json` now has a
`deployables` block per cell with a floor of 2 for each unit: **10 at the floor** in every cell size.
Normal-traffic shares from its mix: `commerce` 48.6%, `operations` 35.0%, `access` 15.2%, `ticvai-ai`
1.2%. Its note already says Catalogue is 23.6% of normal traffic (the review's "11%" is fixed).

**A flat floor of 2 per unit does not survive a zone loss for the sale path.** With three zones and two
replicas, losing the wrong zone halves `commerce` at the moment it is needed. And `ticvai-ai` is three
process groups with different failure profiles (AI design 4.3), which one floor cannot express.

---

## Decision

**A floor is survivability: enough replicas to lose one zone and keep serving. It is set per
deployable.**

| Deployable | Floor | Why |
|---|---:|---|
| `commerce` | 3 | One per zone. The sale path must survive a zone loss without a cold start |
| `access` (cloud side) | 2 | The gate decides locally (ADR-0013); the cloud side can lose one replica |
| `operations` | 2 | Back office tolerates a short scale-out |
| `workers` | 2 | Relay leases fail over between replicas (ADR-0058) |
| `ticvai-ai` real-time | 2 (3 in large cells, as AI design 4.3 asks) | Fraud and recommendations fail open anyway |
| `ticvai-ai` interactive | 1 | Assistants tolerate a short outage |
| `ticvai-ai` batch | 0 | Scales from zero on queue depth |
| **Total, small cell** | **12** | Down from 34 per service; up from the 10 in `sizing.json` today |

- Above the floor, each deployable autoscales on RPS (not CPU), as ADR-0032 says.
- **Peak, from the package's own arithmetic** (`sizing.json`, large cell, 7,036 rps): `commerce` 17, `operations` 12, `access` 3, `ticvai-ai` 2, `workers` 2 = 36, against 50 per service. It rests on the `rpsPerReplica` hypotheses until the benchmark replaces them.
- **Burst environment** (ADR-0035, amended 3 September): the floor is the expected peak, as today, computed for `commerce` instead of three services.

---

## Options Considered

### Option A: Keep per-service floors (34)

| Dimension | Assessment |
|---|---|
| Complexity | Low (already computed) |
| Cost | Highest; mostly idle |
| Scalability | Per service |
| Team familiarity | n/a |
| Time to Block A | None, but does not match ADR-0055 |

**Pros:** No change.
**Cons:** Pays for 34 idle replicas in the smallest cell.

### Option B: Per-deployable floors with zone spread (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | About a third of Option A at the floor |
| Scalability | Autoscale above the floor per deployable |
| Team familiarity | High |
| Time to Block A | A deriver change |

**Pros:** Survives a zone loss; cheapest safe floor.
**Cons:** Larger blast radius per replica than per-service replicas.

### Option C: Scale everything but `commerce` to zero when idle

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | Lowest |
| Scalability | Cold starts on the first request of the day |
| Team familiarity | Medium |
| Time to Block A | Similar |

**Pros:** Cheapest.
**Cons:** Back-office cold starts at opening time; the relay cannot be at zero.

---

## Trade-off Analysis

B keeps the survivability argument that set the floor at 2 in the first place, applied to the unit
that is actually deployed, and adds the third `commerce` replica that a zone loss needs. C saves a few
replicas at the price of cold starts where staff notice them.

---

## Consequences

**Easier:** small tenants cost less; one sizing model per deployable.
**Harder:** sizing tools change; diagrams re-derive.
**Revisit:** after `tools/bench.py` gives real `rpsPerReplica` per deployable (sprint 2).

---

## Action Items

**Sprint 1**

1. [x] Chinmay: accepted 1 October 2026.
2. [ ] Package: the floors above in `sizing.json`'s `deployables` block (`commerce` 3; `ticvai-ai` split into its three process groups), and its note no longer calls this ADR a proposed draft; re-derive, mirrors, check. (1 pt) — **Authored 1 October** in `tools/derive-sizing.py` (`DEPLOYABLE_FLOORS`, `AI_PROCESS_GROUP_FLOORS`): 12 at the floor in the small and medium cells, 13 in the large (real-time 3). `sizing.json` takes it at the next refresh.
3. [ ] Put the floors in the deploy configs and the Terraform `cell` module. (1 pt) — **Authored 1 October**: `replica_floors` in the Terraform `cell` module (a variable with the floors above and a validation, and an output for the bootstrap Helm values), `x-ticvai-replica-floors` in `deploy/a-independent-tenant.yml` and `deploy/b-shared-platform.yml`, and the five `commerce` modules at 3 in the shared-platform config.

**Sprint 2**

4. [ ] Run `tools/bench.py` per deployable; replace the `rpsPerReplica` hypotheses. (2 pts, with the hold-contention benchmark)
