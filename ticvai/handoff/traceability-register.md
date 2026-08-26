# Traceability — contracts against requirements

**Every contract, the requirement domain it serves, and the two that serve none.**

CF-49 found that thirteen Platform Admin screens were raised in a workshop on 30 July, minuted,
and written into a contract without ever becoming a requirement. **A decision reaching a
contract without passing through a requirement has skipped the step where scope is agreed and
estimated**, and this register is what makes that visible rather than discoverable by accident.

## Contracts that serve a requirement domain

| Domain | Reqs | Contracts | Ops |
|---|---|---|---|
| F&B & Guest Management | 411 | `finance` | 46 |
| Ticketing Sales | 343 | `orders`, `shift` | 51 |
| Unified Operations Dashboard | 332 | `ai`, `reporting` | 45 |
| Marketing & CRM | 319 | `marketing-crm` | 49 |
| Ticketing Catalogue | 312 | `catalogue` | 45 |
| Bundles and Promotions | 229 | `promotions` | 31 |
| Admission and Access | 201 | `access`, `queue` | 40 |
| F&B POS | 151 | `fnb` | 41 |
| Seat Management & Venue Mapping | 112 | `seating` | 29 |
| Guest Mobile App & Branding | 107 | `white-label` | 41 |
| Inventory Management | 98 | `inventory` | 43 |
| Developer & API Management | 94 | **none** | — |
| Approval Workflows & Governance | 80 | `approvals` | 13 |
| Retail POS | 78 | `retail` | 26 |
| Device Management | 60 | **none** | — |
| Subscription & Licensing Management | 59 | `subscription` | 41 |
| Accreditation & Credential Management | 58 | **none** | — |
| Maintenance & Safety Management | 50 | `maintenance` | 36 |
| Employee Mobile App & AI Assistant | 50 | `workforce` | 11 |
| Games & F&B Integration | 25 | `games` | 13 |
| Digital Asset Management | 15 | `assets` | 10 |

## Cross-cutting contracts

Serve every domain rather than one, which is legitimate and traceable through the domains they
support.

| Contract | Ops | Serves |
|---|---|---|
| `identity` | 38 | Every domain. Authentication and authorisation |
| `tenancy` | 18 | Every domain. Scope tree, venues, workstations, devices |

## The two that trace to nothing

| Contract | Ops | Origin |
|---|---|---|
| **`platform-ops`** | 24 | **A workshop on 30 July.** Release management, rollouts, migrations, environments. Minuted, contracted, never a requirement |
| **`cross-cell`** | 16 | **ADR-0001 and CF-31.** Multi-region entitlement propagation, guest links, DSAR across cells. Derived from an architecture decision, not from the matrix |

**40 operations, roughly 6% of the platform.**

### Why each is defensible, and why that is not enough

**`cross-cell` follows from a decision the client made.** Data residency forces separate cells
per jurisdiction (ADR-0001), and a membership valid across them has to be propagated somehow.
The matrix asks for cross-venue membership (CF-31) without saying how, so the operations are
downstream of a requirement even though no requirement names them.

**`platform-ops` is weaker.** It exists because TICVAI needs to ship software to cells, which
is true and necessary and **entirely absent from a matrix the client signed**. It is scope the
client is paying for and has never seen itemised.

### What we propose

**Add a domain to the matrix — Platform Operations — with the 24 operations expressed as
requirements**, and take it to the client as an addition rather than leaving it as an
assumption. It is not new work; it is work already done that nobody agreed to.

**`cross-cell` we propose leaving as-is**, cited to ADR-0001 and CF-31 in its module header,
because it genuinely derives from a requirement even though it does not restate one.

## How this stays true

`check-package.py` fails a contract whose `x-ticvai-module` names neither a requirement domain
nor a documented cross-cutting reason. **A contract can still be written without a requirement —
sometimes that is right — but not silently.**
