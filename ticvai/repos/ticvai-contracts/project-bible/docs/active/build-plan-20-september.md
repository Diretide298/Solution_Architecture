# Build plan — 20 September 2026

> Everything open on the project, ordered by what unblocks what. **Contracts are unfrozen for
> this plan**; the freeze of 20 September covered cleanup, and this is new capability.
>
> Nine backlog entries and twelve conflicts. **Five of the twelve conflicts need a number or a
> position from a person and nothing can be built past them**; the other seven are work.

## Phase 0 — the five decisions everything else waits on

| # | Decision | Who | Blocks |
|---|---|---|---|
| D1 | The consent model for biometrics: opt-in at ticket type, or opt-in at the gate | Chinmay + Allam | BL-096, BL-105, BL-106, CF-35 |
| D2 | Retention floors and the tightest RPO any tenant may buy | Dinesh + Qossai | CF-64, CF-165, and the burst design |
| D3 | The instance-growth threshold — ADR-0042 proposes 70% on three days in seven | Chinmay + Dinesh | CF-168, CF-162 |
| D4 | How far ABAC goes: attributes on the existing model, or a second model | Chinmay | BL-110 |
| D5 | What one guest may see of another on a leaderboard | Chinmay + Allam | BL-173 |

---

## Phase 1 — biometrics and consent (CF-35, BL-096, BL-105, BL-106)

**The client's position, 20 September: the venue turns biometrics on or off per ticket type, and
consent is taken from the guest as a consequence.** That is the right shape and it is what the
market does — Disneyland's April 2026 rollout keeps non-biometric lanes open at the main
entrances, and Universal Orlando has run facial entry as an *option* since 2023. **The live
lawsuit against Disney is about consent quality, not about the technology**: the claim is that
signage and terms-of-service language are not meaningful consent when the alternative requires a
guest to go and find a different lane.

**So the design rule is: the switch is the venue's, the consent is the guest's, and neither
substitutes for the other.**

Under PDPL (Federal Decree-Law 45/2021), biometric data is sensitive personal data. It needs
**explicit, clear and voluntary consent**, it is **withdrawable at any time**, and Article 21
requires a **DPIA** before processing that uses new technology at high risk. Three things follow
that the package does not currently have:

1. **A non-biometric path must always exist for the same ticket.** A ticket type that *requires*
   biometrics makes consent a condition of entry, and consent that is a condition of entry is
   not voluntary. `biometricPolicy` is therefore `disabled | offered | preferred` — **never
   `required`.**
2. **Withdrawal has to delete, not just flag.** A withdrawn consent that leaves the template on
   the reader is the erasure that did not happen — the same rule `removeIndexEntry` already
   carries for the RAG index.
3. **Turning it on must warn the venue** (the client's own instruction): enabling biometrics on
   a ticket type surfaces the DPIA and consent-form obligation at the moment of the switch,
   because that is the only moment somebody is paying attention.

### The work

| | |
|---|---|
| **BL-105** | `biometricPolicy` on the admission profile — `disabled/offered/preferred`, per ticket type. `setAdmissionProfile` gains it; enabling returns a warning payload naming the DPIA and consent obligations (CF-35) |
| **BL-106** | `Face Tag` and `Face Pass` as distinct kinds with distinct retention. **Tag is discarded when the ticket expires; Pass survives the visit.** Same column cannot serve both because the retention rule is the difference |
| **BL-096** | Identity verification — a presented document checked against the entitlement holder. **Modelled apart from enrolment**, because verifying a document is not storing a face |
| **CF-35** | Closed by the above plus the warning path, with the DPIA recorded as a deliverable rather than a contract artefact |

**Face Tag is the one with a real modelling trap.** It is temporary facial storage discarded at
ticket expiry — so its retention is a *function of another object's lifetime*, not a configured
period. That is the only retention rule in the package that is not a number, and it has to be
written before D2 sets the general floors, not after.

---

## Phase 2 — compliance (CF-133 → BL-140, CF-127 → BL-073)

### CF-133 is more urgent than the register says, and the answer is not "build an invoice"

**The UAE has a dated e-invoicing mandate and it is already running.** Pilot from 1 July 2026;
large businesses from 1 January 2027; SMEs from 1 July 2027. **Businesses at AED 50m+ revenue
must appoint an Accredited Service Provider by 30 October 2026** — six weeks from today, and
every venue operator of the size this platform targets is over that line.

The model is **Peppol five-corner (DCTCE)**: supplier → supplier's ASP → buyer's ASP → buyer,
with the **FTA as the fifth corner**, receiving tax data as the invoice moves. Invoices are
**PINT AE XML** with **51 mandatory fields**.

**So TICVAI does not integrate with the Federal Tax Authority.** It produces a compliant invoice
payload and hands it to the tenant's ASP over Peppol. That is an adaptor — ADR-0012's shape
exactly — not a document feature, and it changes what BL-140 has to build:

    not        a PDF renderer and a numbering scheme
    but        a tax invoice MODEL carrying all 51 PINT AE fields, an ASP adaptor,
               and the credit memo as its paired obligation

**The tenant is the taxable person, not TICVAI**, so `LegalEntity.taxRegistrationNumber` is the
right home and the ASP is tenant configuration. **5.10.3 — what a VAT receipt at the till must
show — is the same obligation one layer down** and is answered by the same field set.

**For Qossai:** which ASP, and has the client appointed one? That is a procurement question with
a deadline, and it is the only part of this we cannot start without them.

### CF-127 — cookie consent

Fifteen requirements, a regulatory obligation, and **normally bought rather than built**. The
register is right. **For Qossai: buy or build.** If bought, BL-073 becomes an integration and a
consent record in `pii`; if built, it is a product line — banner, categorisation, script
blocking, scanning, multi-domain preference sharing and analytics — that nothing in the
estimate carries.

**Either way the consent record itself belongs to us**, because `recordConsent` already exists
and CF-160 settled that a merge takes the narrower of two consents. A bought banner that keeps
its own consent store creates a second answer to a question we already answer.

---

## Phase 3 — the three build entries

### BL-110 — ABAC (43 refs, the largest unbuilt thing left)

48 requirements against a role-based model chosen deliberately. **This is D4 and it is a genuine
fork.** `Session.scope` already resolves once at login from the ltree hierarchy with
deny-overrides-allow, and clients filter navigation against it rather than computing it.

    (a) attributes on the existing model   conditions on an existing grant -- scope path,
                                           time window, device, channel. Cheap, and it is
                                           what most of the 48 actually ask for
    (b) a second, general policy engine    subject/resource/action/environment evaluated
                                           per request. Complete, and it puts a policy
                                           decision on the hot path of every call

**Recommendation: (a).** The package's whole performance position is that permissions resolve
once at login and never on the hot path; (b) reverses that. Walk the 48 first and report how
many genuinely need an attribute the scope tree cannot express — **that walk is the deliverable
before any contract change**, and it is startable now.

### BL-100 — dunning, retry schedules, billing statements

The other five capabilities exist. These three appear nowhere. **Plus a boundary question that
is now a fact rather than a hypothetical**: `setRenewalAutoMembership` is guest membership
billing and it lives in `subscription.yaml`, which the backlog entry itself argued is the
Control Plane and the wrong place for it. **Decide the boundary before adding three more
operations to it**, or the wrong home gets three more reasons to stay.

### BL-173 — leaderboards

Everything else in gamification is built. **This is D5 and it is a privacy question before it is
an operation**: a leaderboard shows one guest something about another. Display name, initials, a
rank with no identity, opt-in visibility — the answer changes the schema, and under PDPL an
opt-out leaderboard that shows a full name is a disclosure nobody consented to.

---

## Phase 4 — the three that must be read together (CF-162, CF-165, CF-168)

**They are one question — where data lives and for how long — and reading them apart is why each
has stalled.**

### The connection nobody has drawn

ADR-0042 places a tenant on the **emptiest** instance, where *emptiest* is peak concurrent
connections over the trailing 7 days as a fraction of that instance's `max_connections`, with a
pin override for a client buying a quiet neighbour.

**A burst environment (CF-162) breaks that rule by construction.** It is a short-lived
environment standing up for one flash sale, taking tens of thousands of concurrent users within
hours, with **no trailing history at all**. Emptiest-first would place the single most violent
workload in the estate onto the instance with the least headroom to spare, and the first symptom
would be the sale.

    So: a burst environment is never PLACED. It is pinned, by construction --
    the pin override used as the rule rather than the exception.
    And its load must never enter another instance's placement metric,
    or one flash sale poisons the trailing average for a week.

**And CF-165 is the third side of the same shape.** A burst environment has no tenancy of its
own, reads a catalogue it does not own, and its orders must reconcile back into the permanent
platform. **The reconciliation path is the part with no design** — and once it lands, the burst
environment's own copy has to be destroyed. That is a retention rule that is **not configurable
and not a number**: *kept until reconciled, plus the audit window, then gone*. It is the same
answer as Face Tag in Phase 1, arriving from the infrastructure side.

### Proposed decisions

| | |
|---|---|
| **CF-168** | **Take 70% on three days in a rolling seven, at least two non-consecutive.** ADR-0042 already argues it and nothing has contradicted it in twelve days. Add: **a burst instance is excluded from every placement metric.** |
| **CF-162** | **A burst environment is a pinned `control.cell_instance` with no `cell_tenant` of its own**, a read-only catalogue replica, and an outbox that reconciles orders into the permanent cell. Not a cell — it has no tenancy — which is why ADR-0001 does not describe it and should not be stretched to. |
| **CF-165 + CF-64** | **The two registers get read against each other and closed as one.** Guest-profile retention is the hole; the burst copy and Face Tag are the two rules that are lifetimes rather than periods. |

---

## Phase 5 — CF-64 in full, because it is the one most misread

**The row says "89 retention requirements" and that is not 89 open questions.**

| | |
|---|---|
| **2 requirements name a period** | 4.3.4 — ten years, payment records. 6.1.78 — seven years |
| **87 say "configurable"** | they ask the platform to let somebody set a period, not to pick one |
| **RPO/RTO is separate and narrower** | DR requirements 11 and 12 ask the platform to **support configurable** RPO and RTO, not to hit a number. Refined 17 August after CF-60 counted the DR sheet: 62 of its requirements are infrastructure — backup schedules, replication, restore drills — and **only RPO and RTO sit in the platform at all** |

**So what is actually being asked of a person is two numbers and one policy.**

**1. The RPO floor.** A configurable RPO still needs a floor, and the floor is a topology
decision made once: **offering an RPO near zero requires synchronous replication and a second
site.** The question is *not* "what is Miral's RPO" — it is **"what is the tightest RPO any
tenant may ever buy"**, because that is what the estate has to be built to support. Recommend
tying it to CF-168's pin: **asynchronous replication with a several-minute RPO as standard, and
near-zero available only on a pinned dedicated instance**, which is what a dedicated client is
already paying for. That makes one decision serve two conflicts.

**2. The retention floor and ceiling.** The two stated periods become minimums — ten years for
payment, seven for financial — and "configurable" gets a **range** rather than a free field. A
configurable retention with no minimum lets a tenant set thirty days on a record the law
requires for seven years.

**3. Guest-profile retention, which is CF-165's hole and has no answer at all.** Nothing says how
long a guest profile is kept or what happens to it afterwards. **This is the one that is genuinely
missing rather than merely unset** — there is no operation, no column and no policy, and consent
without retention is half a privacy position.

---

## Phase 6 — the artefact conflicts

| CF | What | Startable now |
|---|---|---|
| **CF-171** | **Re-measured 20 September: 577 of 2,056 provisional, 28%** — was 577 of 1,626, 35%. **Not one has been specified.** It looks better only because the denominator grew. Concentrated in access (146), catalogue (108), promotions (96), orders (89) | Yes — specify by cluster, biggest first |
| **CF-170** | 17 screens promise a publication their operations cannot perform; 5 are a broken workflow, not a naming defect | Yes — separate the 5 first |
| **CF-169** | Contract half closed 20 September. Remaining: dashboard authoring screens and seatp's 130 seat-map screens | Yes — design |
| **CF-166** | Three of four gaps closed, the fourth was never a gap. **No owner recorded** — assign and close | Yes |
| **CF-140** | The plan prices 7,552 person-days and its priorities contradict the dependency order the walk found. **This plan is the input to re-pricing it** | After Phase 0 |

---

## Order of work

    now, no decision needed     BL-110's walk of the 48 requirements
                                CF-170's 17 screens, separating the 5 broken workflows
                                CF-166 close, CF-171 specification by cluster
    after D1                    Phase 1 entire -- biometrics is the largest cluster
    after D2                    CF-64, CF-165, and the burst retention rule
    after D3                    CF-162 burst design
    with Qossai                 CF-133 ASP appointment, CF-127 buy-or-build
    last                        CF-140 re-priced against everything above
