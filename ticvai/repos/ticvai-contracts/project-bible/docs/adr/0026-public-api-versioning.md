# ADR-0026: Public API versioning, scopes and deprecation

**Status:** Accepted
**Date:** 18 August 2026
**Supersedes in part:** the single-supported-production-version position of 30 July (CF-141)
**Related:** [ADR-0024](0024-contract-first-delivery.md) contract as deliverable · ADR-0004 sessions

---

## Amended 3 November 2026: one server definition per host, and what `info.version` means

**Source:** the r13 system review, finding B-12 (contracts disagreed on host and base path: seven served from a global
`https://api.ticvai.com/v1`, three from `https://api.{region}.ticvai.com/<module>/v1`, the rest from `{cellHost}` or
`{controlPlaneHost}` under `/api/v1`, and `info.version` was 0.1.0 on 17 contracts and 1.0.0 on 18 with no rule). The
lead, 3 November 2026, on the review's fixes: "All four, one release". Change entry CHG-R14J-020.

1. **A contract is served from the host where its data lives.** A tenant's data is in its cell, a database per tenant
   (ADR-0038, amended by ADR-0040), so every module of the five deployables (ADR-0055) is served from the tenant's
   cell host: `https://{cellHost}/api/v1`. The Control Plane's own data (ADR-0039, ADR-0043: `control`, the plan
   catalogue, developer accounts and keys) is served from `https://{controlPlaneHost}/api/v1`: `subscription`,
   `platform-ops` and `public-api`. `cross-region` is served from both (the Guest Link Registry and DSAR
   orchestration on the Control Plane, redemption in the cell). **No contract is served from a global host with no
   cell**: payments and wallet are a tenant's money, kept in its cell, and a host that cannot know the cell cannot
   serve them. Where the Control Plane itself runs is the control-plane placement decision, not this one; the
   contracts name it only as `{controlPlaneHost}`.
2. **One base path per runtime.** The three .NET deployables that serve requests (`commerce`, `access`,
   `operations`) share `/api/v1` on the cell host: the cell's ingress sends each path to the deployable that
   composes its module (ADR-0055), so a method and path are unique on a host (check-package rule 47). The Python AI
   runtime (`ticvai-ai`, ADR-0020 as amended by ADR-0049) is served from the same cell host under `/ai/v1`, its own
   base, because the ingress routes it by prefix and its paths are its own. **No module puts its name in the base path**:
   `/workforce/v1` and `/approvals/v1` were the module's name, not a runtime's, and both are `/api/v1` now.
3. **The definitions are written once**, in `contracts/shared/common.yaml` `x-ticvai-servers` (`cell`,
   `controlPlane`, `ai`), and each contract names the ones it is served from in `info.x-ticvai-hosts`; its `servers`
   block is those definitions, in that order, url and variables as written there. `tools/check-contract-servers.py`
   fails a contract whose `servers` differ, whose hosts do not include the one its module's service implies
   (`handoff/service-decomposition.json`: the service that owns `control` is the Control Plane, `ticvai-ai` is the
   AI runtime, every other service the cell), or whose `info.version` breaks rule 4.
4. **`info.version` is the URL version, as `<major>.0.0`.** The major is the `v<N>` every server of the contract
   carries (1 today), and it changes only when a new URL version is published under the two-version rule above.
   Within a major the package's release tag (`rN`) is the contract's version: an additive change ships in the next
   release, and a breaking one is approved in `docs/active/breaking-changes.yaml` with the tag its producer and
   consumers move to (check-contract-compat, which since this amendment compares each operation's full route, the
   server's base path included). Minor and patch are not used, so a generated client's package version is the major
   and the tag.

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
