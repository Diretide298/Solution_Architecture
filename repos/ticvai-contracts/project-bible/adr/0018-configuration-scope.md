# ADR-0018 — Configuration scope

**Status:** Accepted
**Date:** 14 August 2026
**Relates to:** [ADR-0008](0008-money-carries-per-region-scale.md) money scale ·
[ADR-0011](0011-hierarchy-is-binding.md) hierarchy · [ADR-0006](0006-tiered-guest-app-distribution.md) app distribution

---

## Context

The requirements matrix uses the word "configurable" 321 times. **263 of those do not say at
what level.**

Every one is a design decision. A refund threshold configurable per venue needs a row per venue
and an inheritance rule; per tenant needs neither. We had already been guessing — CF-36 settled
the refund threshold as venue policy and CF-38 did the same for price variance, both by asking,
and both happened to be confirmed. The other 261 had not been.

That is the largest single source of latent rework in the matrix, and it cannot be fixed 263
times. It needs a rule.

## Decision

**Configuration resolves up the scope tree. Nearest ancestor wins. There are three levels.**

    tenant  ─────► region ─────► venue
                                   │
                        assigned, not configured
                                   │
                    ┌──────────────┴──────────────┐
                 workstation                   outlet

**Venue is the floor.** A tenant sets a default, a region overrides it where law or commerce
requires, a venue overrides it for itself. Nothing below venue configures anything.

### Below venue you assign, you do not configure

This is the correction that makes the rule work, and it came from the client on 14 August.

A workstation does not configure itself. **The venue defines workstation profiles — type,
layout, which products are sellable, which devices attach — and a workstation is assigned
one.** That is exactly how the 14 August wireframes describe it: configure the layout, then
link it to the workstation.

The same holds for an outlet. **Menus, stations and course timing are defined at venue level
and an outlet is assigned them.** A restaurant does not invent its own menu structure
independently of the park it sits in.

The consequence is worth stating: a venue with forty workstations has a handful of profiles,
not forty configurations. Forty configurations is forty things to keep in step, and they will
not stay in step.

## The levels

### Region — law and money

| | Why not venue |
|---|---|
| Currency and decimal scale | OMR has three decimal places because Oman says so (ADR-0008) |
| Tax rates | A venue cannot choose its VAT |
| Cash denominations | Bahrain has no 1000 note |
| Date and number format | Follows currency, not preference |
| Chart of accounts and account mappings | A venue posts into the legal entity's books |
| Settlement and acquirer files | Arrive per entity, not per venue |
| FX rates | Per region base currency (CF-37) |
| Seat map templates | So a chain reuses a layout |
| Promotions and bundles | Commercial campaigns usually run across venues. **Overridable at venue** where a single site runs its own offer |

### Tenant — brand, identity and one-scheme concerns

| | Why not venue |
|---|---|
| Brand, theme, fonts, app icons | One app, one store listing, tenant's developer account (ADR-0006) |
| Navigation, homepage, module enablement | Same app |
| SSO configuration | A tenant's directory is theirs |
| Consent purposes and notices | **Consent is a controller-level legal act**, and the controller is the tenant. This is what makes cross-venue entitlements lawful (CF-31) |
| Licensing and subscription | A commercial contract with the tenant |
| Loyalty and membership schemes | A membership sold at one venue and honoured at another cannot have per-venue earning rules without the guest holding several balances |
| Security policy — password, MFA, session, lockout | A venue that can lower its own MFA is a hole in the tenant's posture |
| Notification templates and sender identity | Brand. **Which events fire is venue** — a venue with no F&B sends no order-ready messages |
| Report definitions | So figures are comparable. **Scheduling and recipients are venue** |
| Languages offered | Brand. Date format is regional |
| B2B contracts, credit limits, net rates | Agreed with the tenant. **Allocation per venue** |
| Guest profile and segments | One profile per guest per tenant |
| Suppliers and purchase approval | One commercial relationship |

### Venue — everything else

Ticket and entitlement rules · pricing and price lists · capacity and availability · approval
thresholds · refund and cancellation policy · cash float and variance tolerance · seat maps ·
access points and gate rules · queue configuration · par levels and reorder points ·
**workstation profiles and device bindings** · **menus, kitchen stations and course timing** ·
report scheduling and recipients · which notification events fire.

Roughly 380 of the 321 classified requirements land here once the region and tenant exceptions
are removed, which is why venue is the default rather than one option among several.

## Consequences

**Every configuration operation declares `x-ticvai-config-scope`**, checked in CI the way
permissions already are. An operation declaring a level it is not entitled to fails the build.

**Resolution is a scope-tree walk, which already exists.** `scope_node` is an `ltree` and
`in_scope()` walks it for row-level security. Configuration resolving by nearest ancestor uses
the same mechanism and costs nothing new.

**A configuration read must say where the value came from.** A venue manager looking at a
setting needs to know whether they are seeing their own value, their region's or their
tenant's — otherwise they change it, nothing happens, and they conclude the system is broken.

**Below venue, assignment replaces configuration.** Workstation and outlet operations set
*which profile applies*, never the profile's contents.

### Costs accepted

| | |
|---|---|
| Three levels is three places a value might live | Real, and the reason resolution must report its source |
| Some venues will want a per-workstation exception | Answered by another profile, not by lowering the floor |
| The region layer is thin for a single-region tenant | Accepted. It costs nothing when unused and is the difference between one UAE deployment and two |

## Alternatives considered

**Everything at venue.** Simplest, and wrong four ways: currency, ledger, brand and consent
cannot be per venue without breaking law, store rules or the cross-venue guarantees in CF-31.

**A level per concern, decided individually.** 263 decisions, each defensible, and no rule
underneath. New requirements would arrive without an answer and get one by whoever implemented
them first.

**Workstation and outlet as configuration levels.** Rejected by the client on 14 August, and
correctly: forty workstations configured individually is forty things that drift.

---

## Provenance

**Confirmed by the client on 14 August:** workstation and device configuration belongs at venue
with a master profile; F&B and kitchen configuration belongs at venue.

**Settled earlier and not reopened here:** currency and money to region (ADR-0008, and Allam's
three-decimal confirmation), ledger and settlement to region, brand and guest app to tenant
(ADR-0006), identity and consent and licensing to tenant.

**Accepted by the client on 14 August:** all twenty categories in
`active/configuration-scope-decision.md`, and the sixty previously uncategorised requirements
assigned alongside them. Two were corrected in that conversation — workstation and device
configuration moved from workstation level to venue with a master profile, and F&B and kitchen
moved from outlet to venue. Those two corrections are what produced the "venue is the floor"
rule; the rest stand as recommended and confirmed.

The two most arguable — promotions at region and loyalty at tenant — were put to the client
with the case for the alternative and accepted as recommended. Both remain cheap to move until
something is built against them.

**Every configuration requirement in the matrix now has a level.** 321 classified, none
outstanding.
