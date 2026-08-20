# The delivery plan against the package

**18 August 2026.** `sources/client/TAIS_Product_Planning_and_Delivery_Plan.xlsx` — nine sheets,
**23 epics, 444 features, 2,173 tasks, 7,552 person-days, six milestones**, plus a Jira import of
2,640 issues.

**It has existed for six days and nothing in this package knew about it.**

---

## 🔴 Two independent plans over the same work

**The plan sequences by milestone. The package sequences by wave. Neither references the other.**

| | Milestones | Waves |
|---|---|---|
| Structure | M1 Foundation · M2 Core Platform · M3 Business Features · M4 Integrations · M5 Testing · M6 Release | Wave 1 · 2 · 3 |
| Unit | 444 features | 374 screens |
| Sized | **7,552 person-days** | Not sized |
| Derived from | The requirement matrix, by epic and dependency | Flow dependencies between screens |

**CF-101 re-waved nine screens and three flows yesterday**, and the register records the
reasoning as *"if a wave's flow needs a screen, that screen is in that wave."* That reasoning is
sound and it was made without knowing a milestone plan existed.

**These have to reconcile before either is used for scheduling.** The plan has effort and the
waves have dependencies, and neither alone is a schedule.

---

## The effort figure is the thing to read first

**7,552 person-days.** M4 Integrations alone is **3,900** — more than M1, M2 and M3 combined.

That is a shape worth arguing with. **M4 carries payment certification, external gateways and
intelligence**, and this package has been treating integrations as adaptor-shaped work behind
ADR-0012 and ADR-0015 precisely so they are not a 3,900-day risk. Either the estimate predates
that decision or the decision has not reduced it.

**M5 Testing is 58 days and M6 Production Release is 26.** Against 7,468 days of build, that is
1.1% for testing and cutover on a platform whose gates cannot fail.

---

## Where the plan and the package agree

**Its Dependency Matrix says what ADR-0024 says**: *"Nothing functional ships without the
multi-tenant core"*, *"UI cannot be completed before backend APIs"*, and offline POS is flagged
**high-complexity, architectural**.

**Its Missing Components sheet found what our audits found**, independently — audit logging,
notifications as one service, configuration and feature flags, localisation with Arabic RTL,
offline-first for POS and gates. Two lists built from the same matrix by different routes, and
they converge.

## Where they diverge

**Two components the plan marks `MISSING` outright:**

**DevOps / IaC** and **CI/CD** — *"MISSING — add Infrastructure-as-Code and environment
provisioning"*, *"MISSING — add CI/CD pipelines with automated gates"*. Neither appears in the
package either. **Sprint 0 has been at 0 of 11 since 30 July**, and this is the same finding from
the other side.

**The plan counts 3,332 requirements across its epics.** The matrix Functionality sheet has 3,184
rows and 3,156 distinct references (`handoff/requirement-count.md`). **A third number**, and the
plan's own total row reports 6,664 — double-counted. Worth reconciling once rather than
repeatedly.

---

## What I would do

**Map the 23 epics to the 25 contracts.** They are close — E01 Ticketing to `catalogue`, E03
Admission to `access`, E04 Payments to `orders` and `finance` — and a mapping makes the effort
figures attach to artefacts that exist rather than to feature names.

**Then reconcile milestones to waves**, in that direction. The milestones carry effort and
priority from the client's own register; the waves carry the dependency reasoning. **A wave that
contradicts a milestone should move, unless the flow dependency makes it impossible** — and where
it does, that is worth saying rather than silently re-waving.

**Raised as CF-124.**
