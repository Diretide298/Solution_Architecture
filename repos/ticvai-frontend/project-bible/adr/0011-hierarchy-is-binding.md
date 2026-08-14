# ADR-0011: The Hierarchy Is Binding

**Status:** Accepted
**Date:** 13 August 2026
**Closes:** CF-34, CF-27

---

## Context

The seven-level hierarchy was derived from a client-supplied diagram. The diagram was later
confirmed to be **illustrative** — the named tenant, brands, regions and venues in it are an
example, not a deployment.

That raised CF-34: if the example is illustrative, is the *structure* illustrative too? The
diagram was the sole source for several load-bearing decisions — the `ScopeLevel` enum, the
`ltree` model, reporting levels, the partition key, and the assertion driving row-level
security.

## Decision

**The hierarchy is binding. Only the example populating it was illustrative.**

```
Tenant → Brand/Organisation → Region/Branch → Venue → Department → Sub-Department → Workstation
```

Seven levels, these names, this order.

### What this confirms

| # | Position | Now settled |
|---|---|---|
| 1 | Seven levels, named as above | Yes |
| 2 | **Brand** exists as a level between Tenant and Region | Yes |
| 3 | **Sub-Department** exists between Department and Workstation | Yes |
| 4 | **Region** owns currency, decimal scale, time zone, date format and fiscal year — inherited by every venue beneath, not overridable at venue level | Yes |
| 5 | **Venue** is the configuration isolation unit | Yes |
| 6 | *"No cross-venue data access unless explicitly permitted"* is a **requirement**, not commentary | Yes |
| 7 | Reporting is available at all seven levels, drilling from Tenant to Workstation | Yes |

## Consequences

| | |
|---|---|
| **`ScopeLevel` enum is no longer provisional** | `tenancy.yaml` can proceed to v1.0 |
| **The permission specification is confirmed** | Deny-overrides-allow and sibling venue isolation rest on position 6, which is now a requirement |
| **Venue stays the partition key** | ADR-0005 unaffected |
| **CF-27 closes with it** | The rights cascade across seven levels is original work, but the depth is no longer in question |
| **Warehouse must support seven drill-down levels** | Position 7 |
| `x-ticvai-scope-level` on 32 operations | Values confirmed correct as written |

## What was already right

`ltree` paths are variable-length by construction, so the model would have absorbed a
different depth without redesign. The exposure was the **enum in a published contract** —
which is why this needed closing before any spine contract reached v1.0, and why it has.

## Note

Position 6 is the most consequential and had the weakest provenance — one sentence in a
rank-3 document, now confirmed as binding. It drives row-level security, the default-deny
posture, and permission test vector V05.

Worth recording in a MoM so it has rank-1 authority rather than resting on this ADR.
