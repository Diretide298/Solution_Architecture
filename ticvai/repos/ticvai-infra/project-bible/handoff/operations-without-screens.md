# Operations no screen consumes

**Decided 20 September 2026. This exists so the question stops being re-asked.**

`link-screens-contracts` prints *"N operations have no screen consuming them"* on every refresh.
The number has been read as a design backlog at least three times, and it is not one: **on 20
September, 105 of 257 needed no screen and 152 did.** Without a recorded answer the whole 257
gets re-litigated, and the re-litigation reaches the same five conclusions each time.

This is the companion to [`schema-storage-only.md`](schema-storage-only.md), which does the same
job for tables that deliberately have no API. `tools/audit-screenless-operations.py` applies the
rules below and reports only what is left.

---

## Five reasons an operation legitimately has no screen

### 1 · A write reached from the screen its sibling read feeds — **the largest group**

`setJobTitle` is a PUT on `/job-titles`; `listJobTitles` is the GET, and it is consumed by the
screen that shows the list. **The button that calls the PUT is on that screen.**

The linker matches a screen to the operations it *reads*, because that is what a screen
specification names. A write beside a screened read looks uncovered and is not.

> **Only writes are excused this way.** A *read* beside a screened read is usually a detail view,
> and a detail view is a screen. `getRentalAgreement` beside `listRentalAgreements` needs one.

### 2 · It runs inside hardware — the device is the interface

A turnstile runs a thick client that validates a scan locally and syncs afterwards. A queue
sensor submits a reading. A signage panel pulls the board it displays. **Drawing a wireframe for
these would describe a screen nobody builds**, and the firmware is specified by the device
integration rather than by a board.

Declared by `x-ticvai-audience: [device]`.

> Most device-facing operations are *not* in this group, and that is correct. `listScans` and
> `syncScans` are called by the turnstile client and by fifteen staff screens — the turnstile
> having no screen does not mean the operation has none.

### 3 · Machine to machine

`service` or `anonymous` audience only: webhooks, provider callbacks, health and readiness.
Nobody is looking at the response.

### 4 · One cell calling another

The caller is a service in another cell. The screen that started the journey belongs to whichever
cell the person is actually in, and it is already counted there.

### 5 · A job, however it is triggered

`x-ticvai-singleton: true` — a period close, an FX revaluation, a synchronisation run. A person
may press something to start it, and that button lives on a screen that reads its *result*; the
job itself is not a surface.

---

## How to record a case none of these five covers

Put it on the operation:

```yaml
      x-ticvai-no-screen: >
        why this one has no design surface
```

**On the operation rather than in a list here**, so that an operation which moves to another
contract takes its reason with it. `derive-lineage` learned that the hard way with `service`:
fifteen operations moved contract and kept a stale value because the record lived apart from the
thing it described.

---

## What this does not excuse

**152 operations did need a screen on 20 September** and that number is a real backlog. Roughly
forty of them are the operations written that same day — loyalty rules, membership, the workforce
integration console, dynamic pricing, rental agreements — and a new operation with no screen is
expected for exactly as long as it takes to specify one.

The rest are older, and the largest clusters are worth naming because they are features rather
than gaps:

| Contract | Resource | Why it is a real screen |
|---|---|---|
| `subscription` | `/burst-environments` | five operations to stand up, drain, reconcile and decommission temporary capacity, and no page showing what is running or what it costs |
| `subscription` | `/tenant-migrations` | plan, apply, roll back — a migration nobody can watch |
| `tenancy` | `/device-firmware` | a rollout with no rollout screen |
| `catalogue` | `/entitlements` | suspend, freeze and reinstate a guest's pass, from nowhere |
| `ai` | `/index-sources` | what the assistant has indexed |

**A screen backlog is useful and a screen backlog inflated by 105 false entries is not**, which
is the whole reason for this file.
