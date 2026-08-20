# Gotchas

> **Purpose:** Things that will bite you  
> **Owner:** Everyone  
> **Status:** Living


Append as found. Symptom first, then cause.

---

### RLS looks enabled but does nothing

`ENABLE ROW LEVEL SECURITY` alone does not apply to the table **owner**. If the application role owns the table, every policy is bypassed — and it reviews clean.

**Always `ALTER TABLE ... FORCE ROW LEVEL SECURITY`.** Asserted monthly in runbooks/restore-drill step 6.

### Money silently truncates in Oman

`decimal(18,2)` looks obviously right. OMR uses **3 decimal places**. Every Omani transaction loses a digit, the ledger is append-only, and corrections are new entries rather than edits.

Use `Money` — `{amount, currency, scale}` — and `numeric(18,4)` in SQL.

### Revenue reported against the wrong day

`recorded_at` is when the **device** recorded it. `synced_at` is when the server received it. `created_at` is when the row was written. For an offline sale on the night of the 31st that syncs on the 1st, these are three different dates.

Reporting on the wrong column misstates revenue by trading day.

### Ticket ID is not the Media Code

A ticket can be re-linked to new media over its life. The Media Code changes; the Ticket ID does not. Any code treating them as one field is wrong. Settled 07 Aug 2026.

### Order, Reservation and Ticket are three things

Three entities, three lifecycles. A Reservation is unpaid and expires. An Order posts to the ledger. A Ticket is the instrument. See [glossary](glossary.md).

### A supervisor sees a button that 403s

Frontend spelled the permission `ORDERS.REFUND.APPROVE`, backend enforces `ORDER_REFUND_APPROVE`. Invisible in code review, obvious in production.

**Permission strings are generated from one enum in `ticvai-contracts`.** Never hand-typed.

### A valid ticket is refused at the gate

Sold at the front gate, guest-app walks 20 metres, scans. Validation read a lagging replica.

**Access validation reads the primary unconditionally.** Everything else carries `X-Consistency-Token`.

### The matrix sheet name has a trailing space

`'Funactionality '`. Any programmatic access must account for it.

### Requirement IDs 5.6.1–5.6.8 appear twice

Different text, same IDs. 46 rows, 38 unique IDs in the Virtual Queue sub-domain. Citations to those IDs are ambiguous — quote the text.

### Two different things are called "queue management"

**Q1** Virtual Queue — ride queues, third-party sensor fed. **Q2** Virtual Waiting Room — traffic throttling at on-sale, in-house, zero matrix requirements. The MoM record conflates them. See [CF-33](registers/conflicts.md).

### A void arrives before the sale it voids

Outbox drain must be **strictly sequential per device**. Skipping a failed entry to keep the batch moving means the server rejects the dependent operation and the device retries forever.

`SyncOrchestrator` halts the batch on failure by design.

### The whole venue retries at once

Network blips, every terminal reconnects and retries simultaneously, recreating the outage.

Backoff is **jittered**.

### A month-end report takes down a tenant

Reporting query hits the primary during a venue spike. Reporting has its own lag-tolerant replica and the `ticvai_reporting` role has no access to primary or OLTP replicas.

### Connections exhaust before CPU does

Naive maths: tenants × services × pods × pool size runs to thousands. Postgres degrades past a few hundred.

**PgBouncer in transaction mode is mandatory**, with per-service pool caps.

### An architecture test that cannot fail

`NetArchTest` resolves **type** dependencies only. A rule written against `System.DateTime.Now` silently passes and gives false assurance.

Member-level bans go in `BannedSymbols.txt` with `BannedApiAnalyzers` — compile-time.

### Brace expansion in `sh`

`/bin/sh` is dash in most containers. `mkdir -p src/{a,b,c}` creates one directory literally named `{a,b,c}`. Use `bash` or explicit paths.
