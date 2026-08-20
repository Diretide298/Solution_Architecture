# Hierarchy & Authorisation

> **Purpose:** Permission resolution across seven levels  
> **Owner:** Chinmay + Dinesh  
> **Status:** **Blocking — spec needed Week 1**


The largest security surface in the platform. The hierarchy diagram asserts *"no cross-venue data access unless explicitly permitted"*, and a permissive default silently violates it.

## The hierarchy

```
Tenant → Brand/Organisation → Region/Branch → Venue → Department → Sub-Department → Workstation
```

Seven levels. The reference system has three (Site → Operating Area → Workstation), so its rights model **does not transfer**. Cascade, inheritance and override semantics are original design work.

## Settled: authorisation is user-driven

**A user logs in from any device and carries their access.** Workstation is not a permission source.

What the workstation still determines — none of it authorisation:

| Concern | Why device-bound |
|---|---|
| Hardware binding | Printer, drawer, venue-scanner, payment terminal are physically attached |
| Sale Board / landing UI | The F&B terminal opens the F&B board (12 Aug §3) |
| Till / deposit box identity | Cash reconciles to a drawer, not a person |
| Access Point inheritance | The gate derives from the workstation, never selected |
| Reporting dimension | Revenue by workstation (6.1.67) |

> **Role decides what you may do. Workstation decides what you can physically do it with, and where the money and the UI land.**

The 12 Aug decision block contradicts itself on this — one bullet says front-end selection is role-driven, another says it auto-loads from the workstation. Both are true of *different layers*: Sale Board is presentation and is workstation-bound; rights are authorisation and are user-bound.

## Resolution model

```
Grant = (principal, permission, scope_node, effect)
effect ∈ { allow, deny }
```

**Deny-overrides-allow.** A deny at any node suppresses that permission for the node and everything beneath, regardless of allows at other depths. Denies inherit downward and are never overridden by a more specific allow.

Resolved **once at login** into the session registry — not per request. A seven-level tree across 70+ venues cannot be walked with recursive CTEs at 1,000 req/s.

## Implementation

| Concern | Approach |
|---|---|
| Tree storage | PostgreSQL `ltree`, GiST-indexed. Materialised path, e.g. `t_ref.b_betapark.r_offshore.v_beta2` |
| Grant evaluation | At login; result cached in the Redis session registry (already required for single-session) |
| Enforcement | **Data layer** via RLS keyed on `ticvai.scope_paths`, plus service-layer checks as defence in depth |
| Contract | `x-ticvai-permission` and `x-ticvai-scope-level` on every operation |
| Client | Consumes `effectivePermissions`. **Never computes permissions locally** |

RLS uses `platform.in_scope(target ltree)` — true when the target sits at or beneath any granted path. Tables carry `ENABLE` **and** `FORCE ROW LEVEL SECURITY`; without FORCE the owner bypasses every policy.

## Roles are groupings, not permission sets

Nothing is predefined (12 Aug §9). A Role is Code + Name + Description; rights attach separately. The 7.1.12 list — Administrator, Finance, Marketing, Operations, Call Center, POS Cashier, Inventory Manager, Membership Manager, Venue Manager — is a **seed template set**, not a taxonomy.

## Multi-role users

One role → direct login. Several → selection prompt (12 Aug §4). Role selection resolves the effective permission set for the session.

## Before any code

**A decision table with test vectors.** Every permission × every scope level × allow/deny combination, asserted. This is not documentation to write afterwards — it is the specification the implementation is checked against.

## Deviation

Matrix 2.7.x (workstation-scoped sales permission) is knowingly not implemented. See [registers/deviations](../registers/deviations.md).
