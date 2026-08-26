# Design principles

**Read this before the ADRs.** There are twenty-four of them and they are long; the principles
beneath them are fewer, they repeat, and knowing them is usually enough to predict what an ADR
says.

Each principle names where it came from and what it rules out. **The ones marked *corrected* were
wrong first**, and those are the ones to trust most — they have been tested against something.

---

## Isolation

### Tenant isolation is structural, not a filter — where a cell holds one tenant

*Corrected twice, 17 August. ADR-0021, CF-97.*

**Postgres enforces row-level security. Qdrant enforces nothing.** On shared Postgres a careless
join returns no rows because the database stops you. On shared Qdrant a query missing its filter
returns every tenant's vectors, and nothing stops it.

So the boundary is the cell where a cell holds one tenant, and a dedicated shard where it does
not. **Rules out**: relying on a filter alone anywhere the isolation is between paying customers.

### The scope a caller acts under is resolved, never supplied

True of RLS, of `scope_path` in retrieval, of the shard key, of every `x-ticvai-scope-level`.

**A parameter the caller controls is not a boundary.** The retrieval client takes a session and a
question and offers no way to ask about somebody else's data — not by convention, by having no
parameter for it.

### Venues are partitioned, not separated

*ADR-0005.* List partitioning on `venue_id` inside the tenant database. **Rules out**: a database
per venue, and the operational cost that comes with it.

### AI is read-only against the transactional core

*ADR-0020.* It reads, it writes its own stores, and **a generated artefact enters a contract at
that contract's existing human commit step** rather than at a new gate invented for AI.

`generateVenueLayout` wrote directly into `seating.import_job` on the day this ADR was written,
which would have let a generated seat map reach a real one without a person looking at it.

### Personal data is a reference the ledger holds, never a value

*ADR-0023.* Which is how an immutable ledger and an erasable subject coexist: erasure empties the
person and the entry still balances.

**Rules out**: a name inside a ledger row, and with it the choice between a mutable ledger and a
dishonest erasure.

---

## Configuration

### Nearest ancestor wins, and venue is the floor

*ADR-0018. Chinmay's correction, which became the governing rule.*

Configuration resolves up the scope tree. **Workstations and outlets are assigned, not
configured** — a till does not have its own tax rate.

**Rules out**: a configuration surface at every level, and the drift that follows.

### Authorisation follows the user, not the device

*ADR-0002.* A person logs in anywhere and carries their access. **Rules out**: a workstation that
is a permission, and the shared login that always follows.

---

## Money

### Money carries its own scale

*ADR-0008.* `{ amount, currency, scale }` at every layer. **Rules out**: assuming two decimals,
which is wrong for KWD and BHD before it is wrong anywhere else.

### Approve, then gateway, then cancel the entitlement — never the reverse

*`states/refund.yaml`.* A refund that cancels first and fails at the gateway leaves a guest with
no ticket and no money, **and they will be at a gate rather than on a phone.**

### The guest's money does not stop being theirs

`closeWallet` refuses where a balance remains and no settlement is given. A closed account is not
a forfeited one.

### A preview computes; it does not mutate

Three operations violated this on 17 August — `previewAllocationSplit`, `previewSubscriptionChange`
and `evaluatePromotions` all showed writes. **Nine operations now carry `isComputation`.**

### Retrying an unknown charge is how a guest is charged twice

*`states/payment.yaml`.* `pendingConfirmation` inquires with the gateway; it never retries. **The
second charge is discovered by the guest, not by us.**

---

## Failure

### Degrade, never stop

*CF-61, extended to AI spend in CF-14.*

A `pastDue` subscription keeps serving. The AI ceiling warns and the assistant keeps answering.
**A closed gate over an unpaid invoice is worse than the unpaid invoice**, and a cap that stops
mid-visit turns a cost control into a guest-facing outage the venue had no warning of.

**Rules out**: any automatic termination. Ending a service is a decision with a person behind it.

### Local-first: one read path, always local

*ADR-0013.* Not an online path with an offline fallback — **the same path either way**, so the
offline case is exercised constantly rather than on the day the network fails.

### Different data classes need different offline strategies

*ADR-0013.* Catalogue and configuration replicate; contended inventory takes leases; transactions
journal locally and sync idempotently. **Three answers, not one** — and finding that was what dissolved the online-versus-offline argument rather than
settling it.

### An event with no critical consumer should say why

Four events were missing one on 17 August. `access.validated` releases a held queue slot, so
losing it **leaks capacity**; `fnb.orderReady` means a guest never learns their food is ready,
with no recovery path. Three others are correctly non-critical and now record the reasoning.

---

## Data

### Derived, not listed

Domain membership, navigation graphs, screen indexes, the AI page. **Anything hand-typed drifts** —
`ai-index.md` drifted four times in a single day before it was replaced by a closure over the
contracts.

**Rules out**: a register maintained in parallel with the thing it describes.

### Append where the design allows it

62 operations. **Facts do not collide**, which is what makes offline work at all — a steward
scanning two hundred tickets offline is adding two hundred facts, not competing with anybody.

Most hard offline cases were solved by turning them into this.

### A vocabulary with no written definition drifts

`lastWriteWins` and `lastWriterWins` coexisted on 17 August — one policy, two spellings, ten
operations split between them, **and every checker passed because each value was individually
plausible.** Closed sets are now enforced for conflict policy, scope level, read routing, auth and
ADR status.

### Standards first, adaptors second, vendors last

*ADR-0012, ADR-0015.* ESC/POS and UnifiedPOS before a driver; a queue adaptor before a queue
vendor. **Rules out**: a vendor decision embedded where a capability belongs.

---

## Method

### The contract is the deliverable

*ADR-0024.* Requirement → contract → schema → screen → flow → build, and **an artefact may not
reference something that does not exist.** Seven validators enforce that.

It has found: a cart that did not exist, a gift card that could be issued and blocked but never
activated or redeemed, an inter-entity obligation that could be listed and never settled, and
`updateWorkOrder` doing six jobs so no audit could say which action caused which state change.

**The cost is stated honestly in the ADR**: seven weeks and nothing runs.

### Wrong framing is worse than a hard choice

The offline question, the Qdrant question and CF-99 all dissolved when the framing changed rather
than being settled as posed. **Online-versus-offline was the wrong question** — different data
classes need different strategies. **Collection-versus-payload was the wrong question** — the
split criterion is the embedding model. **Handover was the wrong question** — a conversation is
not a case.

### A label nobody reads is not a control

Three separate labels said ADR-0001 (retired — see ADR-0014 and ADR-0017)'s decision no longer held, and it was built on anyway. **The
fix was not a fourth label** — it was a checker that fails any ADR citing a superseded one without
naming the supersession.

### Find the defect, not just the task

Every session-level instruction here has been short. The work that mattered was usually adjacent
to it: checking whether CF-100 was a blocker found eight flows stepping through later-wave
screens; adding an AI cap found that nothing joined the meter to an invoice.

---

## The six corrections

These were wrong first, which is why they are the load-bearing ones.

| | Was | Is |
|---|---|---|
| **Qdrant partitioning** | Collection per tenant | One collection per model, tenant is the shard *(twice corrected)* |
| **Configuration floor** | Configurable at every level | Venue is the floor |
| **Offline architecture** | Online-primary with offline fallback | Three data classes, three strategies |
| **Cell tenancy** | A cell holds one tenant | True of dedicated placement only |
| **AI scope** | Guest assistant deferred | In Phase 1, bounded and capped |
| **Support conversations** | A case | A live session that may create one |
