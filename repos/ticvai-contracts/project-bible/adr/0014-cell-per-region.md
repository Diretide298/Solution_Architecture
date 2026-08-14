# ADR-0014: Cell Per Region

**Status:** Accepted
**Date:** 13 August 2026
**Supersedes:** the ADR-0001 default of one cell per tenant per jurisdiction
**Closes:** CF-32
**Elevates:** ADR-0010 cross-cell machinery from exception path to normal path

---

## Context

ADR-0001 set **Cell = Tenant × Jurisdiction**, with region-level splitting available as a
configuration but discouraged as a default. The reasoning was cost: splitting within a
jurisdiction multiplies the cost floor and fragments guest identity domestically, while
buying blast radius that canary-gated migrations already provide.

Two things have changed.

**First, the illustrative example was mistaken for a deployment.** CF-32 was raised as
*"verify hyperscaler presence in the second jurisdiction"* — but that jurisdiction came from
a reference diagram, not a real target. The question was answerable only for a deployment
nobody had committed to.

**Second, ADR-0013 established a principle that applies here.** Local-first was chosen not
because local reads are faster, but because *a path exercised 2% of the time is a path
nobody trusts and nobody tests properly*. One path, always taken, cannot rot undetected.

Cross-cell entitlement redemption (ADR-0010) is exactly that kind of path under the
jurisdiction-only rule: machinery that exists, that most tenants never touch, and that would
be exercised for the first time by a real guest at a real gate.

## Decision

**Cell = Tenant × Region.**

Every region is its own cell. Not only where jurisdictions differ — always.

### Why this is the better rule

| # | Reason |
|---|---|
| 1 | **Region is already the configuration boundary.** It owns currency, decimal scale, time zone, date format, fiscal year and tax regime (ADR-0011). Making it the deployment boundary aligns two things that were arbitrarily separate |
| 2 | **One rule, no conditional.** No "split at jurisdiction, sometimes at region, depending." Uniform rules are testable; conditional ones accumulate exceptions |
| 3 | **Cross-cell becomes the normal path.** ADR-0010's redemption delegation, guest linking and wallet authorisation are exercised by every multi-region tenant, continuously — not first encountered in production at a border |
| 4 | **Sizing is per region**, which is where load actually concentrates. A region's venues share a catchment, a calendar and a peak |
| 5 | **Jurisdiction availability stops being an architectural question.** It becomes a provisioning-time placement check per deployment, which is where it belongs |

Point 3 is the decisive one, and it is the same argument that settled ADR-0013.

### Logical cell, physical placement

The logical model is uniform. Cost is controlled by **placement**, not by varying the rule.

| Placement | Infrastructure | Fits |
|---|---|---|
| `shared` | Own database on a shared cluster | Small regions, single-venue regions |
| `dedicated` | Own cluster | Regions with material load |
| `isolated` | Own cluster, own region, own key management | Residency or contractual isolation |
| `clientHosted` | Client's own subscription | Full physical separation, or where no in-region cloud exists |

A tenant with three small regions gets **three databases on one shared cluster** — three
logical cells, one cost floor. A tenant with three large regions gets three dedicated
clusters.

**The application cannot tell the difference.** Placement is a Control Plane attribute.

### Jurisdiction remains a hard constraint on placement

Regions in different countries **must** have placements in their respective jurisdictions.
Regions in the same country **may** share a cluster.

So the jurisdiction rule is not removed — it moves from being the *split rule* to being a
*placement constraint*.

---

## Consequences

### Elevated

| | |
|---|---|
| **ADR-0010 machinery moves to Wave 1** | Guest Link Registry, redemption delegation, cross-cell wallet authorisation. These are no longer edge cases — a two-region tenant needs them on day one |
| **Guest Link Registry is core, not compliance scaffolding** | Every multi-region guest has a link, whether or not a border is crossed |
| **Cross-cell testing is mandatory in CI** | The reference fixture already carries three regions. Cross-cell paths are now default-path tests |

### Simplified

| | |
|---|---|
| **CF-32 dissolves** | Jurisdiction availability is a provisioning check per real deployment, not a design blocker |
| **No conditional split logic** | One rule everywhere |
| **Sizing is per region** | Rather than per tenant with correlated-peak modelling across regions that may not correlate |

### Costs, accepted knowingly

| Cost | Mitigation |
|---|---|
| **Cost floor per region** | `shared` placement — multiple regions' databases on one cluster |
| **Guest identity fragments within a country** | Guest Link Registry handles it. Now exercised continuously rather than rarely |
| **A pass across two regions in one country becomes a cross-cell redemption** | Same machinery, same code path, now well-tested. Latency is on wallet authorisation only; entitlement redemption stays local |
| **More migration and backup targets** | Migration orchestrator fans out regardless. Linear, parallelisable |
| **Cross-region reporting always needs the warehouse** | It already did, for cross-jurisdiction tenants |

---

## What This Corrects

My earlier recommendation weighed cost against blast radius and concluded region-splitting
was rarely worth it. That analysis was right on its own terms and wrong on the terms that
matter: it treated the cross-cell path as a liability to be avoided rather than a capability
to be exercised.

Under jurisdiction-only splitting, most tenants sit entirely within one cell, the cross-cell
code runs almost never, and the first real exercise of it is a guest at a gate in another
country. That is the failure mode ADR-0013 was written to eliminate.

---

## Alternatives

| Rejected | Why |
|---|---|
| Cell per jurisdiction, region split optional | Conditional rule; cross-cell path rarely exercised; jurisdiction availability becomes an architectural blocker |
| Cell per tenant | Fails residency outright |
| Cell per venue | Breaks cross-venue passes, wallets, memberships and consolidated reporting within a single region |
| **Cell per region** | **Accepted** |

---

## Note on the Reference Fixture

The synthetic fixture (`t_ref`, three regions across two countries) is **named for its
shape, not modelled on any client**. It exists to exercise structural properties — multiple
brands, a brand spanning jurisdictions, two currencies with different decimal scales,
sibling venue isolation.

Under this decision it also exercises **three cells**, which makes it a better fixture than
it was: cross-cell paths are now default-path tests rather than a special case bolted on.

No client deployment topology is implied by it, and none should be inferred.
