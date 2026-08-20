# ADR-0026: Public API versioning, scopes and deprecation

**Status:** Accepted
**Date:** 18 August 2026
**Supersedes in part:** the single-supported-production-version position of 30 July (CF-141)
**Related:** [ADR-0024](0024-contract-first-delivery.md) contract as deliverable · ADR-0004 sessions

---

## Context

The 30 July decision was **one supported production version**. That was tenable while the only
caller was Softlabs: a breaking change is coordinated with the team that has to absorb it, in the
same release train.

**Decision D1 makes third-party developers first-class.** They register, obtain credentials, test in
a sandbox, and publish certified integrations. And **a breaking change with no deprecation window
now breaks somebody else's business** — somebody with no visibility of the release train and no
ability to absorb it on our schedule.

CF-141 was open on this contradiction. **It is sharper under D1 than it was under the earlier
reading**, which is why it is being decided now rather than deferred.

---

## Decision

### One current version, one deprecated version, twelve months' notice

**At most two versions serve production traffic at any time.** A current one and, during a
transition, one deprecated one.

**Deprecation is announced with a date** and the minimum notice is **twelve months**, recorded as
`ApiVersion.minimumNoticeMonths`. **The commitment is in the model, not in a policy document** — a
deprecation policy without a stated minimum is a policy that shortens under pressure.

**Sunset is the date the version stops answering.** Not the date it stops being recommended.

### What counts as breaking

**Removing an operation, removing a field, narrowing a type, adding a required request field,
changing an enum's meaning, or tightening validation.**

**Adding an optional field is not breaking.** Adding an enum value is — a consumer with an
exhaustive switch fails on a value it has never seen, and pretending otherwise is how a minor
release takes down an integrator.

### Scopes resolve against the tenant's licence

**A token carries the intersection of what the client was granted and what its tenant has licensed**
(13.3.24, decision D5).

**The refusal happens at token issue, not at call time.** An integrator whose tenant has not
licensed the F&B API finds out in testing, once, rather than at 3am against a 403 on one endpoint.

### Notification names what the integrator actually calls

**A generic *"v1 is retiring"* to somebody using three of two hundred endpoints is a message they
will ignore.** `deprecateApiVersion` notifies each client with the operations they have actually
called in the notice period.

---

## Consequences

**We carry two versions during every transition.** That is the cost of the decision and it is real —
two code paths, two sets of tests, and a year of it.

**A breaking change now has a twelve-month lead time.** Anything that cannot wait a year is not a
breaking change and must be delivered another way — which is a healthy constraint and will be
resented at least once.

**Certification is version-bound.** `IntegrationListing.certifiedAgainstVersion` and
`certifiedUntil` exist because **an integration certified against v1 and still listed after v3 is
TICVAI vouching for something it has not looked at in two years.**

**The internal-only path is unaffected.** Softlabs-to-Softlabs calls are not public API traffic, and
this ADR does not slow down work behind the platform's own front door.

---

## Alternatives considered

**Keep one supported version.** Simplest to operate and **incompatible with D1** — it asks a third
party to redeploy on our schedule with no notice, which no integrator will accept and no
certification programme survives.

**Version per operation rather than per API.** More precise, and **it makes the deprecation
conversation unmanageable**: an integrator would track two hundred independent lifecycles instead of
one.

**Six months' notice.** Cheaper for us. **A twelve-month cycle is what a venue's own annual planning
runs on**, and an integrator asked to schedule work inside their own frozen budget year will simply
not do it.

---

## Provenance

**Decisions D1 to D5, recorded 18 August 2026 (CF-135).** D1 established the extensible-platform
posture; this ADR is a direct consequence of it. **The 30 July single-version position is superseded
for the public API only** — it stands for internal contracts, where the original reasoning still
holds.
