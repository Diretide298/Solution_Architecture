# ADR-0013: Local-First Point of Sale

**Status:** Accepted
**Date:** 13 August 2026
**Closes:** CF-15
**Withdraws:** the 31 July middle-ground proposal
**Constrains:** Order & Payment spine · Product & Entitlement spine · offline-core · venue edge

---

## Context

CF-15 was framed as *online-first versus offline-first catalogue*. The framing was wrong.
The real question is **how many read paths the transaction path maintains**, and the answer
determines everything else.

Three positions were on the table:

| Position | Outcome |
|---|---|
| Online-first, offline as fallback | **Rejected** |
| Middle ground — online when available, local when not | **Withdrawn** |
| Local-first, unconditionally | **Accepted** |

## Decision

**Local-first. One read path, always local, online or offline.**

### 1. Catalogue reads are always local

Products, prices, tax rules, promotions and configuration are read from **local SQLite on
every transaction, unconditionally**. Never fetched on the transaction path — not as a
fallback, not as a preference, not when the network happens to be good.

| Consequence | |
|---|---|
| **One code path** | No second implementation to keep correct |
| **Sub-millisecond reads** | No network variance in the sale loop |
| **Continuously exercised** | The offline path is the only path, so it cannot rot undetected |

The last point is the decisive one. A fallback path that runs 2% of the time is a path
nobody trusts and nobody tests properly. Making it the only path removes the failure mode
entirely.

The server publishes **signed, versioned bundles**; the terminal applies deltas atomically.
A bundle is either fully applied or not applied — a terminal never trades against a
half-updated catalogue.

### 2. Contended inventory uses leases, not replication

Seats, timed capacity and retail stock cannot be replicated — two terminals would sell the
same unit.

**Leases** formalise the 5 August position that a node holds a working allocation:

| Property | |
|---|---|
| Grant | A terminal or edge node holds N units for a TTL |
| Return | Unsold units return automatically on TTL expiry or explicit release |
| Renewal | Extended while the link is up and the allocation is being consumed |
| Exhaustion | Terminal refuses the sale rather than overselling |

**Seated inventory stays blocked offline**, as ratified. A seat map is not a count, and a
lease over specific seats at a gate is not worth the complexity.

### 3. Transactions are journalled locally, then synced

| Step | |
|---|---|
| 1 | Write to a local **write-ahead journal** |
| 2 | **Commit before the cashier is acknowledged.** The guest-app is not waiting on a network |
| 3 | Idempotent, ordered sync on reconnect — the existing outbox |
| 4 | **Server re-prices every line on ingest** |

Step 4 is the integrity guarantee. The local price gives the guest-app an immediate, correct
answer; the server remains authoritative for the ledger.

### 4. Deployment profiles — configuration, not architecture

"Let clients choose" is rejected as architecture and granted as configuration. **Three
profiles, one codebase:**

| Profile | Fits | Catalogue | Leases | Edge node |
|---|---|---|---|---|
| **Terminal-local** | Small venues, single-counter sites, 4G-connected pop-ups | Local SQLite per terminal | Direct from cell | No |
| **Venue edge** | Mid and large venues, stadium gates | Local per terminal, distributed via edge | Held by edge, sub-leased to terminals | **Yes** |
| **Thin** | Back office, B2C web, call centre — non-transactional surfaces | None. Server reads | N/A | No |

The venue edge profile turns **WAN-down-LAN-up** — the common failure — into a fully
working venue rather than a degraded one. It is also the only coherent implementation of the
network zoning the client asked for.

### 5. What was rejected, and why

**Online-first.** Fails four requirements outright — 2.3.1, 2.14.2, 4.3.4 and 3.2.x offline
gate validation — and fails at peak load precisely when a queue is watching.

**The 31 July middle ground.** Pays the full cost of offline-first *and* maintains a second
read path that is exercised rarely enough to be untrustworthy. Strictly worse than either
pure position.

## Cost

| Approach | Relative build effort |
|---|---|
| Online-first | 1.0× |
| **Local-first** | **~2.2×** |
| Bare local-first without profiles or edge | ~1.7× |

The premium is what makes 4G-connected sites and stadium gates viable at all. It is not
paid for robustness in the abstract — it is paid for two specific deployment classes that
otherwise cannot be served.

---

## Consequences — New Subsystems

Three things this decision creates that did not previously exist as scope.

### C102 — Catalogue bundle publication

Server-side: compute a bundle from current catalogue state, version it, **sign it**,
compute deltas against prior versions, publish.

Client-side: verify signature, apply delta atomically, roll back on failure, report applied
version.

| Open | |
|---|---|
| Signing key custody | Per cell, in the cell key vault. Rotation policy needed |
| Stale-key handling | A terminal offline across a rotation cannot verify. Needs a grace window |
| Bundle size | Full catalogue for a large venue may be substantial. Delta strategy matters |

**Settled for the first release (20 October 2026, r8 cause FOUNDATION-AI-C14):** the bundle is signed with
**Ed25519 over its `contentHash`**; the public keys are served by `catalogue.getBundleSigningKeys`, and a retired
key stays verifiable for a **7-day grace** so a terminal offline across a rotation still verifies. The signing key
lives in the cell's Key Vault (ADR-0063). A bundle that does not verify is refused whole.

### C103 — Inventory lease management

Grant, renew, release, expire, reconcile. Server-side allocation ledger; client-side held
lease with a countdown.

| Open | |
|---|---|
| **Lease stranding** | A terminal that dies holding a lease strands capacity until TTL. At a gate during peak that is visible. Short TTLs with aggressive renewal, or an operator-triggered force-release? |
| Sub-leasing | Edge node holds a venue lease and sub-leases to terminals. Two-level TTLs |
| Oversell tolerance | Is any oversell acceptable, or is exhaustion always a hard refusal? |

**Settled for the first release (20 October 2026, r8 causes FOUNDATION-AI-C45, GPS-C37, FOUNDATION-AI-C46):**
**Block A takes no standing lease.** Contended timed entry is online-only at the till: offline, the sale drawer
refuses it and says it needs a connection; the cart's hold, taken online by `addCartLine`, is the only hold.
**Oversell:** an offline sale replayed after the hold it relied on expired is **accepted and flagged `unitsGone`**
for the reconciler, never dropped and never silently counted; exhaustion online is still a hard refusal. Lease
stranding and sub-leasing return with standing leases, not before.

### C104 — Catalogue staleness policy

A terminal offline for an hour is fine. A terminal offline for a week is selling last
month's prices.

**There must be a bound.** Beyond it the terminal refuses to trade rather than transacting
against stale data.

| Open | |
|---|---|
| The bound itself | Per tenant? Per product class? Prices and promotions age differently from product definitions |
| Behaviour at the bound | Hard refusal, or cash-only degraded mode, or supervisor override? |

---

## The Open Item That Matters Most

**Server re-prices on ingest. What happens when it disagrees?**

The guest-app was quoted and charged a local price. The server computes a different one — a
promotion expired, a price list changed, a tax rule updated between bundle and sync.

| Option | Consequence |
|---|---|
| **Honour the quoted price** | Guest experience intact. Ledger records a variance against list. Requires a variance account and a reporting line |
| Reject the transaction | Unacceptable — the guest-app has left with the ticket |
| Post the server price | The guest-app was charged one amount and the ledger says another. Reconciliation nightmare |

**Recommendation: honour the quoted price, post the variance.** The guest-app transaction is
already complete and irreversible; the ledger's job is to record what happened, not what
should have happened.

But that means:

- A **price variance account** in the chart of accounts
- A variance report so drift is visible rather than silent
- A **threshold** above which a variance is an exception requiring review, not a posting

This is a **commercial decision, not a technical one**, and it lands in Finance & Ledger —
the next context to be contracted. It should be settled before those contracts are drafted.

Raised as **CF-38**.

---

## Amendment — 13 August 2026: channel allocation

The Phase 1 screen hierarchy (2 August) carries **P08-047 Channel Inventory Allocation**,
noted as *"new scope — channel-based offline inventory pooling. Design not yet agreed."*

That note is now stale, and the apparent conflict dissolves once the two ideas are
separated:

| | Channel allocation | Lease |
|---|---|---|
| Concern | **Commercial** — how much capacity each channel may sell | **Technical** — how a node holds units safely offline |
| Set by | Revenue management, per performance | Requested by a terminal at point of sale |
| Lifetime | The selling window | Seconds to minutes, with a TTL |
| Granularity | Channel: web, POS, OTA, B2B, kiosk | Terminal or venue edge node |
| Failure mode | Channel exhausted — nothing left to sell through that route | Lease expired — units return to the pool |

**They compose. Allocation is the pool a lease draws from.**

A lease is granted against a channel allocation rather than against raw envelope capacity.
The terminal asks for ten units, the lease manager checks the POS channel's remaining
allocation, and grants from it. Web cannot consume the counter allocation, and an offline
terminal cannot oversell a channel it was never given.

This is what the 5 August "100 tickets per node" position meant in practice, and it is why
the two artefacts describe one design rather than two.

### Consequences

- `Envelope` gains channel allocations. `AcquireLeaseRequest` gains an optional channel;
  the session's channel is used when it is omitted
- Availability is reported **per channel**, not only in total. A guest-app seeing "sold out"
  online while seats remain at the counter is correct behaviour, not a defect
- Unsold channel allocation may be released back to a general pool at a configured time
  before the performance — the standard mechanism for freeing OTA holds close to the event
- **P08-047's design question is closed.** The screen remains; its note should be updated

---

## Consequences — Existing Artefacts

| Artefact | Change |
|---|---|
| `x-ticvai-offline-capable` | Semantics sharpen. For **reads** it is now always true on transactional surfaces — catalogue is local by definition. For **writes** it retains its current meaning |
| `offline-core` | Gains bundle application and lease handling alongside the outbox |
| Venue edge node | Promoted from an availability nicety to a **deployment profile** with defined responsibilities |
| Access control | Unaffected. Already local-first with the offline package — this decision generalises that pattern to the catalogue |
| Retail | Still blocked offline. Real-time inventory depletion is a lease problem, and retail stock leases are Wave 2 |
| Seated inventory | Still blocked offline, as ratified |

---

## Note

This decision makes the platform's read path uniform: **access control already worked this
way** — local package, local evaluation, sync on reconnect. Local-first for the catalogue
means the two highest-frequency operations in the venue, selling and validating, now share
one architectural pattern rather than two.

That uniformity is worth more than the effort premium suggests, because it is one pattern
to test, one to debug at 2am, and one to explain to a new engineer.
---

## Amendment — 3 November 2026: an offline supervisor step-up is checked by the till's offline verifier and re-checked at sync (Chinmay, CHG-R14V-001)

**Decided by Chinmay, 3 November 2026, on system review finding F-01: "Offline verifier" (the till keeps a
verifier, re-checked at sync).** The review of the r13 tag found three operations that are offline-capable and
take a same-device PIN step-up (`voidOrder`, `recordNoSale`, `withdrawFromDepositBox`), a step-up only the server
could check (`SupervisorStepUp`, `identity.verifySupervisorStepUp`), a picker that was online only
(`listStepUpSupervisors`), and two contradictory answers in the contracts: the void and the no-sale said "offline
only a caller who holds the permission can do this", the withdrawal queued the witness's PIN unchecked and let the
cash leave the box. The till's approved screens promise it keeps working offline (POS-014, POS-018).

**The decision.**

1. **The offline package carries a verifier per eligible signer and venue.** Identity keeps one
   `identity.offline_pin_verifier` row per principal and venue: an Argon2id PHC string over the PIN with its own
   salt, **never the PIN** and never the server's peppered credential hash, stored encrypted with the tenant's field
   key (ADR-0063). Identity never holds a PIN, so a verifier is minted only where it has just checked one itself: a
   correct `pin` sign-in (`login`), a correct online step-up (`verifySupervisorStepUp`) and a new PIN
   (`changeOwnCredential`), for the venue the PIN was used at and every venue where the principal holds an offline
   step-up permission. A verifier expires 30 days after it was minted and stops counting at once when the PIN is
   changed or reset, while it is locked, or when the principal is deactivated or loses the permission.
2. **The till fetches its package with its own device credential** (`getOfflineStepUpPackage`, `deviceAuth`):
   the signers of its venue, by display name, with the offline step-up permissions each holds there and whether
   they may witness (a shift open at the venue), each with its verifier. The package expires 24 hours after it was
   issued; the till fetches a new one after every sync and at least hourly while online, and **replaces it
   whole, so a verifier revoked on the server is gone from the till at its next sync.** It is kept only in the
   device's encrypted local store.
3. **Offline, the prompt works from the package** (`supervisorPinPrompt`'s `offline` state): the local picker
   offers the signers who hold the act's permission (or may witness), the signed-in person left out; the typed PIN
   is checked against the signer's verifier on the till; **the local attempt limit is the tenant's
   `pinLockoutAfterAttempts`**, after which that signer is locked on that till until it reconnects. With no package,
   or after it expires, the step-up needs a connection.
4. **Every offline step-up is recorded and re-verified at sync.** The queued call carries the step-up as online
   (the PIN sealed in the encrypted outbox and deleted from it once synced) plus its `offline` evidence (package,
   verifier, when it matched, the wrong PINs before it). At sync Identity re-checks it **as at the act's
   `recordedAt`**: the PIN against the PIN credential in force then, the verifier (for that venue, not expired or
   revoked then), the signer active and holding the permission there then, and not the caller. The result is one
   `identity.offline_step_up` row, `confirmed` or `refusedAtSync` with its reason. A wrong PIN found at sync is not
   a new attempt and does not count towards the server's lockout.
5. **The rejection path is named, and it never drops the act.** The void, the no-sale or the withdrawal happened
   at the till (the drawer opened, the cash left the box), so a `refusedAtSync` act is recorded as sent, as an
   offline sale replayed after its hold expired is accepted and flagged `unitsGone` (C103 above), never dropped and
   never silently counted. Its success response carries `X-Ticvai-Step-Up-Verdict: refusedAtSync`; **the operator**
   sees, once, "Supervisor approval for <the act> was not confirmed when the till synced. The venue manager has been
   told."; Identity publishes `identity.offlineStepUpRefused`, and **the supervisor's managers at the venue** see the
   alert reporting raises from it on Shift Exceptions & Alerts (POS-020) and Offline Alerts, Limits & Audit
   (BO-133) until it is acknowledged.
6. **Each offline-capable step-up operation declares its offline step-up behaviour**:
   `x-ticvai-offline-step-up: verifier` (this amendment) or `refused` (the act needs a connection, and its
   `x-ticvai-offline-note` says so). An MFA or rule-dependent step-up can only be `refused`: its factor is checked by
   the server. `tools/check-step-up.py` (SU-OFFLINE) fails an operation that declares neither.

**What it does not change.** Online, a failed step-up is still `403 supervisor-step-up-refused` and nothing is
written. A cashier who holds the act's permission still acts alone, offline as online. An escalated permission
(`x-ticvai-permission-escalated`, as on `compItem` and `cancelFnbOrder`) is the caller's own permission, resolved at
sign-in and held by the till; it involves no supervisor and no verifier. Sign-in itself still needs the network
(identity `login`, CHG-R8SPN-027).

**The cost, stated.** A 4-digit PIN has 10,000 values, so a verifier taken from a stolen, unlocked till can be
reversed offline (ADR-0071's context). The server-side copy is encrypted and the package is served only to a
registered device, so the exposure is one venue's signers for at most 24 hours from one device, and every PIN
checked offline is checked again by the server at sync. ADR-0071, as amended 3 November 2026, records the exception.
