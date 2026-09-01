# Renames — 26 August 2026

**For the backend team. Nothing is built yet, so none of this is a migration** — build is 0%, no DDL
exists, and every name below changes in the contracts before a single table is written.

**Two services, ten tables, ten schemas, four operations.** All nine validators pass.

---

## Why now

**The names were readable to whoever wrote them and opaque to everybody else.** Fifty of 368 tables
had a name that did not say what they held; thirty-four of those had no description either.

**Renaming after the build is a migration. Renaming now is a find-and-replace.** This is the last
cheap moment.

---

## Services

| Was | Now | Why |
|---|---|---|
| `CrossCellService` | **`CrossRegionService`** | Read quickly, `CrossCell` is *cross-sell* — and this platform has a real cross-sell surface (`GST-058`, `createUpsellRule`). **Two things one letter apart, one about revenue and one about jurisdictions.** |
| `ControlService` | **`PlatformService`** | *Control* of what? It provisions tenants, holds licensing and owns the developer API. It is the service behind `P09 TICVAI Web`, the platform console, and now says so. |

**Not renamed, deliberately.** `FnbService`, `AccessService` and `VenueOpsService` are terse but not
misleading, and renaming them costs 1,025 lineage entries and sixteen LLD files for less than it
gains.

**`CrossDBService` was considered and rejected.** The service crosses a **legal** boundary, not a
storage one — ADR-0010 has it moving a pseudonymous guest link rather than a guest, because personal
data may not leave the jurisdiction. **And CF-161 is open**: if per-service database segregation
wins, every service crosses databases and the name means nothing.

---

## Tables

| Was | Now | Cols | Ops | FKs in |
|---|---|---:|---:|---:|
| `platform.scope_node` | **`platform.org_unit`** | 8 | 17 | **76** |
| `catalogue.envelope` | **`catalogue.channel_capacity`** | 12 | 13 | 2 |
| `catalogue.attribute_axis` | **`catalogue.variant_dimension`** | 3 | 2 | 0 |
| `catalogue.inventory_lease` | **`catalogue.inventory_hold`** | 14 | 14 | 3 |
| `identity.grant` | **`identity.delegated_access`** | 19 | 17 | 0 |
| `ledger.entry` | **`ledger.posting`** | 12 | 17 | 3 |
| `queue.entry` | **`queue.waiting_guest`** | 18 | 9 | 1 |
| `access.admission_profile` | **`access.admission_rules`** | 9 | 7 | 3 |
| `platform.redemption_right` | **`platform.cross_region_entitlement`** | 16 | 5 | 1 |
| `control.plan` | **`control.subscription_plan`** | 15 | 8 | 7 |

### The reasoning, one line each

**`org_unit`** — one row is one organisational unit: a tenant, a brand, a region, a venue, a
department, a workstation, an outlet. *Node* said *this is a graph* and hid what the graph is of.
**76 tables reference it, more than any other table in the package.**

**`channel_capacity`** — how many of a performance's seats the web may sell versus the box office.
*Envelope* was unguessable.

**`variant_dimension`** — the dimension a variant varies on: size, colour.

**`inventory_hold`** — a temporary claim on contended stock (CF-115). *Lease* reads as a rental
agreement, which this platform also has.

**`delegated_access`** — one principal acting on another's behalf. *Grant* is a verb, a subsidy, or
a permission, and seventeen operations used it without any of them being obvious.

**`posting`** — it sat beside `journal_entry` and `journal_line`. **Three "entry" things in one
schema is a schema nobody reads twice.**

**`waiting_guest`** — it is a person in a queue, not a row in a table.

**`admission_rules`** — the rules a gate applies. *Profile* reads as a person, and this schema is
full of people.

**`cross_region_entitlement`** — an entitlement bought in one jurisdiction and honoured in another.
*RedemptionRight* asked *a right to redeem what, where?*

**`subscription_plan`** — it sat beside `migration_plan` and `production_plan`.

---

## Contract schemas

**Table names derive from these**, so the schema is where the rename actually happens.

```
tenancy.ScopeNode             -> tenancy.OrgUnit
catalogue.Envelope            -> catalogue.ChannelCapacity
catalogue.AttributeAxis       -> catalogue.VariantDimension
catalogue.Lease               -> catalogue.InventoryHold
identity.Grant                -> identity.DelegatedAccess
finance.LedgerEntry           -> finance.Posting
queue.QueueEntry              -> queue.WaitingGuest
access.AdmissionProfile       -> access.AdmissionRules
cross-cell.RedemptionRight    -> cross-cell.CrossRegionEntitlement
subscription.Plan             -> subscription.SubscriptionPlan
```

---

## Operations and paths — 24 renamed

**A table renamed while its API keeps the old word is worse than neither.** A developer reading
`createScopeNode` and finding `platform.org_unit` has two vocabularies for one thing.

**Six of the ten tables had operations named after them**, and the first draft of this document
caught only one of the six.

```
createScopeNode              -> createOrgUnit
getScopeNode                 -> getOrgUnit
listScopeNodes               -> listOrgUnits
updateScopeNode              -> updateOrgUnit

createEnvelope               -> createChannelCapacity
listEnvelopes                -> listChannelCapacities
updateEnvelope               -> updateChannelCapacity

acquireLease                 -> acquireInventoryHold
releaseLease                 -> releaseInventoryHold
renewLease                   -> renewInventoryHold
listLeases                   -> listInventoryHolds
forceReleaseLease            -> forceReleaseInventoryHold

createGrant                  -> createDelegatedAccess
deleteGrant                  -> deleteDelegatedAccess
listGrants                   -> listDelegatedAccess

getQueueEntry                -> getWaitingGuest
overrideQueueEntry           -> overrideWaitingGuest
redeemQueueEntry             -> redeemWaitingGuest

createAdmissionProfile       -> createAdmissionRules
listAdmissionProfiles        -> listAdmissionRules
updateAdmissionProfile       -> updateAdmissionRules

consumeRedemptionRight       -> consumeCrossRegionEntitlement
getRedemptionRight           -> getCrossRegionEntitlement
propagateRedemptionRight     -> propagateCrossRegionEntitlement
revokeRedemptionRight        -> revokeCrossRegionEntitlement
```

**Paths follow the operation.** `/scope-nodes` -> `/org-units`, `/leases` -> `/inventory-holds`,
`/grants` -> `/delegated-access`, `/redemption-rights` -> `/cross-region-entitlements`.

**Path parameters too**: `scopeNodeId` -> `orgUnitId`, `leaseId` -> `inventoryHoldId`,
`redemptionRightId` -> `crossRegionEntitlementId`.

### Two words that look like renames and are not

**`createRelease`, `promoteRelease`, `getReleaseReadiness`** are the *deployment* sense of release
and are untouched. **`releaseCustomDomain`, `releaseSeatHold`, `releaseStoredValue`** are the *let
go of* sense. Only `releaseLease` — releasing a lease — was in scope, and a naive
find-and-replace on `Lease` would have broken nineteen operations that merely contain the letters.

**`grantDelegation`** keeps `grant` as a verb. The table was renamed because *Grant* as a noun was
ambiguous; the verb is not.

---

## What deliberately did **not** change

**`scope_path` stays, on 28 tables.** So does `ScopeLevel`, and `x-ticvai-scope-level` on all 1,025
operations. **"Scope" appears 1,426 times across the contracts and it is the right word.**

**The org unit is the thing; a scope is what you get when you use one for authorisation.** Same row,
two roles. `identity.delegated_access` carries a `scope_path` because a grant is *scoped*;
`platform.org_unit` is the structure being scoped against.

**Renaming `scope_path` to `org_path` would have traded one confusion for a much larger one.**

**Column names are unchanged.** The primary key stays `id` and foreign keys stay `<referent>_id` —
`venue_id` 59 times, `subject_id` 46, `principal_id` 24. **Renaming the key to `<table>_id` was
considered and dropped**: the column names come from contract properties, so it would mean renaming
`id` in every schema and in 522 path parameters, for readability the foreign-key naming already
provides.

---

## What to do with this

**Nothing urgent.** No code exists against the old names and no data exists in them.

**When you write the DDL, write it from `handoff/schema-reference.json`** — that is the derived
truth, it now carries the new names, and it is regenerated from the contracts on every
`refresh.sh`.

**If you have a local branch that names any of the ten**, the mapping above is the whole change. The
package has no other reference to the old names: verified by search across contracts, screens,
flows, states, events, diagrams, handoff and tools.

---

## Also landing in the same drop

**`subject` is a new config scope** for guest-owned settings — consent, marketing preferences,
registered devices, wishlist. **Nine operations moved onto it.** It is not a level of the org tree:
it does not inherit down and an operator cannot override it.

**`ingestFxRates` and `setFxProvider` are new**, with `FxRateSource` widened to name the provider —
`uaeCentralBank` is the default for AED pairs because it is what a UAE auditor expects.

**Cross-region wallet spend now records its conversion**: `fxRate`, `fxRateId`, `fxRateSource`,
`amountInConsumingCurrency` on the authorisation, **fixed at authorisation rather than capture** —
a hold taken Friday and captured Monday converts at Friday's rate.
