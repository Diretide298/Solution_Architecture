# BL-110 — the 48 ABAC requirements, walked one at a time

> The traceability rows for 3.3.1–3.3.48 carry **one note repeated 40 times** — *"Attribute-based
> access control does not exist. `Grant` is principal, role, p…"* — which is a verdict stamped
> across a section rather than 48 judgements. It is not wrong. It is just not an answer to
> *"how much of this do we actually have to build"*, and that is the question D4 asks.
>
> Read against the package, **31 of the 48 are already served or are a condition on an existing
> grant.** Six need something genuinely new. Eleven are not authorisation at all.

## The finding

| | Count | What it means |
|---|---:|---|
| **A — already served** | 17 | The scope tree, the audit tables, approvals or delegated access answer it today |
| **B — a condition on a grant** | 14 | An attribute attached to an existing `Grant`. No new evaluation model |
| **C — genuinely new** | 6 | Needs state the authorisation decision does not currently have |
| **D — not authorisation** | 11 | A screen, a dashboard or a report |

**So the answer to D4 is (a), and the margin is not close.** A general policy engine would be
built to serve six requirements, five of which are about live venue state rather than identity,
and it would put a policy decision on the hot path of all 2,056 operations to do it.

## A — seventeen are already served

| Req | Asks for | Answered by |
|---|---|---|
| 3.3.2 | Location-based access | **the scope tree.** `Session.scope` resolves from the ltree hierarchy; a venue *is* a scope node |
| 3.3.13 | Venue attribute evaluation | same |
| 3.3.40 | Tenant-specific policies | same — `tenant` is the root level |
| 3.3.41 | Venue-specific policies | same |
| 3.3.43 | Policy inheritance across org structures | **the ltree path is inheritance.** `t_ref.b_alpha.r_north.v_alpha1` — a grant at region applies beneath it |
| 3.3.32 | Least-privilege enforcement | **deny-overrides-allow**, already the resolution rule |
| 3.3.28 | Authorization caching | **resolving once at login *is* the cache.** `Session.scope` — *"clients filter navigation against this, they never compute it"* |
| 3.3.30 | Local policy evaluation when offline | **ADR-0013 local-first.** A reader holds an offline package of valid entitlements |
| 3.3.35 | Delegated administration of access | **`identity.delegated_access`** |
| 3.3.26 | Approval workflow for policy changes | **the `approvals` contract**, with SLA and escalation |
| 3.3.36 | Policy change audit logs | **`identity.authz_audit`** |
| 3.3.37 | Authorization decision audit logs | same |
| 3.3.39 | Policy change history | same |
| 3.3.6 | Emergency override | **already `CONTRACTED_PARTIAL`** — override with an operator and a stated reason, audited |
| 3.3.29 | Centralized policy evaluation | resolution at login is central by construction |
| 3.3.15 | Device attribute evaluation | **partly `RegisteredDevice.offlineScope`** — what a device may do with no connection is already a device attribute gating authority |
| 3.3.25 | Policy simulation and testing | **the 28 permission test vectors** in `permission-resolution.md` are this, unwired to an operation |

**Eleven of the seventeen are the scope tree and the audit tables**, which is the whole reason
the role-based model was chosen deliberately. The requirement authors did not know that, and the
walk stamped `GAP_CONTRACT` on them anyway.

## B — fourteen are a condition on an existing grant

These need `Grant` to carry conditions. **One schema change, not a second model.**

    3.3.3   time of day / shift          3.3.16  day of week
    3.3.17  season                       3.3.18  specific event
    3.3.7   user attributes              3.3.8   employee attributes
    3.3.9   membership attributes        3.3.10  accreditation attributes
    3.3.11  customer segment             3.3.12  resource classification
    3.3.14  attraction attributes        3.3.42  cross-venue policies
    3.3.33  temporary grants             3.3.34  automatic expiry

**Every attribute named already exists as a modelled thing.** `workforce` has shifts, `membership`
has tiers, `accreditation` has profiles, `marketing` has segments, `catalogue` has classifications.
None of them needs inventing — they need referencing from a grant condition.

**3.3.33 and 3.3.34 are nearly free**: `delegated_access` already carries `revokedAt`, so a
`validFrom`/`validUntil` pair on a grant plus expiry at resolution is the whole of "temporary
access" and "automatic revocation".

## C — six are genuinely new, and five are the same new thing

| Req | Asks for | Why it is different |
|---|---|---|
| 3.3.19 | Capacity-based restriction | **the decision needs live venue state.** Capacity is a number that changes minute to minute; a permission resolved at login cannot know it |
| 3.3.20 | Occupancy-based restriction | same |
| 3.3.21 | Risk-based restriction | needs a risk score that does not exist |
| 3.3.44 | Access risk scoring | the score itself |
| 3.3.45 | Access anomaly detection | needs a behavioural baseline |
| 3.3.31 | Segregation of duties | **the only one that is about identity** — "the person who raised it may not approve it" is a rule over *pairs* of grants, which no current structure expresses |

**Five of the six are live-state gating, not authorisation**, and the package already has the
right place for them: **capacity and occupancy belong at the gate, in `access`, not in
`identity`.** An admission decision that consults capacity is the scanner's job and it already
consults an offline entitlement package. Treating "the park is full" as a *permission* is what
would force a policy engine onto the hot path.

**3.3.31 segregation of duties is the one real authorisation gap**, and it is small and worth
doing: `approvals` already knows who raised a thing.

**3.3.46 (AI policy recommendations) is deliberately not counted here** — it belongs with the
AI-parked rows, not in an authorisation decision.

## D — eleven are a screen or a report

    3.3.22  visual policy builder        3.3.23  reusable templates
    3.3.24  policy versioning            3.3.38  investigation reporting
    3.3.47  analytics dashboard          3.3.48  effectiveness reporting
    3.3.1   the umbrella statement       3.3.4   status-based (restates 3.3.12/3.3.18)
    3.3.5   configure without code       3.3.27  real-time evaluation
    3.3.46  AI recommendations

**3.3.5 and 3.3.22 are the same requirement** — "administrators configure access policies without
software development" is a policy builder screen over the grant conditions of group B. It is real
work and it is frontend, not a second authorisation model.

**3.3.27 "real-time authorization" is the one to push back on.** Read literally it contradicts
`Session.scope`'s stated design and the performance position behind it. Read as *"a revoked
permission takes effect promptly"* it is a session-invalidation question, which `forceLogout`
already answers. **Worth confirming with the client which they meant** — it is one sentence and
it decides whether the hot path changes.

## What this means for the estimate

BL-110 has been carried as *"48 requirements, the largest single unbuilt thing left"*. It is not
48 things:

    one schema change      conditions on Grant, referencing attributes that all exist
    one small new rule     segregation of duties, over pairs
    two gate features      capacity and occupancy, in `access` where the state lives
    two deferred           risk scoring and anomaly detection -- needs a baseline
                           nobody has, and honest to defer rather than stub
    one screen             the policy builder, which is 3.3.5 and 3.3.22 together
    the rest               already shipped, and the register did not know

**One question for the client before any of it**: 3.3.27, whether "real-time" means the hot path
or prompt revocation.
