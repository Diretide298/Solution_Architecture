# ADR-0047: How long data is kept, and where it goes next

**Status:** Accepted — two numbers pending sign-off, marked below
**Date:** 20 September 2026
**Decides:** **CF-64** and **CF-165**, which are the same hole seen from the infrastructure side and the CRM side
**Amends:** [ADR-0042](0042-when-a-region-grows-and-where-a-tenant-lands.md) — an instance now has a role, and only one role is placed onto

---

## Context

**CF-64 reads as 89 open questions and is three.** Of its 89 retention requirements, **two name a
period** — 4.3.4, ten years for payment; 6.1.78, seven years — and **87 say "configurable"**, which
asks the platform to let somebody set a number rather than to pick one. RPO and RTO are separate
and narrower still: CF-60 counted the DR sheet and found 62 of its requirements are infrastructure,
with **only RPO and RTO sitting in the platform at all**.

**CF-165 is the same hole from the CRM side and says so.** Its own text records that it and CF-64
*"have not been read against each other"*. The 20 August session walked *"consent policy, data
privacy and retention/archival"* as one topic; the package treats consent as solved — `recordConsent`
exists, CF-160 settled that a merge takes the narrower of two consents, `pii` is separate from
`identity` so a subject-access export is answerable — and **has no operation, no column and no
policy for how long a guest profile is kept.**

**Consent without retention is half a privacy position.** A platform that can prove a guest agreed
and cannot say when it will stop holding them has answered the easier question.

### What already exists, which is more than the conflicts suggest

    pii.subject                 is_erased, erased_at, erasure_request_id
                                -- erasure is ALREADY a tombstone rather than a delete
    pii.subject_biometric       expires_at, is_active, consent_purpose_id, consent_given_at
                                -- Face Tag's expiry is already a column, with consent linked
    listDataRetentionExpiry     the screen exists (CMS-037); the operation is one of the 577
                                provisional drafts read off a workshop PDF and never specified

**And the gap the whole policy hangs off: there is no erase operation.** `ai.yaml` names
`pii.erase_subject` as *"the erasure path"* and nothing implements it.

---

## Decision

### 1. Three stages, not one number

    active      readable by operations, on the tenant's own instance
    archived    moved to a separate instance, reachable only by an explicit
                restore or investigation path
    erased      tombstoned -- is_erased, erased_at, erasure_request_id, which
                pii.subject already carries

**Retention is a lifecycle and the 87 "configurable" requirements are asking for the transitions,
not for a single field.**

### 2. The base stage is five years **from last activity**, not from creation

**This is the part that is easy to get wrong and expensive to discover.** A guest who visits every
year never expires; one who visited once in 2021 expires in 2026. **Retention measured from
creation deletes the best customers on a schedule**, and it is invisible until year six.

### 3. The default is floor-aware, or it is illegal

A flat five years applied to a payment record breaks 4.3.4.

    defaultYears   5, everywhere, as the base stage
    classMinimum   overrides UPWARD and cannot be configured below
    ceiling        because PDPL also says not longer than necessary -- keeping
                   personal data because nobody chose a number is its own breach

| Class | Default | Floor | Ceiling |
|---|---|---|---|
| Guest profile | **5y from last activity** | — | 7y *(pending)* |
| Payment record | 10y | **10y** — 4.3.4 | — |
| Financial record | 7y | **7y** — 6.1.78 | — |
| Face Tag | ticket expiry **+ 7d** | — | 30d |
| Face Pass | follows the guest profile | — | — |
| Burst environment copy | reconciled **+ 30d** | — | 90d |
| Audit — authz, device | 2y | 1y | 7y |

**Every retention in the package is a number, including the event-anchored ones.** Face Tag and the
burst copy were each described as lasting "until" something — a lifetime rather than a period — and
a lifetime is what nobody can audit. They are now `anchor + grace`, with the grace defaulted.

### 4. The archive is a separate instance, and that makes it a `cell_instance` role

A separate instance rather than a tablespace, so that archived personal data is not one query
mistake away from an operational read, and so its storage can be sized and priced differently.

**ADR-0042 gave us the model for this twelve days ago without knowing it.** `control.cell_instance`
exists and a region may hold more than one. **What it lacks is a role**, and that single omission
is a live defect in the placement rule:

> ADR-0042 places a new tenant on the **emptiest** instance in the region, by peak connections over
> the trailing 7 days as a fraction of `max_connections`. **An archive instance is, by design, the
> emptiest thing in the estate.** So the first tenant provisioned after an archive server exists
> would be placed onto it.

The same column fixes CF-162. A burst environment has **no trailing history at all**, so
emptiest-first would place the most violent workload in the estate onto whichever instance has the
least headroom to absorb it.

    control.cell_instance.role    primary | archive | burst

    **Only `primary` participates in placement.** `archive` and `burst` are addressed
    deliberately or not at all, and **neither contributes to any other instance's
    placement metric** -- a flash sale that entered the trailing average would
    poison a region's placement for a week after it ended.

**Three conflicts, one column.** CF-64 and CF-165 needed somewhere for archived data to live;
CF-162 needed a burst environment that is not a cell; CF-168 needed its placement rule not to be
wrong the first time either existed.

### 5. Derived stores purge at **archive**, not at erasure

**Moving personal data to another server does not leave PDPL.** The archive is still personal data:
still erasable on request, still tenant-isolated, still inside the cross-border transfer position,
and **it must stay in the same jurisdiction as the cell it came from** or archival is itself a
transfer.

And the one that bites:

> **A knowledge base still answering from an archived profile is an archive that did not happen.**

`rag-index-sources.md` already states this rule for erasure — *"a knowledge base still answering
from an erased subject is an erasure that did not happen"* — and `removeIndexEntry` already exists
to do it. **Archive is the same event, one stage earlier.** Nothing cascades between Postgres and
Qdrant, so the call is explicit or it does not occur.

### 6. Notification is to the tenant, ninety days before

**Not to the guest.** Telling somebody "we are about to delete you" invites a response that then has
to be handled, and nothing requires it.

The tenant needs it because **erasure is irreversible** and a legal hold may have to be applied
first. `listDataRetentionExpiry` is the screen for exactly this and is currently a provisional draft
read out of a PDF — **promoting it out of provisional is what makes the policy operable** rather
than declared.

### 7. The erase operation gets written

The whole of this hangs on an operation that is referenced and does not exist. It tombstones rather
than deletes, because `pii.subject.is_erased` already says that is the pattern, and because an
erasure with no record that it happened cannot be proven to a regulator.

---

## Pending sign-off

**Two numbers, both marked in place above, in the same way ADR-0042 left its threshold.**

**The guest-profile ceiling**, proposed at seven years. Five is the default and a tenant may extend;
the question is how far before the platform refuses.

**The RPO floor**, which is the rest of CF-64 and belongs to Dinesh. The question is *not* what
Miral's RPO is — it is **the tightest RPO any tenant may ever buy**, because offering one near zero
requires synchronous replication and a second site, which is a topology decision made once.
**Recommendation: tie it to ADR-0042's pin** — asynchronous replication with a several-minute RPO as
standard, near-zero available only on a pinned dedicated instance, which is what a dedicated client
is already paying for. One decision then serves two conflicts, and the commercial model already
carries the pin.

---

## Consequences

**Contract work this implies**, in order:

    1. control.cell_instance.role          primary | archive | burst, and placement
                                           reads it -- this is a live defect, not a feature
    2. the retention policy model          class, default, floor, ceiling, anchor + grace
    3. eraseSubject                        the operation the erasure path already names
    4. archiveSubject / restoreSubject     the stage transition, with the derived-store
                                           purge in the same call
    5. listDataRetentionExpiry             promoted out of provisional against this ADR
                                           rather than against a screen title

**What this does not decide.** Backup schedules, replication topology and restore drills stay
infrastructure — CF-60 was right that 62 of the DR sheet is Dinesh's layer and not a contract.

**BL-106 is smaller than its entry says.** `pii.subject_biometric` already carries `expires_at`,
`is_active` and the consent linkage; Face Tag and Face Pass need a kind and two different anchors,
not a new model.
