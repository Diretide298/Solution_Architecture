# Audit register

**134 requirements ask for something to be audited, and nothing listed what.**

The answer is not a list of 134 items. **Every operation that writes is auditable**, and the
register's job is to say what is recorded, for how long, and which subset needs more than the
default.

## The default

**All 431 write operations produce an audit record.** Not a design choice per operation —
the platform records who, what, when, from where and under which permission for every state
change, because deciding per operation is how something gets missed.

| Field | Source |
|---|---|
| Principal, and delegate where one acted | `identity.session` |
| Scope path | The session, never the request |
| Permission exercised | Resolved at the call |
| Operation and idempotency key | The request |
| Before and after | The state model transition |
| Workstation and device | Where the session carries one |
| Occurred and recorded time | **Both** — an offline action happened when it happened |

**`occurredAt` and `recordedAt` are both kept everywhere**, because an offline scan, clock-in or
journal entry is evidence of when it happened, not when it synced.

## Where the default is not enough

| | Why | Beyond the default |
|---|---|---|
| **Money** — payments, refunds, journals, period close | Regulated and disputed | The reversal chain, and the approval that permitted it |
| **Access** — scans, overrides, blacklist | A person was let in or refused | The offline bundle version the decision was made against |
| **PII** — profile reads, DSAR, erasure | PDPL | **The read is audited, not just the write.** Who looked at a passport number is the question a regulator asks |
| **Permissions** — grants, roles, delegation | Escalation path | The prior grant, so a widening is visible as a widening |
| **AI** — prompts, responses, proposals | 8.3.55–8.3.57 | Prompt, response, sources, model, tokens, and whether a proposal was applied or refused |
| **Approvals** | Evidence | Immutable once complete. Reopening creates a new record linked to the old |
| **Configuration** | Silent blast radius | The level it was set at, because a tenant-level change reaches every venue |

**Reads are audited in exactly one place: PII.** Auditing every read would produce a log nobody
can search and a bill nobody predicted; auditing none of them fails the one question a
regulator actually asks.

## What is still missing

| | |
|---|---|
| **Retention** | **CF-64.** An audit trail with no retention period is a table that grows until someone notices |
| **Tamper evidence** | 11.1.62 asks for detection. Append-only plus a hash chain is the usual answer and nobody has decided |
| **Export format** | 11.1.55 asks for records suitable for a regulatory audit. Which regulator, and in what shape |
| **The `audit` table itself** | Not in the 267. `platform.outbox` carries events; an audit record is not an event and needs its own home |

**The last one is the actionable gap.** Everything above describes a table that does not exist.
