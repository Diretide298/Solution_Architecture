# ADR-0022 — Conflict policy is declared per operation, from a closed set of four

**Status:** Accepted · 17 August 2026, recording a decision already implemented
**Relates to:** ADR-0013 (local-first POS — replication, leases and the local journal), ADR-0016
(read/write separation)

---

## Why this is written late

**Every one of the 755 operations already carries `x-ticvai-conflict-policy`.** The decision was
made in practice, applied consistently, and never recorded — so the taxonomy existed only as a
pattern somebody would have to infer by reading contracts.

That gap produced a real defect. On 17 August, **`lastWriteWins` and `lastWriterWins` were both
in use** — one policy, two spellings, ten operations split between them. Every checker passed,
because each value was individually plausible and nothing said what the set was.

**A vocabulary with no written definition is a vocabulary that drifts.**

---

## Context

The platform is offline-capable at the edge. A POS journals locally and replays through
`/sync/orders`; a scanner validates from a bundle and syncs a journal; a technician pauses a work
order in a plant room with no signal.

**Two writers can therefore act on the same record without seeing each other**, and something has
to decide what happens when they meet. Deciding that per operation rather than globally is the
whole point: a cash count and a work order note fail differently, and a single platform-wide
rule would be wrong for one of them.

---

## Decision

**Four policies. The set is closed, and `check-package.py` enforces it.**

### `serverWins` — 701 operations

**The default, and the right default.** The server's version stands; the client's write is
rejected and the client re-reads.

Correct wherever the server holds authority the client cannot have: pricing, availability,
permissions, configuration, anything that resolves up a scope tree. **A till that has been
offline for an hour does not know that a price changed**, and letting its version win would sell
at a price nobody set.

### `append` — 64 operations

**No conflict is possible because nothing is overwritten.** Scan events, journal entries, audit
records, attendance, cash count lines, media attachments.

This is the policy that makes offline work at all. A steward who scans two hundred tickets
offline is not in conflict with anybody — they are adding two hundred facts, and facts do not
collide. **Where a design can be made append-only it should be**, and most of the hard offline
cases were solved by turning them into this.

### `lastWriterWins` — 11 operations

**Deliberately rare, and every use is a small mutable annotation.** Accepting a work order,
pausing it, requesting a bill, seating a table, holding an order.

The test is: **if two people do this and one silently overwrites the other, is anything lost?**
For "this table asked for the bill" the answer is no — the later signal is the true one. For
anything carrying a number, the answer is yes, and it is not this policy.

### `manualMerge` — 0 operations

**Declared and unused, which is intentional.** It exists so that a case demanding a human
decision has somewhere to be declared rather than being forced into `serverWins` and silently
losing a write.

**If it stays empty at go-live that is a good outcome**, not an unused feature. The moment it is
needed is the moment somebody would otherwise have picked the wrong policy.

---

## What this is not

**It is not the offline data model.** **ADR-0013** settles what may be held offline and how:
catalogue and configuration are replicated, contended inventory takes leases, and transactions are
journalled locally then synced.

*(This paragraph cited ADR-0011 until 17 August, which is The Hierarchy Is Binding and says
nothing about offline. Two Accepted ADRs rested on a document that does not contain what they
attributed to it — found by an external audit, not by any checker here.)* **This decides what happens when a write
arrives, not whether the write was allowed to be made offline.** The two are independent: an
online-only operation still declares a conflict policy, because two staff at two workstations
can still collide.

**It is not idempotency.** Every write carries an idempotency key so a *retry* is safe. Conflict
policy handles two *different* writes. Ninety-three operations were missing the key on 17 August
and that was a separate defect.

---

## Consequences

**A reviewer can see the decision without reading the implementation.** `serverWins` on a
pricing operation and `append` on a scan are both visible in the contract, and a wrong one is
visible too.

**The client can be generated from it.** An offline queue that knows an operation is `append`
never needs to reconcile it; one that knows an operation is `serverWins` must re-read on
rejection and tell the user.

**`lastWriterWins` should be reviewed whenever it grows, and it has.** It said ten was defensible
and it is eleven — `setAgentAvailability`, added with the conversation contract, where the later
signal genuinely is the true one and nothing is lost.

**The trigger fired and nobody noticed**, which is the useful part: a review threshold written
into prose is a threshold nobody checks. Thirty would mean the policy had become a way of avoiding
a decision, and the question is always the same — what is lost when one write overwrites the
other.

**The vocabulary is now enforced.** Adding a fifth policy means changing the closed set in
`check-package.py`, which is a deliberate act rather than a typo that spreads.
