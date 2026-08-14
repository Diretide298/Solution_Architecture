# ADR-0012: Queue Integration — Adaptor-First, Vendor Deferred

**Status:** Accepted (partial — vendor selection deferred)
**Date:** 13 August 2026
**Partially closes:** CF-33

---

## Context

Three distinct systems have been called "queue management", and the MoM record conflates
two of them:

| | System | What it is | Reqs |
|---|---|---|---|
| **Q1** | **Virtual Queue** | Ride and attraction queues, Fast Pass, live wait times, reservations, no-shows | 46 |
| **Q2** | **Virtual Waiting Room** | Traffic throttling at on-sale — branded queue page above a concurrency threshold, batched release | **0 in matrix** |
| **Q3** | Chat queues | Agent assignment in the support inbox | 2 |

31 Jul recorded *"built-in queue management will be developed in-house rather than sourced
from a third party"* — in context, about throttling traffic from the back office, i.e. Q2.

10 Aug recorded that live wait times *"typically depend on a third-party camera/sensor
system at the venue"*, with TICVAI exposing a standard API — i.e. Q1, third-party fed.

As written the two contradict. They reconcile once Q1 and Q2 are separated.

## Decision

### Q1 Virtual Queue — build the adaptor layer, defer the vendor

TICVAI builds:

1. **Inbound data ingestion API** (C99) — a standard interface any third-party queue system
   or people-counting sensor feeds into
2. **Adaptor framework** — per-vendor translation into that interface. Ships with none
3. **Frontend** — wait-time display, queue join, position, redirect, queue calls. Renders
   whatever the feed supplies
4. **Venue-level integration toggle** — venue management carries an *enable queue
   integration* option, with per-venue adaptor selection and credentials

**Vendor selection and per-vendor adaptor work are deferred** pending client confirmation.
This follows the standard integration pattern (10 Aug §83): TICVAI exposes an inbound API,
the client's chosen system feeds it, and direct integration with a named vendor is bespoke
work quoted separately.

### Q2 Virtual Waiting Room — in-house infrastructure, Wave 1

Owned by infrastructure, not product. Concurrency threshold detection, branded queue page,
position and wait estimate, batched release, session preservation, guaranteed confirmation
on completion.

**Zero matrix requirements.** It exists only in the MoM record, and it is what keeps the
platform standing at peak concurrency during an on-sale. A matrix-driven scope would have
missed it entirely.

### Q3 Chat queues — CRM, Wave 3

Unaffected.

## Consequences

| | |
|---|---|
| The 31 Jul and 10 Aug decisions both stand | They were about different systems |
| **No sensor hardware in the lab** | Wait-time accuracy is a third-party feed. A conforming mock against the inbound API is sufficient |
| Scanning devices and a signage display **are** needed | Queue entry validation and queue calls |
| Q1 can be built and demonstrated without any vendor | The frontend renders mock feed data |
| Venue management gains an integration configuration surface | Toggle, adaptor selection, credentials, health |
| C98 Waiting Room stays Wave 1 | Independent of this |

## Still open

| # | Question | Owner |
|---|---|---|
| 1 | Which queue vendor, or which sensor system, per venue | **Client — deferred** |
| 2 | Is a first-party sensor option in scope at all, or always third-party? | Client |
| 3 | Does any tenant have an existing queue system to integrate on day one? | Client |

These are **procurement questions, not architecture questions**. The adaptor layer is
vendor-agnostic by design, so answering them later costs an adaptor rather than a redesign.

## Note — Fast Pass is not a queue feature

Fast Pass is an **entitlement with a consumption counter**, spanning four contexts:

| Ref | Context |
|---|---|
| 3.2.40, 3.2.60 | Access control — *a wristband limited to 3 accesses, system counts usage* |
| 7.4.9 | F&B POS — Fast Pass products |
| 4.6.34 | Kitchen order prioritisation |
| 5.6.x | Queue priority tiers |

**Model it in the Product & Entitlement spine.** Inside the queue module, the wristband
counter and the kitchen prioritisation both break.
