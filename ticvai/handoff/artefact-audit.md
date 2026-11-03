# Artefact audit — what the requirements demand that we do not have

> Re-derived 3 November 2026 (r14) against the current package, superseding the 20 September
> re-verification, the 19 September rewrite and the 17 August original. The August version was
> written before the requirement walk and asked "which artefact classes does the package lack?"
> The walk answered most of it, so this asks it the other way round: **of 3,184 rows, which are
> still not designed against, and what kind of thing is missing?**

**3,184 matrix rows, every one carrying a verdict, and all 142 sections closed.** The August
version counted 3,297 across four sheets; the walk resolved the difference as duplicates and
superseded rows.

**The 20 September version of this page counted 89 gap rows and 396 parked. There are none and
19.** The build of 29 September and its re-trace (529 row notes say *re-traced 29 September*)
re-read the gap and parked rows against the operations written that day, and the verdict table below is now read straight off
`handoff/traceability.json`, which `tools/check-authored-inputs.py` holds it to. The 3 November
pass moved one more row: 5.6.7b (priority queueing) is CONTRACTED, because `QueueFastPass` grants
priority by loyalty tier and by declared accessibility need, the two things its note said were
missing.

## Where the rows landed

| Verdict | Rows | | What it means |
|---|---:|---:|---|
| `CONTRACTED` | 3,154 | 99.1% | An operation or schema field demonstrably serves it |
| `PARKED` | 19 | 0.6% | Declined or reclassified by a named decision, with the reason recorded |
| `CONTRACTED_PARTIAL` | 11 | 0.3% | Served, but a field, operation or decision is still missing |
| `GAP_CONTRACT` | 0 | 0% | Needs an operation or schema that does not exist |
| `GAP_DECISION` | 0 | 0% | Undesignable without a client answer |

**No row is a genuine gap.** The 11 partial rows wait on three things, none of them contract work
that is merely unwritten: the regulator's e-invoicing field set and the client's VAT receipt
answer (CF-133, 5.10.3 and 6.1.1), a decision kept partial on purpose (CF-130, 3.2.45, gender
verification advisory only), and eight AI rows that BL-182 holds open, each waiting on the
make-or-break answer or owner decision its note names (L4 auto-optimisation is deferred by the AI
system design, section 5.5). The 19 parked rows are all
declines: parking payment (CF-124), the DET feed (CF-69), tenant sandboxes and cloning (CF-21),
the warehouse execution layer (CF-138) and AI approve-or-reject recommendations (MoM 8 September).

## Artefact classes, and what stands behind each

**The requirement counts are the August classification and cannot be re-derived** — the walk
records a verdict per row, not an artefact class, so they are kept as the only classification
that exists. **Everything in the "What we hold" column was recounted on 3 November 2026**, and
the check refuses a figure higher than the package holds; the artefact column comes from
`handoff/closed_classes.json`.

| Reqs | Class | What we hold (3 November 2026) | Artefact |
|---|---|---|---|
| 347 | Report | **51 operations** in `reporting`, a definition engine, the report register | ✅ closed |
| 290 | Permission / role | **176 distinct permissions**, 22 test vectors | ✅ `permission-resolution.md` |
| 273 | Configuration | the configuration catalogue | ✅ closed — **and the scope checker is clean, see below** |
| 206 | Audit | `identity.authz_audit`, `platform.audit_record` and the audit register | ✅ closed |
| 193 | Notification | `MessageTemplate` and the notification catalogue | ✅ closed |
| 171 | Integration | adaptor patterns, ADR-0012/0015, the integration register | ✅ closed |
| 117 | State model | **210 state models** in `states/` | ✅ closed |
| **105** | **Device / hardware** | **24 device kinds**, one register (ADR-0067), standards-first drivers (ADR-0015), the hardware model library (`setHardwareModel`) | 🟡 **Not in `closed_classes.json`.** No gap rows remain |
| 94 | Validation rule | the business rules register | ✅ closed |
| **89** | **Retention / archive** | ADR-0047's three stages; `setDataRetentionPolicy`, `runDataRetention`, `listArchivalJobs`, `setLegalHold` | 🟡 **Not in `closed_classes.json`.** CF-64 closed; CF-165 still open in the register |
| 53 | Event / async | **113 events**, consumers, idempotency | ✅ closed |
| 40 | Test / acceptance | **22 permission vectors** | ✅ closed |
| — | Accessibility | WCAG 2.2 AA obligations | ✅ closed |
| — | Localisation | translation and locale handling | ✅ closed |

**Every count in that column had moved since 20 September** — reports 43 → 51, permissions
154 → 176, device kinds 20 → 24, state models 126 → 210, events 30 → 113. The permission vectors
went 28 → 22, which is the one that fell; the vectors file now holds 22. None was wrong when
written. That is the whole argument for re-deriving rather than carrying forward.

## The artefact classes the August audit called missing

Twelve are closed, recorded in `handoff/closed_classes.json`:

> accessibility · audit · configuration · event / async · integration · localisation · notification · permission / role · report · state model · test / acceptance · validation rule

That covers six of the seven the August version marked 🔴 — Report, Configuration, Audit,
Notification, Integration and Validation rule all have the register or catalogue it said was
absent.

**Two do not appear in the closed list. Both now have the artefact; whether to add them to it is
a decision, not a count**, and it is left to whoever owns `closed_classes.json`.

### Retention / archive — decided by ADR-0047 and contracted

**The August finding was "mentioned nowhere concrete", and that is no longer true.** ADR-0047
(accepted 20 September; one number still pending sign-off) decides three stages, a base period of
five years from last activity, a floor-aware default, the archive as a separate instance, and that
derived stores purge at archive. **CF-64 closed on 21 September**, its provider half on 28 September.

The operations exist: `setDataRetentionPolicy` and `listDataRetentionSettings` /
`setDataRetentionSetting` hold the policy, `runDataRetention` applies it, `listArchivalJobs` shows
what moved, `setLegalHold` stops a deletion that must not happen, and `listDataRetentionExpiry`
reads what is due. Erasure is a tombstone on `pii.subject` (`is_erased`, `erased_at`) with
`deleteGuestAccount` and `ai.eraseSubject` behind it.

**CF-165 is still listed open in the conflict register**, with text saying the retention half is
decided and not built and that no erase operation exists. Both halves of that text are behind the
contracts. Closing it is the register owner's step.

### Device / hardware — one register and a driver decision

August called it 🟡, *"no driver register or vendor matrix"*. **Both halves have an answer now.**
ADR-0015 decides standards-first drivers (amended for BOCA on 5 October and for the Windows device
host on 1 and 2 November), and external-dependencies §4.3 replaces the vendor matrix with one
standard inbound interface plus paid adapters. **ADR-0067 (1 October) made `platform.device` the
one register** for every device class, and Access keeps only where a device is placed; the
hardware model library is `setHardwareModel`. `DeviceKind` carries 24 kinds. **No device row is a
gap or partial any more**: the 17 gap rows this page listed on 20 September were all re-traced.

## Where the rows that are not CONTRACTED are

| Domain | Partial | Parked | Rows |
|---|---:|---:|---:|
| Inventory Management | 1 | 10 | 11 |
| Admission and Access | 3 | 2 | 5 |
| F&B POS | 1 | 2 | 3 |
| Ticketing Catalogue | 2 | 0 | 2 |
| Ticketing Sales | 1 | 1 | 2 |
| F&B & Guest Management | 2 | 0 | 2 |
| Developer & API Management | 0 | 2 | 2 |
| Guest Mobile App & Branding | 0 | 1 | 1 |
| Retail POS | 1 | 0 | 1 |
| Approval Workflows & Governance | 0 | 1 | 1 |

**Inventory at 11 is the warehouse execution layer the client declined** (CF-138, 18 August): ten
parked rows and one partial (15.4.7, par levels recommended for a person to apply). It is the
largest concentration and none of it is work.

## The configuration-scope finding, which has now moved

This is the one claim on this page that changed direction rather than degree.

The August audit's strongest observation was that **most configuration requirements do not state
a scope level** — 263 of 273. On 19 September this file recorded that `check-config-scope`
**reported 57 errors** against the package. **It reported none on 3 November 2026.**

**That closes the package half and not the requirement half.** Every configuration setting the
package defines declares whether it applies at tenant, venue, outlet or workstation. The
requirements still mostly do not say, which means each of those declarations is a decision the
package made rather than one the matrix specified — **defensible, recorded, and worth a client
read rather than an assumption.** A setting changed at the wrong level is a setting somebody
changes once and cannot explain afterwards.

## How to re-derive this

Verdicts, domains and sections come from `handoff/traceability.json`; artefact classes from
`handoff/closed_classes.json`. **Both are authored inputs** — ring 4 of
`docs/contract-change-runbook.md` — so this file is rewritten by hand when they change.
`tools/check-authored-inputs.py` fails it when its verdict or domain table disagrees with
traceability, when its closed-class list is not the file's, when a held count is higher than
the package holds, or when it names something that does not exist; and it reports it stale when
a conflict it cites, or the closed-class list, moves.

Everything else is counted from the package directly:

    operations per contract        handoff/api-data-lineage.json
    distinct permissions           x-ticvai-permission across contracts/
    permission vectors             docs/architecture/specs/permission-vectors.json
    device kinds                   DeviceKind enum, contracts/spine/tenancy.yaml
    state models · events          states/ · events/
    configuration scope            python3 tools/check-config-scope.py
