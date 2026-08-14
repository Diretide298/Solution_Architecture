# What is in this package, and what is not

**14 August 2026.** An honest account of the delivery against the whole build.

The short version: **the design layer is substantially complete and nothing has been executed.**
Every number below is counted from the files in this package, not from memory.

---

## What exists

| | | Against |
|---|---|---|
| **API operations** | **654** | Every unblocked module. 233 spine, 409 satellite |
| API schemas | 546 | Across 22 contract files |
| Permissions | 111 | With a resolution spec and 28 test vectors |
| **Tables designed** | **230** | 2,026 columns. 226 derived from the contracts, 4 PII tables held only in the reference |
| **Tables written as DDL** | **0** | Deliberate — see below |
| Screens inventoried | 347 | Across 12 platforms |
| **Screens defined** | **347** | **All twelve platforms** |
| Screens with operations declared | 155 | Of 347 |
| **Screens with states written** | **67** | Of 347 — the honest gap |
| State models | 39 | Of 39 status enums |
| Domain events | 16 | Publisher, consumers, idempotency keys |
| User flows | 12 | Of roughly 60 |
| ADRs | 18 | |
| Requirements mapped | 3,184 | Plus 113 on three sheets nobody had counted |
| **Requirements covered by a contract** | **2,842 (89%)** | |
| Configuration levels decided | 321 of 321 | |
| Validators | 5 | Plus 2 generators |

**1,771 files.**

---

## Coverage, honestly

### Contracts — effectively complete

**654 operations.** Every module that is not waiting on a client workshop has a contract, and
all of them validate: no duplicate operation ids, no unresolved `$ref`, every operation carries
the four required extensions, every permission resolves, every GET declares its read routing.

**What is genuinely missing is not ours to write:**

| | Reqs | Blocker |
|---|---|---|
| Developer & API Management | 94 | Workshop |
| Device Management | 60 | Workshop |
| Accreditation & Credential | 58 | Workshop. **Wave 1's scanner depends on it** |
| Approval Workflows | 80 | Cross-cutting, implemented in four places, owned by none |
| Employee Mobile App | 50 | A surface, so it maps to screens — and P06 has none written |

**212 workshop-blocked, not the ~276 the register claimed until today.** Rentals turned out not
to be a domain; it is 30 requirements scattered across seven, mostly in `catalogue` Resource
Management, which is contracted.

### Database — designed, none written

**230 tables and 2,026 columns exist as a reference, regenerated from the contracts whenever
they change. No SQL.**

Six migrations existed and were removed on 14 August. Writing DDL against a design that is
still moving produces migrations that must be rewritten, and a forward-only migration cannot be
rewritten.

The 30% of a migration that does not derive from the contracts — RLS with `FORCE`, level-typed
foreign keys, partitioning rules, 53 indexes, 28 constraints, seven functions — is written up
in `handoff/storage-design.md`. **That is the part worth keeping, and it is kept.**

**174 tables have no index strategy.** That is the largest gap in the storage design and the
one that decides whether the read replicas in ADR-0016 help or merely spread the problem.

### Screens — 347 of 347, and that number flatters us

| Platform | Screens | With operations | States written |
|---|---|---|---|
| P01 Guest Web | 29 | 26 | 10 |
| P02 Guest App | 62 | 21 | 2 |
| P04 Staff POS | 10 | 10 | **10** |
| P05 Guest Kiosk | 14 | 11 | 0 |
| P06 Staff App | 50 | 7 | 0 |
| **P07 Staff Scanner** | 16 | 15 | **0** |
| P08 Staff Web | 73 | 5 | 5 |
| P09 Admin Web | 36 | 24 | 0 |
| P10 Partner Web | 21 | 18 | 0 |
| P11 Accreditation | 8 | 0 | 0 |
| P12 Support Console | 8 | 7 | 0 |
| P13 White-Label CMS | 20 | 0 | 0 |
| **Total** | **347** | **144** | **27** |

**Every screen is defined. Twenty-seven have their states written.**

That distinction is the one to hold. A screen with a purpose, a route and navigation can be
drawn; it cannot be built from. The states are where the behaviour lives — loading, empty,
error, and on offline surfaces the offline state, which is the most important line on the page
and is `TODO` on all sixteen scanner screens.

167 of the 347 arrived on 14 August, extracted from the wireframe boards. They carry real
purposes and real navigation because the boards do. They carry no components and no states
because the boards are pictures, and a picture does not say what happens when the network dies.

**9 wireframes are approved** — P04 only. 338 are drafted or not started.

**143 of 642 operations reach a defined screen**, up from 125. The gap is no longer missing
screens; it is screens that name no operation.

### The layers that check each other

This is what the package has that a document set usually does not.

    requirement ──► contract ──► schema ──► table ──► column
                        │           │
                    operation ──► screen ──► route ──► component
                        │            │
                      event ◄── state model
                        │
                       flow

**Five validators run over it**, and between them they found 24 real defects on 14 August in
artefacts that had all previously reported clean. The most expensive:

- `createReservation` **silently absent** — `/reservations` declared twice, YAML kept the last block
- **17 enum values nothing could reach** — the contracts could start and finish things, not manage them mid-flight
- `platform.outbox` carrying venue payloads **with no RLS policy**
- Four foreign keys pointing at `pii.subject`, **a table no migration created**
- **Three Postgres enums disagreeing with their contracts**, including a hierarchy level that would not resolve
- **No concept of a payment provider**, while two gateways are named — settlement would have reconciled on amount and time alone

---

## What is not here

### Not built

**No code.** No `dotnet build`, no `pnpm install`, no container, no pipeline run. The 26
permission tests have never executed. Six repositories are scaffolded and empty of
implementation.

**No database.** No `psql`, no restored snapshot, no rollback test. Everything in
`storage-design.md` is structurally reasoned and syntactically unverified.

**Sprint 0 is 0 of 11.**

### Artefact classes still open

From `handoff/artefact-audit.md` — 3,297 requirements classified by the artefact each needs.
**Four of fifteen classes are closed.**

| Reqs | Class | |
|---|---|---|
| 347 | Report | No register. 52 named by title |
| 206 | Audit | No register of what must be audited |
| 193 | Notification | No event → channel → consent catalogue |
| 105 | Device / hardware | No driver or vendor matrix |
| 94 | Validation rule | 179 rules living in contract prose |
| 40 | Test / acceptance | Permission vectors only |
| 38 | Localisation | No translation key inventory |
| 26 | Accessibility | No criteria or audit plan |

**~1,049 requirements' worth, all buildable without asking anyone.**

### Blocked on the client

| | |
|---|---|
| **Retention and recovery** | 89 requirements, **two stated periods, no RPO, no RTO.** Recovery objectives determine the database topology |
| **Performance targets** | 30 requirements, one number |
| **Four workshops** | 212 requirements. Accreditation is on a Wave 1 surface |
| **9 open decisions** | Including Q2 waiting room build-or-buy, biometrics under PDPL, and AI configuration assistance moving to Wave 1 |

`conflict-status.md` has all 72, one line each.

### Unowned

**The migration orchestrator, since 30 July.** It now has a contract — 24 operations in
`platform-ops` — and a console screen, which makes it assignable. Every one of the 230 tables
lands through it.

**No AI engineer.** AI-61→66 is a Wave 1 commitment at roughly four weeks.

---

## The honest summary

**Design is ahead of where a project this age usually is, and execution has not started.**

The contracts, the schema design, the screens, the states and events and their cross-checks are
real work that will not need redoing. The 24 defects found on 14 August were found *because*
the artefacts are machine-checkable, which is the argument for having built them this way.

**The risk is the same one it has been since 30 July: nothing has run.** Six defects surfaced
the moment proper checks existed, in files that had reported clean for days. The first real
`psql` and the first real `dotnet build` will find more, and finding them against 230 designed
tables is cheaper than against 230 written ones — which is the reason the SQL is not here.

**If one thing moves next week, it should be the CI run.** Not the orchestrator, and not more
tables: a written migration nobody can apply is still better than 230 more tables written
against untested assumptions.
