# ADR-0033: Every asynchronous handoff has an outbox and a place to fail

**Status:** Accepted
**Date:** 31 August 2026
**Related:** [ADR-0013](0013-local-first-point-of-sale.md) · [ADR-0032](0032-load-shedding-and-pooling.md) · CF-165

---

## Context

**`platform.outbox` exists and one operation writes it.** Its own note says why it works —
*"written in the same transaction as the state change, by the platform, not by an operation; that
is what makes it exactly-once"* — and then twenty-nine events are emitted across the package with
no stated delivery mechanism.

**`sync.rejection` exists and covers one path.** An offline record the server refused, kept because
*a till that loses a rejected sale silently is worse than one that reports it.* **That reasoning is
correct and it applies to every asynchronous handoff in the platform, not only to a till.**

**What has no failure home today**: `message_dispatch` to a provider that is down, an outbox row
whose consumer keeps throwing, a webhook to a partner endpoint that has moved, an index job whose
document will not parse.

---

## Decision

### The outbox carries every event, not one

**A state change that must reach anything outside its own transaction writes an outbox row in that
transaction.** All twenty-nine declared events.

**Not a queue write inside a transaction.** A message broker acknowledging a publish that then
rolls back is the exactly-once problem restated — **the row and the state change commit together or
neither does.**

**A relay reads the outbox and publishes.** At-least-once to the broker, and the consumer is
idempotent because every write in this platform already carries an idempotency key. **660
operations do; the mechanism is there.**

### Failure is a row somebody works, not a log line

**Three tables, one pattern.**

`sync.rejection` — an offline record the server refused **on its merits**. Already exists. **A 429 is
not a rejection**; the till retries.

`platform.dead_letter` — an outbox row whose delivery failed after its retry budget. **Carries the
payload, the attempt count, the last error and the consumer that failed**, because a dead letter
you cannot replay is a log entry with a table's overhead.

`ai.index_failure` — a document that would not chunk, embed or parse. `ai.index_job` already counts
`records_failed` and holds a `failure_sample`; **this is where the other 4,999 go.**

### Retry is bounded, backed off and jittered

**Five attempts, exponential from one second, jittered.** Then dead-letter.

**Jitter for the reason in ADR-0032** (whose pooling half is amended by ADR-0038, and this is not the amended half): a thousand failures at the same instant retry at the same
instant, and the retry is the second outage.

**A dead letter is replayable by an operator.** `replayDeadLetter` takes an id, re-enters the
delivery path, and **records the replay as a new attempt rather than resetting the count** — an
operator retrying the same poison message forty times should be able to see that they did.

### What must not be dead-lettered

**A financial posting.** `ledger.journal_entry` is append-only and a failed posting is an incident,
not a queue item. **It halts and alerts.**

**A DSAR.** `platform.dsar_request` carries a legal clock. A dead-lettered erasure that nobody works
is a regulatory failure with a timestamp on it.

**Both raise an alert and stop.** The distinction is whether silent accumulation is acceptable, and
for those two it never is.

---

## Consequences

**A relay process per cell** — one more thing to deploy, monitor and reason about at 6 a.m.

**Three failure tables somebody has to actually work.** A dead-letter table nobody reads is worse
than no table, because it converts a visible outage into an invisible backlog. **The dashboard for
these is a screen the package does not have yet.**

**🔴 CF-165 is adjacent and still open.** Retention and archival are absent, and dead-letter rows
are exactly the kind of data that accumulates forever unless something says otherwise. **These
tables need a retention rule the moment they exist.**

---

## Alternatives considered

**Publish directly from the operation.** Rejected: the broker acknowledges and the transaction rolls
back, or the reverse. **That is the bug the outbox exists to prevent.**

**Change data capture instead of an outbox.** Genuinely tempting — no application code, no relay —
and rejected for one reason: **CDC publishes what changed, not what happened.** `order.paid` and
`order.refunded` can be the same column change, and the consumer would have to reconstruct
intent from a diff.

**One shared dead-letter table.** Rejected: sync, delivery and indexing failures are worked by
different people with different urgency, and one table sorts them into a filter nobody applies.
