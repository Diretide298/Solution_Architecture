# Artefact audit — what the requirements demand that we do not have

> Re-verified 20 September 2026 against the current package, superseding the 19 September
> rewrite, which superseded the 17 August original. The August version was written before the
> requirement walk and asked "which artefact classes does the package lack?" The walk answered
> most of it, so this asks it the other way round: **of 3,184 rows, which are still not designed
> against, and what kind of thing is missing?**

**3,184 matrix rows, every one carrying a verdict, and all 142 sections closed.** The August
version counted 3,297 across four sheets; the walk resolved the difference as duplicates and
superseded rows.

> **The verdicts below were assigned during the walk and have not been re-tested since
> 18 August, except five re-tested on 21 September** — 2.13.41, 2.14.22, 2.14.23, 3.2.9 and
> 3.2.44, against the biometric cluster and the dunning model built that day.** The package has gained roughly 83 operations since — including the device
> lifecycle work that closed BL-160 on 20 September — so **some rows counted as gaps here are
> likely served now.** `tools/retest-gap-rows.py` reports which are worth re-reading and
> deliberately proposes no verdicts: re-deciding one is a judgement, and a tool that overwrote
> them in bulk would destroy the reasoning they hold. Every other number on this page is
> re-derived from the current package.

## Where the rows landed

| Verdict | Rows | | What it means |
|---|---:|---:|---|
| `CONTRACTED` | 2,650 | 83.2% | An operation or schema field demonstrably serves it |
| `PARKED` | 396 | 12.4% | AI-parked or workshop-blocked, with the reason named |
| `GAP_CONTRACT` | 89 | 2.8% | Needs an operation or schema that does not exist |
| `CONTRACTED_PARTIAL` | 44 | 1.4% | Served, but a field, operation or state is missing |
| `GAP_DECISION` | 5 | 0.2% | Undesignable without a client answer |

**94 rows are a genuine gap** — 89 needing contract work and 5 needing the client. That is
**3.1% of the matrix**, against an August position where whole artefact classes had no register
at all.

## Artefact classes, and what stands behind each

**The requirement counts are the August classification and cannot be re-derived** — the walk
records a verdict per row, not an artefact class, so these are kept as the only classification
that exists. **Everything in the "What we hold" column was recounted on 20 September**; the
`Artefact` column comes from `handoff/closed_classes.json`.

| Reqs | Class | What we hold | Artefact |
|---|---|---|---|
| 347 | Report | **43 operations**, a definition engine, the report register | ✅ closed |
| 290 | Permission / role | **154 distinct permissions**, 28 test vectors | ✅ `permission-resolution.md` |
| 273 | Configuration | the configuration catalogue | ✅ closed — **and the scope checker is now clean, see below** |
| 206 | Audit | `identity.authz_audit` and the audit register | ✅ closed |
| 193 | Notification | `MessageTemplate` and the notification catalogue | ✅ closed |
| 171 | Integration | adaptor patterns, ADR-0012/0015, the integration register | ✅ closed |
| 117 | State model | **126 state definitions**, transitions checked at 95% coverage | ✅ closed |
| **105** | **Device / hardware** | **20 device kinds**, ADR-0015, and the lifecycle closed 20 September | 🟡 **No driver register or vendor matrix.** 17 gap rows, all predating BL-160 |
| 94 | Validation rule | the business rules register | ✅ closed |
| **89** | **Retention / archive** | mentioned nowhere concrete | 🔴 **Nothing.** CF-64 and CF-165 |
| 53 | Event / async | **30 events**, consumers, idempotency | ✅ closed |
| 40 | Test / acceptance | 28 permission vectors | ✅ closed |
| — | Accessibility | WCAG 2.2 AA obligations | ✅ closed |
| — | Localisation | translation and locale handling | ✅ closed |

**Four of these counts had drifted since 19 September** — reports 23 → 43, permissions 111 → 154,
device kinds 11 → 20, state models 6 → 126. None was wrong when written. That is the whole
argument for re-deriving rather than carrying forward.

## The artefact classes the August audit called missing

Twelve are now closed, recorded in `handoff/closed_classes.json`:

> accessibility · audit · configuration · event / async · integration · localisation ·
> notification · permission / role · report · state model · test / acceptance ·
> validation rule

That covers six of the seven the August version marked 🔴 — Report, Configuration, Audit,
Notification, Integration and Validation rule all now have the register or catalogue it said was
absent.

**Two do not appear in the closed list, and both are still open:**

### Retention / archive — nothing concrete, and two registers that have never been read together

**The August finding stands; its shape is narrower than this file said.** It claimed five
contradictory periods. **There are two stated periods across 89 requirements** — 4.3.4 (ten
years, payment) and 6.1.78 (seven years) — and **the other 87 say "configurable"** (CF-64,
refined 17 August). That is a smaller and more answerable question than a contradiction: what is
needed is the tightest retention and RPO any tenant may buy, not the number for one client.

**CF-165 is the same hole from the other side and nobody has joined them up.** The 20 August CRM
session walked *"consent policy, data privacy and retention/archival"* as one topic. Consent is
built — `recordConsent` exists, CF-160 settled that a merge takes the narrower of two consents,
and `pii` is separate from `identity` so a subject-access export is answerable. **Retention and
archival have no operation, no column and no policy**: nothing says how long a guest profile is
kept or what happens to it afterwards. CF-165 records in its own text that the two registers
*"have not been read against each other"*, and that is still true.

There is still no retention register saying what is kept, for how long, and who may see it.

### Device / hardware — the gap has moved, and what is left is a register

August called it 🟡, *"no driver register or vendor matrix"*. **That half is unchanged.**

**The lifecycle half closed on 20 September.** BL-160 had been marked done in August against
CF-136 device health — evidence for a different gap — and re-testing it found `enrolDevice`
moving a device through six states while writing nothing, because `platform.device` had no
column to hold the state. `RegisteredDevice` now carries `enrolmentState`, `retiredAt` and
`configurationProfileId`, and `maintenance.asset.deviceId` joins a device to the asset register
so a turnstile can raise a work order against itself.

**The 17 gap rows below all predate that**, so this domain is the clearest case for the re-test.
`DeviceKind` carries 20 kinds, not the 11 this file claimed — **the list was never the gap**;
the driver register and vendor matrix behind it still are.

## Where the remaining 98 gaps are

All thirteen domains, not the eight this file previously showed — those summed to 92 of 98.

| Domain | Gap rows |
|---|---:|
| Admission and Access | 36 |
| Ticketing Sales | 21 |
| **Device Management** | **17** |
| F&B & Guest Management | 5 |
| F&B POS | 5 |
| Retail POS | 3 |
| Marketing & CRM | 3 |
| Bundles and Promotions | 2 |
| Approval Workflows & Governance | 2 |
| Guest Mobile App & Branding | 1 |
| Maintenance & Safety Management | 1 |
| Subscription & Licensing Management | 1 |
| Seat Management & Venue Mapping | 1 |

**Admission and Access at 36 is the one to look at first.** It is the largest single
concentration left, and access is the highest-frequency operation in a venue — the one place
where a missing rule is felt by every guest rather than by an administrator.

## The configuration-scope finding, which has now moved

This is the one claim on this page that has changed direction rather than degree.

The August audit's strongest observation was that **most configuration requirements do not state
a scope level** — 263 of 273. On 19 September this file recorded that `check-config-scope`
**reported 57 errors** against the package. **It now reports zero.**

**That closes the package half and not the requirement half.** Every configuration setting the
package defines now declares whether it applies at tenant, venue, outlet or workstation. The
requirements still mostly do not say, which means each of those declarations is a decision the
package made rather than one the matrix specified — **defensible, recorded, and worth a client
read rather than an assumption.** A setting changed at the wrong level is a setting somebody
changes once and cannot explain afterwards.

## How to re-derive this

Verdicts, domains and sections come from `handoff/traceability.json`; artefact classes from
`handoff/closed_classes.json`. **Both are authored inputs** — ring 4 of
`docs/contract-change-runbook.md` — so this file is rewritten by hand when they change, and
`tools/check-authored-inputs.py` reports when the contracts have moved underneath it.

Everything else is counted from the package directly:

    operations per contract        handoff/api-data-lineage.json
    distinct permissions           x-ticvai-permission across contracts/
    device kinds                   DeviceKind enum, contracts/spine/tenancy.yaml
    state models · events          states/ · events/
    configuration scope            python3 tools/check-config-scope.py
