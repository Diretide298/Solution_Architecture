# Artefact audit — what the requirements demand that we do not have

> Rewritten 19 September 2026, superseding the 17 August version. That one was written
> before the requirement walk and asked "which artefact classes does the package lack?"
> The walk has since answered most of it, so this asks the question the other way round:
> **of 3,184 rows, which are still not designed against, and what kind of thing is
> missing?**

**3,184 matrix rows, every one carrying a verdict, and all 142 sections closed.** The
August version counted 3,297 across four sheets; the walk resolved the difference as
duplicates and superseded rows. Derived from `handoff/traceability.json` and
`handoff/closed_classes.json`.

## Where the rows landed

| Verdict | Rows | | What it means |
|---|---:|---:|---|
| `CONTRACTED` | 2,647 | 83.1% | An operation or schema field demonstrably serves it |
| `PARKED` | 396 | 12.4% | AI-parked or workshop-blocked, with the reason named |
| `GAP_CONTRACT` | 93 | 2.9% | Needs an operation or schema that does not exist |
| `CONTRACTED_PARTIAL` | 43 | 1.4% | Served, but a field, operation or state is missing |
| `GAP_DECISION` | 5 | 0.2% | Undesignable without a client answer |

**98 rows are a genuine gap** — 93 needing contract work and 5 needing the client. That is
**3.1% of the matrix**, against an August position where whole artefact classes had no
register at all.

## The artefact classes the August audit called missing

Twelve are now closed, recorded in `handoff/closed_classes.json`:

> accessibility · audit · configuration · event / async · integration · localisation ·
> notification · permission / role · report · state model · test / acceptance ·
> validation rule

That covers six of the seven the August version marked 🔴 — Report, Configuration, Audit,
Notification, Integration and Validation rule all now have the register or catalogue it
said was absent.

**Two do not appear in the closed list, and both are still open:**

### Retention / archive — still nothing concrete

The August finding stands and is unchanged: **retention requirements state contradictory
periods**, five different ones, recorded as CF-64. There is still no retention register
saying what is kept, for how long, and who may see it. 89 rows asked for this in August
and nothing in the closed list answers them.

### Device / hardware — and the walk agrees

August called it 🟡, "no driver register or vendor matrix". **Device Management is now the
third-worst gap domain in the entire matrix**, with 17 unresolved rows — which is
independent evidence for the same finding, reached from the opposite direction.

## Where the remaining 98 gaps are

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

**Admission and Access at 36 is the one to look at first.** It is the largest single
concentration left, and access is the highest-frequency operation in a venue — the one
place where a missing rule is felt by every guest rather than by an administrator.

## The configuration-scope finding, which has not moved

The August audit's strongest observation was that **most configuration requirements do not
state a scope level** — 263 of 273. Configuration is now a closed class, so the catalogue
exists; the scope problem does not go away with it, and there is a live checker saying so:
**`check-config-scope` reports 57 errors** in the current package. A configuration setting
that does not say whether it applies to a tenant, a venue or a workstation is a setting
somebody will change at the wrong level, and the closed class did not close that.

## How to re-derive this

Everything above is counted from `handoff/traceability.json` (verdicts, domains, sections)
and `handoff/closed_classes.json` (artefact classes). **Both are authored inputs** — see
ring 4 of `docs/contract-change-runbook.md` — so this file has to be rewritten by hand when
they change. `tools/check-authored-inputs.py` reports when the contracts have moved
underneath it.
