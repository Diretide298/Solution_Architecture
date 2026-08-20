# Artefact audit — what the requirements demand that we do not have

**3,297 requirements across four sheets, classified by the kind of artefact each one needs.**
Not a checklist from elsewhere — derived from the requirement text itself.

Two of these were closed today. The rest are open, and they divide into gaps that are ours
and ambiguities that are the client's.

| Reqs | Class | What we hold | Artefact |
|---|---|---|---|
| **347** | **Report** | 23 operations, a definition engine | 🔴 **No register.** 52 reports are named by title and nothing lists them |
| 290 | Permission / role | 111 permissions, 28 test vectors | ✅ `permission-resolution.md` |
| **273** | **Configuration** | ~18 config operations | 🔴 **No catalogue.** And 263 of 273 do not say at what level |
| **206** | **Audit** | `identity.authz_audit` | 🔴 **No register** of what must be audited, kept how long, seen by whom |
| **193** | **Notification** | `MessageTemplate` | 🔴 **No catalogue.** Email 83, SMS 34, WhatsApp 30, push 20 |
| **171** | **Integration** | Adaptor patterns, ADR-0012/0015 | 🔴 **No register.** 19 software and 16 hardware named, never itemised |
| 117 | State model | 6 models, transitions checked | ✅ Added 14 Aug |
| **105** | **Device / hardware** | 11 device kinds, ADR-0015 | 🟡 No driver register or vendor matrix |
| **94** | **Validation rule** | Prose in contract descriptions | 🔴 **No business rules register** |
| **89** | **Retention / archive** | Mentioned nowhere concrete | 🔴 **Nothing.** Two requirements state a period; the rest do not |
| 53 | Event / async | 12 events, consumers, idempotency | ✅ Added 14 Aug |
| **40** | Test / acceptance | 28 permission vectors | 🟡 No scenario set beyond permissions |
| **38** | Localisation | `LocalisedText`, RTL in ADR | 🟡 No translation key inventory |
| **30** | Performance / SLA | Read routing, ADR-0016 | 🔴 **No stated targets** |
| **26** | Accessibility | `altText`, focus order on screens | 🟡 No criteria or audit plan |

---

## The two findings that change what to ask the client

### 263 of 273 configuration requirements do not say at what level

"Configurable" appears 273 times. **Ten say per venue, per region, per tenant or per
workstation. Two hundred and sixty-three say nothing.**

Every one is a design decision that someone will make by default if nobody asks. A refund
threshold configurable per venue is a different system from one configurable per tenant — the
first needs a row per venue and an inheritance rule, the second needs neither.

We have already been guessing. CF-36 settled the refund threshold as venue policy; CF-38 did
the same for price variance. **Both were guesses that happened to be confirmed.** The other
261 have not been.

**This is the single largest source of latent rework in the matrix**, and it is cheap to fix:
one column, filled in during the workshops.

### 89 retention requirements and two stated periods

Only **4.3.4 (10 years, payment)** and **6.1.78 (7 years)** name a number. Everything else
says retain, archive or purge without saying for how long.

**And Disaster Recovery & BCP is 62 requirements with no RPO and no RTO** — see CF-60. Recovery
objectives determine the database topology: a one-hour RPO and a one-minute RPO are different
replication architectures, and we are building without knowing which.

This lands hardest on **on-premise** (ADR-0017), where backup is the client's responsibility
and they will ask us what good looks like.

---

## The 52 named reports

The matrix names reports by title — not as a capability, as a list. A sample:

- Access Control Override Report
- Advance Booking Report
- B2B Sales Report
- Booking Status Report
- Commission Report
- Cost Center Allocation Report
- Cost Center Configuration Report
- Cost Center Revenue Report
- Damage Fee Report
- Deferred Revenue Report
- Deposit Refund Report
- Deposit Report
- Donation Reconciliation Report
- Donation Settlement Report
- Equipment Allocation Report
- Equipment Usage Report
- Equipment Utilization Report
- Flight Session Report
- Gate Utilization Report
- Group Booking Report
- Group Utilization Report
- Incident Report
- Instructor Assignment Report
- Inventory Availability Report

**52 distinct titles**, counted strictly — a looser match gives 83, and the difference is lines
like "Attendance by Product" that name a dimension rather than a report. The register should
resolve which they are. We have a report *definition engine* — `createReport`,
`runReport`, `scheduleReport` — which is the right shape. What we cannot do is show that any
particular named report is covered, because nothing maps title to definition.

A register is a day's work and turns 347 requirements from unverifiable into countable.

---

## What I would do, in order

| | | Why first |
|---|---|---|
| 1 | **Configuration level column in the matrix** | 263 unstated decisions, and each one is rework if guessed wrong |
| 2 | **Retention and recovery objectives** | Determines database topology. Cannot be retrofitted |
| 3 | **Report register** | 347 requirements become countable |
| 4 | **Integration register** | 35 named systems, several with no contract behind them |
| 5 | Notification catalogue | Which event, which channel, whose consent |
| 6 | Business rules register | 94 rules currently living in prose |

Items 1 and 2 are **client questions**, and they belong in the next workshop rather than in a
document we write. Items 3 to 6 are ours.

## What this audit is not

Keyword classification over 3,297 requirements. A requirement mentioning "report" is not
necessarily a report requirement, and 188 hits for "call" turned out to be call centre. The
counts are indicative; **the two findings above were verified by reading the requirements
themselves**, and they are the ones worth acting on.

## Position, 17 August

**12 of 15 classes closed. 1,848 of 2,072 requirements have an artefact — 89%.**

| Class | Reqs | Artefact |
|---|---|---|
| report | 347 | `report-register.md` — 20 engine capabilities, 113 definitions to seed |
| permission / role | 290 | 110 permissions; every operation declares one or an auth model |
| configuration | 273 | 321 levels decided, ADR-0018, `check-config-scope` |
| **audit** | 206 | **`audit-register.md`** — 431 write operations, and the subset needing more than the default |
| **notification** | 193 | **`notification-catalogue.md`** — event to audience to channel to consent |
| integration | 171 | `integration-register.md` — 35 named systems |
| state model | 117 | 41 models, every status enum covered |
| **validation rule** | 94 | **`validation-rules.md`** — 194 refusals + 327 guards = 521 testable rules |
| event / async | 53 | 26 events with consumers and idempotency keys |
| **test / acceptance** | 40 | **`test-and-acceptance.md`** — four layers, all derivable |
| **localisation** | 38 | **`localisation.md`** — 3,088 keys derivable today |
| **accessibility** | 26 | **`accessibility.md`** — WCAG 2.2 AA, per surface, with an audit plan |

### The three left, and all three are blocked

| Class | Reqs | Blocked by |
|---|---|---|
| **device / hardware** | 105 | **Workshop** — Device Management (CF-21) |
| **retention / archive** | 89 | **Client** — CF-64. Two periods stated of 89 |
| **performance / SLA** | 30 | **Client** — no targets given, so there is nothing to assert |

**224 requirements, none of them ours.**

### What closing six of them actually took

Almost none of it was design. **The audit register found that every write is auditable and the
question was what beyond the default.** The validation rules were already written — in 409
descriptions — and had never been listed. Localisation's 3,088 keys were sitting in the screens
and the enums.

**The exception is notification**, which needed a real decision: event to audience to channel to
consent, and three events that deliberately notify nobody. A catalogue that only lists what
sends cannot be reviewed, because a reader cannot tell absent-by-decision from forgotten.

