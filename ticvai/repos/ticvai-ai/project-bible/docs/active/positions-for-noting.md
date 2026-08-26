# Three positions, for noting

**18 August 2026.** These are technical decisions Softlabs is taking. **They go to the client as
positions, not questions** — with the reasoning and the reversal cost, so that noting them is
informed rather than passive.

**Two things go to Qossai as actual decisions** and are not in this file: CL-11, whether TICVAI is
a platform others build on, and the funds-flow half of CL-06 — which acquirer, and whether a
refund may settle into a balance. **One thing is a written input**: the legal basis for
gender-segregated access.

**Each position below states what it costs to reverse.** A position nobody can price is a
position nobody can disagree with usefully.

---

## Position 1 — A bookable resource is a bounded context, and we are building one

**CL-01 · 9 backlog entries · 98 row citations · CF-125**

### What we are doing

Adding a resource model: a typed object with attributes, a calendar, and a check-out and check-in
lifecycle. Rentals, lockers, cabanas, wheelchairs, strollers, instructors and allocatable
equipment all resolve to it.

### Why it is not a product

**A cabana is currently a product with an availability envelope.** That sells a slot. It cannot
express *this specific object, checked out to that guest, returned at 4pm, with a deposit against
it.*

Ten requirements define the entity directly, and the utilisation reporting behind them has no
source — **you cannot report on the utilisation of something the model does not know exists.**

**7.6 is fifteen rows of rentals and none of them is served.** Not partially — none.

### What we are not doing here

**We are not deciding whether rentals ship in Phase 1.** The delivery plan puts this work at P3
against 98 row citations, and that contradiction is real — **it belongs to CF-140, the delivery
plan reconciliation, and not to this position.**

Building the model without the phasing answer risks building early. Building the phasing answer
without the model risks committing to a date for something undesigned. **They are separable and
should stay separate.**

### Cost to reverse

**High, and rising.** A resource model touches `catalogue`, `orders`, `inventory` and
`maintenance`. Reversing after those are wired means unpicking four contracts. **Before anything
is built, it is a design conversation; after, it is a migration.**

---

## Position 2 — A waiver, a survey and a capture form are one mechanism

**CL-04 · 4 backlog entries · 79 row citations · CF-129**

### What we are doing

Building one configurable form: versioned, with a field library, conditional logic, and a signed
or unsigned artefact stored against the guest. **A waiver is that form with a signature. A survey
is that form with a scale. A demographic capture is that form at the point of sale.**

### Why one and not three

They were raised separately and share every part: field configuration, conditional display,
versioning, an acceptance record and a stored artefact. **Three implementations would drift on the
version rule first** — a waiver signed against version 3 must stay bound to version 3, and that is
the same requirement a survey has when the question wording changes mid-campaign.

**`signature` appears today only on maintenance work-order attachments**, and `signaturePad` is a
device kind with nothing to sign. The pieces exist and are pointed at the wrong thing.

### What we are raising rather than deciding

**2.15.9 makes ticket issuance conditional on a signed waiver.** That is a legal instrument
gating a sale, and **whether an e-signature captured this way is enforceable in the UAE is a
question for counsel, not for us.** We are building the mechanism; we are not asserting it is
sufficient.

### Cost to reverse

**Low.** One contract, and the three uses are configuration on top of it. If the client later
wants a bought survey tool, the form mechanism still serves waivers and capture — **splitting
later is cheap, merging later is not.**

---

## Position 3 — Portfolio is delegated authority, not a household table

**CL-05 · 4 backlog entries · 49 row citations · CF-132**

**This is the position most likely to sound like a deflection, so the reasoning matters more than
the conclusion.**

### What the client asked for

Section 5.5 specifies it fully: multiple portfolios per account, **a primary holder assigning
entitlements**, transfer between linked portfolios, **shared wallets with individual tracking**,
and merging. It appears ten times across ten sections. BL-028 adds a group leader with per-
attendee capture; BL-035 adds corporate allocations and member enrolment.

### What we are building

**Not a family tree. A grant.**

Every one of those requirements reduces to the same question: **who may act on whose behalf, over
what, and until when.** A primary holder assigning an entitlement is a grant. A group leader
holding tickets for twelve people is a grant. A corporate account enrolling members is a grant
with a quota. **A shared wallet with individual tracking is a grant over a balance, with the
transaction log already recording who spent.**

`Grant` today carries principal, role, permission, `scopePath`, effect and a validity window.
**It already does two thirds of this** — what it does not yet express is a grant held by a guest
rather than a staff member, and a grant scoped to an object rather than a scope node.

### Why this is better than a household model

**A household table answers one question and this answers four.** Group bookings, corporate
accounts, family portfolios and shared wallets are one mechanism, and a bespoke family structure
would leave the other three unserved.

**And it inherits the audit.** Who assigned what to whom, when, and whether it has expired is
already recorded for every grant. A household model would need that built.

### What we are not claiming

**This does not make the work smaller.** Extending grants to guest-held, object-scoped authority
is real work in `identity` and touches `orders`, `access` and `retail`. **The claim is that it is
one piece of work rather than four**, and that it lands on a mechanism with audit and expiry
already in it.

### Cost to reverse

**Medium.** If the client comes back with a requirement that is genuinely structural — a legal
household entity with its own identity, for instance — a portfolio table can be added beside the
grants without unpicking them. **The grants remain correct even if a structure is added later.**

---

## How these three should be presented

**Together, in five minutes, before the two real decisions.** They set the frame: this is what we
have decided and why, and here is what we still need from you.

**Do not present them as questions.** The moment CL-05 is framed as *"we were thinking of doing it
this way, what do you think"*, it becomes a fourth thread and the meeting is a survey again.

**Do present the reversal cost.** It is what distinguishes a position from an assertion, and it
gives the client a real place to push back — on the cost, not on the design.
