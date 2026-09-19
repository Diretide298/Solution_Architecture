# ADR-0046: On-premise has two configurations, and the difference is a control channel

**Status:** Accepted
**Date:** 19 September 2026
**Decides:** the on-premise half of the RFP's deployment requirement; re-answers **CF-61**
**Amends:** [ADR-0017](0017-deployment-models.md), itself already amended by ADR-0038 — its on-premise model is one of the two described here, not both
**Depends on:** [ADR-0043](0043-the-control-plane-splits-on-personal-data.md), [ADR-0038](0038-cell-is-a-region-database-per-tenant.md) — amended by ADR-0040, which lets a region hold more than one instance — [ADR-0020](0020-ai-isolation-boundary.md), [ADR-0021](0021-qdrant-partitioning.md)

---

## Context

**The RFP asks for three deployment models and the package has two.**

> *"Deployment model supporting Cloud, On-Premise, and Hybrid environments"*
> — RFP §Vendor Proposal Requirements, rank 2

`CellKind` reads `shared`, `dedicated`, `onPremise`, `controlPlane`, `burst`. Cloud is covered
three times over. On-premise is covered once. **Hybrid is not covered at all**, and that absence
was consistent rather than accidental — nothing anywhere in the package models a split workload.

The obvious move is to add `hybrid`, and it is the wrong one. **Hybrid in this industry means
workloads split across locations** — transactions local, analytics and inference in the vendor's
cloud. We do not do that, we have not been asked for it, and naming a model after a thing it is not
would cost more in a year than the gap costs now.

**What we were actually missing is smaller and more specific.** ADR-0017 describes on-premise as a
site that cannot be reached:

> *"Nothing leaves the site… The orchestrator cannot push… An on-premise installation may sit behind
> a firewall with no inbound route… registered with `isReachable: false`."*

Every one of its seven consequences follows from that. And it is true of one kind of on-premise
client and false of another. **A venue running the platform on its own servers still needs TICVAI
for tenancy, subscription state and software updates** — that is the ordinary case, and the
air-gapped site is the exception. ADR-0017 wrote down the exception and called it the model.

That matters because the platform *has* update machinery — `createRelease`, `promoteRelease`,
`startRollout`, `scheduleTenantUpgrade`, `getVersionSkew` in `platform-ops.yaml`, with screens
against all of it — and **every operation in it assumes TICVAI can reach the cell.** Under
ADR-0017's on-premise model none of it can ever run. Either that machinery is wrong or the model
is incomplete.

## Decision

**Two deployment locations. On-premise has two configurations, and the only thing that
distinguishes them is whether an outbound control channel exists.**

```
Cloud        shared · dedicated · additional region      TICVAI operates
On-premise   onPremiseIsolated · onPremiseConnected      the client operates
```

**There is no third model, and the RFP's "Hybrid" is answered by `onPremiseConnected`** — the
client's hardware, kept current by us. If a client ever asks for a genuine split workload, that is a
new decision with its own cost, and ADR-0009 and ADR-0020 both reopen when it is taken.

### 1 · `onPremiseIsolated` — ADR-0017's model, unchanged

Nothing leaves the site, in either direction. **Everything ADR-0017 says about on-premise applies
here and applies in full**: updates pull-initiated or physically delivered, version skew that is
legitimately permanent and must not be counted against a rollout, licensing by signed file that
degrades rather than stops, blind support, client-owned backups, cross-cell entitlements excluded
by default.

Those seven consequences stop being a list of caveats and become **the price of isolation**, which
is a better thing to put in front of a client than a list of things that do not work.

### 2 · `onPremiseConnected` — the client's hardware, our control plane

An outbound channel from the site to the Control Plane. The site initiates it; no inbound route is
required, which is what makes it deployable behind a firewall the client controls.

**It carries control traffic only.** ADR-0043 is what makes that a structural claim rather than a
promise: the global control database holds *"the cell registry, `cell_instance` and placement,
releases and rollouts, licences and plans, migrations and their fan-out"* and **holds no natural
person** — 47 of its 50 tables, measured. So the channel carries tenancy, subscription state,
licence validity, release metadata and health telemetry, and **there is no guest on it by
construction.**

`"Nothing leaves the site"` becomes **`"No personal data leaves the site"`**, which is what an
on-premise client is actually buying.

### 3 · Connectivity is not the AI question — data egress is

**This re-answers CF-61, which ADR-0020 left open and which the two-configuration split does not by
itself close.** The naive reading is that connected sites get the assistant and isolated ones do
not. That is wrong in both directions.

**AI inference is data traffic, not control traffic.** A guest's question, a support transcript, a
prompt with a booking in it — sending any of those to a hosted provider is personal data leaving
the site, and routing it down the control channel would destroy the one property that makes the
channel acceptable.

| configuration | AI | why |
|---|---|---|
| `onPremiseIsolated`, no model shipped | **none** | ADR-0020's honest default. Said in the contract, not discovered at install |
| `onPremiseIsolated` **+ client-hosted local model** | **yes, locally** | ADR-0021: *"gets a locally hosted model. Its vectors are a different size in a different space, so that tenant has its own collection whether we like it or not"* |
| `onPremiseConnected`, control channel only | **none** | the channel is PII-free by construction; inference is not |
| `onPremiseConnected` **+ explicit inference-egress consent** | **yes, hosted** | a separate consent, not implied by connectivity. Subject to ADR-0009 residency |

**An isolated site with its own GPU gets a better assistant than a connected site whose client will
not let content leave.** That is counter-intuitive and it is the correct answer, and it is written
here because the naive reading — *connected means more features* — is the one a reader will arrive
with.

## Consequences

**`CellKind` gains a value and loses one.** `shared`, `dedicated`, **`onPremiseIsolated`**,
**`onPremiseConnected`**, `controlPlane`, `burst`. `onPremise` is replaced rather than kept, because
a name that no longer says which of two things it means is worse than a rename.

**The rename is small and was measured before it was proposed**: 5 occurrences across two contract
files, zero in `backend/`, `screens/`, `flows/`, `diagrams/` and `tools/`. `handoff/` holds 34 in
generated artefacts, which are regenerated rather than edited.

**`onPremiseNotScheduled` in `platform-ops.yaml` is a rollout status and not a cell kind.** A blind
find-and-replace corrupts it. Named here because this ADR is what will prompt somebody to try.

**Two field descriptions in `subscription.yaml` assert the old premise and must follow:**

| field | was | becomes |
|---|---|---|
| `isReachable` | *"False for `onPremise`"* | false for isolated, **true for connected** |
| cross-cell entitlements | *"False by default for `onPremise`"* | false for isolated, available for connected |

**The update machinery becomes reachable for the first time.** `startRollout` and
`scheduleTenantUpgrade` work against `onPremiseConnected` exactly as they do against a cloud cell.
Against `onPremiseIsolated` they must continue to be unreachable-tolerant, which ADR-0017 already
requires and nothing yet implements.

**Version skew means two different things and the skew report must say which.** ADR-0016
distinguishes mid-rollout skew from unexplained skew; `onPremiseIsolated` is a third case and
`onPremiseConnected` is not — a connected site behind on version is behind for the same reasons a
cloud cell is.

**Three decisions ADR-0017 required before the first on-premise sale now have a scope.** Cross-cell
entitlements, expired-licence behaviour and backup responsibility are **questions about
`onPremiseIsolated`**. For `onPremiseConnected` the first is answered (it works), the second
collapses into ordinary subscription handling, and only backups remain genuinely open.

### Costs accepted

| | |
|---|---|
| Two on-premise configurations is two support products | Real, and smaller than it looks — they share one codebase and differ in whether one channel exists |
| A rename touching live contracts | Accepted. 5 occurrences, and the ambiguity costs more than the edit |
| `onPremiseConnected` needs a channel nothing has built | Accepted and named. The alternative is update machinery that can never run on client hardware |
| Four AI outcomes rather than one | Accepted. The alternative is a default that is wrong for half of on-premise clients |

## Alternatives considered

**Add `hybrid`.** Rejected above. It names a model we do not build, and the RFP's use of the word is
satisfied by `onPremiseConnected` without borrowing a term that means something else everywhere
else.

**Keep `onPremise` and add `onPremiseConnected`.** Cheaper by five edits and leaves the older value
meaning *the isolated one* by convention rather than by name. Rejected on CF-97's precedent: a value
whose meaning has to be remembered rather than read is how a careful reader builds a defect on it.

**Treat connectivity as a property of the cell rather than a kind.** Genuinely tempting — it is one
boolean, and `isReachable` already exists. Rejected because the two configurations differ in seven
consequences, not one flag, and a `CellKind` is what the rest of the package branches on. A boolean
would leave every one of those consequences to be rediscovered at each branch.

**Route inference over the control channel for connected sites.** Rejected. It would make the
channel carry personal data, which removes the ADR-0043 guarantee that is the entire reason the
channel is acceptable on a client's hardware.
