# Build order

**Ten apps, classified by what has to happen before someone can start.**

Named by operator on 17 August. This is the second cut: **not who runs it, but whether it can
be built.**

The gate is **specified**, not defined. Every screen in the platform is defined — it has a
purpose, a route and navigation, which is enough to draw. Specified means it also names its
operations and its states, and **the states are what a developer builds from**. A screen with
`loading: TODO` and no offline state is a screen someone will invent behaviour for.

---

## 1 — Ready to build · 26 screens

| App | Screens | Wave 1 | Specified | |
|---|---|---|---|---|
| **`venue-scanner`** | 16 | 16 | **16 (100%)** | offline |
| **`venue-pos`** | 10 | 7 | **10 (100%)** | offline |

**Both are offline-mandatory, and both are fully specified — that is not a coincidence.** They
were specified first precisely because a gate that cannot validate without a network is a queue
and a till that cannot sell is a closed counter, and those states had to be written down before
anyone could build them.

**Twenty-six screens is a small enough surface to be the first thing that runs.** The scanner
in particular has one job, sixteen screens, a complete state model and a flow (F06) with eight
branches. It is the best candidate for the first vertical slice.

## 2 — Wave 1 critical, specify first · 79 screens

| App | Screens | Wave 1 | Specified | |
|---|---|---|---|---|
| `venue-staff-app` | 50 | 27 | 10 (20%) | offline |
| `guest-web` | 29 | 18 | 10 (34%) | |

**More than half of each is Wave 1**, so neither can slip, and neither is ready.

`venue-staff-app` is the harder of the two: it is offline-capable, forty of its screens have no
offline state written, **and a task has no contract at all** (CF-71) — fifty screens are built
around an object that appears in none of 689 operations.

`guest-web` is the purchase path. F01 and F02 run end to end through it, which means its gaps
are the most visible ones.

## 3 — Wave 1 partial · 205 screens

| App | Screens | Wave 1 | Specified | |
|---|---|---|---|---|
| `venue-management-web` | 93 | 35 | **5 (5%)** | |
| `guest-app` | 76 | 20 | 16 (21%) | |
| `ticvai-web` | 36 | 10 | **0 (0%)** | |

**The bulk of the platform, and the least ready.** `venue-management-web` is 93 screens with
five specified — sixty-seven of them arrived on 14 August from the wireframe boards and carry
purposes and navigation and nothing else.

`ticvai-web` at zero specified is the one to notice: **it provisions cells and ships releases**,
so nothing else can be deployed without it, and it has no states written at all.

**Only a third of these are Wave 1.** The rest can wait, and treating all 205 as urgent is how
the Wave 1 third gets no attention.

## 4 — Wave 2 or later · 37 screens

| App | Screens | |
|---|---|---|
| `partner-web` | 21 | No Wave 1 screens |
| `accreditation-web` | 8 | **Workshop-blocked** (CF-21) |
| `venue-support-web` | 8 | No Wave 1 screens |

**None has a Wave 1 screen, so none blocks opening.** Accreditation is the one with a caveat:
its 58 requirements are workshop-blocked, and **accreditation validation appears on the Wave 1
scanner** — the portal can wait, the credential kind it issues cannot.

---

## What this says to do

**Build the scanner.** Sixteen screens, fully specified, offline-mandatory, one flow with its
unhappy paths written, and the smallest complete surface in the platform. It proves the
contract-to-schema derivation, the RLS policies, the offline bundle, the lease, the sync
reconciliation and the event catalogue against real infrastructure — and it does it in
twenty-six screens rather than three hundred.

**Then specify, in this order:** `ticvai-web` because nothing deploys without it,
`venue-staff-app` because it is half Wave 1 and offline, then `guest-web` because it is the
purchase path.

**Do not specify `venue-management-web` yet.** Ninety-three screens at 5% is a week of writing
that would be better spent after the first slice has run, because the first slice will change
what a specification needs to contain.

## The number underneath all of this

**67 of 347 specified — 19%.** That single figure explains why only two apps are buildable, and
it is the one measure that has barely moved while everything else went green.
